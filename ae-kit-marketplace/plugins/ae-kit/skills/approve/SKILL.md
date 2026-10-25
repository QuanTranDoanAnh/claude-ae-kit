---
name: approve
description: Người duyệt một quality gate (G1 spec, GP prototype — khách duyệt, G2 plan, G5 merge) — chỉ cho phép duyệt khi mọi ô máy của gate đó đã xanh trong spec/gates.yaml (scripts/gates.py kiểm, không tick tay). Dùng sau khi đã đọc artifact của gate. G3/G4 là gate máy, không duyệt tay.
disable-model-invocation: true
argument-hint: "<G1|GP|G2|G5> [\"<tên khách — chỉ GP>\"] [--force \"<lý do>\"]"
allowed-tools: Read Edit Bash(bash *) Bash(git *) Bash(gh *) Glob Grep
---

Duyệt gate `$0`. `G=bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py"` (viết tắt `$G` bên dưới; luôn gọi qua wrapper `scripts/py` vì `python3` có thể không chạy trên Windows).

## Nguyên tắc
Bạn KHÔNG tự tick ô nào trong `checks`. `gates.py approve` từ chối nếu còn ô chưa xanh; khi đó bạn liệt kê ô đỏ và lệnh sửa, rồi DỪNG. Người có thể ép bằng `--force "<lý do>"`; lý do được lưu vào gate để ratchet nhìn thấy.

## Các bước
1. Nhắc người dùng những gì họ **nên đã đọc** trước khi duyệt (một dòng mỗi gate):
   - G1: `spec/requirements.md` (R accepted, Non-goals), `spec/lint-*.md` mới nhất, cột Nhãn của Q trong `spec/discovery-*.md` (và O nếu brownfield); nhiều nguồn: `spec/claims.md` (cột Giải quyết của mọi conflict, danh sách single) và `intake/sources.yaml` (ai/ngày/authority đứng sau từng nguồn). Chạy `$G compute G1` trước nếu vừa intake nguồn mới.
   - GP: `spec/prototype/screens.md` (S ↔ R, "R không có UI"), `approval-P<v>.md` (3 dòng đầu, bảng S ↔ kết luận ↔ §), `spec/discovery-T<n>.md` của buổi demo. `who` ở GP là **tên khách/người đại diện đã duyệt** (bắt buộc), ghi thêm consultant trong progress.md. Chạy `$G compute GP` trước (drift guard: requirements đổi sau khi khách duyệt → ô đỏ, phải demo lại hoặc khách xác nhận lại bằng approval mới).
   - G2: `spec/tasks.md` — thứ tự, done-condition, Files, 3 task rủi ro planner đã đánh dấu.
   - G5: `spec/sprint-<N>.contract.md` bảng Chốt, `spec/eval-sprint-<N>-r<k>.md` mới nhất, và diff ở mức cao (không đọc từng dòng).
2. **G5 chỉ:**
   a. In nguyên văn mục "## Bất đồng" (và "## Invariant / ngưỡng cứng FAIL" nếu có) của `spec/eval-sprint-<N>-r<k>.md` mới nhất — đây là chỗ các evaluator khác model không thống nhất; người quyết đọc trước khi duyệt. Panel tắt → bỏ qua.
   b. Chạy `$G compute G5` (git diff so với `Files:` của sprint; kiểm spec có đổi khi code đổi hành vi). Nếu script báo "code đổi nhưng spec/ không đổi" → hỏi người xác nhận "không đổi hành vi?" (với sprint chỉ gồm task `Loại: refactor`, câu trả lời "có" là điều mong đợi) — có → `$G set G5_merge.checks.spec_diff_present_if_behavior_changed true`; không → DỪNG, bảo cập nhật spec trong cùng PR.
   c. In tóm tắt diff theo từng task (3–5 dòng) và hỏi "Diff khớp contract?" — có → `$G set G5_merge.checks.diff_within_contract true`.
3. Lấy `who` = `git config user.name` (trống → hỏi); với GP, `who` = tên khách trong `$1` (trống → hỏi, không dùng git user). Chạy `$G approve $0 "<who>"` (thêm `--force "<lý do>"` nếu người yêu cầu). Exit code 2 → in output của script (ô đỏ + gate trước chưa passed) và DỪNG.
4. Thành công → thêm vào `spec/progress.md` mục "Gate" dòng `- <ngày> | $0 passed | <who>` (+ `| FORCED: <lý do>` nếu có); G5 → ghi link PR/commit vào `$G set G5_merge.evidence "<ref>"`, chạy `bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/tracker.py" sync --sprint <N>` (đóng issue của task `[x]` nếu project bật tracker; `none` → script bỏ qua), rồi `$G new-sprint`.
5. `git add spec/gates.yaml spec/progress.md && git commit -m "gate: $0 passed"` nếu là git repo và người đồng ý.
6. In đúng một dòng bước tiếp theo: `$G next`.
