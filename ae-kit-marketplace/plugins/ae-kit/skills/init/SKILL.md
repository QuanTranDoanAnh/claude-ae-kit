---
name: init
description: Khởi tạo cấu trúc ae-kit cho một project — intake/, spec/ (gates.yaml, progress.md), docs/product/ (mission, tech, roadmap), CLAUDE.md tầng luật, .ae-kit/check.cmd. Tự nhận diện repo đã có code (brownfield). Dùng ngay sau khi tạo repo hoặc khi đưa ae-kit vào codebase cũ.
disable-model-invocation: true
argument-hint: "<project-name> \"<stack>\" \"<check-cmd>\" [\"<sản phẩm là gì, 1 câu>\"]"
allowed-tools: Read Write Bash(mkdir *) Bash(ls *) Bash(git *) Bash(python3 *) Bash(cp *) Bash(date *) Glob
---

Khởi tạo ae-kit cho project hiện tại. Tham số: `$0` = tên project, `$1` = stack (ví dụ "TypeScript, Next.js, Prisma/SQLite"), `$2` = lệnh kiểm tra nhanh (ví dụ "pnpm typecheck --silent && pnpm lint --silent"), `$3` = sản phẩm là gì trong một câu (tuỳ chọn).

Nếu thiếu `$0`–`$2`, hỏi người dùng đúng các giá trị còn thiếu rồi mới tiếp tục. Template nằm ở `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/templates/`.

## Bước 0 — Nhận diện greenfield / brownfield
Repo là **brownfield** nếu có bất kỳ: `package.json`, `pyproject.toml`, `pom.xml`, `go.mod`, `Cargo.toml`, hoặc thư mục `src/`/`app/`/`lib/` không rỗng. Ghi nhớ kết quả cho các bước dưới.

## Việc cần làm
1. Tạo thư mục: `intake/`, `spec/`, `docs/product/`, `.ae-kit/`.
2. **CLAUDE.md (tầng luật).** Nếu chưa tồn tại: copy template `CLAUDE.md`, thay `{{PROJECT_NAME}}`, `{{STACK}}`, `{{CHECK_CMD}}`. Nếu đã tồn tại: KHÔNG ghi đè; in ra khối "## Nguồn sự thật" + "## Vòng lặp làm việc" của template và bảo người dùng tự merge; nhắc định dạng luật `- <luật>. — <lý do> — [<nguồn>]`.
   - Brownfield: KHÔNG điền mục "## Kỹ thuật" ngoài dòng Stack; thêm comment `<!-- luật kỹ thuật sẽ đến từ discovery-C1 sau khi người xác nhận -->`.
3. **docs/product/ (tầng context).** Copy `mission.md`, `tech.md`, `roadmap.md`, thay `{{PROJECT_NAME}}`, `{{STACK}}`, `{{CHECK_CMD}}`, `{{DATE}}` (hôm nay).
   - Greenfield: nếu không có `$3`, hỏi đúng 3 câu — (a) sản phẩm là gì trong 1 câu, (b) cho ai, (c) non-goal lớn nhất — rồi điền `mission.md` với `[src: owner <ngày>]`. Điền bảng Stack trong `tech.md` từ `$1`, cột Src = `owner <ngày>`.
   - Brownfield: để bảng Stack trong `tech.md` trống với ghi chú `<!-- điền từ discovery-C1 sau khi người xác nhận -->`; vẫn hỏi 3 câu cho mission.md (codebase không trả lời được "cho ai").
4. **spec/gates.yaml.** Copy template `gates.yaml`, thay `{{PROJECT_NAME}}`. Brownfield: chạy `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" set G1_spec.checks.observed_classified false`.
5. Ghi `.ae-kit/check.cmd` chứa đúng một dòng: `$2` (hook post-edit và gates.py đọc file này).
6. Ghi `spec/progress.md` từ template progress (thay placeholder; sprint 1, trạng thái "chưa bắt đầu").
7. Ghi `spec/README.md` ngắn mô tả các file trong spec/ và thứ tự quy trình:
   `intake (T<n> transcript | C<n> codebase) → specify → lint-spec → approve G1 → design → plan → approve G2 → contract (G3) → next-task ×n → evaluate (G4) → approve G5 → ratchet / replan`.
8. Ghi `intake/README.md`: transcript phải được khách đồng ý, đã che PII (tên, email, số điện thoại, số hợp đồng), đặt tên `T<n>-transcript.md`, KHÔNG sửa sau khi commit. Với codebase cũ không cần file trong intake/, chạy `/ae-kit:intake C1`.
9. Nếu là git repo: KHÔNG thêm `.ae-kit/` vào `.gitignore` — `check.cmd` cần được commit để cả team dùng.
10. Chạy `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" show` để xác nhận 5 gate hiện đúng.
11. In cây thư mục vừa tạo và bước tiếp theo:
    - Greenfield: "Đặt transcript vào intake/T1-transcript.md rồi chạy `/ae-kit:intake T1`".
    - Brownfield: "Chạy `/ae-kit:intake C1` để quan sát codebase TRƯỚC khi specify".
