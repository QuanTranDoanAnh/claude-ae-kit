---
name: principle-guard-the-context-window
description: Giữ context của session gọn — đọc có chủ đích, đẩy việc đọc hàng loạt và output lớn sang subagent, ghi kết luận vào file thay vì giữ trong chat. Đọc đầu mỗi next-task, khi phải đọc > 10 file, hoặc khi output lệnh dài.
---

# Giữ cửa sổ context (Guard the Context Window)

**Khi áp dụng:** đầu `/ae-kit:next-task`; intake C; bất kỳ lúc nào sắp `cat` cả thư mục hoặc chạy lệnh có output hàng nghìn dòng.

**Làm gì**
1. Đọc theo thứ tự ae-kit quy định (CLAUDE.md → progress.md → tasks.md → contract → R/I liên quan). KHÔNG đọc `docs/product/*` trừ khi task cần.
2. Cần quét nhiều file → Grep theo mẫu rồi Read đúng file; hoặc giao cho một subagent và chỉ nhận về kết luận + đường dẫn.
3. Output lệnh dài → `| tail -n 40` hoặc ghi ra file rồi đọc phần cần.
4. Kết luận, quyết định, lệnh đã chạy → ghi vào `spec/progress.md` ngay khi có; session sau dựng lại từ file, không từ chat.
5. Cảm thấy context đã nặng → kết thúc task hiện tại đúng quy trình (progress + commit) rồi dừng; không "cố thêm task nữa".

**Dấu hiệu vi phạm:** đọc lại cùng file lần thứ ba; `cat src/**`; quyết định chỉ tồn tại trong chat.

Nguồn: phỏng theo pstack "Guard the Context Window" (MIT) — xem NOTICE.md.
