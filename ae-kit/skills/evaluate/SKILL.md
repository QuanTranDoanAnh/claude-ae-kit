---
name: evaluate
description: G4 — Tầng 1 tất định (check.cmd, e2e) rồi Tầng 2 evaluator độc lập chấm sprint N theo requirements, invariants và sprint contract. Nếu spec/gates.yaml bật panel (G4_evidence.panel.models), chạy nhiều evaluator khác model song song và để gates.py panel tổng hợp Verdict một cách tất định. FAIL → vòng fix có budget retry; vượt budget → G4 blocked, cần người.
disable-model-invocation: true
argument-hint: "<sprint-number>"
allowed-tools: Read Write Edit Glob Grep Bash Agent
---

Sprint `$0` (trống → `current_sprint` từ gates.py). `G=bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py"` (viết tắt `$G` bên dưới; luôn gọi qua wrapper `scripts/py` vì `python3` có thể không chạy trên Windows).

## Điều kiện vào
`$G get G3_contract.status` = `passed` và mọi task của sprint đã `[x]` trong `spec/tasks.md`. Còn task `[ ]` → DỪNG: "Còn task chưa xong — `/ae-kit:next-task`". `$G get G4_evidence.status` = `blocked` → DỪNG, in hướng dẫn mở khoá.

## Tầng 1 — tất định (KHÔNG gọi evaluator LLM nếu tầng này fail)
1. Chạy `$G compute G4`. Script chạy `.ae-kit/check.cmd` và ghi `check_cmd: pass|fail`; nếu `docs/product/tech.md` có lệnh E2E, chạy nó và ghi `e2e: pass|fail` (không có → `n/a`).
2. Bất kỳ `fail` → `$G incr G4_evidence.retries`; sửa lỗi (tối đa 5 lượt chạy lại trong cùng retry), rồi quay lại bước 1. Script tự khoá G4 khi `retries ≥ max_retries` → DỪNG và báo người.

## Tầng 2 — evaluator độc lập, vòng k
Vòng k = số vòng eval đã có của sprint + 1. Đọc cấu hình panel: `$G get G4_evidence.panel.models` (ví dụ `[opus, sonnet]`) và `$G get G4_evidence.panel.min_agree`.

Quy tắc chung cho mọi evaluator: subagent KHÔNG được thấy diff bạn vừa làm, lời giải thích của bạn, hay báo cáo của evaluator khác — chỉ spec + contract + mã nguồn hiện tại. Nó phải trả bảng `| R/I/Contract# | loại | PASS/FAIL | bằng chứng | fix hint |` cho MỌI tiêu chí trong bảng Chốt.

### 2a. Panel bật (`models` không rỗng) — đa model, tổng hợp bằng máy
1. Trong **một** message, gọi song song một subagent `ae-kit:evaluator` cho mỗi model trong `models`, với `model: <tên model>` và yêu cầu: "Chấm sprint $0, vòng k, đây là evaluator p<i> của panel; ghi `spec/eval-sprint-$0-r<k>-p<i>.md`; thêm dòng `Model: <tên model>` ngay dưới dòng Verdict." (i = 1, 2, … theo thứ tự trong `models`.)
2. Đợi tất cả xong. Chạy `$G panel $0 <k>`. Script tổng hợp TẤT ĐỊNH: đếm Verdict PASS so với `min_agree`, FAIL invariant/ngưỡng cứng bởi bất kỳ model nào → FAIL, liệt kê tiêu chí bất đồng, gộp "Đề xuất ratchet"; ghi `spec/eval-sprint-$0-r<k>.md` và ô `panel_agree`. Bạn KHÔNG tự viết file tổng hợp và KHÔNG tự chấm lại thay model nào.
3. Nếu script báo "panel chưa đủ" → evaluator nào chưa ghi file; gọi lại đúng evaluator đó (cùng p<i>), không gọi thêm model khác.

### 2b. Panel tắt (`models` rỗng) — một evaluator
Gọi subagent `ae-kit:evaluator`: chấm sprint $0, vòng k, ghi `spec/eval-sprint-$0-r<k>.md` (không hậu tố -p).

### Sau khi có báo cáo tổng hợp (cả 2a và 2b)
1. Chạy `$G compute G4` (đọc Verdict của eval tổng hợp mới nhất → `evaluator_pass_per_R`, `evidence`; panel tắt → `panel_agree: n/a`).
2. **Verdict PASS** → `$G pass G4`; ghi vào progress.md; báo người dùng: sprint đạt, số model PASS, danh sách tiêu chí bất đồng (nếu có — người sẽ xem ở G5), bước tiếp là mở PR (PR phải kèm spec delta nếu spec có thay đổi) rồi `/ae-kit:approve G5`; các "Đề xuất ratchet" trong báo cáo → `/ae-kit:ratchet`.
3. **Verdict FAIL** → `$G incr G4_evidence.retries`. Với mỗi FAIL: sửa theo Fix hint. Nếu hai lần sửa liên tiếp cùng một tiêu chí đều FAIL → đọc skill `ae-kit:principle-attack-the-premise` trước khi sửa lần ba. Nếu bạn cho rằng evaluator sai (tiêu chí hiểu nhầm spec), KHÔNG sửa để "làm hài lòng" nó — ghi tranh chấp vào progress.md "Câu hỏi cần người quyết" và hỏi người dùng. Với panel: một tiêu chí chỉ 1/N model FAIL vẫn là FAIL cho tới khi người phân xử; bạn không được dùng đa số để tự gạt một model. Người dùng là trọng tài. Sau khi sửa: chạy lại toàn bộ done-condition của sprint, quay lại Tầng 1 (vòng k+1).

## Dừng
- Script khoá G4 (`blocked`) khi vượt budget → DỪNG. Báo người dùng criterion nào kẹt, đã thử gì, và gợi ý: thiếu thông tin trong spec? invariant đặt sai tầng? task quá to? Người mở khoá bằng `$G set G4_evidence.status pending` sau khi quyết.
- Không bao giờ tự nới ngưỡng, bỏ tiêu chí, comment-out test, đổi `panel.models`/`min_agree`, hay sửa `gates.yaml` tay để pass. Tắt/bật panel là việc của người: `$G set G4_evidence.panel.models "[]"` hoặc `"[opus, sonnet, haiku]"`.
