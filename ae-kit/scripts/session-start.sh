#!/usr/bin/env bash
# SessionStart hook: in trạng thái gate + handoff để agent (và người) thấy ngay đang ở đâu.
# Nguyên tắc: gate blocked in trước tiên; không có gates.yaml thì nhắc init.
set -uo pipefail
root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$root/spec/gates.yaml" ]; then
  echo "=== ae-kit: quality gates ==="
  if printf '%s' "$(cat "$root/spec/gates.yaml")" | grep -q 'status: blocked'; then
    echo "!!! Có gate đang BLOCKED — xem dòng [✗] bên dưới, cần người quyết trước khi làm tiếp."
  fi
  python3 "$here/gates.py" show 2>&1 || echo "(gates.py lỗi — chạy /ae-kit:status để xem chi tiết)"
  echo
elif [ -d "$root/spec" ]; then
  echo "=== ae-kit: spec/gates.yaml chưa có — chạy /ae-kit:init (an toàn, không ghi đè) để tạo ==="
fi

if [ -f "$root/spec/progress.md" ]; then
  echo "=== ae-kit: spec/progress.md (trạng thái handoff) ==="
  sed -n '1,25p' "$root/spec/progress.md"
  echo
fi
if [ -f "$root/spec/tasks.md" ]; then
  next="$(grep -m1 -E '^- \[ \] T' "$root/spec/tasks.md" || true)"
  [ -n "$next" ] && echo "=== ae-kit: task tiếp theo === $next"
fi
exit 0
