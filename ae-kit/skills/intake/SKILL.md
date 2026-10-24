---
name: intake
description: Chuyển transcript trao đổi với khách (intake/T<n>-transcript.md) thành spec/discovery-T<n>.md — chỉ TRÍCH XUẤT và ĐẶT CÂU HỎI, không suy diễn requirement. Bước đầu tiên của quy trình.
disable-model-invocation: true
argument-hint: "<T-id, ví dụ T1>"
allowed-tools: Read Write Glob Grep
---

Xử lý transcript `intake/$0-transcript.md` (nếu `$0` trống, liệt kê các transcript trong `intake/` và hỏi).

## Nguyên tắc cốt lõi
Bạn đang làm việc với lời của khách hàng. Nhiệm vụ của bạn là **làm lộ ra những gì người cần quyết định**, không phải thay họ quyết định. Mọi chỗ trống trong transcript là một CÂU HỎI, không phải một chỗ để bạn điền giả định hợp lý.

## Các bước
1. Đọc toàn bộ transcript. Đánh số đoạn (§1, §2, …) theo lượt nói hoặc theo đoạn tự nhiên nếu transcript chưa đánh số; nếu phải đánh số, ghi phiên bản đã đánh số vào `intake/$0-transcript.numbered.md` (KHÔNG sửa file gốc).
2. Tạo `spec/discovery-$0.md` từ template `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/templates/discovery.md`:
   - **Statements**: mỗi điều khách nói có giá trị requirement → một dòng S<n>, trích dẫn sát nghĩa (không "làm đẹp"), vị trí §, loại (goal / constraint / pain / example / out-of-scope).
   - **Glossary nháp**: thuật ngữ nội bộ của khách, theo nghĩa khách dùng.
   - **Open Questions**: với mỗi khoảng trống, mơ hồ, hoặc chỗ có ≥2 cách hiểu → một câu hỏi cụ thể cho khách, kèm "vì sao quan trọng" và "giả định mặc định A<n> nếu không được trả lời". Đây là OUTPUT CHÍNH.
   - **Mâu thuẫn**: hai statement nói ngược nhau.
   - **Những gì khách KHÔNG nói**: checklist tối thiểu — đăng nhập/phân quyền, dữ liệu cũ/migration, đa ngôn ngữ, mobile, hiệu năng/khối lượng, audit/log, tích hợp hệ thống khác, ai vận hành, ngân sách/thời hạn.
3. Tuyệt đối KHÔNG viết requirement, KHÔNG đề xuất giải pháp, KHÔNG chọn stack ở bước này.
4. Kết thúc bằng tóm tắt cho người dùng: số statement, số câu hỏi, 3 câu hỏi quan trọng nhất cần hỏi khách trước. Gợi ý: gửi mục Open Questions cho khách; câu trả lời ghi thành `intake/T<n+1>-transcript.md`, rồi chạy lại `/ae-kit:intake` cho transcript mới hoặc chạy `/ae-kit:specify` nếu đủ thông tin.
