# Constitution — {{PROJECT_NAME}}

<!-- Mỗi dòng dưới đây phải truy ngược được về một lý do cụ thể.
     Thêm dòng mới CHỈ qua /ae:ratchet sau một lỗi thực tế. Giữ dưới 40 dòng. -->

## Nguồn sự thật
- `spec/requirements.md` và `spec/design.md` là nguồn sự thật. Code mâu thuẫn spec → sửa spec trước, nêu lý do trong PR.
- Mọi requirement phải có tag nguồn gốc: `[src: T<n> §<m>]` (khách nói) hoặc `[src: A<n>]` (giả định, chưa xác nhận). Không tạo requirement không có tag.
- `spec/progress.md` là handoff giữa các session. Đọc nó đầu session, cập nhật nó cuối session.

## Vòng lặp làm việc
- Mỗi session implement DUY NHẤT một task trong `spec/tasks.md`, rồi dừng.
- Không báo "xong" khi bất kỳ lệnh trong done-condition của task còn fail.
- Không tự mở rộng scope. Thứ không có trong tasks.md → ghi vào `spec/backlog.md`, không làm.

## Kỹ thuật (điền theo stack của dự án)
- Ngôn ngữ/stack: {{STACK}}
- Lệnh kiểm tra: `{{CHECK_CMD}}`
- Thời gian: lưu UTC, chỉ convert ở UI.
- Không dùng `any` / không bỏ qua lỗi type bằng cast.

## Cấm
- Không comment-out test. Sửa hoặc xoá.
- Không push thẳng lên `main`. Luôn branch + PR.
- Không chạy lệnh phá hoại (rm -rf, git push --force, DROP, reset --hard) — hook sẽ chặn.

## Ratchet log
<!-- Dạng: - YYYY-MM-DD | lỗi gì | rule nào được thêm | test/hook nào được thêm -->
