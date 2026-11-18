# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `DaiDaiDi`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-DaiDaiDi-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S8`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Đậu Phúc Đức | 2A202603580 | Kỹ sư cổng | ✓ |
|   2 | Võ Công Minh | 2A202603520 | Sản phẩm và kinh doanh | |
|   3 | Bùi Xuân Thành | 2A202603521 | Vận hành và pháp lý | |
|   4 | Nguyễn Đắc Tuấn Nghĩa | 2A202603442 | Vận hành và pháp lý | |

**Ghi chú về đổi vai.** Lúc ký tiêu chí (commit `2eb05b8`, 15:17:15) bàn đang phân Thành vai Sản phẩm và kinh doanh, Minh vai
Vận hành và pháp lý. Khoảng 15:50 hai bạn đổi vai cho nhau (Minh báo ở issue #6), bảng trên là vai hiện tại. Hai chỗ sau vẫn
ghi theo phân vai cũ và **không sửa**, vì luật lab cấm sửa sau khi chốt: `signed_by` trong `config/acceptance_criteria.json`
("Thành, vai Sản phẩm và kinh doanh") và ô "PIC ký" ở cột v1 của Phiếu B mục B8. Thành đã ký thay mặt bàn theo phân vai lúc đó.

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## DauPhucDuc-2A202603580

### Phần việc phụ trách

Trưởng nhóm, vai Kỹ sư cổng. Tạo repo; ký tiêu chí (`config/acceptance_criteria.json`, `.lock`); code cổng vòng 1 và vòng 2
trong `lab10/guards.py`; chốt vòng 1 (`lab10.checkpoint`); monitor trong `lab10/monitors.py`; chạy mọi lần `eval` / `grade`.
Phiếu A mục A1–A5; Phiếu B mục B0–B2, B7.1, B8 (v1); Phiếu C mục C0, C1, C2, C6, C7, C8, C9. PIC dòng 1, 3, 4 của checklist B5.

### Đóng góp cụ thể

- Cổng vòng 1: ghim chính sách theo ngày (`pre_guard`), cổng tiền `_refund_gate` (người trả, hoàn trùng, phê duyệt đủ bốn
  điều kiện, số tiền theo DB), cổng lỗi hãng `_carrier_fault_gate` (đúng kiện, đúng nguyên nhân, trần theo hãng).
- Cổng vòng 2 cho thẻ S8: trần hoàn tự động 300.000đ cho một khách mỗi ngày; monitor `max_customer_auto_refund_day`.
- Chạy và ghi nhật ký các lần đo của bàn; ghi chú ô `1 integrity` ở Phiếu C mục C0.

### Bằng chứng

- Commit `2eb05b8` (ký tiêu chí), `d277e9f` (Phiếu A, B0–B2), `304b537` (cổng vòng 1), `efe5e24` (chốt vòng 1, v1),
  `8073208` (nhận thẻ S8), `0a322a1` (cổng vòng 2), `eb6642a`, `8bd89c2`, `c69f060`, `381e06d`, `21cf51e` (Phiếu C).
- Mã lần chạy: `R-base-before-20261118-152543-b45eeb`, `R-base-prepared-20261118-160514-13228c`,
  `R-S8-grade-20261118-164228-13228c`, `R-S8-after-20261118-170341-1a5589`, `R-S8-grade-20261118-170338-1a5589`.

### Exit ticket

*(Đức tự viết: một điều học được, một điều còn chưa chắc.)*

## VoCongMinh-2A202603520

### Phần việc phụ trách

Vai Sản phẩm và kinh doanh (đổi vai với Thành khoảng 15:50, xem ghi chú ở trên). PIC dòng 2 (Dữ liệu), 6 (Chi phí),
9 (Quyết định) của checklist Phiếu B mục B5; PIC ký quyết định v2 ở Phiếu C mục C12; PIC hai dòng risk register ở Phiếu C
mục C10 (cộng dồn theo khách, kho `?`).

### Đóng góp cụ thể

- Theo dõi ngưỡng chi phí và ROI đã ký (`cost_per_ticket_vnd_max` 8.000đ, `roi_min` 0,25) so với report; kho `?`
  10.359đ/ticket là lý do của quyết định Thu hẹp ở v1 và v2.
- Báo đổi vai ở issue #6.

### Bằng chứng

- Phiếu B mục B5, các dòng 2, 6, 9 (cột PIC); Phiếu C mục C11 (checklist cập nhật, dòng 6 và 9); Phiếu C mục C12 (PIC ký).

### Exit ticket

*(Minh tự viết: một điều học được, một điều còn chưa chắc.)*

## BuiXuanThanh-2A202603521

### Phần việc phụ trách

Vai Vận hành và pháp lý. Phiếu B mục B4 (HAZOP vòng 1), B5 (checklist 9 nhóm); Phiếu C mục C3, C4, C5 (câu 3.3), C9, C10, C11.

### Đóng góp cụ thể

- B5: điền checklist 9 nhóm, PIC có tên cho từng dòng (issue #3).

### Bằng chứng

- Commit 5c771b6, 82ff732 (B5).
- Commit 72df8a7 (B4, HAZOP vòng 1 trên `issue_refund`); 083da5b (Phiếu C mục C3.1 dòng S8, C3.4, C4, C5 câu 3.3).

### Exit ticket

(viết cuối buổi)

## NguyenDacTuanNghia-2A202603442

### Phần việc phụ trách

Vai Vận hành và pháp lý. Người viết Runbook phần 1–3 (Phiếu B mục B7.5); PIC dòng 7 (Vận hành) của checklist B5.
Vòng 2: Phiếu C mục C5 (câu 3.2, specification), C10 (risk register), C11 (checklist cập nhật, Runbook 4–5), C12 (quyết
định v2 và ba dòng bắt buộc); Phiếu B mục B7.6 (giờ cao điểm, bổ sung ở vòng 2); `submission/submission.json`.

### Đóng góp cụ thể

- Runbook 1–3: người chịu trách nhiệm (NV-TUNG, NV-HANH, NV-OANH), tín hiệu VÀNG/ĐỎ khớp `config/operating_gates.json`,
  điều kiện dừng và cách dừng bằng `config/switches.json`.
- Risk register sau sự cố S8: 4 dòng mới, mỗi dòng gắn một metric trong report hoặc `monitors.py` và một dòng `decision_rule`.
- Runbook 4–5: tín hiệu lẽ ra phải báo trước sự cố (tổng hoàn theo khách, tỉ lệ kiểm lại), việc với bên thứ ba, ba kịch bản
  tuần đầu pilot.
- Quyết định v2 **Thu hẹp** (giữ v1): mọi ngưỡng đã ký đạt trên S8, còn kho `?` 10.359đ/ticket > 8.000đ.
- Giờ cao điểm: thử `reviewers_on_shift = 2` trên bản sao để đọc chi phí và ROI khi thêm người.

### Bằng chứng

- Phiếu B mục B7.5 (dòng "Người viết"), B7.6; Phiếu C mục C5, C10, C11, C12; `submission/submission.json`.
- Số liệu dẫn từ `R-S8-after-20261118-170341-1a5589`, `R-S8-grade-20261118-170338-1a5589`, `R-base-after-20261118-171143-1a5589`.
- Commit `8b9fa84` (C5, C10–C12, B7.6, `submission.json`, TEAM.md). Sau buổi học: thêm `incidents/S1`–`S7` (khớp hash
  `MANIFEST.json`), chạy lại tự kiểm `R-S8-grade-20261118-225046-1a5589` (`1 integrity ✅`, PASS-VISIBLE), gom bài bằng lệnh 7.

**Dùng AI:** dùng Claude (Claude Code) để soát phiếu so với đề và rubric, đọc report, soạn nháp các mục C5 câu 3.2, C10,
C11, C12, B7.6, và tìm, kiểm hash 28 file thẻ S1–S7. Mọi con số trong các mục đó lấy từ report của bàn; quyết định v2
(Thu hẹp, giữ v1) theo đúng `decision_rule` đã ký, và mình giải thích được lúc demo.

### Exit ticket

- **Một điều học được:** report "được phép cân nhắc Tiếp tục" chưa phải là lý do để Tiếp tục. Tổng của gói S8 đạt hết
  ngưỡng đã ký, nhưng tách theo kho thì kho `?` vẫn tốn 10.359đ/ticket, đắt hơn làm tay. Quyết định phải đọc cả phân khúc
  và khớp `decision_rule`, không chỉ đọc dòng tổng. Mình cũng học được rằng runbook tốt phải có tín hiệu báo **trước** sự
  cố: Runbook 2 vòng 1 chỉ theo dõi tổng hoàn cả ngày (498.000đ, không báo gì), nên không thấy một khách đã vượt trần
  300.000đ.
- **Một điều còn chưa chắc:** tỉ lệ nhân viên kiểm lại 10% chỉ là giả định của bộ thử (`staff_behavior`). Mình chưa chắc
  ngoài thực tế trưởng ca có thật sự thôi kiểm tay chỉ nhờ ghi chú giải thích, và chưa biết bảng `approvals` cập nhật chậm
  bao lâu sau khi chị thu hồi mã. Cả hai phải đo trong tuần pilot đầu tiên.