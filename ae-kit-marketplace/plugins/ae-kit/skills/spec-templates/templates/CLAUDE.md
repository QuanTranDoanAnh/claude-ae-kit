# Constitution — {{PROJECT_NAME}}

<!-- TẦNG LUẬT. Những điều agent phải/không được làm bất kể task. Giữ dưới 40 dòng.
     Thêm dòng CHỈ qua /ae-kit:ratchet sau một lỗi thực tế. /ae-kit:replan không được chạm file này.
     Product context (mission, stack, roadmap) KHÔNG phải luật → docs/product/, đọc khi cần.
     Định dạng mỗi luật:  - <luật>. — <lý do> — [<nguồn>]
     Nguồn: [harness] có từ đầu · [ratchet #n] từ lỗi thực · [N<n>]/[I<n>] ép xuống từ spec/design · [C<n> O<m>] brownfield đã xác nhận -->

## Nguồn sự thật
- `spec/requirements.md` + `spec/design.md` là nguồn sự thật. Code mâu thuẫn spec → sửa spec trước, nêu lý do trong PR. — spec-anchored — [harness]
- Mọi requirement có tag `[src: T<n> §<m>]`, `[src: A<n>]` hoặc `[src: C<n> O<m>]`. Không nguồn → không viết. — traceability — [harness]
- `spec/gates.yaml` là trạng thái quy trình; `spec/progress.md` là handoff. Đọc đầu session, cập nhật cuối session. — context decay — [harness]

## Vòng lặp làm việc
- Mỗi session implement DUY NHẤT một task trong `spec/tasks.md`, rồi dừng. — một task một context — [harness]
- Không báo "xong" khi bất kỳ lệnh trong done-condition còn fail; chạy `{{CHECK_CMD}}` và dán kết quả. — generator tự khen — [harness]
- Không tự mở rộng scope. Thứ không có trong tasks.md → `spec/backlog.md`, không làm. — scope creep — [harness]
- Gặp điều spec không nói → ghi câu hỏi vào progress.md mục "Câu hỏi cần người quyết", KHÔNG tự chọn. — intake không suy diễn — [harness]

## Kỹ thuật
- Stack: {{STACK}}. Không thêm dependency ngoài stack khi chưa có D* trong spec/design.md. — agent kéo thư viện lạ — [harness]
- Thời gian: lưu UTC, chỉ convert ở UI. — bẫy timezone — [harness]
- Không dùng `any` / không bỏ qua lỗi type bằng cast. — agent né type — [harness]

## Cấm
- Không comment-out test. Sửa hoặc xoá. — [harness]
- Không push thẳng lên `main`. Luôn branch + PR. — [harness]
- Không chạy lệnh phá hoại (rm -rf, git push --force, DROP, reset --hard) — hook chặn. — [harness]

## Ratchet log
<!-- - YYYY-MM-DD | ratchet #n | lỗi gì | rule/test/hook nào được thêm -->
