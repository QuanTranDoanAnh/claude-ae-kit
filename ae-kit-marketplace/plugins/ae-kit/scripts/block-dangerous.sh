#!/usr/bin/env bash
# PreToolUse hook cho Bash: chặn lệnh phá hoại.
# Đọc JSON từ stdin, lấy .tool_input.command, exit 2 + thông báo trên stderr để chặn.
set -euo pipefail

input="$(cat)"
cmd="$(printf '%s' "$input" | bash "$(dirname "${BASH_SOURCE[0]}")/py" -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("command",""))' 2>/dev/null || true)"

[ -z "$cmd" ] && exit 0

# Mỗi pattern là một bài học đã trả giá. Thêm pattern qua /ae:ratchet, kèm lý do.
patterns=(
  'rm\s+-[a-zA-Z]*r[a-zA-Z]*f'          # rm -rf / rm -fr
  'git\s+push\s+.*--force'               # force push
  'git\s+push\s+.*-f(\s|$)'
  'git\s+reset\s+--hard'
  'git\s+checkout\s+--\s+\.'             # vứt toàn bộ working tree
  'git\s+clean\s+-[a-zA-Z]*f'
  'DROP\s+(TABLE|DATABASE|SCHEMA)'
  'TRUNCATE\s+TABLE'
  'prisma\s+migrate\s+reset'
  'chmod\s+-R\s+777'
  '>\s*/dev/sd'
  'mkfs\.'
)

# Pattern riêng của project, được /ae-kit:ratchet thêm vào (một regex mỗi dòng, '#' là comment)
root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
if [ -f "$root/.ae-kit/block-patterns.txt" ]; then
  while IFS= read -r line; do
    line="${line%%#*}"; line="$(printf '%s' "$line" | sed 's/[[:space:]]*$//')"
    [ -n "$line" ] && patterns+=("$line")
  done < "$root/.ae-kit/block-patterns.txt"
fi

for p in "${patterns[@]}"; do
  if printf '%s' "$cmd" | grep -Eiq "$p"; then
    echo "BLOCKED by ae-kit constitution: lệnh khớp pattern nguy hiểm '$p'." >&2
    echo "Nếu thật sự cần, hãy yêu cầu người dùng chạy thủ công và giải thích lý do." >&2
    exit 2
  fi
done

exit 0
