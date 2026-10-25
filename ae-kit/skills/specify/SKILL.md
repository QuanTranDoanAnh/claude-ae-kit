---
name: specify
description: Tổng hợp các spec/discovery-*.md (T transcript, F tài liệu, C codebase) — qua spec/claims.md khi có ≥2 nguồn — thành spec/requirements.md (EARS, có tag nguồn gốc nhiều nguồn, non-goals, glossary). Gộp vai trò SRS + PRD thành một file requirement. Chạy sau /ae-kit:intake (và /ae-kit:reconcile).
disable-model-invocation: true
allowed-tools: Read Write Glob Grep Bash(bash *)
---

Tạo hoặc cập nhật `spec/requirements.md` từ toàn bộ `spec/discovery-*.md` (và `intake/*` để đối chiếu). **Điều kiện vào:** ≥2 file discovery → `spec/claims.md` phải tồn tại và dòng `Nguồn đã đối chiếu:` phủ mọi ID; thiếu → DỪNG: "Chạy `/ae-kit:reconcile` trước". Khi có claims.md, **đi từ claim xuống R**, không đi từ từng discovery (một claim → 0..n R; nguồn của R = nguồn của claim).

## Quy tắc không thương lượng
- Mỗi requirement PHẢI có tag `[src: T<n> §<m>]` (khách nói), `[src: F<n> §<m>]` (tài liệu khách gửi — § / mã / trang của tài liệu gốc), `[src: C<n> O<m>]` (quan sát codebase) hoặc `[src: A<n>]` (giả định đã khai báo trong discovery); claim `corroborated` → ghi **mọi** nguồn cách nhau `;` (`[src: T1 §12; F1 §3.2]`). Không có nguồn → không được viết. Nếu bạn thấy cần một requirement mà không có nguồn, thêm nó vào mục "Open Questions bổ sung" ở cuối file, dưới dạng câu hỏi.
- **Claim `conflict` (spec/claims.md):** cột Giải quyết trống → KHÔNG tạo R; thêm vào "Open Questions bổ sung" ("CL<n> chưa giải quyết"). Giải quyết = "<nguồn> thắng" → R lấy nguồn thắng; phía thua nếu là một tính năng → Non-goals với ghi chú `(F1 §4.3 bị T2 §9 thay thế — CL<n>)`. Giải quyết = `send Q<k>` → R từ A mặc định với `[src: A<k>]` (proposed, chờ khách). Giải quyết = `defer` → không tạo R, ghi ở Open Questions bổ sung.
- **Claim `single` nguồn F** (chỉ tài liệu nói, chưa ai xác nhận bằng lời): vẫn tạo R với `[src: F<n> §<m>]`, giữ `proposed`; nếu claim có Q xác nhận → thêm `[src: A<k>]` cạnh nguồn F. Linter sẽ WARN khi nguồn F có `trust` ≠ high — đó là chủ ý, người quyết `accepted` hay chờ khách.
- **Tài liệu bị thay thế** (`note: superseded by F<k>` trong sources.yaml): không trích `[src: F<n>]` từ bản cũ; dùng F<k>.
- **Nguồn C (brownfield):** trước khi dùng O<m> làm nguồn, đọc nhãn của nó trong `spec/discovery-C<n>.md`:
  - nhãn `?` → KHÔNG tạo R; thêm Q vào "Open Questions bổ sung" ("O<m> chưa được người xác nhận").
  - nhãn `debt` → tạo R với ghi chú `(phase 0)` trong cột Requirement, để roadmap xếp vào Phase 0 Ổn định.
  - nhãn `decided` loại rule/tech → KHÔNG tạo R (đó là luật/tech, không phải hành vi); bỏ qua ở đây.
  - nhãn `ignore` → bỏ qua.
- Viết theo EARS (xem template). Mỗi câu phải testable: nếu không viết được một test cho nó, viết lại hoặc chuyển thành câu hỏi.
- Trạng thái khởi tạo: `proposed`. Chỉ người dùng chuyển sang `accepted`.
- **Non-goals** bắt buộc không trống: mọi tính năng được nhắc trong discovery mà không thành requirement phải xuất hiện ở Non-goals kèm lý do. Không để tính năng "lửng lơ".
- Non-functional (hiệu năng, bảo mật, i18n, audit) tách riêng nhóm N*.
- Glossary: thống nhất mỗi thuật ngữ một nghĩa; nếu khách dùng một từ theo hai nghĩa, tách thành hai thuật ngữ và ghi nguồn. Thuật ngữ lệch nghĩa giữa nguồn (bảng trong claims.md) chưa có Giải quyết → giữ cả hai nghĩa, đánh dấu `(lệch: T1 vs F1)` và thêm Q vào Open Questions bổ sung.

## Nếu requirements.md đã tồn tại
Không viết lại từ đầu. Giữ nguyên mã R hiện có và trạng thái của chúng; chỉ thêm/sửa dựa trên discovery/claim mới, ghi rõ `(updated from T<n>)` / `(updated from CL<n>)` ở dòng bị sửa. R `accepted` mà nguồn mới mâu thuẫn (claim chuyển sang conflict) → KHÔNG tự đổi R; ghi vào Open Questions bổ sung và báo người rằng G1/GP sẽ về pending sau compute. Requirement bị khách rút lại → chuyển sang Non-goals với ghi chú, không xoá.

## Kết thúc
Tóm tắt: số R theo nhóm, số dòng còn tag A* (cần khách xác nhận), số R chỉ có nguồn F (chưa xác nhận bằng lời), số R từ nguồn C, số claim conflict/defer bị bỏ qua, và nhắc bước tiếp theo: `/ae-kit:lint-spec` rồi `/ae-kit:approve G1`.
