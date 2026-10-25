# ae-kit — Agentic Engineering kit cho Claude Code

Đóng gói quy trình **intake → spec → prototype (khách duyệt) → design → tasks → contract → implement → evaluate → ratchet / replan** thành một plugin dùng lại được cho mọi project, với **6 quality gate** được ghi trong `spec/gates.yaml` và kiểm bằng script tất định (`scripts/gates.py`), không để LLM tự chấm.

## Định vị: tầng "delivery governance", không phải framework thay bạn viết code

ae-kit sinh ra cho bối cảnh **làm phần mềm cho khách hàng**: yêu cầu đến từ lời khách (transcript), tài liệu khách gửi (SRS, BRD, ghi chú, email) hoặc codebase cũ — các nguồn này hiếm khi đồng ý với nhau — phải truy vết được, có người duyệt ở đúng chỗ, và có biên bản khi bàn giao. Nó quản ba thứ: *yêu cầu đến từ đâu*, *done nghĩa là gì*, và *gate nào đã qua* — rồi để agent tự làm phần còn lại.

| Việc | ae-kit | Bộ khác làm tốt hơn |
|------|--------|---------------------|
| Transcript / tài liệu / codebase cũ → claim đối chiếu chéo → requirement có nguồn, câu hỏi theo vòng, 6 gate, sprint contract, panel evaluator, ratchet | **ae-kit** | — |
| Cách viết code bên trong một task (playbook bug/perf/refactor, design đa model, PR babysit, shipping) | playbook tối thiểu | [pstack](https://github.com/michael-denyer/pstack-claude) (Lauren Tan, port M. Denyer) |
| Skill nhỏ, composable, người tự xâu chuỗi (grill, TDD, code review 2 trục) | mượn ý tưởng (xem NOTICE.md) | [Skills for Real Engineers](https://github.com/mattpocock/skills) (Matt Pocock) |

Cài cả ba không xung đột: ae-kit lo intake → spec → gate; bên trong `/ae-kit:next-task` bạn có thể gọi `/tdd` của Pocock hay `poteto-mode` của pstack miễn là tôn trọng `Files:`, seam đã chốt và không tự tick gate. Quy trình của ae-kit **minh bạch và vượt được**: logic gate nằm trong `gates.py` đọc được, `approve --force "<lý do>"` cho người vượt gate có ghi vết. Đó là khác biệt với framework "sở hữu quy trình".

```
Transcript khách (T<n>)   ┐
Tài liệu khách (F<n>)     ┼→ /ae-kit:intake    → spec/discovery-{T,F,C}<n>.md  (bằng chứng, câu hỏi; không suy diễn)
Codebase cũ (C<n>)        ┘    + intake/sources.yaml (origin · date · authority · trust — scripts/sources.py)
                           → /ae-kit:reconcile → spec/claims.md  (≥2 nguồn: corroborated / single / CONFLICT → người quyết theo đề xuất precedence)
                           → /ae-kit:specify   → spec/requirements.md  (EARS, [src: T§; F§; C O] tag, non-goals)
                           → /ae-kit:lint-spec → spec/lint-*.md + gates.py compute G1
                                                                      ══ G1 Spec ══  /ae-kit:approve G1  (người)
                           → /ae-kit:prototype → spec/prototype/P<v>/ + screens.md (S<n> ↔ R; click-through; artifact spec, KHÔNG phải code)
                              demo cho khách → intake/T<n> → /ae-kit:intake T<n> → /ae-kit:prototype approve P<v> T<n> → approval-P<v>.md
                                                                      ══ GP Prototype ══  /ae-kit:approve GP "<khách>"  (KHÁCH duyệt; n/a nếu không có UI)
                           → /ae-kit:design    → spec/design.md        (invariants ép xuống đúng tầng; mục UX theo S<n> đã duyệt; luật → "Đề xuất ratchet")
                           → /ae-kit:plan      → spec/tasks.md (↔ R, Done:, Files:) + gates.py compute G2
                                                                      ══ G2 Plan ══  /ae-kit:approve G2  (người)
                           → /ae-kit:publish   → GitHub Issues (bản chiếu; tasks.md vẫn là nguồn sự thật)   [tuỳ chọn]
                           → /ae-kit:contract N → spec/sprint-N.contract.md  (generator ↔ reviewer, ≤ max_rounds; chốt SEAM)
                                                                      ══ G3 Contract ══  (agent–agent, tự passed)
                           → /ae-kit:next-task ×n  (1 task / session, playbook theo Loại: feature|bugfix|refactor,
                                                    nạp principle theo trigger, chỉ đụng Files: của task)
                           → /ae-kit:evaluate N → tầng 1 check.cmd/e2e → tầng 2 PANEL evaluator khác model, gates.py panel
                                                   tổng hợp tất định (≥ min_agree PASS, invariant FAIL = FAIL), ≤ max_retries
                                                                      ══ G4 Evidence ══  (máy, tự passed / blocked)
                                                                      ══ G5 Merge ══  /ae-kit:approve G5  (người: diff ↔ contract, spec đã đổi?)
                           → /ae-kit:ratchet   → CLAUDE.md rule (có [nguồn]) + test + hook     ← tầng LUẬT
                           → /ae-kit:replan    → docs/product/{mission,tech,roadmap}.md          ← tầng CONTEXT
```

## Ba tầng constitution

| Tầng | File | Ai sửa | Nội dung |
|------|------|--------|----------|
| **Luật** | `CLAUDE.md` (≤ 40 dòng) | chỉ `/ae-kit:ratchet` (mức 1) | Điều agent phải/không được làm **bất kể task**. Mỗi dòng: `- <luật>. — <lý do> — [<nguồn>]` với nguồn `[harness]`, `[ratchet #n]`, `[I<n>]`/`[N<n>]`, `[C<n> O<m>]`. |
| **Context** | `docs/product/mission.md`, `tech.md`, `roadmap.md` | chỉ `/ae-kit:replan` | Sản phẩm là gì, cho ai, stack và lý do, roadmap. Không được chứa luật. Agent đọc khi cần, không nạp mặc định. |
| **Principle có điều kiện** | `ae-kit:principle-*` (10 leaf) + trigger riêng `.ae-kit/principles.md` | plugin; project thêm trigger qua `/ae-kit:ratchet` mức 4 | Thói quen chỉ đúng trong **tình huống** (khi refactor, khi sửa bug, khi chạm biên…). `next-task` khớp trigger rồi đọc đủ leaf; không khớp thì không nạp. Tra bảng bằng `/ae-kit:principles`. |

Lý do tách: `CLAUDE.md` nạp mọi turn, nên mỗi dòng cạnh tranh sự chú ý với task; roadmap đổi mỗi sprint còn luật chỉ đổi khi có lỗi thực; luật tình huống nếu nhét vào CLAUDE.md sẽ chiếm chỗ ở mọi turn không liên quan.

## 6 quality gate (`spec/gates.yaml`)

| Gate | Loại | Ô máy (do skill ghi qua `gates.py compute`) | Qua khi |
|------|------|----------------------------------------------|---------|
| G1 Spec | người | mọi nguồn T/F/C đã đăng ký metadata (`sources_registered`) · ≥2 nguồn → `claims.md` phủ mọi nguồn, không conflict chưa giải quyết, mọi statement goal/constraint thuộc một claim (`claims_reconciled`) · lint sạch ERROR · không R `proposed` · mọi Q có nhãn send/assume/defer · mọi O (brownfield) có nhãn decided/debt/ignore | `/ae-kit:approve G1`; nguồn mới intake sau khi passed → `compute G1` đưa về pending (drift guard) |
| GP Prototype | **khách** (consultant ghi nhận) | mọi R accepted có màn hình S<n> hoặc khai "R không có UI" · mọi S có ≥ 1 R (chặn scope creep) · luồng task đầu ≥ 2 S click được · file màn hình tồn tại · `approval-P<v>.md` trỏ tới transcript buổi duyệt T<n> đã intake + "Xác nhận mô hình: yes" · Q phát sinh ở demo có nhãn | `/ae-kit:approve GP "<tên khách>"`; drift guard: requirements đổi sau khi duyệt → về pending, approval cũ bị đánh dấu stale, cần approval mới. Dự án không có UI: `status: n/a` (init hỏi) |
| G2 Plan | người | mọi R accepted có task · mọi task có ↔/Done:/Files: · task đầu là vertical slice | `/ae-kit:approve G2` |
| G3 Contract | agent–agent | reviewer `agreed` · mọi tiêu chí quan sát được · rounds ≤ 3 | tự passed trong `/ae-kit:contract` |
| G4 Evidence | máy | check.cmd pass · e2e pass/n/a · evaluator Verdict PASS · panel_agree (≥ min_agree model PASS, invariant FAIL bởi bất kỳ model → FAIL; panel tắt → n/a) · retries ≤ 3 | tự passed trong `/ae-kit:evaluate`; vượt retry → **blocked** |
| G5 Merge | người | diff nằm trong Files: của sprint · spec đổi khi hành vi đổi · người xác nhận diff ↔ contract | `/ae-kit:approve G5` → sprint mới |

`approve` từ chối khi còn ô đỏ; `--force "<lý do>"` để ép và lý do được lưu lại. Mỗi skill đọc gate trước làm điều kiện vào, nên không chạy sai thứ tự được. `blocked` là stop rule: agent dừng, người quyết.

**Panel đa model (G4):** `G4_evidence.panel.models` (mặc định `[opus, sonnet]`, `min_agree: 2`). `/ae-kit:evaluate` gọi mỗi model một evaluator độc lập (không thấy nhau, không thấy diff của generator) ghi `eval-sprint-N-r<k>-p<i>.md`; `gates.py panel` tổng hợp **bằng máy** thành `eval-sprint-N-r<k>.md`: đếm Verdict, liệt kê tiêu chí bất đồng (người xem ở G5), gộp đề xuất ratchet. Generator không được viết file tổng hợp hay dùng đa số để gạt một model. Tắt: `gates.py set G4_evidence.panel.models "[]"`.

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

## Nhiều nguồn đầu vào: transcript, tài liệu, codebase (v0.5)

Yêu cầu hiếm khi chỉ đến từ một transcript: khách gửi SRS họ tự viết, ghi chú họp, email, spec của hệ thống cũ. ae-kit coi **mọi nguồn là bằng chứng, không phải sự thật** — một câu trong SRS là bằng chứng rằng ai đó đã viết nó vào ngày đó, chưa phải điều khách muốn hôm nay.

| Nguồn | File | Discovery | Tag nguồn trong R |
|-------|------|-----------|-------------------|
| `T<n>` transcript | `intake/T<n>-transcript.md` | `discovery-T<n>.md` (S statement, Q) | `[src: T1 §12]` |
| `F<n>` tài liệu khách gửi (SRS / BRD / RFP / ghi chú / email / spec cũ) | `intake/F<n>-<slug>.*` (+ `.extracted.md` nếu docx/pdf) | `discovery-F<n>.md` (cấu trúc tài liệu, mục trống/TBD → Q, S, Q) | `[src: F1 §3.2]` |
| `C<n>` codebase | — | `discovery-C<n>.md` (O quan sát, nhãn `?`) | `[src: C1 O4]` |

Ba cơ chế giữ cho nhiều nguồn không thành "ai nói sau cùng thì đúng":
1. **Manifest `intake/sources.yaml`** (chỉ `scripts/sources.py` ghi): mỗi nguồn có `origin`, `date`, `author`, `authority` (decision-maker / stakeholder / end-user / unknown), `trust`. G1 đỏ khi nguồn đã intake mà thiếu metadata. `sources.py precedence` in thứ tự ưu tiên **đề xuất** khi mâu thuẫn: mới hơn > authority cao hơn > transcript > tài liệu > codebase > trust (ghi đè bằng `precedence: [T2, T1, F1]`).
2. **`/ae-kit:reconcile` → `spec/claims.md`** (bắt buộc khi ≥2 nguồn): mỗi claim một câu trung lập, cột Nguồn ghi `T1 S3 (§14); F1 S7 (§3.2)`, trạng thái `corroborated` / `single` / `conflict`. Conflict được hỏi theo vòng frontier với đề xuất theo precedence; **chỉ người** điền cột Giải quyết. Specify đi từ claim xuống R; phía thua của conflict thành Non-goals có ghi chú. Nguồn mới đến sau → intake, chạy lại reconcile; G1 (và GP) tự về pending.
3. **Linter**: R dựa trên claim conflict chưa giải quyết = ERROR; R chỉ có nguồn tài liệu `trust ≠ high` chưa được khách xác nhận bằng lời = WARN (ERROR nếu đã accepted).

Agent không suy diễn ở bước này: ghi chú rời rạc được trích nguyên văn và mọi chỗ mơ hồ thành Q; câu "shall" trong SRS vẫn là statement, không tự thành R. Mâu thuẫn giữa SRS và lời khách thường là chỗ khách chưa nghĩ kỹ — đó là câu hỏi đáng giá nhất để hỏi họ.

## UI/UX và prototype (GP)

Prototype trong ae-kit là **artifact spec để khách phản ứng**, không phải mã sản phẩm: nằm trong `spec/prototype/P<v>/` (HTML tĩnh, export từ Claude Design, hoặc Figma + screenshot), mỗi màn hình `S<n>` ↔ R, `next-task` bị cấm import từ đó (tái dùng layout phải là một `D<n>` tường minh trong `design.md`). Buổi demo cho khách được ghi thành transcript `T<n>` và đi qua `/ae-kit:intake` như mọi transcript khác, nên phản ứng của khách có `[src: T<n> §m]` và yêu cầu "xin thêm" tại demo đi qua Q/R chứ không đi thẳng vào prototype. Q trong discovery có thêm nhãn `prototype`: câu "nên trông/hoạt động thế nào" được trả lời bằng màn hình thay vì bằng email. `design.md` có mục 4b UX (luồng, trạng thái bắt buộc rỗng/lỗi/đang tải/không có quyền, ràng buộc i18n/a11y) và contract của sprint có UI phải có tiêu chí "khớp S<n>" ở seam e2e với screenshot.

## Dùng cho project mới (greenfield)

```
cd my-startup-project && git init
claude
> /ae-kit:init my-project "TypeScript, Next.js, Prisma/SQLite" "pnpm typecheck --silent" "Đặt lịch tư vấn cho consultant độc lập"
> (đặt transcript đã che PII vào intake/T1-transcript.md; SRS khách gửi vào intake/F1-srs-v0.3.docx)
> /ae-kit:intake T1          ← đăng ký nguồn (origin/date/authority/trust); điền cột Nhãn cho Q (send/assume/defer) sau khi hỏi khách
> /ae-kit:intake F1          ← mục trống/TBD và câu "shall" không kiểm chứng được → Q; không tự thành R
> /ae-kit:reconcile          ← ≥2 nguồn: claims.md; conflict T1 ⟂ F1 hỏi theo vòng, người quyết
> /ae-kit:specify
> /ae-kit:lint-spec          ← sửa tay, đổi status → accepted, chạy lại tới khi ô xanh
> /ae-kit:approve G1
> /ae-kit:prototype          ← dựng P1 + screens.md + demo-P1.md (dự án có UI)
> (demo cho khách, ghi transcript → intake/T2-transcript.md)
> /ae-kit:intake T2
> /ae-kit:prototype approve P1 T2
> /ae-kit:approve GP "Tên khách"
> /ae-kit:design
> /ae-kit:plan
> /ae-kit:approve G2
> /ae-kit:publish            ← tuỳ chọn: .ae-kit/tracker = github → mỗi task một issue
> /ae-kit:contract 1         ← G3, chốt cả SEAM test
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
> /ae-kit:intake T1                   ← transcript với chủ dự án nếu có (hoặc F1: tài liệu thiết kế của hệ thống cũ)
> /ae-kit:reconcile                   ← C1 ⟂ T1: code làm X, chủ dự án nói Y → conflict, người quyết
> /ae-kit:specify                     ← O debt → R phase 0; O ? → câu hỏi, không thành R
> /ae-kit:ratchet                     ← O decided loại rule → luật với [C1 O<n>]
> /ae-kit:replan                      ← O decided loại tech → docs/product/tech.md
> … tiếp như greenfield từ lint-spec
```

Nhãn `observed` ≠ `decided`: code cũ chứa cả quyết định lẫn tai nạn lịch sử; agent chỉ đề xuất, người mới biến quan sát thành luật.

## Thành phần

| Loại | Tên | Vai trò |
|------|-----|---------|
| skill | init, intake, reconcile, specify, lint-spec, approve, prototype, design, plan, publish, contract, next-task, evaluate, ratchet, replan, status, principles | Các bước quy trình (gọi bằng `/ae-kit:<tên>`) |
| skill | principle-laziness-protocol, -model-the-domain, -boundary-discipline, -prove-it-works, -fix-root-causes, -attack-the-premise, -test-behavior-not-implementation, -sequence-verifiable-units, -guard-the-context-window, -encode-lessons-in-structure | Tầng 3 constitution; agent nạp theo trigger (bảng trong `/ae-kit:principles`) |
| skill | spec-templates | Template artifact + `references/grilling.md` (vòng hỏi) (không gọi trực tiếp) |
| playbook | `skills/next-task/playbooks/{feature,bugfix,refactor}.md`, `references/tdd.md` | Cách làm một task theo `Loại:`; test tại seam đã chốt |
| script | `scripts/gates.py` | Logic gate tất định: `show / short / get / set / incr / compute G1\|GP\|G2\|G4\|G5 / panel / approve / pass / next / new-sprint` |
| script | `scripts/sources.py` | Manifest nguồn `intake/sources.yaml`: `init / add / set / list / check / precedence` (metadata nguồn T/F/C; thứ tự ưu tiên đề xuất khi mâu thuẫn) |
| script | `scripts/tracker.py` | Chiếu tasks.md lên GitHub Issues qua `gh`: `status / plan / push / sync / link` (idempotent qua `Issue: #n`) |
| agent | requirement-linter | Chỉ trả về câu hỏi (ERROR/WARN); không điền chỗ trống; kiểm claim conflict và nguồn tài liệu chưa xác nhận |
| agent | planner | Vertical slice, depth-first; mỗi task ↔ R, Done:, Files: |
| agent | contract-reviewer | Phản biện "done" trước khi code; trả JSON agreed/unobservable |
| agent | evaluator | QA hoài nghi, độc lập; bảng PASS/FAIL cho mọi tiêu chí; `Verdict:` dòng đầu; chạy nhiều bản khác model khi panel bật |
| hook | SessionStart | In 6 gate (blocked trước tiên) + handoff từ spec/progress.md |
| hook | PreToolUse(Bash) | Chặn lệnh phá hoại (+ pattern riêng trong `.ae-kit/block-patterns.txt`) |
| hook | PostToolUse(Edit\|Write) | Chạy `.ae-kit/check.cmd`; im lặng khi pass, chi tiết khi fail |

## Nguyên tắc thiết kế (để bạn sửa plugin đúng tinh thần)

1. **Artifact là file trong repo**, không phải nội dung chat. Session mới phải dựng lại được trạng thái chỉ từ `spec/` + `docs/product/`.
2. **Traceability**: mọi requirement có `[src: T§]`, `[src: F§]`, `[src: C O]` hoặc `[src: A]` (nhiều nguồn cách nhau `;`); mọi luật có `[nguồn]`; mọi nguồn có metadata (ai, ngày, thẩm quyền). Không nguồn → không viết.
3. **LLM đặt câu hỏi, người trả lời.** Intake (T, F, C), reconcile và lint chỉ sinh câu hỏi, hỏi theo vòng frontier, mỗi câu kèm giả định mặc định A<n> (`yes` = chấp nhận); sự thật tra cứu được thì agent tự tra, chỉ quyết định mới hỏi người. "Làm mịn" spec là làm với khách, không với model.
3b. **Nguồn là bằng chứng, không phải sự thật; mâu thuẫn giữa nguồn là câu hỏi, không phải thứ tự ưu tiên.** Reconcile chỉ *đề xuất* theo precedence (mới hơn, thẩm quyền cao hơn); người điền Giải quyết. Ngày tháng không phải thẩm quyền.
4. **Tách generator và evaluator.** Agent tự chấm sẽ tự khen. Evaluator không được xem lời giải thích của generator; nhiều evaluator khác model không được xem nhau, và máy (không phải generator) tổng hợp verdict.
5. **Khách phản ứng với thứ thật, không với chữ** (GP). Prototype là spec, không phải code; mọi màn hình trả lời một R; phản ứng của khách là transcript.
5b. **Chốt "done" trước khi code** (sprint contract, G3). Ranh giới ≥/> và **seam** test chốt ở đây, không ở lúc debug.
6. **Gate là trạng thái trên đĩa, kiểm bằng máy.** Ô máy do skill ghi sau khi kiểm thật; người chỉ duyệt thứ máy không bắt được. Logic tất định nằm trong `gates.py`, không trong prompt.
7. **Ba tầng constitution.** Luật (`CLAUDE.md`, ratchet) tách khỏi context (`docs/product/`, replan) và khỏi principle có điều kiện (nạp theo trigger); công cụ ép ranh giới, không dựa vào kỷ luật.
8. **Mỗi component là một giả định về điều model không tự làm được.** Khi model mới ra, xem lại: bỏ cái không còn load-bearing.
9. **Ratchet, không brainstorm.** CLAUDE.md chỉ dài ra sau lỗi thực tế. Dưới 40 dòng; `ratchet --audit` kiểm.
10. **Loop có stop rule.** next-task làm 1 task rồi dừng; G3 có max_rounds, G4 có max_retries → `blocked` thay vì chạy mãi.

## Tuỳ biến theo project

- `.ae-kit/check.cmd` — lệnh kiểm tra nhanh chạy sau mỗi edit và ở tầng 1 của G4. Mỗi project tự đặt.
- `.ae-kit/block-patterns.txt` — regex lệnh Bash cần chặn thêm, một dòng một pattern.
- `spec/gates.yaml` — đổi `max_rounds` / `max_retries` / `panel.models` / `panel.min_agree` bằng `gates.py set`; đặt `AE_BASE_BRANCH` nếu nhánh gốc không phải `main`.
- `.ae-kit/principles.md` — trigger principle riêng của project (chỉ qua `/ae-kit:ratchet` mức 4, mỗi dòng có `[nguồn]`).
- `intake/sources.yaml` — chỉ qua `scripts/sources.py`; `precedence: [T2, T1, F1]` để ghi đè thứ tự ưu tiên đề xuất.
- `.ae-kit/tracker` — `none` (mặc định) hoặc `github` (+ `labels: …`, `repo: owner/name`); cần `gh auth login`.
- `CLAUDE.md` — chỉ qua `/ae-kit:ratchet`. `docs/product/*` — chỉ qua `/ae-kit:replan`.
- Muốn evaluator dùng Playwright: thêm MCP Playwright vào project (`.mcp.json`) và cho phép tool `mcp__playwright__.*` trong `agents/evaluator.md` → `tools:`.

## Dữ liệu khách hàng
Transcript và tài liệu khách gửi phải có sự đồng ý của khách, đã che PII, và không được sửa sau khi commit (phiên bản mới = ID mới). Cân nhắc dùng API/plan có cam kết không dùng dữ liệu để huấn luyện cho các project có dữ liệu nhạy cảm.
