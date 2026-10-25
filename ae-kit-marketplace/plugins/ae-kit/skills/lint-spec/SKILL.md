---
name: lint-spec
description: Chạy requirement-linter lên spec/requirements.md — tìm câu không testable, mâu thuẫn, thuật ngữ chưa định nghĩa, khoảng trống what-if, thiếu nguồn gốc, nguồn brownfield chưa xác nhận. Chỉ trả về câu hỏi, trình bày theo vòng (frontier, mỗi câu kèm đề xuất). Sau đó tính lại các ô máy của G1 trong spec/gates.yaml.
disable-model-invocation: true
allowed-tools: Read Edit Glob Grep Agent Bash(bash *)
---

Gọi subagent `ae-kit:requirement-linter` với yêu cầu: lint `spec/requirements.md` và các `spec/discovery-*.md`, ghi kết quả vào `spec/lint-<YYYY-MM-DD>.md` (bảng có cột **Mức** = ERROR | WARN, cột **Hỏi ai** = khách | người dùng, cột **Sau** = mã phát hiện phải chốt trước, cột **Quyết định** để trống).

Cách hỏi theo vòng: `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/references/grilling.md`.

Sau khi subagent trả về:
1. Đọc file lint vừa tạo. Phát hiện nào thực ra là **sự thật tra cứu được** (grilling.md §1) → tự tra, ghi kết quả vào cột Quyết định với bằng chứng, không hỏi.
2. Tính frontier (phát hiện chưa có Quyết định, mọi "Sau" đã có Quyết định). Trình bày **vòng 1** theo định dạng grilling.md §3, chia hai nhóm trong cùng vòng:
   - **Cần hỏi lại khách** — mỗi câu sẵn sàng copy gửi khách; đề xuất là giả định mặc định sẽ dùng nếu khách không trả lời; người chỉ chọn `send` hoặc `defer` (hoặc trả lời thay khách nếu họ có thẩm quyền — ghi rõ "người dùng quyết thay").
   - **Người dùng tự quyết được** (ranh giới kỹ thuật, wording, ngưỡng) — mỗi mục đúng 2 lựa chọn kèm hệ quả; đề xuất một trong hai; `yes` = chọn đề xuất.
   Tối đa 7 mục/vòng; ERROR đi trước WARN.
3. Chờ trả lời. Ghi vào cột Quyết định của `spec/lint-<ngày>.md` (chỉ `Edit` file lint; với Q mới cần hỏi khách, thêm dòng Q vào bảng Open Questions của discovery liên quan với nhãn người chọn). KHÔNG tự sửa `requirements.md`: liệt kê gọn những dòng R người cần sửa tay theo quyết định vừa chốt, rồi người đổi trạng thái sang `accepted`. Tính lại frontier, vòng tiếp, cho tới khi hết hoặc người dừng.
4. Nhắc điền cột **Nhãn** (`send | assume | defer`) cho mọi Q trong discovery và `decided | debt | ignore` cho mọi O (brownfield), nếu còn.
5. **Ghi ô máy của G1:** chạy
   ```
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" compute G1
   ```
   Script tự đếm ERROR trong lint mới nhất, R còn `proposed`, Q chưa có nhãn, O chưa phân loại, và ghi vào `spec/gates.yaml`. Dán output cho người dùng. Lưu ý: ERROR vẫn tính là ERROR cho tới khi người sửa `requirements.md` và chạy lại lint — cột Quyết định chỉ là biên bản.
6. Kết thúc bằng đúng một dòng: nếu script báo "tất cả ô xanh" → "Chạy `/ae-kit:approve G1`"; nếu còn ô đỏ → liệt kê ô đỏ và việc cần làm, rồi "chạy lại `/ae-kit:lint-spec`".
