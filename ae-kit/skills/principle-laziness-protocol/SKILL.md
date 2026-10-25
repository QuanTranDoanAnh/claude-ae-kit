---
name: principle-laziness-protocol
description: Lười có kỷ luật — chọn thay đổi nhỏ nhất giải quyết đúng vấn đề, xoá trước khi thêm. Đọc khi sắp refactor, khi diff đang phình, hoặc khi thấy mình muốn thêm lớp trừu tượng, helper, tham số "cho linh hoạt sau này".
---

# Lười có kỷ luật (Laziness Protocol)

**Khi áp dụng:** trước khi thêm một abstraction, một lớp, một tham số, một file; khi diff vượt quá `Files:` của task; khi refactor.

**Làm gì**
1. Viết ra một câu: vấn đề *thực sự* là gì (lỗi nào, R nào). Thay đổi nào nhỏ nhất làm câu đó đúng?
2. Thử **xoá** trước: code chết, wrapper chỉ một nơi gọi, tham số không ai truyền, cờ boolean không bao giờ false.
3. Chỉ thêm abstraction khi có ≥ 2 nơi dùng *đang tồn tại* trong diff này, không phải "sẽ có".
4. Một task = một mục đích. Thứ "tiện tay" → `spec/backlog.md`.

**Dấu hiệu vi phạm:** interface có một implementation; hàm `handleX` chỉ gọi `doX`; file `utils` mọc thêm; PR mô tả bằng "và cũng".

**Không áp dụng cho:** tách generator/evaluator, worktree riêng cho delegate, test — các thứ này tồn tại để tách vai trò, không phải để tiết kiệm dòng.

Nguồn: phỏng theo pstack "Laziness Protocol" (MIT) — xem NOTICE.md.
