---
name: principle-encode-lessons-in-structure
description: Khi thấy mình viết cùng một lời nhắc lần thứ hai, biến nó thành lint, hook, test, type hoặc script thay vì thêm chữ vào CLAUDE.md. Đọc khi chạy /ae-kit:ratchet và khi CLAUDE.md tiến gần 40 dòng.
---

# Mã hoá bài học vào cấu trúc

**Khi áp dụng:** `/ae-kit:ratchet`; audit CLAUDE.md; mỗi lần "Đề xuất ratchet" lặp lại một ý đã có.

**Làm gì**
1. Với mỗi bài học, hỏi theo thứ tự: chặn được bằng **hook** không (lệnh, pattern)? bắt được bằng **test/lint/type** không? ép được bằng **cấu trúc** không (bảng tra, type không biểu diễn được trạng thái sai)? Chỉ khi cả ba không được mới thành **dòng CLAUDE.md**.
2. Luật chỉ đúng trong *tình huống* (khi refactor, khi sửa bug) → không vào CLAUDE.md; thêm dòng trigger vào `.ae-kit/principles.md` trỏ tới principle phù hợp (ratchet mức 4).
3. Dòng CLAUDE.md đã có hook/test tương đương → đề xuất xoá dòng, giữ cơ chế.
4. Mỗi thay đổi ghi được nguồn `[ratchet #n]`; không có lỗi thật đứng sau → không thêm.

**Dấu hiệu vi phạm:** CLAUDE.md > 40 dòng; hai dòng cùng ý; luật "hãy cẩn thận với X" không ai kiểm được.

Nguồn: phỏng theo pstack "Encode Lessons in Structure" (MIT) — xem NOTICE.md.
