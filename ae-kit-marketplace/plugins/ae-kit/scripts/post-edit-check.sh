#!/usr/bin/env bash
# PostToolUse hook cho Edit|Write: chạy lệnh kiểm tra nhanh của dự án.
# Nguyên tắc: thành công thì IM LẶNG, thất bại thì NÓI CHI TIẾT (đẩy vào context để agent tự sửa).
# Lệnh kiểm tra lấy từ file .ae-kit/check.cmd trong project (mỗi project tự định nghĩa),
# ví dụ: "pnpm typecheck --silent" hoặc "ruff check . && mypy src".
set -uo pipefail

input="$(cat)"
file="$(printf '%s' "$input" | bash "$(dirname "${BASH_SOURCE[0]}")/py" -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("file_path",""))' 2>/dev/null || true)"

root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cfg="$root/.ae-kit/check.cmd"

[ -f "$cfg" ] || exit 0                       # project chưa cấu hình → không làm gì
case "$file" in
  *.md|*.txt|*.json|*.yml|*.yaml) exit 0 ;;   # sửa tài liệu/cấu hình thì không cần typecheck
esac

check="$(head -n1 "$cfg")"
[ -z "$check" ] && exit 0

out="$(cd "$root" && bash -c "$check" 2>&1)"
rc=$?
if [ $rc -ne 0 ]; then
  echo "CHECK FAILED after editing $file" >&2
  echo "Command: $check" >&2
  echo "$out" | tail -n 60 >&2
  exit 2   # exit 2 = đưa stderr vào context của Claude như feedback
fi
exit 0
