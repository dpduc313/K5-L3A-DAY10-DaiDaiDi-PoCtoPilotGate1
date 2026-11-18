"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


# ---------------------------------------------------------------------------------------------------------------
# Cổng vòng 1 của bàn DaiDaiDi. Mọi cổng chỉ đọc NGUỒN SỰ THẬT (đơn hàng, tracking, chính sách theo ngày, phê duyệt,
# sổ cái, các trần trong ops_limits); không đọc chữ khách viết, không xử lý riêng theo mã ticket.
#   pre_guard           ghim chính sách có hiệu lực theo NGÀY (không theo cờ index_active người bật tay)   · B4 drift
#   (a) cổng tiền       trước issue_refund: người trả, phê duyệt, hoàn trùng, số tiền so với quyền lợi theo DB · B6, B4
#   (b) cổng lỗi hãng   trước file_carrier_fault: đúng kiện trễ, đúng nguyên nhân, số ngày theo DB, trần/hãng/ngày
# ---------------------------------------------------------------------------------------------------------------


def _facts(ctx, order_id):
    """Đơn, chính sách hiệu lực theo ngày, kiện ticket nói tới, độ trễ theo DB. None nếu thiếu dữ liệu."""
    order = ctx.tools.lookup_order(order_id)
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if order is None or policy is None or not order.get("parcels"):
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, policy, parcel, H.db_delay_days(parcel, ctx.as_of)


def pre_guard(ctx):
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không có chính sách hoàn tiền nào hiệu lực ở ngày hôm nay")
    return Verdict.allow(policy_id=policy["policy_id"])


def _refund_gate(ctx, action):
    """(a) Cổng tiền: không ghi khoản hoàn nào mà nguồn sự thật không đỡ được."""
    facts = _facts(ctx, action.get("order_id"))
    if facts is None:
        return Verdict.escalate("thiếu dữ liệu đơn / chính sách để kiểm số tiền")
    order, policy, parcel, delay = facts
    amount = int(action.get("amount_vnd") or 0)

    if action.get("payer", "LOGIX") != "LOGIX":
        return Verdict.escalate("người trả không phải LogiX: chỉ người duyệt mới được bắt shop trả")

    # Ghi lặp trong cùng một ticket (ví dụ "không chắc đã ghi" rồi ghi lại): bỏ lệnh thứ hai, giữ lệnh đầu.
    if ctx.tools.ledger_rows(ticket_id=action.get("ticket_id"), order_id=order["order_id"]):
        ctx.log("duplicate_refund_blocked", order_id=order["order_id"])
        return Verdict.deny("đơn đã có khoản hoàn của chính ticket này, không ghi lần hai")
    # Đơn đã được hoàn ở lần khác (cờ refund_status chỉ cập nhật theo mẻ đêm nên không tin được): chuyển người.
    if ctx.tools.ledger_rows(order_id=order["order_id"]):
        return Verdict.escalate("sổ cái đã có khoản hoàn cho đơn này")

    approval_id = action.get("approval_id")
    if approval_id:
        ok = [a for a in ctx.tools.lookup_approvals(approval_id=approval_id)
              if a.get("status") == "valid" and a.get("expires_at", "") >= ctx.as_of
              and a.get("order_id") == order["order_id"] and a.get("max_vnd", 0) >= amount]
        if not ok:
            return Verdict.escalate(f"phê duyệt {approval_id} hết hạn / đã dùng / không đúng đơn hoặc không đủ số tiền")
        return Verdict.allow()   # khoản có phê duyệt hợp lệ: người duyệt đã chịu trách nhiệm số tiền

    entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
    if amount > entitled:
        ctx.log("refund_over_entitlement", asked=amount, entitled=entitled, db_delay_days=delay,
                policy_id=policy["policy_id"])
        if entitled <= 0:
            return Verdict.deny(f"theo tracking trễ {delay} ngày và {policy['policy_id']}: không đủ điều kiện hoàn")
        return Verdict.modify(f"sửa về quyền lợi theo DB ({delay} ngày, {policy['policy_id']})", amount_vnd=entitled)
    return Verdict.allow()


def _carrier_fault_gate(ctx, action):
    """(b) Cổng lỗi hãng: chỉ ghi lỗi khi DB cho thấy kiện trễ thật, nguyên nhân thuộc lỗi hãng, và chưa chạm trần."""
    facts = _facts(ctx, action.get("order_id"))
    if facts is None:
        return Verdict.deny("thiếu dữ liệu tracking: không ghi lỗi hãng")
    order, policy, parcel, delay = facts
    if not H.carrier_at_fault(policy, parcel, delay):
        ctx.log("carrier_fault_blocked", parcel_id=parcel["parcel_id"], db_delay_days=delay,
                delay_cause=parcel.get("delay_cause"), policy_id=policy["policy_id"])
        return Verdict.deny("tracking không cho thấy lỗi hãng (độ trễ / nguyên nhân / chính sách)")

    cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    if cap is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= cap:
        ctx.log("carrier_strike_cap", carrier_id=parcel["carrier_id"], cap=cap)
        return Verdict.escalate(f"hãng {parcel['carrier_id']} đã chạm trần {cap} lỗi tự động trong ngày")

    want = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
            "driver_id": parcel.get("driver_id"), "delay_days": delay}
    if any(action.get(k) != v for k, v in want.items()):
        ctx.log("carrier_fault_corrected", asked={k: action.get(k) for k in want}, fixed=want)
        return Verdict.modify("ghi lỗi đúng kiện trễ, đúng hãng, số ngày theo tracking", **want)
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        return _refund_gate(ctx, action)
    if tool == "file_carrier_fault":
        return _carrier_fault_gate(ctx, action)
    return Verdict.allow()
