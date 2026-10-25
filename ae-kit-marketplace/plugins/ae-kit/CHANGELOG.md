# Changelog

## 0.5.0 — 2026-10-25
- **Nhiều nguồn đầu vào cho intake → requirements.** Nguồn mới **`F<n>`** = file tài liệu khách gửi (SRS / BRD / RFP / ghi chú họp / email / spec hệ thống cũ) bên cạnh `T<n>` transcript và `C<n>` codebase. `/ae-kit:intake F<n>`: bản trích `.extracted.md` (pandoc/pdftotext, không sửa gốc), template `discovery-document.md` (cấu trúc tài liệu — mục trống/TBD → Q; câu "shall" trong SRS vẫn là statement; ghi chú rời rạc trích nguyên văn, mơ hồ → Q; phiên bản mới = F mới, `superseded`). Tag nguồn `[src: F<n> §<m>]`; nhiều nguồn cách nhau `;`.
- **Manifest nguồn `intake/sources.yaml`** + `scripts/sources.py` (`init / add / set / list / check / precedence`): mỗi nguồn có `type`, `origin`, `date`, `author`, `authority`, `trust`; intake hỏi và đăng ký ở Bước 0; thứ tự ưu tiên **đề xuất** khi mâu thuẫn (mới hơn > authority > transcript > tài liệu > codebase > trust; ghi đè `precedence: [...]`).
- **Skill mới `/ae-kit:reconcile` → `spec/claims.md`** (bắt buộc khi ≥2 nguồn, trước specify, chạy lại khi có nguồn mới): claim trung lập với nguồn `T1 S3 (§14); F1 S7 (§3.2)`, trạng thái `corroborated | single | conflict`; conflict/single hỏi theo vòng frontier với đề xuất theo precedence, chỉ người ghi cột Giải quyết; thuật ngữ lệch nghĩa; khoảng trống chung → Q vào discovery mới nhất.
- **G1 thêm hai ô máy** (`gates.py compute G1`): `sources_registered` (mọi nguồn đã intake có metadata) và `claims_reconciled` (≥2 nguồn → claims.md phủ mọi nguồn, không conflict trống Giải quyết, mọi S goal/constraint/out-of-scope thuộc một claim; 1 nguồn → true). Nguồn mới sau khi G1 passed → về pending (drift guard sẵn có). `show` in dòng Nguồn + claims; `next` biết reconcile.
- Specify đi từ claim xuống R (phía thua conflict → Non-goals có ghi chú; `send` → `[src: A]`; `defer` → Open Questions bổ sung); linter thêm kiểm 9 (R trên claim conflict chưa giải quyết = ERROR) và 10 (R chỉ có nguồn tài liệu `trust ≠ high` chưa xác nhận bằng lời = WARN); approve G1 đọc claims.md + sources.yaml; init tạo sources.yaml và intake/README ba loại nguồn; status in `sources.py list`; grilling.md thêm bối cảnh intake F và reconcile. `gates.py`: `load_yaml`/`save_yaml` dùng chung.
- Tương thích: project v0.4 chỉ cần `sources.py init` rồi điền metadata; gates.yaml cũ được thêm hai ô khi `compute G1`.

## 0.4.0 — 2026-10-24
- **Gate GP (Prototype) — khách duyệt UI/UX trước khi plan.** `gates.py`: gate `GP_prototype` giữa G1 và G2 (ORDER/HUMAN), `compute GP` với 6 ô máy (R có màn hình hoặc khai không-UI · S có ≥1 R · luồng task đầu ≥2 S · file màn hình tồn tại · approval trỏ transcript đã intake + xác nhận mô hình · Q demo có nhãn), `approve GP "<khách>"` ghi `req_fingerprint`; drift guard: requirements đổi sau khi duyệt → pending và approval cũ bị đánh dấu `stale_approval`, phải có approval mới. `status: n/a` cho dự án không có UI (init hỏi); gates.yaml v0.3 không có GP vẫn chạy (coi n/a). `show` hiển thị `[–]`.
- Skill mới **`/ae-kit:prototype`** (`new | demo | approve P<v> T<n>`): dựng `spec/prototype/P<v>/` + `screens.md` + `demo-P<v>.md`; sau demo ghi `approval-P<v>.md`. Ba nguyên tắc: prototype là artifact spec; mọi màn hình ↔ R; khách phản ứng với thứ thật.
- Template `screens.md`, `approval.md`; `design.md` thêm mục 4b UX (luồng, trạng thái bắt buộc, ràng buộc, "Tái dùng từ prototype: KHÔNG mặc định").
- Nhãn Q mới `prototype` (intake, grilling, G1 chấp nhận); intake nhận diện transcript buổi demo; design/plan có điều kiện vào GP; next-task cấm import `spec/prototype/`; contract-reviewer đòi tiêu chí "khớp S<n>" ở seam e2e cho sprint có UI; evaluator so screenshot với S<n>; approve GP bắt buộc tên khách.

## 0.3.0 — 2026-10-24
Kết quả so sánh ae-kit với pstack (Lauren Tan / Michael Denyer) và Skills for Real Engineers (Matt Pocock); mượn ý tưởng, không mượn mã. Xem NOTICE.md.

- **Panel evaluator đa model (G4).** `G4_evidence.panel.models` / `min_agree` trong gates.yaml; `/ae-kit:evaluate` gọi mỗi model một evaluator độc lập (`eval-sprint-N-r<k>-p<i>.md`); lệnh mới `gates.py panel` tổng hợp tất định (Verdict, tiêu chí × model, bất đồng, hard FAIL, gộp đề xuất ratchet) và ghi ô mới `checks.panel_agree`. `compute G4` phát hiện vòng panel chưa tổng hợp. `approve G5` in mục Bất đồng trước khi duyệt. Template eval-report có cột Loại chuẩn (`invariant | requirement | contract [cứng]`) và dòng `Model:`.
- **Vòng hỏi theo frontier (grilling).** `spec-templates/references/grilling.md`; cột `Sau Q` trong discovery; intake (T/C) và lint-spec hỏi theo vòng, mỗi câu kèm `➡️ Đề xuất: A<n>` (`yes` = assume); sự thật tra cứu được thì agent tự tra. Linter có thêm cột Đề xuất / Hỏi ai / Sau / Quyết định.
- **Tầng 3 constitution: principle có điều kiện.** 10 skill `principle-*`, index `/ae-kit:principles`, trigger riêng `.ae-kit/principles.md` (init tạo), `/ae-kit:ratchet` mức 4 (trigger thay vì dòng CLAUDE.md cho luật tình huống), audit kiểm principles.md.
- **Playbook theo `Loại:` task + seam.** `tasks.md` có `Loại: feature | bugfix | refactor`; `next-task` rẽ nhánh theo `playbooks/{feature,bugfix,refactor}.md`, `references/tdd.md`; sprint contract có bảng **Seam** và cột Seam trong bảng Chốt; contract-reviewer coi tiêu chí không seam là không quan sát được; `approve G5` biết sprint refactor không đổi spec.
- **Chiếu task ra GitHub Issues.** `scripts/tracker.py` (`status / plan / push / sync / link`, idempotent qua `Issue: #n` trong tasks.md, label `ae-kit` + `sprint-N`, Blocked by có số issue thật); skill `/ae-kit:publish` (chỉ sau G2); `approve G5` gọi `sync` để đóng issue; `.ae-kit/tracker` (init ghi `none`).
- README: mục Định vị (delivery governance, kết hợp với pstack/Pocock), ba tầng constitution, thành phần mới. NOTICE.md ghi nguồn ý tưởng.

## 0.2.1
- Sửa lỗi nhỏ sau fixture test (Q-label regex, e2e fallback, base branch, new-sprint guard).

## 0.2.0
- Hai tầng constitution, brownfield intake C<n> (observed/decided), 5 gate G1–G5 trong `spec/gates.yaml`, `scripts/gates.py`, skill approve/replan.
