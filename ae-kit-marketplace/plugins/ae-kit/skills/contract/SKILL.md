---
name: contract
description: Thương lượng sprint contract cho sprint N — generator đề xuất "done là gì / verify bằng gì", contract-reviewer phản biện, lặp tối đa max_rounds, người dùng chốt. Đây là G3 (gate agent–agent). Chạy TRƯỚC khi viết dòng code nào của sprint.
disable-model-invocation: true
argument-hint: "<sprint-number>"
allowed-tools: Read Write Edit Glob Grep Agent Bash(bash *)
---

Sprint `$0` (nếu trống: lấy `current_sprint` từ gates.py, hoặc sprint đầu tiên còn task `[ ]` trong `spec/tasks.md`).
`G=bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py"` (viết tắt `$G` bên dưới; luôn gọi qua wrapper `scripts/py` vì `python3` có thể không chạy trên Windows).

## Điều kiện vào
`$G get G2_plan.status` = `passed`. Không → DỪNG: "G2 chưa passed — `/ae-kit:approve G2`".
Nếu `$G get G3_contract.sprint` ≠ `$0` → chạy `$G new-sprint` cho tới khi khớp (hoặc báo người nếu nhảy sprint).

## Bước 1 — Generator đề xuất (chính bạn)
Tạo `spec/sprint-$0.contract.md` từ template sprint-contract. Điền mục "Generator đề xuất":
- Sẽ build gì (theo task của sprint).
- **Seam** (bảng Seam): nơi test sẽ quan sát hành vi — ưu tiên seam cao nhất còn chạy được trong CI, càng ít càng tốt (lý tưởng là 1–2); nêu prior art (test tương tự đã có trong repo, tìm bằng Grep). Đọc `ae-kit:principle-test-behavior-not-implementation` trước khi đề xuất. Seam là quyết định của người ở bước 3; `next-task` không được mở seam mới.
- Verify bằng gì: lệnh cụ thể + kỳ vọng cụ thể, mỗi tiêu chí gắn một seam.
- Giả định đang dựa vào: liệt kê thẳng thắn, kể cả giả định "hiển nhiên".

## Bước 2 — Evaluator phản biện (lặp có giới hạn)
Gọi subagent `ae-kit:contract-reviewer` lên file contract. Nó điền mục "Evaluator phản biện" và kết thúc bằng một dòng JSON `{"agreed": true|false, "unobservable": [...]}`.
- Chạy `$G incr G3_contract.rounds`.
- `agreed: false` → sửa đề xuất theo phản biện (chỉ phần generator), gọi reviewer lại. Script tự chuyển G3 sang `blocked` khi rounds ≥ max_rounds; khi đó DỪNG, in các tiêu chí còn tranh cãi để người quyết, rồi người chạy `$G set G3_contract.status pending` và `/ae-kit:contract $0` lại.
- `agreed: true` và `unobservable` rỗng → `$G set G3_contract.checks.reviewer_agreed true` và `$G set G3_contract.checks.criteria_observable true`.

## Bước 3 — Người dùng là trọng tài
Trình bày các mục "Cần chốt" dưới dạng câu hỏi lựa chọn (A/B kèm hệ quả), theo vòng của `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/references/grilling.md` §3 (`yes` = chấp nhận đề xuất). Bảng Seam cũng là một mục cần chốt: "Test ở S1 (api) và S2 (unit slots)? yes = đồng ý". Chờ người dùng quyết. Ghi quyết định vào bảng "Chốt", đặt ngưỡng cứng cho mọi tiêu chí liên quan invariant. Budget vòng fix của G4 = `$G get G4_evidence.max_retries` (mặc định 3); ghi vào contract.

## Kết thúc
`$G set G3_contract.evidence spec/sprint-$0.contract.md` rồi `$G pass G3`. Không bắt đầu implement trong lệnh này. In: "Contract sprint $0 đã chốt (G3 passed). Chạy `/ae-kit:next-task` để bắt đầu."
