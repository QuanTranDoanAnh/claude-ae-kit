---
name: plan
description: Gọi planner để phân rã requirements + design thành spec/tasks.md (vertical slice, depth-first, done-condition chạy được). Gate 2 — người dùng duyệt thứ tự và done-condition trước khi implement.
disable-model-invocation: true
allowed-tools: Read Glob Grep Agent
---

Gọi subagent `ae-kit:planner` để tạo/cập nhật `spec/tasks.md`.

Sau khi planner trả về:
1. Đọc `spec/tasks.md`. Kiểm tra nhanh: mỗi task có `↔ R/I` và `Done:` là lệnh/bằng chứng cụ thể không? Task nào vi phạm → liệt kê.
2. Trình bày cho người dùng: bảng sprint → task → R → done-condition. Đánh dấu 3 task rủi ro nhất.
3. Đây là **gate 2**: nói rõ người dùng cần duyệt (hoặc sửa tay) trước khi chạy `/ae-kit:contract 1`. Không tự chuyển sang bước tiếp.
