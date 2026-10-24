---
name: ratchet
description: Biến một lỗi thực tế thành rule vĩnh viễn — thêm dòng vào CLAUDE.md theo định dạng `- <luật>. — <lý do> — [<nguồn>]`, test regression, và/hoặc pattern vào hook. Giữ CLAUDE.md dưới 40 dòng. `--audit` chỉ kiểm tra, không thêm. Là nơi DUY NHẤT được sửa tầng luật.
disable-model-invocation: true
argument-hint: "\"<mô tả lỗi>\" | --audit"
allowed-tools: Read Write Edit Glob Grep Bash
---

`$ARGUMENTS`:
- `--audit` → chỉ kiểm tra (mục Audit dưới), không thêm gì.
- mô tả lỗi → ratchet lỗi đó.
- trống → đọc mục "Đề xuất ratchet" trong `spec/progress.md` và trong file `spec/eval-sprint-*` mới nhất; liệt kê, hỏi người dùng chọn dòng nào, rồi ratchet từng dòng.

## Audit (luôn chạy trước khi thêm, và là toàn bộ việc khi `--audit`)
1. Đếm dòng `CLAUDE.md`. ≥ 40 → không được thêm dòng mới trước khi gộp/xoá: đề xuất dòng ít load-bearing nhất (không truy ngược về lỗi, trùng ý với dòng khác, hoặc đã được hook/lint/test bắt cơ học) và hỏi người.
2. Liệt kê dòng luật (bắt đầu bằng `- `) KHÔNG kết thúc bằng `[harness]`, `[ratchet #n]`, `[N<n>]`, `[I<n>]` hoặc `[C<n> O<m>]` → đề xuất bổ sung nguồn hoặc xoá.
3. Liệt kê cặp dòng trùng ý.
4. Kiểm tra `CLAUDE.md` không chứa nội dung tầng context (mission, roadmap, danh sách feature) — nếu có → đề xuất chuyển sang `docs/product/`.
In kết quả dạng bảng ngắn. Nếu `--audit` → dừng ở đây.

## Ratchet một lỗi
Nguyên tắc: **mỗi lỗi → tối đa ba thay đổi, mỗi thay đổi có lý do truy ngược được.** Không thêm rule phòng ngừa cho lỗi chưa xảy ra. CLAUDE.md là pilot's checklist, không phải style guide.

Số ratchet `n` = số lớn nhất trong Ratchet log + 1.

Với lỗi này, quyết định (và giải thích cho người dùng) từng mức:

1. **Rule trong `CLAUDE.md`** — chỉ khi lỗi là do agent *không biết* một quy ước. Viết đúng một dòng theo định dạng `- <luật>. — <lý do> — [ratchet #n]` (nguồn `[I<n>]`/`[N<n>]` nếu đến từ đề xuất của design; `[C<n> O<m>]` nếu từ brownfield decided). Thiếu nguồn → KHÔNG ghi. Thêm vào đúng mục. Thêm dòng vào "Ratchet log": `- <date> | ratchet #n | <lỗi> | <rule/test/hook>`.
2. **Test regression** — chỉ khi lỗi có thể tái hiện bằng code. Đặt tên file nêu rõ lỗi (`slots.tokyo-boundary.test.ts`). Test phải FAIL trên code cũ và PASS trên code đã sửa — xác nhận bằng cách chạy.
3. **Hook / pattern** — chỉ khi lỗi là một *hành động* có thể chặn cơ học (lệnh nguy hiểm, pattern code cấm). Với lệnh Bash: thêm regex vào `${CLAUDE_PROJECT_DIR}/.ae-kit/block-patterns.txt` (một pattern một dòng, kèm `# lý do`). Với pattern code: thêm vào lệnh trong `.ae-kit/check.cmd` hoặc lint config của dự án.

Nếu dòng đề xuất đến từ "Đề xuất ratchet" của progress.md → sau khi ghi, xoá dòng đó khỏi progress.md.

Kết thúc: liệt kê đúng những gì đã thêm (file, dòng) và mức nào đã bỏ qua kèm lý do; in số dòng CLAUDE.md hiện tại /40.
