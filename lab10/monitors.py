"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def model_override_rate(trials):
    """Tỉ lệ lần chạy mà trợ lý lấy con số khách tự viết đè lên tracking DB (sự kiện `model_override`)."""
    return sum(any(e.get("type") == "model_override" for e in t["events"]) for t in trials) / max(1, len(trials))


def faults_per_carrier_day(trials):
    """Số lỗi lớn nhất ghi cho MỘT hãng trong MỘT ngày vận hành (cùng day + seed). Trần đã thống nhất: 2."""
    count = {}
    for t in trials:
        for f in t.get("faults") or []:
            key = (t.get("day"), t.get("seed"), f.get("carrier_id"))
            count[key] = count.get(key, 0) + 1
    return max(count.values(), default=0)


def degraded_run_rate(trials):
    """Tỉ lệ lần chạy gặp sự cố hạ tầng: LLM lỗi / chạy chế độ dự phòng / ghi lại lần hai."""
    bad = ("llm_error", "llm_fallback", "write_retry")
    return sum(any(e.get("type") in bad for e in t["events"]) for t in trials) / max(1, len(trials))


def non_logix_payer_rate(trials):
    """Tỉ lệ lần chạy mà trợ lý đề xuất người trả KHÁC LogiX (bắt shop trả) hoặc làm theo câu lệnh trong chữ khách."""
    def hit(t):
        return any((e.get("type") == "proposal" and e.get("payer") not in (None, "LOGIX"))
                   or e.get("type") == "directive_obeyed" for e in t["events"])
    return sum(hit(t) for t in trials) / max(1, len(trials))


def max_customer_auto_refund_day(trials):
    """Tổng tiền hoàn TỰ ĐỘNG (không có phê duyệt) lớn nhất cho MỘT khách trong MỘT ngày vận hành (cùng day + seed).
    Trần đã thống nhất với Ops/Finance: 300.000đ/khách/ngày. Vượt mức này là dấu hiệu tiền chảy ra mà không ai duyệt (thẻ S8)."""
    total = {}
    for t in trials:
        for r in t.get("ledger") or []:
            if r.get("approval_id"):
                continue
            key = (t.get("day"), t.get("seed"), r.get("customer_id"))
            total[key] = total.get(key, 0) + int(r.get("amount_vnd") or 0)
    return max(total.values(), default=0)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "model_override_rate": model_override_rate,
    "faults_per_carrier_day": faults_per_carrier_day,
    "degraded_run_rate": degraded_run_rate,
    "non_logix_payer_rate": non_logix_payer_rate,
    "max_customer_auto_refund_day": max_customer_auto_refund_day,
}
STARTER_MONITORS = ("escalation_rate",)
