---
name: specify
description: Tổng hợp các spec/discovery-*.md thành spec/requirements.md (EARS, có tag nguồn gốc, non-goals, glossary). Gộp vai trò SRS + PRD thành một file requirement. Chạy sau /ae-kit:intake.
disable-model-invocation: true
allowed-tools: Read Write Glob Grep
---

Tạo hoặc cập nhật `spec/requirements.md` từ toàn bộ `spec/discovery-*.md` (và `intake/*` để đối chiếu).

## Quy tắc không thương lượng
- Mỗi requirement PHẢI có tag `[src: T<n> §<m>]` (khách nói) hoặc `[src: A<n>]` (giả định đã khai báo trong discovery). Không có nguồn → không được viết. Nếu bạn thấy cần một requirement mà không có nguồn, thêm nó vào mục "Open Questions bổ sung" ở cuối file, dưới dạng câu hỏi.
- Viết theo EARS (xem template). Mỗi câu phải testable: nếu không viết được một test cho nó, viết lại hoặc chuyển thành câu hỏi.
- Trạng thái khởi tạo: `proposed`. Chỉ người dùng chuyển sang `accepted`.
- **Non-goals** bắt buộc không trống: mọi tính năng được nhắc trong discovery mà không thành requirement phải xuất hiện ở Non-goals kèm lý do. Không để tính năng "lửng lơ".
- Non-functional (hiệu năng, bảo mật, i18n, audit) tách riêng nhóm N*.
- Glossary: thống nhất mỗi thuật ngữ một nghĩa; nếu khách dùng một từ theo hai nghĩa, tách thành hai thuật ngữ và ghi nguồn.

## Nếu requirements.md đã tồn tại
Không viết lại từ đầu. Giữ nguyên mã R hiện có và trạng thái của chúng; chỉ thêm/sửa dựa trên discovery mới, ghi rõ `(updated from T<n>)` ở dòng bị sửa. Requirement bị khách rút lại → chuyển sang Non-goals với ghi chú, không xoá.

## Kết thúc
Tóm tắt: số R theo nhóm, số dòng còn tag A* (cần khách xác nhận), và nhắc bước tiếp theo: `/ae-kit:lint-spec` rồi duyệt (gate 1).
