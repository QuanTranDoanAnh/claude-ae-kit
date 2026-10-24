#!/usr/bin/env bash
# SessionStart hook: in trạng thái handoff để agent (và người) thấy ngay đang ở đâu.
set -uo pipefail
root="${CLAUDE_PROJECT_DIR:-$(pwd)}"

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
