---
name: evaluate
description: G4 — Tầng 1 tất định (check.cmd, e2e) rồi Tầng 2 evaluator độc lập chấm sprint N theo requirements, invariants và sprint contract; nếu FAIL, vòng fix có budget retry trong spec/gates.yaml rồi chấm lại. Vượt budget → G4 blocked, cần người.
disable-model-invocation: true
argument-hint: "<sprint-number>"
allowed-tools: Read Write Edit Glob Grep Bash Agent
---

Sprint `$0` (trống → `current_sprint` từ gates.py). `G=bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py"` (viết tắt `$G` bên dưới; luôn gọi qua wrapper `scripts/py` vì `python3` có thể không chạy trên Windows).

## Điều kiện vào
`$G get G3_contract.status` = `passed` và mọi task của sprint đã `[x]` trong `spec/tasks.md`. Còn task `[ ]` → DỪNG: "Còn task chưa xong — `/ae-kit:next-task`". `$G get G4_evidence.status` = `blocked` → DỪNG, in hướng dẫn mở khoá.

## Tầng 1 — tất định (KHÔNG gọi evaluator LLM nếu tầng này fail)
1. Chạy `$G compute G4`. Script chạy `.ae-kit/check.cmd` và ghi `check_cmd: pass|fail`; nếu `docs/product/tech.md` có lệnh E2E, chạy nó và `$G set G4_evidence.checks.e2e pass|fail` (không có → `n/a`).
2. Bất kỳ `fail` → `$G incr G4_evidence.retries`; sửa lỗi (tối đa 5 lượt chạy lại trong cùng retry), rồi quay lại bước 1. Script tự khoá G4 khi `retries ≥ max_retries` → DỪNG và báo người.

## Tầng 2 — evaluator độc lập, vòng k
1. Gọi subagent `ae-kit:evaluator`: chấm sprint $0, vòng k, ghi `spec/eval-sprint-$0-r<k>.md`. Subagent KHÔNG được thấy diff bạn vừa làm hay lời giải thích của bạn — chỉ spec + contract + mã nguồn hiện tại. Nó phải trả bảng `| R/I/Contract# | PASS/FAIL | bằng chứng |` cho MỌI tiêu chí trong bảng Chốt.
2. Chạy `$G compute G4` lần nữa (đọc Verdict của eval mới nhất → `evaluator_pass_per_R`, `evidence`).
3. **Verdict PASS** → `$G pass G4`; ghi vào progress.md; báo người dùng: sprint đạt, bước tiếp là mở PR (PR phải kèm spec delta nếu spec có thay đổi) rồi `/ae-kit:approve G5`; các "Đề xuất ratchet" trong báo cáo → `/ae-kit:ratchet`.
4. **Verdict FAIL** → `$G incr G4_evidence.retries`. Với mỗi FAIL: sửa theo Fix hint. Nếu bạn cho rằng evaluator sai (tiêu chí hiểu nhầm spec), KHÔNG sửa để "làm hài lòng" nó — ghi tranh chấp vào progress.md "Câu hỏi cần người quyết" và hỏi người dùng. Người dùng là trọng tài. Sau khi sửa: chạy lại toàn bộ done-condition của sprint, quay lại Tầng 1.

## Dừng
- Script khoá G4 (`blocked`) khi vượt budget → DỪNG. Báo người dùng criterion nào kẹt, đã thử gì, và gợi ý: thiếu thông tin trong spec? invariant đặt sai tầng? task quá to? Người mở khoá bằng `$G set G4_evidence.status pending` sau khi quyết.
- Không bao giờ tự nới ngưỡng, bỏ tiêu chí, comment-out test, hay sửa `gates.yaml` tay để pass.
