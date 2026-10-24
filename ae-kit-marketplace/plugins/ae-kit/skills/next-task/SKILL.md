---
name: next-task
description: Vòng lặp implement — làm DUY NHẤT task chưa hoàn thành đầu tiên trong spec/tasks.md, chạy done-condition, cập nhật spec/progress.md, commit, rồi dừng. Chạy lặp lại cho tới hết sprint.
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash
---

## Khởi động (bắt buộc, theo thứ tự)
1. Đọc `CLAUDE.md`, `spec/progress.md`, `spec/tasks.md`, contract của sprint hiện tại (`spec/sprint-<N>.contract.md`), và các R/I liên quan trong `spec/requirements.md` + `spec/design.md`.
2. Chọn **task `[ ]` đầu tiên** có `Depends` đã `[x]`. Nếu task trước đó trong progress.md ghi "chưa xong", tiếp tục nó.
3. Nếu sprint hiện tại chưa có contract → dừng, bảo người dùng chạy `/ae-kit:contract`.

Trạng thái hiện tại (tự động):
```!
cat spec/progress.md 2>/dev/null | head -20; echo ---; grep -m1 -E '^- \[ \] T' spec/tasks.md 2>/dev/null
```

## Thực hiện — chỉ task đó
- Làm tối thiểu để done-condition pass. Không refactor ngoài phạm vi, không "tiện tay" làm task sau.
- Thứ gì phát hiện cần làm mà không có trong tasks.md → ghi vào `spec/backlog.md` hoặc mục Backlog của tasks.md. Không làm.
- Code mâu thuẫn spec → DỪNG, ghi mâu thuẫn vào progress.md mục "Câu hỏi cần người quyết", báo người dùng. Không tự sửa spec, không tự sửa code cho khớp.
- Chạy đúng lệnh trong `Done:` của task. Nếu fail, sửa và chạy lại; tối đa 5 lượt rồi dừng và báo.

## Kết thúc (bắt buộc)
1. `spec/progress.md`: thêm mục nhật ký (làm gì, quyết định gì và vì sao, lệnh đã chạy + kết quả, điều cần lưu ý cho session sau). Cập nhật "Trạng thái hiện tại".
2. Đánh `[x]` task trong tasks.md CHỈ KHI done-condition thực sự pass.
3. Commit trên branch hiện tại (không phải main) với message `T<x>: <tóm tắt> (↔ R…)`. Không push.
4. Trả lời người dùng ≤ 6 dòng: task gì, pass/fail, bằng chứng, task tiếp theo. Rồi DỪNG — không tự chạy task tiếp.

Nếu đây là task cuối của sprint: nhắc chạy `/ae-kit:evaluate <N>`.
