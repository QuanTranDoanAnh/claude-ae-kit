# ae-kit — Agentic Engineering kit cho Claude Code

Đóng gói quy trình **intake → spec → design → tasks → contract → implement → evaluate → ratchet** thành một plugin dùng lại được cho mọi project.

```
Transcript khách  →  /ae-kit:intake     →  spec/discovery-T1.md  (câu hỏi, không suy diễn)
                  →  /ae-kit:specify    →  spec/requirements.md  (EARS, [src:] tag, non-goals)
                  →  /ae-kit:lint-spec  →  spec/lint-*.md        ─┐
                                                                   ├─ GATE 1: bạn duyệt R → accepted
                  →  /ae-kit:design     →  spec/design.md        (invariants ép xuống đúng tầng)
                  →  /ae-kit:plan       →  spec/tasks.md         ─┐
                                                                   ├─ GATE 2: bạn duyệt task & done-condition
                  →  /ae-kit:contract N →  spec/sprint-N.contract.md  (định nghĩa DONE trước khi code)
                  →  /ae-kit:next-task  ×n  (1 task / session, progress.md là handoff)
                  →  /ae-kit:evaluate N →  spec/eval-sprint-N-r*.md  ─┐
                                                                       ├─ GATE 3: bạn duyệt diff + PR
                  →  /ae-kit:ratchet    →  CLAUDE.md rule + test + hook
```

## Cài đặt

Thử trong một session (không cài):
```bash
claude plugin validate ./ae-kit
claude --plugin-dir ./ae-kit
```

Cài cố định từ thư mục local (marketplace kèm sẵn ở `../ae-kit-marketplace`, hoặc push lên GitHub rồi `claude plugin marketplace add <owner>/<repo>`):
```bash
claude plugin marketplace add ./ae-kit-marketplace
claude plugin install ae-kit@ae-kit-marketplace
```

## Dùng cho project mới

```
cd my-startup-project && git init
claude
> /ae-kit:init my-startup-project "TypeScript, Next.js, Prisma/SQLite" "pnpm typecheck --silent"
> (đặt transcript đã che PII vào intake/T1-transcript.md)
> /ae-kit:intake T1
> /ae-kit:specify
> /ae-kit:lint-spec        ← đọc câu hỏi, hỏi khách, sửa tay, đổi status → accepted
> /ae-kit:design
> /ae-kit:plan             ← duyệt tasks.md
> /ae-kit:contract 1
> /ae-kit:next-task        ← lặp
> /ae-kit:evaluate 1
> /ae-kit:ratchet "mô tả lỗi"
> /ae-kit:status           ← bất cứ lúc nào
```

## Thành phần

| Loại | Tên | Vai trò |
|------|-----|---------|
| skill | init, intake, specify, lint-spec, design, plan, contract, next-task, evaluate, ratchet, status | Các bước quy trình (gọi bằng `/ae-kit:<tên>`) |
| skill | spec-templates | Template artifact (không gọi trực tiếp) |
| agent | requirement-linter | Chỉ trả về câu hỏi; không điền chỗ trống |
| agent | planner | Vertical slice, depth-first, done-condition chạy được |
| agent | contract-reviewer | Phản biện "done" trước khi code |
| agent | evaluator | QA hoài nghi, độc lập, ngưỡng cứng cho invariants |
| hook | SessionStart | In trạng thái handoff từ spec/progress.md |
| hook | PreToolUse(Bash) | Chặn lệnh phá hoại (+ pattern riêng của project trong `.ae-kit/block-patterns.txt`) |
| hook | PostToolUse(Edit\|Write) | Chạy `.ae-kit/check.cmd`; im lặng khi pass, chi tiết khi fail |

## Nguyên tắc thiết kế (để bạn sửa plugin đúng tinh thần)

1. **Artifact là file trong repo**, không phải nội dung chat. Session mới phải dựng lại được trạng thái chỉ từ `spec/`.
2. **Traceability**: mọi requirement có `[src: T§]` hoặc `[src: A]`. Không nguồn → không viết.
3. **LLM đặt câu hỏi, người trả lời.** Intake và lint chỉ sinh câu hỏi. "Làm mịn" spec là làm với khách, không với model.
4. **Tách generator và evaluator.** Agent tự chấm sẽ tự khen. Evaluator không được xem lời giải thích của generator.
5. **Chốt "done" trước khi code** (sprint contract). Ranh giới ≥/> chốt ở đây, không ở lúc debug.
6. **Mỗi component là một giả định về điều model không tự làm được.** Khi model mới ra, xem lại: bỏ cái không còn load-bearing.
7. **Ratchet, không brainstorm.** CLAUDE.md chỉ dài ra sau lỗi thực tế. Dưới 40 dòng.
8. **Loop có stop rule.** next-task làm 1 task rồi dừng; evaluate có budget vòng fix.

## Tuỳ biến theo project

- `.ae-kit/check.cmd` — lệnh kiểm tra nhanh chạy sau mỗi edit (typecheck/lint). Mỗi project tự đặt.
- `.ae-kit/block-patterns.txt` — regex lệnh Bash cần chặn thêm, một dòng một pattern.
- `CLAUDE.md` — constitution; mục "Kỹ thuật" điền theo stack.
- Muốn evaluator dùng Playwright: thêm MCP Playwright vào project (`.mcp.json`) và cho phép tool `mcp__playwright__.*` trong `agents/evaluator.md` → `tools:`.

## Dữ liệu khách hàng
Transcript phải có sự đồng ý của khách, đã che PII, và không được sửa sau khi commit. Cân nhắc dùng API/plan có cam kết không dùng dữ liệu để huấn luyện cho các project có dữ liệu nhạy cảm.
