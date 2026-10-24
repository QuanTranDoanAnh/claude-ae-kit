---
name: status
description: Hiện trạng thái dự án theo quy trình ae-kit — đang ở bước nào, số R theo trạng thái, task đã/chưa xong, gate nào đang chờ người dùng.
disable-model-invocation: true
allowed-tools: Read Glob Grep Bash(grep *) Bash(ls *)
---

```!
echo "== intake =="; ls intake 2>/dev/null
echo "== spec =="; ls spec 2>/dev/null
echo "== requirements by status =="; grep -oE '\| (proposed|accepted|implemented|verified) \|' spec/requirements.md 2>/dev/null | sort | uniq -c
echo "== tasks =="; grep -cE '^- \[x\] T' spec/tasks.md 2>/dev/null | sed 's/^/done: /'; grep -cE '^- \[ \] T' spec/tasks.md 2>/dev/null | sed 's/^/todo: /'
echo "== latest eval =="; ls -t spec/eval-sprint-* 2>/dev/null | head -1 | xargs -r head -3
echo "== progress =="; head -8 spec/progress.md 2>/dev/null
```

Từ dữ liệu trên, trả lời ngắn gọn: dự án đang ở bước nào trong chuỗi `intake → specify → lint-spec → [gate 1] → design → plan → [gate 2] → contract → next-task → evaluate → [gate 3] → ratchet`, gate nào đang chờ người dùng, và lệnh `/ae-kit:...` nên chạy tiếp theo.
