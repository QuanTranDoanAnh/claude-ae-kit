---
name: principle-model-the-domain
description: Đặt tên hình dạng dữ liệu trước khi viết logic; dùng state machine, typed model, bảng tra thay cho boolean rải rác và if-else lặp. Đọc khi task có trạng thái, có nhiều nhánh rẽ, hoặc cùng một giả định về shape lặp ở nhiều file.
---

# Mô hình hoá domain trước (Model the Domain)

**Khi áp dụng:** bất kỳ task nào có *trạng thái* (đơn hàng, lịch hẹn, phiên), có ≥ 3 nhánh `if` trên cùng một thứ, hoặc một shape dữ liệu được giả định ở nhiều file.

**Làm gì**
1. Trước dòng code đầu tiên, ghi vào `spec/progress.md` mục nhật ký: *tên* của data shape chính và *cấu trúc tổ chức* nó: state machine / typed model / bảng-registry / reducer / collection đúng loại.
2. Trạng thái: liệt kê đủ state và transition hợp lệ; transition không hợp lệ phải không biểu diễn được (type) hoặc bị từ chối ở một chỗ duy nhất.
3. Nhánh rẽ theo loại: một bảng tra `{loại → hành vi}` thay vì `switch` lặp ở nhiều nơi.
4. Đối chiếu với `spec/design.md` (entities, invariants). Shape mới không có trong design → ghi "Câu hỏi cần người quyết", không tự thêm entity.

**Dấu hiệu vi phạm:** `isPaid && !isCancelled && hasSlot`; cùng một `switch(type)` ở 3 file; `any`/`dict` không có schema đi qua nhiều tầng.

Nguồn: phỏng theo pstack "Model the Domain" (MIT) — xem NOTICE.md.
