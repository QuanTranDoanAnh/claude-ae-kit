---
name: plan
description: Gọi planner để phân rã requirements + design thành spec/tasks.md (vertical slice, depth-first, mỗi task có ↔ R, Done:, Files:). Sau đó tính lại ô máy của G2 trong spec/gates.yaml. Người duyệt bằng /ae-kit:approve G2.
disable-model-invocation: true
allowed-tools: Read Glob Grep Agent Bash(bash *)
---

## Điều kiện vào
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" get G1_spec.status` phải là `passed`; nếu không → DỪNG, in "G1 chưa passed — `/ae-kit:approve G1` trước".

## Chạy
Gọi subagent `ae-kit:planner` để tạo/cập nhật `spec/tasks.md`. Nhắc planner: mỗi task bắt buộc có 3 dòng `↔`, `Done:`, `Files:`; task đầu tiên phải ghi rõ là vertical slice đi xuyên mọi tầng.

Sau khi planner trả về:
1. Đọc `spec/tasks.md`. Kiểm tra nhanh: mỗi task có `↔ R/I`, `Done:` là lệnh/bằng chứng cụ thể, `Files:` liệt kê file/thư mục dự kiến? Task nào vi phạm → liệt kê.
2. **Ghi ô máy của G2:** chạy
   ```
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" compute G2
   ```
   Script so tập R/N accepted với tập R trong tasks.md, kiểm `Done:`/`Files:` từng task, kiểm task đầu là e2e, và ghi `blocked_by`. Dán output. Nếu có ô đỏ do planner (R chưa có task, task thiếu dòng) → gọi lại planner với danh sách đó, tối đa 2 lần, rồi compute lại.
3. Trình bày cho người dùng: bảng sprint → task → R → done-condition → files. Đánh dấu 3 task rủi ro nhất.
4. Đây là **gate 2**: kết thúc bằng đúng một dòng — mọi ô xanh → "Duyệt bằng `/ae-kit:approve G2`"; còn đỏ → liệt kê và "sửa tasks.md rồi chạy lại `/ae-kit:plan`". Không tự chuyển sang bước tiếp.
