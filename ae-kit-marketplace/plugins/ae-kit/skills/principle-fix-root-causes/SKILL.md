---
name: principle-fix-root-causes
description: Khi sửa lỗi, lần ngược từ triệu chứng về điểm đầu tiên hệ thống sai và sửa ở đó; một guard chỉ là fix khi trạng thái nó xử lý là hợp lệ. Đọc trong playbook bugfix và khi evaluator trả FAIL.
---

# Sửa tận gốc (Fix Root Causes)

**Khi áp dụng:** task `Loại: bugfix`; mỗi FAIL từ evaluator; bất kỳ lúc nào sắp thêm `if (x == null) return`.

**Làm gì**
1. Tái hiện trước (test fail hoặc script fail). Chưa tái hiện được → chưa được sửa.
2. Lần ngược: dữ liệu/trạng thái sai *xuất hiện lần đầu* ở đâu? Ghi chuỗi: triệu chứng ← hàm ← dữ liệu ← nơi tạo ra dữ liệu. Sửa ở mắt xích đầu.
3. Hỏi về mỗi guard định thêm: trạng thái này có hợp lệ theo `spec/design.md` không? Hợp lệ → guard đúng. Không hợp lệ → guard chỉ che; sửa nơi tạo ra nó (hoặc ép invariant ở biên).
4. Sau khi sửa: test tái hiện phải chuyển FAIL → PASS; đặt tên test theo lỗi.
5. Lỗi đến từ quy ước agent không biết → "Đề xuất ratchet" trong progress.md.

**Dấu hiệu vi phạm:** `try/catch` nuốt lỗi; `?? default` ở nơi nhận; sửa hai chỗ cho một lỗi; "thêm null check" là toàn bộ fix.

Nguồn: phỏng theo pstack "Fix Root Causes" (MIT) — xem NOTICE.md.
