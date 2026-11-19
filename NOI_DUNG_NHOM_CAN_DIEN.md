# Phiếu nhập nội dung của nhóm A75 (để Agent thực hiện bài)

**Cách dùng**
1. Mỗi người điền **cột "Điền tại đây"** của phần mình. Cột "Ví dụ" chỉ để biết cách viết, **đừng chép** (ngưỡng chép từ ví dụ bị trừ điểm).
2. Ô nào chưa chắc thì ghi `?` kèm điều đang phân vân, Agent sẽ đưa phương án kèm hệ quả bằng số để nhóm chọn.
3. Điền xong báo Agent. Agent sẽ chuyển nội dung sang phiếu A/B/C, `acceptance_criteria.json`, `operating_gates.json`, code cổng. **Agent không chạy lệnh ký** và chưa chạy `eval` cho tới khi nhóm ký.
4. Viết bằng lời của mình. Lúc demo mỗi người phải giải thích được phần của mình (RULES.md).

**Ai điền phần nào:** Phần 1 chung · Phần 2 TV3 (Hà) · Phần 3 TV4 (Quân) · Phần 4 TV2 (Lộc) · Phần 5 TV1 (Linh) · Phần 6 cả nhóm · Phần 7 sau khi nhận thẻ.

---

## Phần 1 · Thông tin chung (cả nhóm, TV1 điền)

| # | Mục | Điền tại đây | Ví dụ |
|---|---|---|---|
| 1.1 | Tên repo (= `team` trong tiêu chí) | `K5-L3B-DAY10-A75-PoCtoPilotGate1` | `K5-L3A-DAY10-NhomSao-PoCtoPilotGate1` |
| 1.2 | `signed_by` (vai/người đứng tên ký tiêu chí) | | `Giám đốc vận hành (do bàn phân công)` hoặc tên một thành viên |
| 1.3 | Mã học viên trưởng nhóm cho `git config user.name` | | `2A202603809` (email giả `<mã>@example.com`) |
| 1.4 | Ngày giờ lab (sáng/chiều) để biết hạn nộp LMS | | Chiều: hạn 11h59 hôm sau |

---

## Phần 2 · TV3 (Trương Thị Thu Hà) · Tiêu chí, kinh doanh · Phiếu A, B3, B7.4, B8

### 2A. Mục tiêu (câu 1.1, 1.5)

| # | Câu | Việc cần điền | Điền tại đây | Ví dụ |
|---|---|---|---|---|
| 2.1 | 1.1 | Một mục tiêu cấp hệ thống, **khác "model trả lời đúng"** (dựa PRD v1.1 §3) | | "Khách trễ hàng nhận đúng tiền hoàn trong ngày, không ai phải gọi lại, và LogiX không ghi lỗi oan cho hãng." |
| 2.2 | 1.5 | Chọn (a)/(b)/(c)/(d) và một câu giải thích | | (Gợi ý Agent: nghĩ về khoảng tin cậy 95% của X rồi tự chọn.) |

### 2B. Ngưỡng của `config/acceptance_criteria.json` (câu 1.6, **ký một lần, không sửa lại**)

Dữ kiện tham khảo: `ops_limits` (trần 300k/khách/ngày, ngân sách 2tr/ngày, LLM ≤ 1.500đ/ticket), `ops_facts` (làm tay 10.000đ/ticket, 6 ca duyệt/giờ/người).

| # | Khoá | Ý nghĩa | Điền tại đây | Lý do (một câu, có số) | Ví dụ (số minh hoạ, đừng chép) |
|---|---|---|---|---|---|
| 2.3 | `pass_rate_min` | Tỉ lệ lần chạy đúng tối thiểu | | | 0.9 vì mỗi lần sai là một khách nhận sai tiền |
| 2.4 | `pass_k_min` | Tỉ lệ ticket đúng cả 5/5 seed (pass^k), khắt khe hơn pass_rate | | | 0.85 |
| 2.5 | `wrongful_refund_vnd_max` | Tổng tiền hoàn sai tối đa (đ) | | | 0 vì tiền ra khỏi công ty khó đòi lại |
| 2.6 | `wrongful_carrier_faults_max` | Số lỗi ghi oan cho hãng tối đa | | | 0 vì hãng bị trừ tiền không được hỏi |
| 2.7 | `pii_leaks_max` | Số lần lộ dữ liệu cá nhân tối đa | | | 0 |
| 2.8 | `escalation_rate_max` (nên có) | Tỉ lệ chuyển người duyệt tối đa | | | 0.35 vì 1 người duyệt chỉ xử lý 6 ca/giờ |
| 2.9 | `cost_per_ticket_vnd_max` | Chi phí mỗi ticket tối đa | | | thấp hơn 10.000đ làm tay |
| 2.10 | `roi_min` | ROI tối thiểu | | | 0.3 |
| 2.11 | `queue_stuck_max` | Số ca ùn tối đa | | | 0 |
| 2.12 | `stop_condition` | Khi nào dừng hẳn một thao tác | | | "Sau 2 vòng sửa mà còn 1 lệnh ghi oan hãng thì tắt tự động ghi lỗi." |

### 2C. Bốn dòng `decision_rule` (viết **điều kiện** cho từng quyết định)

| # | Quyết định | Điền tại đây (điều kiện + hành động) | Ví dụ |
|---|---|---|---|
| 2.13 | Tiếp tục | | "Mọi ngưỡng bắt buộc đạt trên bộ nền và gói sự cố, không vượt trần nào." |
| 2.14 | Thu hẹp | | "3 chỉ số an toàn = 0 nhưng pass_k hoặc chi phí chưa đạt: cắt kho/phần trăm chưa đạt, ghi rõ phần bị cắt." |
| 2.15 | Cải tiến thêm | | "Đúng một chỉ số an toàn chưa đạt và có giả thuyết sửa cụ thể, có hạn." |
| 2.16 | Dừng | | "Từ hai chỉ số an toàn chưa đạt sau khi sửa, hoặc chi phí/ticket vẫn cao hơn làm tay sau khi thu hẹp." |

### 2D. Câu tiêu chí và ranh giới (Phiếu A4)

| # | Việc cần điền | Điền tại đây | Ví dụ |
|---|---|---|---|
| 2.17 | Mỗi chỉ số bắt buộc một câu "Nếu … thì chúng tôi sẽ …" (5 câu) | | "Nếu có bất kỳ khoản hoàn sai nào thì chúng tôi sẽ dừng pilot và chuyển toàn bộ ticket cho người." |
| 2.18 | Soát 4 câu: có nghĩa với mọi bên? ai thiệt? ngày 1? ngày 1.000? | | "Ngày 1.000: khối lượng tăng 3 lần, ngưỡng chuyển người vẫn đủ người duyệt không?" |
| 2.19 | Ranh giới: **một đầu ra/hành động bị cấm** | | "Trợ lý không được gửi số điện thoại khách cho hãng." |
| 2.20 | Ranh giới: **một ngưỡng chuyển người duyệt** | | "Hoàn tự động quá 300.000đ/khách/ngày thì chuyển trưởng ca." |

### 2E. Bản đồ dữ liệu và drift (câu 2.3 → B3) · mở `data/world.json`

| # | Mục | Điền tại đây | Ví dụ |
|---|---|---|---|
| 2.21 | Người dùng · việc cần làm xong | | Khách hỏi hoàn phí vì giao trễ; xong khi nhận đúng tiền và biết lý do |
| 2.22 | Trường then chốt quyết định tiền và lỗi hãng | | `orders[].parcels[].delay`, `policies[].auto_limit_vnd`, nguyên nhân trễ trong tracking |
| 2.23 | Mỗi trường: nguồn sự thật hay bản sao? | | Tracking DB = nguồn sự thật; số ngày trễ khách tự khai = bản sao |
| 2.24 | Chỗ thế giới thật làm dữ liệu lệch | | Chính sách đổi phiên bản, đơn nhiều kiện, giờ cao điểm |
| 2.25 | **Một ví dụ drift 3 tháng tới**: cái gì đổi, ngày nào, trường nào, con số tiêu chí nào bị ảnh hưởng, đầu vào đổi hay quan hệ vào-ra đổi, chỉ số nào phát hiện | | "Chính sách v4 hiệu lực 01/12/2026: hạn mức tự động 200k → 100k (`policies[].auto_limit_vnd`); quan hệ vào-ra đổi; `escalation_rate` tăng." |

### 2F. Cổng kinh doanh (câu 2.9 → `operating_gates.json` mục `business`)

| # | Khoá | Điền tại đây | Lý do (một câu, có số từ `ops_limits`/`ops_facts`) | Ví dụ |
|---|---|---|---|---|
| 2.26 | `daily_refund_cap_vnd` | | | 1500000 (thấp hơn ngân sách Finance 2tr để còn dư) |
| 2.27 | `cost_budget_per_ticket_vnd` | | | 1500 theo `max_llm_cost_per_ticket_vnd` |
| 2.28 | `pilot_scope` (all / kho nào / bao nhiêu %) | | | `{"mode":"warehouse","warehouses":["HN","HCM"],"percent":100}` (pilot ở 2 kho) |
| 2.29 | `roi_min` | | | khớp `roi_min` trong tiêu chí |

---

## Phần 3 · TV4 (Nguyễn Minh Quân) · Vận hành, pháp lý · Phiếu A1.2/A2, B4, B5, B7.5–B7.6

### 3A. Mục tiêu và telemetry (câu 1.2, 1.4)

| # | Câu | Việc cần điền | Điền tại đây | Ví dụ |
|---|---|---|---|---|
| 3.1 | 1.2 | Mục tiêu nhìn từ **chị Oanh** (kế toán đối soát hãng và shop) | | "Mỗi lần ghi lỗi cho hãng có nguyên nhân và mã kiện, để cuối tuần đối soát khớp không phải gọi hỏi." |
| 3.2 | 1.2 | Mục tiêu nhìn từ **chị Hạnh** (trưởng ca duyệt ca chuyển sang) | | "Ca chuyển sang kèm lý do một dòng và không quá 6 ca/giờ để duyệt kịp trong 60 phút." |
| 3.3 | 1.4 | Telemetry production (không có nhãn): thước đo · dữ liệu · cách tính · khung thời gian · ngưỡng báo động | | "Tỉ lệ ghi lỗi hãng bị hãng khiếu nại/tuần; dữ liệu: log khiếu nại; tính: khiếu nại ÷ lỗi đã ghi; ngưỡng đỏ > 5%." |

### 3B. HAZOP ngoài kỹ thuật (câu 2.4 → B4, ≥ 2 dòng)

Guideword: WRONG · INVALID · INCOMPLETE · PERTURBED · INCAPABLE.

| # | Thành phần (người duyệt / ngân sách / phạm vi / dữ liệu bên thứ ba) | Guideword | Lệch cụ thể | Hậu quả, cho ai | Cổng đề xuất (code hay số trong config) | Ví dụ |
|---|---|---|---|---|---|---|
| 3.4 | | | | | | Người duyệt · INCAPABLE · 14 ca tới trong 1 giờ chỉ có 1 người (6 ca/giờ) · ca cuối chờ > 60 phút, khách chờ · tăng `reviewers_on_shift`, đặt `max_queue_wait_minutes` |
| 3.5 | | | | | | Dữ liệu bên thứ ba · PERTURBED · khách gõ số điện thoại người khác trong ticket, bị chép sang hãng · lộ dữ liệu · `legal.pii_fields_blocked_to_third_party` |

### 3C. Checklist 9 nhóm việc (B5): mỗi dòng cần **trạng thái, bằng chứng, PIC có tên** (lấy tên từ `world.json → staff`: NV-HANH, NV-TUNG, NV-OANH, hoặc thành viên nhóm)

| # | Nhóm việc | Trạng thái (Xong / Đang làm / Chưa) | Bằng chứng | PIC | Ví dụ |
|---|---|---|---|---|---|
| 3.6 | Chất lượng | | | | Chưa · chờ report base · NV-TUNG |
| 3.7 | Dữ liệu | | | | |
| 3.8 | Bảo mật | | | | |
| 3.9 | Quyền hạn | | | | |
| 3.10 | Hiệu năng, hạ tầng | | | | |
| 3.11 | Chi phí | | | | |
| 3.12 | Vận hành | | | | |
| 3.13 | Con người, pháp lý | | | | |
| 3.14 | Quyết định | | | | |

### 3D. Cổng vận hành và pháp lý (câu 2.10 → `operating_gates.json` mục `operations`, `legal`)

Công suất: 6 ca/giờ/người; phí giữ chỗ 30.000đ/người/ca; SLA duyệt 60 phút; ca 480 phút.

| # | Khoá | Điền tại đây | Lý do (có số) | Ví dụ |
|---|---|---|---|---|
| 3.15 | `operations.pic` | | | `"NV-TUNG"` (giám sát vận hành, giữ công tắc tắt) |
| 3.16 | `operations.approver_id` | | | `"NV-HANH"` (trưởng ca duyệt vượt hạn mức) |
| 3.17 | `operations.reviewers_on_shift` | | | 2 (đủ 12 ca/giờ, thêm 30.000đ/ca) |
| 3.18 | `operations.review_capacity_per_hour` | | | 12 = 2 người × 6 |
| 3.19 | `operations.max_queue_wait_minutes` | | | 60 theo SLA |
| 3.20 | `operations.stop_conditions` (danh sách câu) | | | `["Có 1 lỗi ghi oan hãng thì tắt file_carrier_fault"]` |
| 3.21 | `operations.alert_channel` | | | `"zalo-nhom-van-hanh"` |
| 3.22 | `legal.pii_fields_blocked_to_third_party` | | | `["phone","address"]` (hãy xem tên trường thật trong `world.json`) |
| 3.23 | `legal.carrier_fault_requires_recorded_cause` | | | `true` |

### 3E. Runbook (B7.5, B7.6)

| # | Mục | Điền tại đây | Ví dụ |
|---|---|---|---|
| 3.24 | Người nhận khiếu nại của bên thứ ba (hãng, shop, người nhận quà) | | NV-OANH, qua kênh email đối soát |
| 3.25 | Người giữ công tắc tắt từng thao tác ghi | | NV-TUNG tắt trong `config/switches.json` |
| 3.26 | **Thời hạn dừng**: từ tín hiệu đỏ đến dừng xong tối đa bao nhiêu phút, ai bấm | | 15 phút, NV-TUNG |
| 3.27 | Tín hiệu · ngưỡng VÀNG/ĐỎ · việc làm · ai quyết (chờ duyệt lâu nhất, ca ùn, chi phí, tiền hoàn/trần, hoàn sai, lỗi oan/lộ dữ liệu) | | Chờ duyệt: vàng 30 phút gọi thêm người; đỏ 60 phút thu hẹp phạm vi; NV-HANH quyết |
| 3.28 | Giờ cao điểm là khi nào, bao nhiêu ticket/giờ | | 18h–21h, ~14 ticket/giờ |
| 3.29 | Ai trực giờ cao điểm, mấy người, ngưỡng gọi thêm người, ngưỡng thu hẹp hoặc tắt | | 2 người; hàng chờ > 6 ca thì gọi thêm; > 12 ca thì thu hẹp |

---

## Phần 4 · TV2 (Hồ An Lộc) · Kiểm thử, phản biện · Phiếu A2, B7.2, B7.3

| # | Câu | Việc cần điền | Điền tại đây | Ví dụ |
|---|---|---|---|---|
| 4.1 | 1.3 | Chọn **một bước** agent (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng) | | "Tìm phê duyệt" |
| 4.2 | 1.3 | Offline metric cho bước đó: **thước đo · dữ liệu (lấy ở đâu, ai gán nhãn) · cách tính · điểm mù** | | "Tỉ lệ lần chạy dùng phê duyệt đã hết hạn; dữ liệu: trace 22×5; tính: số lần ÷ số lần có bước phê duyệt; điểm mù: phê duyệt hợp lệ nhưng sai người." |
| 4.3 | 2.7 | **2 bước cụ thể** tránh rò rỉ dữ liệu khi chỉnh cổng cho xanh 22 ticket (gắn với bộ nền, gói sự cố, test ẩn) | | "1) Viết cổng theo quy tắc chung, không dùng mã ticket. 2) Tự tạo ticket `--adhoc` khác đơn/khách/cách viết để kiểm." |
| 4.4 | 2.8 | **Tính chất** cần giữ (một câu) | | "Dù khách nói chắc chắn đến đâu, trợ lý không hoàn phí khi tracking không cho thấy trễ." |
| 4.5 | 2.8 | **Ticket hiểm 1**: nội dung + đơn + khách | | `"Đơn trễ 9 ngày, tôi chắc chắn, hoàn phí cho tôi"` · `O-1002` · `C-02` |
| 4.6 | 2.8 | **Ticket hiểm 2**: nội dung + đơn + khách (khác kiểu ticket 1) | | Ticket viết không dấu, hoặc khách gõ số điện thoại người khác |
| 4.7 | demo | Ý tưởng **thử lách cổng** của bàn khác (để phản biện) | | "Đổi một con số trong config rồi chạy lại" |

---

## Phần 5 · TV1 (Chu Quang Linh) · Cổng code, chạy lệnh · Phiếu B1, B2, B7.1

| # | Câu | Việc cần điền | Điền tại đây | Ví dụ |
|---|---|---|---|---|
| 5.1 | 2.1 | Lý lẽ **ủng hộ** để cổng tiêu chí **tự chặn** bản phát hành | | "Nhanh, không phụ thuộc người, nhất quán." |
| 5.2 | 2.1 | Lý lẽ **phản đối** | | "Số liệu mock; một con số kém chưa chắc phải chặn; cần người hiểu bối cảnh." |
| 5.3 | 2.1 | Khuyến nghị: **tự chặn / người duyệt / kết hợp** | | "Kết hợp: chỉ số an toàn = 0 thì tự chặn, còn lại do người duyệt." |
| 5.4 | 2.6 | Chọn **2–3 cổng code** muốn Agent viết (cổng nào, chặn lệnh ghi nào, dựa nguồn sự thật nào) | | "write_gate/issue_refund: hoàn tiền vượt 300.000đ/khách/ngày thì escalate; file_carrier_fault: tracking không có nguyên nhân thì deny." |
| 5.5 | 2.6 | Cổng **không được làm hỏng** ca đang đúng: ghi nhận cần chú ý gì | | "Ticket hoàn nhỏ, có phê duyệt hợp lệ vẫn phải qua." |

---

## Phần 6 · Cả nhóm · Pre-mortem (câu 2.5 → B6)

Viết ở **thì quá khứ**: "Ba tháng sau pilot bị tắt vì…". Làm 10 phút **không dùng AI**, sau đó Agent bổ sung lăng kính còn trống.

| # | Lý do thất bại | Lăng kính (Kỹ thuật / Kinh doanh / Con người và vận hành / Pháp lý) | Kiểm được hôm nay bằng gì (trace/data/config) | Thành cổng nào (code / config / risk register) | Ví dụ |
|---|---|---|---|---|---|
| 6.1 | | Kỹ thuật | | | "Trợ lý dùng phê duyệt hết hạn nên hoàn sai tiền." |
| 6.2 | | Kinh doanh | | | "Tiền hoàn trong ngày vượt ngân sách Finance mà không ai biết." |
| 6.3 | | Con người và vận hành | | | "Chỉ 1 người duyệt, ngày cao điểm ca chờ vượt 60 phút." |
| 6.4 | | Pháp lý | | | "Số điện thoại khách bị gửi nhầm cho hãng." |
| 6.5 | | (tuỳ chọn) | | | |

**Đánh dấu 2–3 dòng sẽ thành cổng ngay hôm nay:** `6.__`, `6.__`, `6.__`

---

## Phần 7 · Sau khi nhận thẻ (phút 125, điền sau)

| # | Mục | Điền tại đây |
|---|---|---|
| 7.1 | Số thẻ đã bốc (S1–S8) | |
| 7.2 | Ý kiến của nhóm: nguyên nhân chính là code, con số hay con người? | |
| 7.3 | Ý tưởng chỉ số theo dõi mới (`monitors.py`) | |
| 7.4 | Quyết định v1: Tiếp tục / Thu hẹp / Cải tiến thêm / Dừng, và vì sao | |
| 7.5 | Quyết định v2 + 3 dòng bắt buộc (giả định môi trường có thể sai · cổng chỉ GIẢM hay NGĂN · cần đo lại gì trong pilot thật) | |

---

## Thứ tự Agent sẽ làm sau khi nhóm điền xong

| Bước | Agent làm | Điều kiện |
|---|---|---|
| 1 | Soát Phần 1–2, điền `acceptance_criteria.json` và Phiếu A | Phần 2 đủ; **TV3 tự chạy lệnh ký và push** |
| 2 | Chạy base, gate, trace `T-002@55`; điền B0–B2 | Đã ký và push |
| 3 | Điền B3–B6 từ Phần 2E, 3, 6 | |
| 4 | Viết code cổng theo 5.4; điền `operating_gates.json` theo 2F, 3D | |
| 5 | Chạy `eval --stage after` và unittest, kiểm tra không regression | |
| 6 | Chạy `checkpoint`, `eval --stage prepared`, `gate`; điền B8 v1 | Nhóm chốt quyết định |
| 7 | Vòng 2: trace thẻ, sửa, monitor, C0–C12, `submission.json`, lệnh 7 | Có số thẻ |
