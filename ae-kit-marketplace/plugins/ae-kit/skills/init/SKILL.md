---
name: init
description: Khởi tạo cấu trúc ae-kit cho một project mới — thư mục intake/, spec/, CLAUDE.md constitution, .ae-kit/check.cmd. Dùng ngay sau khi tạo repo.
disable-model-invocation: true
argument-hint: "<project-name> \"<stack>\" \"<check-cmd>\""
allowed-tools: Read Write Bash(mkdir *) Bash(ls *) Bash(git *)
---

Khởi tạo ae-kit cho project hiện tại. Tham số: `$0` = tên project, `$1` = stack (ví dụ "TypeScript, Next.js, Prisma/SQLite"), `$2` = lệnh kiểm tra nhanh (ví dụ "pnpm typecheck --silent && pnpm lint --silent").

Nếu thiếu tham số, hỏi người dùng đúng các giá trị còn thiếu rồi mới tiếp tục.

## Việc cần làm
1. Tạo thư mục: `intake/`, `spec/`, `.ae-kit/`.
2. Nếu `CLAUDE.md` chưa tồn tại: copy `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/templates/CLAUDE.md` thành `CLAUDE.md` ở root, thay `{{PROJECT_NAME}}`, `{{STACK}}`, `{{CHECK_CMD}}`. Nếu đã tồn tại: KHÔNG ghi đè; thêm vào cuối một dòng `@spec/README.md` nếu chưa có và báo người dùng tự merge phần constitution.
3. Ghi `.ae-kit/check.cmd` chứa đúng một dòng: `$2` (hook post-edit đọc file này).
4. Ghi `spec/progress.md` từ template progress (thay placeholder; trạng thái "chưa bắt đầu").
5. Ghi `spec/README.md` ngắn mô tả các file trong spec/ và thứ tự quy trình:
   `intake → specify → lint-spec → (duyệt) → design → plan → (duyệt) → contract → next-task ×n → evaluate → ratchet`.
6. Ghi `intake/README.md`: nhắc rằng transcript phải được khách đồng ý, đã che PII (tên, email, số điện thoại, số hợp đồng), đặt tên `T<n>-transcript.md`, và KHÔNG được sửa sau khi commit.
7. Nếu là git repo: thêm `.ae-kit/` vào `.gitignore`? KHÔNG — `.ae-kit/check.cmd` cần được commit để cả team dùng. Chỉ bỏ qua nếu người dùng yêu cầu.
8. In ra cây thư mục vừa tạo và bước tiếp theo: "Đặt transcript vào intake/T1-transcript.md rồi chạy `/ae-kit:intake T1`".
