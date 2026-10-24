---
name: evaluate
description: Chạy evaluator độc lập lên sprint N theo requirements, invariants và sprint contract; nếu FAIL, chạy vòng fix có giới hạn budget rồi chấm lại. Gate 3 trước khi mở PR.
disable-model-invocation: true
argument-hint: "<sprint-number>"
allowed-tools: Read Write Edit Glob Grep Bash Agent
---

Sprint `$0`. Đọc budget vòng fix từ `spec/sprint-$0.contract.md` (mặc định 3).

## Vòng k = 1
1. Gọi subagent `ae-kit:evaluator` với yêu cầu: chấm sprint $0, vòng k, ghi `spec/eval-sprint-$0-r<k>.md`. Subagent này KHÔNG được thấy diff bạn vừa làm — chỉ đưa nó spec + contract + mã nguồn hiện tại, không đưa lời giải thích của bạn.
2. Đọc verdict.
   - **PASS** → ghi vào progress.md, báo người dùng: sprint đạt, bước tiếp là mở PR (PR phải kèm spec delta nếu spec có thay đổi) và `/ae-kit:ratchet` cho các đề xuất trong báo cáo.
   - **FAIL** → sang bước 3.
3. Với mỗi FAIL: sửa theo Fix hint. Nếu bạn cho rằng evaluator sai (tiêu chí hiểu nhầm spec), KHÔNG sửa để "làm hài lòng" nó — ghi tranh chấp vào progress.md và hỏi người dùng. Người dùng là trọng tài.
4. Chạy lại toàn bộ done-condition của sprint. Pass → k = k+1, quay lại bước 1.

## Dừng
- Vượt budget mà vẫn FAIL cùng một criterion → DỪNG. Báo người dùng criterion nào kẹt, đã thử gì, và gợi ý: thiếu thông tin trong spec? invariant đặt sai tầng? task quá to?
- Không bao giờ tự nới ngưỡng, bỏ tiêu chí, hay comment-out test để pass.
