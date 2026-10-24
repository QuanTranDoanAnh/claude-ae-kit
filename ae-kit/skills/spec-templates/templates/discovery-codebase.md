# Discovery — {{C_ID}} (codebase hiện có)

Nguồn: commit `{{COMMIT}}` · đã đọc: {{FILES_READ}} · ngày {{DATE}}

<!-- Agent chỉ QUAN SÁT và ĐẶT CÂU HỎI. Cột "Đề xuất" là đề xuất; người quyết bằng cách thay `?` ở cột Nhãn
     thành: decided (thành luật/tech.md) · debt (thành R phase 0) · ignore (bỏ qua, không hỏi lại).
     Chỉ O nhãn decided mới được vào CLAUDE.md / docs/product/tech.md, với nguồn [{{C_ID}} O<n>]. -->

## 1. Quan sát (observed) — máy đọc được, CHƯA phải luật
| ID | Quan sát | Bằng chứng (file:dòng / đếm) | Loại | Đề xuất | Nhãn |
|----|----------|------------------------------|------|---------|------|
| O1 | | | tech / convention / rule / debt / documented | | ? |

<!-- Loại "documented" = quyết định đã được ghi trong README/docs; vẫn cần người xác nhận còn hiệu lực. -->

## 2. Câu hỏi cho chủ dự án (mỗi O chưa rõ → đúng một câu)
| ID | Liên quan | Câu hỏi | Vì sao quan trọng | Giả định mặc định nếu không trả lời | Nhãn |
|----|-----------|---------|-------------------|--------------------------------------|------|
| Q1 | O1 | | | A1: | send / assume / defer |

## 3. Những gì codebase KHÔNG nói (phải hỏi người, không đoán)
- Ai là người dùng, mục tiêu kinh doanh → mission.md
- Vì sao chọn stack này → tech.md
- Feature nào đã bỏ dở / không còn dùng
- Môi trường deploy thật, dữ liệu thật
- 

## 4. Số liệu
- O: {{N_O}} · Q: {{N_Q}} · test: {{N_TEST_PASS}} pass / {{N_TEST_FAIL}} fail · TODO/FIXME: {{N_TODO}}
