---
name: replan
description: Cập nhật tầng product context (docs/product/mission.md, tech.md, roadmap.md) giữa các sprint — đồng bộ roadmap với task done, thêm/bỏ feature, ghi lựa chọn kỹ thuật đã loại, chép O decided từ brownfield vào tech.md. KHÔNG được sửa CLAUDE.md (việc của ratchet) hay requirements.md (việc của intake/specify).
disable-model-invocation: true
argument-hint: "[mô tả thay đổi, hoặc trống để replan định kỳ sau G5]"
allowed-tools: Read Write Edit Glob Grep Bash(git *) Bash(date *) Bash(python3 *)
---

Chạy sau khi G5 của một sprint passed, hoặc khi chủ dự án muốn đổi hướng (`$0`).

## Ranh giới cứng
- Chỉ sửa: `docs/product/mission.md`, `docs/product/tech.md`, `docs/product/roadmap.md`.
- KHÔNG sửa `CLAUDE.md`. Cần luật mới → ghi vào `spec/progress.md` mục "Đề xuất ratchet" theo định dạng `- <luật>. — <lý do> — [<nguồn>]` và bảo người chạy `/ae-kit:ratchet`.
- KHÔNG sửa `spec/requirements.md`. Feature mới → cần intake/specify mới: ghi quyết định của chủ dự án thành transcript ngắn `intake/T<n>-transcript.md` (với `[src: owner <ngày>]`) rồi `/ae-kit:intake T<n>`. Replan chỉ ghi *ý định* vào roadmap/backlog, không ghi requirement.
- KHÔNG sửa `spec/gates.yaml`.
- Mọi dòng thêm/sửa trong docs/product phải có nguồn `[src: T<n> §<m>]`, `[src: C<n> O<m>]` hoặc `[src: owner <ngày>]`.

## Các bước
1. Đọc `spec/gates.yaml` (`current_sprint`), `spec/tasks.md`, `spec/requirements.md`, 3 file docs/product, `spec/progress.md`, eval mới nhất `spec/eval-sprint-*.md`, và `spec/discovery-C*.md` nếu có.
2. **Đồng bộ roadmap với thực tế:** với mỗi dòng roadmap, so cột Requirements với trạng thái task trong tasks.md: mọi task của các R đó `[x]` và G5 của sprint passed → `done`; có task `[x]` nhưng chưa hết → `in-progress`. In bảng thay đổi trước khi ghi.
3. **Brownfield:** O nhãn `decided` loại tech/convention trong discovery-C* chưa có trong `tech.md` → đề xuất chép vào bảng Stack / "Đã cân nhắc và loại" với nguồn `[C<n> O<m>]`. O nhãn `debt` chưa có trong roadmap Phase 0 → thêm dòng.
4. **Tổng hợp tín hiệu từ sprint vừa rồi** (chỉ đề xuất, không tự quyết): câu hỏi "Hỏi người" trong progress.md chưa trả lời; Q nhãn `defer`; eval fail lặp lại; lựa chọn kỹ thuật agent đã thử và bỏ (→ "Đã cân nhắc và loại" trong tech.md); dòng `replan tech.md: …` trong "Đề xuất ratchet" (do design ghi) → áp vào tech.md và xoá khỏi progress.md.
5. Nếu có `$0`: diễn giải thành thay đổi cụ thể trên 3 file, in diff đề xuất, hỏi người xác nhận từng mục trước khi ghi.
6. Mâu thuẫn giữa roadmap và non-goal trong mission.md → KHÔNG ghi, in mâu thuẫn và dừng để người quyết.
7. Ghi file, cập nhật dòng "Cập nhật lần cuối". `git commit -m "replan: sprint <n>"` nếu người đồng ý.
8. In đúng một dòng bước tiếp theo: có feature mới → `/ae-kit:intake T<n>`; không → `/ae-kit:contract <current_sprint>`.
