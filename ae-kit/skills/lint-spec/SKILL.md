---
name: lint-spec
description: Chạy requirement-linter lên spec/requirements.md — tìm câu không testable, mâu thuẫn, thuật ngữ chưa định nghĩa, khoảng trống what-if, thiếu nguồn gốc, nguồn brownfield chưa xác nhận. Chỉ trả về câu hỏi. Sau đó tính lại các ô máy của G1 trong spec/gates.yaml.
disable-model-invocation: true
allowed-tools: Read Glob Grep Agent Bash(bash *)
---

Gọi subagent `ae-kit:requirement-linter` với yêu cầu: lint `spec/requirements.md` và các `spec/discovery-*.md`, ghi kết quả vào `spec/lint-<YYYY-MM-DD>.md` (bảng có cột **Mức** = ERROR | WARN).

Sau khi subagent trả về:
1. Đọc file lint vừa tạo.
2. Trình bày cho người dùng theo 2 nhóm:
   - **Cần hỏi lại khách** (không thể tự quyết): liệt kê câu hỏi sẵn sàng gửi.
   - **Người dùng tự quyết được** (ranh giới kỹ thuật, wording): liệt kê kèm 2 lựa chọn mỗi mục.
3. KHÔNG tự sửa requirements.md. Đề nghị: sau khi người dùng trả lời, chạy `/ae-kit:specify` lại (nếu có transcript mới) hoặc người dùng sửa tay rồi đổi trạng thái sang `accepted`; nhắc điền cột **Nhãn** (`send | assume | defer`) cho mọi Q trong discovery và `decided | debt | ignore` cho mọi O (brownfield).
4. **Ghi ô máy của G1:** chạy
   ```
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" compute G1
   ```
   Script tự đếm ERROR trong lint mới nhất, R còn `proposed`, Q chưa có nhãn, O chưa phân loại, và ghi vào `spec/gates.yaml`. Dán output cho người dùng.
5. Kết thúc bằng đúng một dòng: nếu script báo "tất cả ô xanh" → "Chạy `/ae-kit:approve G1`"; nếu còn ô đỏ → liệt kê ô đỏ và việc cần làm, rồi "chạy lại `/ae-kit:lint-spec`".
