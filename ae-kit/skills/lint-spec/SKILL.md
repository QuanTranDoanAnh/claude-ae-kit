---
name: lint-spec
description: Chạy requirement-linter lên spec/requirements.md — tìm câu không testable, mâu thuẫn, thuật ngữ chưa định nghĩa, khoảng trống what-if, thiếu nguồn gốc. Chỉ trả về câu hỏi. Chạy trước gate 1.
disable-model-invocation: true
allowed-tools: Read Glob Grep Agent
---

Gọi subagent `ae-kit:requirement-linter` với yêu cầu: lint `spec/requirements.md` và các `spec/discovery-*.md`, ghi kết quả vào `spec/lint-<YYYY-MM-DD>.md`.

Sau khi subagent trả về:
1. Đọc file lint vừa tạo.
2. Trình bày cho người dùng theo 2 nhóm:
   - **Cần hỏi lại khách** (không thể tự quyết): liệt kê câu hỏi sẵn sàng gửi.
   - **Người dùng tự quyết được** (ranh giới kỹ thuật, wording): liệt kê kèm 2 lựa chọn mỗi mục.
3. KHÔNG tự sửa requirements.md. Đề nghị: sau khi người dùng trả lời, chạy `/ae-kit:specify` lại (nếu có transcript mới) hoặc người dùng sửa tay rồi đổi trạng thái sang `accepted`.
