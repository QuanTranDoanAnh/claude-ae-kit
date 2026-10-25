# Playbook: feature

Mục tiêu: hành vi mới chạy được end-to-end ở mức tối thiểu, có test tại seam đã chốt, done-condition pass.

1. **Đặt tên data shape** (`ae-kit:principle-model-the-domain` nếu task có trạng thái/nhánh). Ghi vào nhật ký progress.md: shape chính + cấu trúc tổ chức nó. Shape không có trong `spec/design.md` → hỏi người, dừng.
2. **Chọn seam** từ bảng Chốt của contract cho các tiêu chí mà task này đáp ứng. Mỗi tiêu chí → một seam đã ghi. Không có → hỏi người.
3. **Red**: viết một test tại seam, tên test đọc như dòng spec có mã R. Chạy — phải FAIL vì thiếu hành vi (không phải vì lỗi cú pháp). Test không fail → test sai, sửa test trước.
4. **Green**: viết lượng code tối thiểu để test đó pass. Không viết trước cho test sau. Chạy `.ae-kit/check.cmd` (hook đã chạy sau mỗi edit; xem output).
5. Lặp 3–4 cho từng tiêu chí của task, **một slice một lần**. Không refactor trong vòng red–green (refactor là task `Loại: refactor` hoặc là bước 6).
6. **Dọn tối thiểu** chỉ trong `Files:` của task, không đổi hành vi, test vẫn xanh (`ae-kit:principle-laziness-protocol` nếu thấy muốn thêm lớp).
7. **Chứng minh** (`ae-kit:principle-prove-it-works`): chạy đúng lệnh `Done:`; bằng chứng cùng bề mặt với người dùng (UI → e2e/Playwright hoặc thao tác thật). Dán output vào progress.md.
8. Hành vi đã mô tả trong spec thay đổi theo quyết định của người → sửa `spec/requirements.md`/`design.md` cùng commit.

Quy tắc test: `references/tdd.md`.
