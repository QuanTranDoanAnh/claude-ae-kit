---
name: principle-prove-it-works
description: Chỉ báo "xong" khi đã kiểm chứng trên artifact thật (lệnh chạy, test có tên, request thật), không phải "compile được" hay "đọc code thấy đúng". Đọc trước khi đánh [x] một task, trước khi kết thúc next-task, và trước khi trả lời người dùng rằng việc đã xong.
---

# Chứng minh nó chạy (Prove It Works)

**Khi áp dụng:** trước khi đánh `[x]`, trước khi commit, trước câu "đã xong".

**Làm gì**
1. Chạy đúng lệnh trong `Done:` của task và dán output vào `spec/progress.md`. Lệnh fail → task chưa xong, dù "chỉ là flaky".
2. Bằng chứng phải cùng bề mặt với người dùng: UI → chạy e2e/Playwright hoặc mô tả thao tác đã làm; API → request thật; CLI → lệnh thật. "Typecheck pass" là điều kiện cần, không phải bằng chứng.
3. Phân biệt trong báo cáo: *đo được* (đã chạy, có output) · *suy ra* (từ code/log) · *đoán*. Không nâng "suy ra" thành "đo được".
4. Bằng chứng không chạy được trong môi trường này → ghi rõ "chưa kiểm chứng" vào progress.md, không đánh `[x]`, hỏi người.

**Dấu hiệu vi phạm:** "Should work now"; test bị skip; đánh `[x]` rồi mới chạy lệnh.

Đây là principle mà evaluator (G4) dùng để chấm bạn; áp dụng trước để khỏi mất retry.

Nguồn: phỏng theo pstack "Prove It Works" (MIT) — xem NOTICE.md.
