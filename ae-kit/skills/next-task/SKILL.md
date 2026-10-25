---
name: next-task
description: Vòng lặp implement — làm DUY NHẤT task chưa hoàn thành đầu tiên trong spec/tasks.md theo playbook của loại task (feature = TDD tại seam đã chốt · bugfix = tái hiện → gốc → sửa · refactor = giữ hành vi, đơn vị nhỏ xanh liên tục), nạp principle theo trigger, chạy done-condition, cập nhật spec/progress.md, commit, rồi dừng. Chỉ chạy khi G3 của sprint đã passed và G4 chưa blocked.
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash
---

## Điều kiện vào (tự động)
```!
bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" short 2>&1
```
- `G3_contract.status` phải là `passed` cho sprint hiện tại. Không → DỪNG: "Sprint chưa có contract — chạy `/ae-kit:contract <N>`".
- `G4_evidence.status` là `blocked` → DỪNG: "G4 bị khoá vì vượt retry. Cần người quyết (sửa spec / chia nhỏ task / `/ae-kit:ratchet`), rồi `gates.py set G4_evidence.status pending`."

## Khởi động (bắt buộc, theo thứ tự — `ae-kit:principle-guard-the-context-window`)
1. Đọc `CLAUDE.md`, `spec/progress.md`, `spec/tasks.md`, contract của sprint hiện tại (`spec/sprint-<N>.contract.md`, nhất là bảng Chốt có cột **Seam**), và các R/I liên quan trong `spec/requirements.md` + `spec/design.md`. KHÔNG đọc `docs/product/*` trừ khi task cần.
2. Chọn **task `[ ]` đầu tiên** có `Depends` đã `[x]`. Nếu task trước đó trong progress.md ghi "chưa xong", tiếp tục nó. Đọc dòng `Loại:` của task (`feature` | `bugfix` | `refactor`; thiếu → `feature`).
3. **Nạp principle theo trigger**: khớp task với bảng mặc định dưới đây và với `.ae-kit/principles.md` (dòng có `[nguồn]`). Đọc TOÀN BỘ leaf khớp trước khi viết code. Không khớp → không đọc.

   | Khi | Đọc |
   |-----|-----|
   | mọi task (trước khi đánh `[x]`) | `ae-kit:principle-prove-it-works` |
   | `Loại: feature` có trạng thái / nhiều nhánh / shape lặp | `ae-kit:principle-model-the-domain` |
   | task chạm biên (HTTP, DB, file, API ngoài), ép invariant | `ae-kit:principle-boundary-discipline` |
   | `Loại: bugfix` | `ae-kit:principle-fix-root-causes` |
   | `Loại: refactor`, `Files:` > 5, task debt phase 0 | `ae-kit:principle-sequence-verifiable-units`, `ae-kit:principle-laziness-protocol` |
   | viết/sửa test | `ae-kit:principle-test-behavior-not-implementation` |
   | `Done:` fail ≥ 3 lượt cùng cách | `ae-kit:principle-attack-the-premise` |

Trạng thái hiện tại (tự động):
```!
cat spec/progress.md 2>/dev/null | head -20; echo ---; grep -m1 -A4 -E '^- \[ \] T' spec/tasks.md 2>/dev/null; echo ---; cat .ae-kit/principles.md 2>/dev/null | grep -E '^\|' | grep -vE '^\| *Khi|^\|-' 
```

## Ranh giới chung (mọi loại)
- Chỉ đụng các file trong dòng `Files:` của task (và test tương ứng). Cần file khác → ghi vào progress.md "Câu hỏi cần người quyết", hỏi trước. Đây là ô `no_file_outside_task_scope` của G5.
- Làm tối thiểu để done-condition pass. Không refactor ngoài phạm vi, không "tiện tay" làm task sau.
- Thứ gì phát hiện cần làm mà không có trong tasks.md → `spec/backlog.md` hoặc mục Backlog của tasks.md. Không làm.
- Code mâu thuẫn spec → DỪNG, ghi mâu thuẫn vào progress.md mục "Câu hỏi cần người quyết", báo người dùng. Không tự sửa spec, không tự sửa code cho khớp.
- Task thay đổi hành vi đã mô tả trong spec (theo quyết định của người) → cập nhật `spec/requirements.md`/`spec/design.md` trong cùng commit (ô `spec_diff_present_if_behavior_changed` của G5).
- Test chỉ viết tại **seam** đã ghi trong bảng Chốt của contract. Cần seam khác → hỏi người, không tự mở.
- **Cấm import/copy từ `spec/prototype/`.** Prototype là artifact spec. Task UI làm theo `spec/design.md` mục 4b (luồng, trạng thái) và khớp màn hình S<n> đã duyệt bằng mắt/screenshot; tái dùng mã prototype chỉ khi design.md có D<n> cho phép, và khi đó vẫn viết lại trên stack sản phẩm.
- Chạy đúng lệnh trong `Done:` của task. Fail → sửa và chạy lại; tối đa 5 lượt rồi dừng và báo.

## Playbook theo `Loại:` (mở file tương ứng, làm theo đúng thứ tự, bước nào bỏ ghi `bỏ: <lý do>` vào progress.md)
- `feature` → `${CLAUDE_PLUGIN_ROOT}/skills/next-task/playbooks/feature.md` (red → green tại seam, theo `references/tdd.md`)
- `bugfix` → `${CLAUDE_PLUGIN_ROOT}/skills/next-task/playbooks/bugfix.md` (tái hiện → lần gốc → sửa → regression test)
- `refactor` → `${CLAUDE_PLUGIN_ROOT}/skills/next-task/playbooks/refactor.md` (mốc xanh → đơn vị nhỏ → xanh liên tục, không đổi spec)

## Kết thúc (bắt buộc)
1. `spec/progress.md`: thêm mục nhật ký (làm gì, quyết định gì và vì sao, **principle nào đã đổi quyết định nào**, lệnh đã chạy + kết quả, điều cần lưu ý cho session sau). Cập nhật "Trạng thái hiện tại".
2. Đánh `[x]` task trong tasks.md CHỈ KHI done-condition thực sự pass (`ae-kit:principle-prove-it-works`).
3. Commit trên branch hiện tại (không phải main) với message `T<x>: <tóm tắt> (↔ R…)`. Không push. Task có dòng `Issue: #n` → thêm `(#n)` vào cuối message để tracker liên kết.
4. Trả lời người dùng ≤ 6 dòng: task gì, loại, pass/fail, bằng chứng, task tiếp theo. Rồi DỪNG — không tự chạy task tiếp.

Nếu đây là task cuối của sprint: nhắc chạy `/ae-kit:evaluate <N>`.
