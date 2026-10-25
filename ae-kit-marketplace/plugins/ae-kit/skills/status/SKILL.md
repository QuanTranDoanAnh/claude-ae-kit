---
name: status
description: Checklist 6 quality gate (G1 spec → G2 plan → G3 contract → G4 evidence → G5 merge) từ spec/gates.yaml, kèm tình trạng tầng luật (CLAUDE.md /40 dòng, dòng thiếu nguồn), brownfield O chưa phân loại, nguồn đã intake (T/F/C) và trạng thái reconcile (claims conflict/single), tiến độ roadmap, câu hỏi đang mở, và đúng một lệnh nên chạy tiếp. Chỉ đọc, không ghi.
disable-model-invocation: true
allowed-tools: Read Glob Grep Bash(grep *) Bash(ls *) Bash(bash *)
---

```!
bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" show 2>&1
echo
echo "== sources =="; bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/sources.py" list 2>/dev/null | head -12
echo "== requirements by status =="; grep -oE '\| (proposed|accepted|implemented|verified) \|' spec/requirements.md 2>/dev/null | sort | uniq -c
echo "== tasks =="; grep -cE '^- \[x\] T' spec/tasks.md 2>/dev/null | sed 's/^/done: /'; grep -cE '^- \[ \] T' spec/tasks.md 2>/dev/null | sed 's/^/todo: /'
echo "== latest eval =="; ls -t spec/eval-sprint-* 2>/dev/null | head -1 | xargs -r head -3
```

Trình bày lại cho người dùng **đúng** khối output của `gates.py show` (không viết lại bằng văn xuôi, không thêm gate), rồi tối đa 3 dòng bổ sung nếu bạn thấy ô máy có vẻ cũ so với artifact (ví dụ `every_R_has_task: true` nhưng số R accepted vừa tăng) → ghi "ô có thể cũ — chạy lại `/ae-kit:plan`". KHÔNG tự sửa `gates.yaml`.

Ký hiệu: `[✓]` passed · `[✗]` blocked · `[~]` sẵn sàng (gate trước đã passed) · `[ ]` chưa tới lượt · `[–]` n/a (GP khi dự án không có UI).
