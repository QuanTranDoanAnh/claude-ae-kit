---
name: ratchet
description: Biến một lỗi thực tế thành rule vĩnh viễn — thêm dòng vào CLAUDE.md (kèm lý do), test regression, và/hoặc pattern vào hook. Chạy sau mỗi lỗi đáng giá được evaluator hoặc người dùng phát hiện.
disable-model-invocation: true
argument-hint: "\"<mô tả lỗi>\""
allowed-tools: Read Write Edit Glob Grep Bash
---

Lỗi cần ratchet: `$ARGUMENTS` (nếu trống, đọc mục "Đề xuất ratchet" trong file `spec/eval-sprint-*` mới nhất và hỏi người dùng chọn).

Nguyên tắc: **mỗi lỗi → tối đa ba thay đổi, mỗi thay đổi có lý do truy ngược được.** Không thêm rule phòng ngừa cho lỗi chưa xảy ra. CLAUDE.md là pilot's checklist, không phải style guide — giữ dưới 40 dòng; nếu vượt, đề xuất gộp/bỏ dòng cũ không còn load-bearing.

Với lỗi này, quyết định (và giải thích cho người dùng) từng mức:

1. **Rule trong `CLAUDE.md`** — chỉ khi lỗi là do agent *không biết* một quy ước. Viết một dòng, cụ thể, kiểm chứng được. Thêm vào đúng mục. Thêm dòng vào "Ratchet log": `- <date> | <lỗi> | <rule> | <test/hook>`.
2. **Test regression** — chỉ khi lỗi có thể tái hiện bằng code. Đặt tên file nêu rõ lỗi (`slots.tokyo-boundary.test.ts`). Test phải FAIL trên code cũ và PASS trên code đã sửa — xác nhận bằng cách chạy.
3. **Hook / pattern** — chỉ khi lỗi là một *hành động* có thể chặn cơ học (lệnh nguy hiểm, pattern code cấm). Với lệnh Bash: thêm regex vào `${CLAUDE_PROJECT_DIR}/.ae-kit/block-patterns.txt` (một pattern một dòng, kèm `# lý do`) — hook của plugin sẽ đọc thêm file này. Với pattern code: thêm vào lệnh trong `.ae-kit/check.cmd` hoặc lint config của dự án.

Kết thúc: liệt kê đúng những gì đã thêm (file, dòng) và mức nào đã bỏ qua kèm lý do.
