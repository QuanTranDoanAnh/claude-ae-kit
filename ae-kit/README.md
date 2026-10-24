# ae-kit — Agentic Engineering kit cho Claude Code

Đóng gói quy trình **intake → spec → design → tasks → contract → implement → evaluate → ratchet / replan** thành một plugin dùng lại được cho mọi project, với **5 quality gate** được ghi trong `spec/gates.yaml` và kiểm bằng script tất định (`scripts/gates.py`), không để LLM tự chấm.

```
Transcript khách (T<n>)   ┐
Codebase cũ (C<n>)        ┴→ /ae-kit:intake    → spec/discovery-T<n>.md | discovery-C<n>.md  (câu hỏi, không suy diễn)
                           → /ae-kit:specify   → spec/requirements.md  (EARS, [src:] tag, non-goals)
                           → /ae-kit:lint-spec → spec/lint-*.md + gates.py compute G1
                                                                      ══ G1 Spec ══  /ae-kit:approve G1  (người)
                           → /ae-kit:design    → spec/design.md        (invariants ép xuống đúng tầng; luật → "Đề xuất ratchet")
                           → /ae-kit:plan      → spec/tasks.md (↔ R, Done:, Files:) + gates.py compute G2
                                                                      ══ G2 Plan ══  /ae-kit:approve G2  (người)
                           → /ae-kit:contract N → spec/sprint-N.contract.md  (generator ↔ reviewer, ≤ max_rounds)
                                                                      ══ G3 Contract ══  (agent–agent, tự passed)
                           → /ae-kit:next-task ×n  (1 task / session, chỉ đụng Files: của task)
                           → /ae-kit:evaluate N → tầng 1 check.cmd/e2e → tầng 2 evaluator độc lập, ≤ max_retries
                                                                      ══ G4 Evidence ══  (máy, tự passed / blocked)
                                                                      ══ G5 Merge ══  /ae-kit:approve G5  (người: diff ↔ contract, spec đã đổi?)
                           → /ae-kit:ratchet   → CLAUDE.md rule (có [nguồn]) + test + hook     ← tầng LUẬT
                           → /ae-kit:replan    → docs/product/{mission,tech,roadmap}.md          ← tầng CONTEXT
```

## Hai tầng constitution

| Tầng | File | Ai sửa | Nội dung |
|------|------|--------|----------|
| **Luật** | `CLAUDE.md` (≤ 40 dòng) | chỉ `/ae-kit:ratchet` | Điều agent phải/không được làm bất kể task. Mỗi dòng: `- <luật>. — <lý do> — [<nguồn>]` với nguồn `[harness]`, `[ratchet #n]`, `[I<n>]`/`[N<n>]`, `[C<n> O<m>]`. |
| **Context** | `docs/product/mission.md`, `tech.md`, `roadmap.md` | chỉ `/ae-kit:replan` | Sản phẩm là gì, cho ai, stack và lý do, roadmap. Không được chứa luật. Agent đọc khi cần, không nạp mặc định. |

Lý do tách: `CLAUDE.md` nạp mọi turn, nên mỗi dòng cạnh tranh sự chú ý với task; roadmap đổi mỗi sprint còn luật chỉ đổi khi có lỗi thực.

## 5 quality gate (`spec/gates.yaml`)

| Gate | Loại | Ô máy (do skill ghi qua `gates.py compute`) | Qua khi |
|------|------|----------------------------------------------|---------|
| G1 Spec | người | lint sạch ERROR · không R `proposed` · mọi Q có nhãn send/assume/defer · mọi O (brownfield) có nhãn decided/debt/ignore | `/ae-kit:approve G1` |
| G2 Plan | người | mọi R accepted có task · mọi task có ↔/Done:/Files: · task đầu là vertical slice | `/ae-kit:approve G2` |
| G3 Contract | agent–agent | reviewer `agreed` · mọi tiêu chí quan sát được · rounds ≤ 3 | tự passed trong `/ae-kit:contract` |
| G4 Evidence | máy | check.cmd pass · e2e pass/n/a · evaluator Verdict PASS · retries ≤ 3 | tự passed trong `/ae-kit:evaluate`; vượt retry → **blocked** |
| G5 Merge | người | diff nằm trong Files: của sprint · spec đổi khi hành vi đổi · người xác nhận diff ↔ contract | `/ae-kit:approve G5` → sprint mới |

`approve` từ chối khi còn ô đỏ; `--force "<lý do>"` để ép và lý do được lưu lại. Mỗi skill đọc gate trước làm điều kiện vào, nên không chạy sai thứ tự được. `blocked` là stop rule: agent dừng, người quyết.

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

Yêu cầu: Python 3 (bất kỳ tên `python3`, `python` hay `py -3`; không cần thư viện ngoài) và `bash` (Git Bash trên Windows) cho hooks/`gates.py`. Mọi lời gọi Python đi qua `scripts/py`, wrapper tự dò trình thông dịch chạy được và bỏ qua stub Microsoft Store; đặt `AE_PYTHON=<lệnh>` nếu muốn chỉ định.

**Windows:** mở `claude` ngay trong thư mục dự án (nơi sẽ có `spec/`); `gates.py` tự tìm `spec/gates.yaml` theo `CLAUDE_PROJECT_DIR` → thư mục hiện tại → các thư mục cha. Đừng mở file `.sh` bằng Notepad (đổi LF thành CRLF). Nếu Git bật `core.autocrlf=true`, thêm `.gitattributes` với `*.sh text eol=lf` và `scripts/py text eol=lf`.

## Dùng cho project mới (greenfield)

```
cd my-startup-project && git init
claude
> /ae-kit:init my-project "TypeScript, Next.js, Prisma/SQLite" "pnpm typecheck --silent" "Đặt lịch tư vấn cho consultant độc lập"
> (đặt transcript đã che PII vào intake/T1-transcript.md)
> /ae-kit:intake T1          ← điền cột Nhãn cho Q (send/assume/defer) sau khi hỏi khách
> /ae-kit:specify
> /ae-kit:lint-spec          ← sửa tay, đổi status → accepted, chạy lại tới khi ô xanh
> /ae-kit:approve G1
> /ae-kit:design
> /ae-kit:plan
> /ae-kit:approve G2
> /ae-kit:contract 1         ← G3
> /ae-kit:next-task          ← lặp
> /ae-kit:evaluate 1         ← G4
> /ae-kit:approve G5         ← mở PR trước, duyệt sau; tự sang sprint 2
> /ae-kit:ratchet            ← nếu sprint có lỗi đáng ghi
> /ae-kit:replan             ← cập nhật roadmap/tech
> /ae-kit:status             ← bất cứ lúc nào
```

## Dùng cho project có sẵn code (brownfield)

```
> /ae-kit:init my-legacy "…" "…"      ← tự nhận diện brownfield
> /ae-kit:intake C1                   ← quan sát README/manifest/schema/test, KHÔNG suy diễn
> (mở spec/discovery-C1.md: đổi ? → decided | debt | ignore cho từng O; trả lời Q)
> /ae-kit:intake T1                   ← transcript với chủ dự án nếu có
> /ae-kit:specify                     ← O debt → R phase 0; O ? → câu hỏi, không thành R
> /ae-kit:ratchet                     ← O decided loại rule → luật với [C1 O<n>]
> /ae-kit:replan                      ← O decided loại tech → docs/product/tech.md
> … tiếp như greenfield từ lint-spec
```

Nhãn `observed` ≠ `decided`: code cũ chứa cả quyết định lẫn tai nạn lịch sử; agent chỉ đề xuất, người mới biến quan sát thành luật.

## Thành phần

| Loại | Tên | Vai trò |
|------|-----|---------|
| skill | init, intake, specify, lint-spec, approve, design, plan, contract, next-task, evaluate, ratchet, replan, status | Các bước quy trình (gọi bằng `/ae-kit:<tên>`) |
| skill | spec-templates | Template artifact (không gọi trực tiếp) |
| script | `scripts/gates.py` | Logic gate tất định: `show / short / get / set / incr / compute G1\|G2\|G4\|G5 / approve / pass / next / new-sprint` |
| agent | requirement-linter | Chỉ trả về câu hỏi (ERROR/WARN); không điền chỗ trống |
| agent | planner | Vertical slice, depth-first; mỗi task ↔ R, Done:, Files: |
| agent | contract-reviewer | Phản biện "done" trước khi code; trả JSON agreed/unobservable |
| agent | evaluator | QA hoài nghi, độc lập; bảng PASS/FAIL cho mọi tiêu chí; `Verdict:` dòng đầu |
| hook | SessionStart | In 5 gate (blocked trước tiên) + handoff từ spec/progress.md |
| hook | PreToolUse(Bash) | Chặn lệnh phá hoại (+ pattern riêng trong `.ae-kit/block-patterns.txt`) |
| hook | PostToolUse(Edit\|Write) | Chạy `.ae-kit/check.cmd`; im lặng khi pass, chi tiết khi fail |

## Nguyên tắc thiết kế (để bạn sửa plugin đúng tinh thần)

1. **Artifact là file trong repo**, không phải nội dung chat. Session mới phải dựng lại được trạng thái chỉ từ `spec/` + `docs/product/`.
2. **Traceability**: mọi requirement có `[src: T§]`, `[src: A]` hoặc `[src: C O]`; mọi luật có `[nguồn]`. Không nguồn → không viết.
3. **LLM đặt câu hỏi, người trả lời.** Intake (T và C) và lint chỉ sinh câu hỏi. "Làm mịn" spec là làm với khách, không với model.
4. **Tách generator và evaluator.** Agent tự chấm sẽ tự khen. Evaluator không được xem lời giải thích của generator.
5. **Chốt "done" trước khi code** (sprint contract, G3). Ranh giới ≥/> chốt ở đây, không ở lúc debug.
6. **Gate là trạng thái trên đĩa, kiểm bằng máy.** Ô máy do skill ghi sau khi kiểm thật; người chỉ duyệt thứ máy không bắt được. Logic tất định nằm trong `gates.py`, không trong prompt.
7. **Hai tầng constitution.** Luật (`CLAUDE.md`, ratchet) tách khỏi context (`docs/product/`, replan); công cụ ép ranh giới, không dựa vào kỷ luật.
8. **Mỗi component là một giả định về điều model không tự làm được.** Khi model mới ra, xem lại: bỏ cái không còn load-bearing.
9. **Ratchet, không brainstorm.** CLAUDE.md chỉ dài ra sau lỗi thực tế. Dưới 40 dòng; `ratchet --audit` kiểm.
10. **Loop có stop rule.** next-task làm 1 task rồi dừng; G3 có max_rounds, G4 có max_retries → `blocked` thay vì chạy mãi.

## Tuỳ biến theo project

- `.ae-kit/check.cmd` — lệnh kiểm tra nhanh chạy sau mỗi edit và ở tầng 1 của G4. Mỗi project tự đặt.
- `.ae-kit/block-patterns.txt` — regex lệnh Bash cần chặn thêm, một dòng một pattern.
- `spec/gates.yaml` — đổi `max_rounds` / `max_retries` bằng `gates.py set`; đặt `AE_BASE_BRANCH` nếu nhánh gốc không phải `main`.
- `CLAUDE.md` — chỉ qua `/ae-kit:ratchet`. `docs/product/*` — chỉ qua `/ae-kit:replan`.
- Muốn evaluator dùng Playwright: thêm MCP Playwright vào project (`.mcp.json`) và cho phép tool `mcp__playwright__.*` trong `agents/evaluator.md` → `tools:`.

## Dữ liệu khách hàng
Transcript phải có sự đồng ý của khách, đã che PII, và không được sửa sau khi commit. Cân nhắc dùng API/plan có cam kết không dùng dữ liệu để huấn luyện cho các project có dữ liệu nhạy cảm.
