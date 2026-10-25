# Vòng hỏi (grilling) — cách trình bày câu hỏi cho người quyết

Dùng bởi `/ae-kit:intake` (T và C) và `/ae-kit:lint-spec`. Nguyên tắc của ae-kit không đổi: **agent đặt câu hỏi, người trả lời; agent không điền chỗ trống.** Tài liệu này chỉ quy định *cách hỏi* để người trả lời nhanh và không bị hỏi những thứ chưa thể trả lời.

## 1. Sự thật vs quyết định
- **Sự thật** là thứ có thể quan sát được bằng cách đọc file, chạy lệnh, xem schema, đọc transcript. Agent tự tìm. KHÔNG hỏi người ("DB dùng Postgres hay MySQL?" khi `docker-compose.yml` đã nói).
- **Quyết định** là thứ không quan sát được: khách muốn gì, ưu tiên nào, chấp nhận rủi ro nào, ranh giới ở đâu. Chỉ quyết định mới thành câu hỏi Q<n>.
- Một Q mà agent thấy mình có thể trả lời bằng cách tra cứu → tra cứu, ghi kết quả thành statement/quan sát có bằng chứng, xoá Q.

## 2. Cây câu hỏi và frontier
Mỗi Q có thể phụ thuộc một Q khác (không hỏi "giới hạn số lịch mỗi ngày là bao nhiêu" trước khi biết "có giới hạn không"). Ghi phụ thuộc vào cột **Sau Q** của bảng Open Questions (trống = không phụ thuộc).

**Frontier** = tập Q chưa có nhãn mà mọi Q nó phụ thuộc đã có nhãn. Mỗi vòng hỏi **toàn bộ frontier**, không hơn. Q ngoài frontier để vòng sau. Vòng kết thúc khi người trả lời; frontier được tính lại; hết frontier = xong.

## 3. Định dạng một vòng (trong chat)
```
### Vòng <v> — <số Q> câu (còn <n> câu chờ vòng sau)

❓ **Q3 — <tiêu đề ngắn>**
<câu hỏi; nếu có ≥2 cách hiểu, liệt kê A / B / C kèm hệ quả của mỗi lựa chọn>
Vì sao quan trọng: <một câu>
➡️ Đề xuất: **A3** — <giả định mặc định đã ghi trong discovery>. Trả lời `yes` = chấp nhận A3.

---
```
- Đề xuất **luôn là A<n> đã có trong bảng discovery** (giả định mặc định), không phải ý mới nghĩ ra trong chat. Nếu cần sửa A<n>, sửa trong file trước.
- Câu hỏi phải viết sao cho `yes` là chấp nhận đề xuất, `no` cần nói thêm.
- Không gộp hai quyết định vào một Q.

## 4. Người trả lời thế nào, agent ghi thế nào
Người trả lời gọn theo mã, ví dụ: `Q3 yes · Q4 send · Q5 defer · Q6: chỉ admin mới được xoá`.

| Người trả lời | Agent ghi vào discovery (cột Nhãn, cột Giả định) |
|---|---|
| `yes` / "đồng ý" | Nhãn = `assume` (A<n> giữ nguyên) |
| `send` | Nhãn = `send` — câu hỏi sẽ gửi khách; nội dung Q giữ nguyên để copy |
| `defer` | Nhãn = `defer` — không chặn G1, ghi lại ở "Open Questions bổ sung" khi specify |
| `prototype` | Nhãn = `prototype` — câu "nên trông/hoạt động thế nào"; `/ae-kit:prototype` dựng màn hình trả lời, khách phản ứng tại demo |
| câu trả lời cụ thể | Nhãn = `assume`; **thay** nội dung A<n> bằng câu trả lời, ghi `(người quyết <ngày>)` |
| trả lời cho Q ngoài frontier | vẫn ghi; Q phụ thuộc nó có thể vào frontier vòng sau |

Agent chỉ được sửa **cột Nhãn và cột Giả định mặc định** của bảng Q (và cột Nhãn của O với brownfield). Không sửa Statements, không viết requirement, không sửa `spec/requirements.md`.

## 5. Dừng vòng
- Người nói "đủ rồi" / "để sau" → dừng; Q còn lại để trống nhãn, `gates.py compute G1` sẽ đếm chúng ở `open_q_classified`.
- Không hỏi lại Q đã có nhãn, trừ khi người yêu cầu.
- Tối đa 7 Q một vòng; frontier lớn hơn → chia nhiều vòng, ưu tiên Q mà nhiều Q khác phụ thuộc.

## 6. Hai bối cảnh
- **intake T**: người trả lời là consultant đang cầm transcript; `send` nghĩa là sẽ hỏi khách. Transcript câu trả lời của khách → `intake/T<n+1>-transcript.md` → `/ae-kit:intake T<n+1>` tự khớp Q.
- **intake C**: người trả lời là chủ dự án/dev lâu năm; hầu hết Q đi kèm một O; `yes` xác nhận cả đề xuất phân loại O (decided/debt/ignore) ghi ở cột Đề xuất.
- **lint-spec**: Q đến từ linter (ERROR/WARN). Vòng chia hai nhóm: "cần hỏi khách" (chỉ nhận `send`/`defer`) và "người tự quyết được" (nhận `yes`/trả lời). Trả lời của người → ghi vào `spec/lint-<ngày>.md` cột "Quyết định"; người tự sửa `requirements.md` (lint-spec không sửa).

Ý tưởng vòng hỏi theo frontier và "yes chấp nhận đề xuất" phỏng theo skill `grilling` của mattpocock/skills (MIT); xem NOTICE.md.
