---
name: publish
description: Chiếu spec/tasks.md lên issue tracker của project (hiện hỗ trợ GitHub Issues qua gh) — mỗi task một issue có ↔ R, Done, Files, Blocked by; ghi `Issue: #n` ngược vào tasks.md. spec/tasks.md vẫn là nguồn sự thật; issue là bản chiếu để khách/team theo dõi. Chạy sau khi G2 passed; chạy lại sau khi plan đổi.
disable-model-invocation: true
argument-hint: "[sprint-number]"
allowed-tools: Read Bash(bash *) Bash(gh *) Bash(git *) Glob Grep
---

Sprint `$0` (trống → mọi sprint còn task). `T=bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/tracker.py"` (viết tắt `$T`).

## Điều kiện vào
- `bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" get G2_plan.status` = `passed`. Không → DỪNG: "Plan chưa được duyệt — `/ae-kit:approve G2` trước; không đẩy task chưa duyệt ra ngoài."
- `$T status`. Nếu `tracker: none` → DỪNG và giải thích: tạo `.ae-kit/tracker` với dòng đầu `github` (tuỳ chọn `labels: ae-kit, client-x` và `repo: owner/name`), cần `gh auth login`. Không tự bật.

## Các bước
1. `$T plan` (hoặc `$T plan --sprint $0`) — in task sẽ tạo / cập nhật / sẽ đóng và một body mẫu. Trình bày cho người dùng; hỏi "Đẩy lên GitHub? (tạo <n> issue, cập nhật <m>)". Chờ đồng ý.
2. `$T push [--sprint $0]`. Script tạo issue theo thứ tự task (blocker trước), ghi `Issue: #n` vào `spec/tasks.md`, rồi cập nhật body để `Blocked by` có số issue thật. Label: `ae-kit` (+ labels cấu hình) và `sprint-N`.
3. `git add spec/tasks.md && git commit -m "publish: sprint $0 → issues"` nếu người đồng ý.
4. In bảng `T<x> → #n (url)`.

## Quy tắc
- Không sửa nội dung task trong issue bằng tay trên GitHub; đổi `spec/tasks.md` rồi chạy lại `/ae-kit:publish` — script ghi đè title/body.
- Đóng issue là việc của `/ae-kit:approve G5` (gọi `$T sync --sprint N` sau khi gate passed). Không đóng tay trong skill này.
- Issue chỉ chứa thông tin đã có trong `spec/` (không bịa thêm mô tả); transcript khách không bao giờ được chép vào issue (PII, đồng ý của khách).
- Tracker khác (Linear, Jira, GitLab) chưa hỗ trợ: giữ `none`, hoặc viết adapter theo `scripts/tracker.py` (hàm `gh()` là điểm thay).
