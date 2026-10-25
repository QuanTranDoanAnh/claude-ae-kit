---
name: intake
description: Trích xuất MỘT nguồn thành spec/discovery-<ID>.md — T<n> là transcript trao đổi với khách (intake/T<n>-transcript.md), F<n> là file tài liệu khách gửi (SRS, BRD, RFP, ghi chú, email — intake/F<n>-<slug>.*), C<n> là codebase hiện có (brownfield). Chỉ TRÍCH XUẤT và ĐẶT CÂU HỎI, không suy diễn requirement. Đăng ký nguồn vào intake/sources.yaml. Có ≥2 nguồn → /ae-kit:reconcile trước specify. Bước đầu tiên của quy trình.
disable-model-invocation: true
argument-hint: "<T<n> | F<n> | C<n>>"
allowed-tools: Read Write Edit Glob Grep Bash(ls *) Bash(git *) Bash(wc *) Bash(bash *) Bash(pandoc *) Bash(pdftotext *)
---

Nguồn `$0`. Nếu trống: chạy `bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/sources.py" list`, liệt kê file trong `intake/` chưa có discovery và hỏi; nhắc rằng codebase cũ dùng `C1`.
Template ở `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/templates/`. Cách hỏi theo vòng: `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/references/grilling.md` (đọc trước khi trình bày Q). `$S` = `bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/sources.py"`.

## Nguyên tắc cốt lõi (áp dụng cho T, F và C)
Bạn đang làm việc với **lời của khách**, **văn bản ai đó đã viết**, hoặc **dấu vết của người đi trước**. Nhiệm vụ của bạn là **làm lộ ra những gì người cần quyết định**, không phải thay họ quyết định. Mọi chỗ trống là một CÂU HỎI, không phải chỗ để điền giả định hợp lý. Tuyệt đối KHÔNG viết requirement ("SHALL"), KHÔNG đề xuất giải pháp, KHÔNG chọn stack, KHÔNG suy diễn lý do ("có lẽ họ chọn X vì…" là cấm).

Mỗi nguồn là **bằng chứng**, không phải sự thật: một câu trong SRS là bằng chứng rằng tác giả đã viết câu đó vào ngày đó — chưa phải điều khách muốn hôm nay. Mỗi discovery chỉ nói về nguồn của nó; mâu thuẫn **giữa** các nguồn được xử lý ở `/ae-kit:reconcile` (spec/claims.md), không ở đây.

Phân biệt **sự thật** và **quyết định** (grilling.md §1): sự thật tra cứu được (file, lệnh, schema, transcript, tài liệu) thì tự tra và ghi thành statement/quan sát có bằng chứng; chỉ quyết định mới thành Q. Mỗi Q ghi cột **Sau Q** nếu nó chỉ có nghĩa sau khi một Q khác được trả lời.

## Bước 0 (mọi nhánh) — đăng ký nguồn
Chạy `$S list`. Nếu `$0` chưa có mục hoặc còn `?`: hỏi người đúng các trường còn thiếu — `origin` (customer / vendor / internal / third-party), `date` (ngày buổi nói chuyện / phiên bản tài liệu; C: ngày commit — script tự điền), `author` (ai nói/viết), `authority` (decision-maker / stakeholder / end-user / unknown), `trust` (high / medium / low — bạn đề xuất: transcript với người quyết = high; SRS khách tự viết = medium; ghi chú rời rạc / tài liệu không rõ tác giả = low) — rồi `$S add $0 type=… path=… origin=… date=… author="…" authority=… trust=…`. Metadata này quyết định đề xuất khi mâu thuẫn ở reconcile; không đoán, không để `?`.

## Nhánh T — transcript khách (`$0` bắt đầu bằng T)
Xử lý `intake/$0-transcript.md`.
1. Đọc toàn bộ transcript. Đánh số đoạn (§1, §2, …) theo lượt nói hoặc theo đoạn tự nhiên nếu chưa đánh số; nếu phải đánh số, ghi phiên bản đã đánh số vào `intake/$0-transcript.numbered.md` (KHÔNG sửa file gốc).
2. Tạo `spec/discovery-$0.md` từ template `discovery.md`:
   - **Statements**: mỗi điều khách nói có giá trị requirement → một dòng S<n>, trích dẫn sát nghĩa (không "làm đẹp"), vị trí §, loại (goal / constraint / pain / example / out-of-scope).
   - **Glossary nháp**: thuật ngữ nội bộ của khách, theo nghĩa khách dùng.
   - **Open Questions**: với mỗi khoảng trống, mơ hồ, hoặc chỗ có ≥2 cách hiểu → một câu hỏi cụ thể cho khách, kèm "vì sao quan trọng" và "giả định mặc định A<n> nếu không được trả lời". Cột **Nhãn để trống** — người điền `send | assume | defer | prototype` trước gate 1 (`prototype` = câu "nên trông/hoạt động thế nào", trả lời bằng màn hình ở `/ae-kit:prototype` thay vì bằng chữ). Đây là OUTPUT CHÍNH.
   - **Mâu thuẫn**: hai statement nói ngược nhau (trong cùng transcript).
   - **Những gì khách KHÔNG nói**: checklist tối thiểu — đăng nhập/phân quyền, dữ liệu cũ/migration, đa ngôn ngữ, mobile, hiệu năng/khối lượng, audit/log, tích hợp hệ thống khác, ai vận hành, ngân sách/thời hạn.
3. Nếu đây là transcript trả lời cho câu hỏi của nguồn trước (T2 trả lời Q của T1 hoặc Q của F1, hoặc Q mà reconcile đã gửi): ghi rõ mỗi câu trả lời giải quyết Q nào (kèm discovery chứa Q), A nào được xác nhận/bác bỏ, Q nào còn mở; nếu câu trả lời chốt một conflict trong `spec/claims.md` → nhắc chạy lại `/ae-kit:reconcile` (chỉ reconcile mới ghi cột Giải quyết).
4. Nếu đây là transcript **buổi demo prototype** (người nói vậy, hoặc transcript nhắc P<v>/S<n>): với mỗi S<n> được nhắc, ghi statement kết luận (duyệt / duyệt có sửa / làm lại) kèm §; điều khách xin THÊM → statement loại goal + Q/S tương ứng (không viết requirement); câu khách xác nhận "đây là mô hình" → một statement riêng (approval cần). Sau đó nhắc `/ae-kit:prototype approve P<v> $0`.

## Nhánh F — file tài liệu khách gửi (`$0` bắt đầu bằng F)
Xử lý `intake/$0-<slug>.<ext>` (SRS, BRD, RFP, ghi chú họp, email, spec hệ thống cũ). Loại tài liệu = `type` trong sources.yaml.
1. **Bản trích.** Nếu file là `.md`/`.txt`: đọc thẳng. Nếu `.docx`/`.pdf`/khác: tạo `intake/$0-<slug>.extracted.md` bằng `pandoc <file> -t gfm -o …` hoặc `pdftotext -layout`; không có công cụ → DỪNG, bảo người xuất ra `.md`/`.txt` (hoặc dán nội dung) rồi chạy lại. KHÔNG sửa file gốc; bản trích chỉ để tham chiếu, vị trí vẫn ghi theo § / mã / trang của tài liệu gốc. Tài liệu > ~3000 dòng: đọc theo mục, không đọc cả file một lần.
2. Tạo `spec/discovery-$0.md` từ template `discovery-document.md`:
   - **Cấu trúc tài liệu** (mục 0): liệt kê heading cấp 1–2, số statement trích được, mục nào **trống / TBD / chỉ có tiêu đề** → mỗi mục như vậy là một Q (tài liệu tự thừa nhận khoảng trống).
   - **Statements**: mỗi câu có giá trị requirement → S<n>, trích sát nghĩa, vị trí = § của tài liệu + mã riêng nếu có (`§3.2 FR-012`; PDF: `tr.7`), loại goal / constraint / pain / example / out-of-scope. Câu đã viết dạng "shall/phải/hệ thống sẽ" trong SRS **vẫn là statement** — bạn không đổi nó thành R; cũng không "sửa" câu cho đúng EARS. Bảng / danh sách trong tài liệu: mỗi hàng có nghĩa riêng → một S. Với `type=notes`/`email`: ghi chú rời rạc không chủ ngữ → trích nguyên văn, mọi chỗ mơ hồ → Q; **không bổ sung chủ ngữ/ngữ cảnh**.
   - **Glossary nháp**: theo nghĩa tài liệu dùng, kể cả khi bạn nghi khác transcript (reconcile sẽ so).
   - **Open Questions**: mục trống/TBD · câu mơ hồ / ≥2 cách hiểu · câu "shall" không kiểm chứng được (không viết nổi test) · ràng buộc kỹ thuật tài liệu áp đặt mà không nêu lý do (hỏi "còn hiệu lực không?", không đoán lý do). Nếu `trust` của nguồn ≠ high: thêm một Q tổng "tài liệu này đã được <authority> chốt chưa, phiên bản nào là hiện hành?" với A mặc định = chưa chốt. Nhãn để trống.
   - **Mâu thuẫn nội bộ**: hai chỗ trong cùng tài liệu nói ngược nhau (mục tiêu vs FR; bảng vs văn bản).
   - **Những gì tài liệu KHÔNG nói**: checklist như nhánh T + ai viết, ngày, đã chốt chưa.
3. Nếu tài liệu là **phiên bản mới của tài liệu đã intake** (F2 = SRS v0.4 sau F1 = v0.3): ghi ở đầu discovery "thay thế F1" và bảng S<n> của F2 ghi cột Vị trí kèm `(= F1 S<m>)` / `(mới)` / F1 S bị bỏ → mục Mâu thuẫn; `$S set F1 note "superseded by F2"`. Reconcile sẽ coi F2 thắng F1.

## Nhánh C — codebase hiện có (`$0` bắt đầu bằng C)
1. Đọc **có giới hạn**, theo thứ tự: `README*`, manifest (`package.json` / `pyproject.toml` / `pom.xml` / `go.mod` / `Cargo.toml`), cấu trúc thư mục 2 cấp (`ls`), schema DB (`prisma/*.prisma`, `migrations/`, `*.sql`), cấu hình CI (`.github/workflows`, `.gitlab-ci.yml`), lint/format config, thư mục test (đếm file; chạy test nếu `tech.md`/manifest có lệnh chuẩn VÀ người đồng ý). Code nguồn: chỉ `Grep` theo mẫu (handler/route, try/catch, `TODO|FIXME|HACK`, hằng số magic, `any`, `console.log`) và `Read` tối đa 10 file chọn có chủ đích (entry point, model lõi, file bị TODO nhiều nhất). KHÔNG đọc toàn bộ repo.
2. Tạo `spec/discovery-$0.md` từ template `discovery-codebase.md`:
   - **Quan sát O<n>**: mỗi dòng BẮT BUỘC có bằng chứng (file:dòng, hoặc đếm "14/14 bảng"). Loại: tech / convention / rule / debt / documented (quyết định đã ghi trong README/docs). Cột Đề xuất: phân loại bạn nghĩ hợp lý. Cột **Nhãn = `?`** cho mọi dòng — chỉ người đổi thành `decided | debt | ignore`.
   - **Câu hỏi Q<n>**: mỗi O không tự giải thích được → đúng một câu, kèm giả định mặc định A<n>. Cột Nhãn để trống.
   - **Những gì codebase KHÔNG nói**: bắt buộc (người dùng, lý do stack, feature bỏ dở, môi trường thật).
   - **Số liệu**: O, Q, test pass/fail, TODO.
3. Chạy `bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" set G1_spec.checks.observed_classified false` (còn O nhãn `?`). Nếu sources.yaml chưa có `$0`: `$S add $0 type=codebase path=. origin=internal authority=unknown` (date script tự lấy từ commit).

## Vòng hỏi (mọi nhánh) — sau khi file discovery đã ghi
1. Tính frontier (Q chưa nhãn, mọi "Sau Q" đã có nhãn). Trình bày **vòng 1** đúng định dạng grilling.md §3: mỗi Q kèm "vì sao quan trọng" và `➡️ Đề xuất: A<n>`; nêu số Q chờ vòng sau. Tối đa 7 Q/vòng.
2. Chờ người trả lời. Ghi nhãn/giả định vào bảng Q của `spec/discovery-$0.md` theo bảng grilling.md §4 (chỉ `Edit` cột Nhãn và cột Giả định; brownfield: thêm cột Nhãn của O đi kèm khi người `yes`). Tính lại frontier, trình bày vòng tiếp.
3. Dừng khi frontier rỗng hoặc người nói dừng. Q chưa nhãn vẫn nằm trong file; G1 sẽ đếm.

## Kết thúc (mọi nhánh)
1. Cập nhật `spec/progress.md` mục "Trạng thái hiện tại": nguồn nào đã intake (`$S list` — một dòng), số Q mở / đã nhãn (send/assume/defer).
2. Tóm tắt cho người dùng: số statement/quan sát, số câu hỏi, danh sách Q nhãn `send` sẵn sàng gửi khách.
3. Bước tiếp theo — đếm `spec/discovery-*.md`:
   - **≥ 2 nguồn** (hoặc `spec/claims.md` đã có và nguồn này chưa nằm trong dòng "Nguồn đã đối chiếu"): "Chạy `/ae-kit:reconcile`" — bắt buộc trước specify; nếu `requirements.md` đã có và G1 đã passed, nhắc rằng `gates.py compute G1` sẽ đưa G1 về pending cho tới khi reconcile phủ nguồn mới (chống drift, đúng ý).
   - **1 nguồn:** T: gửi Open Questions cho khách; câu trả lời → `intake/T<n+1>-transcript.md` rồi `/ae-kit:intake T<n+1>`; đủ thông tin → `/ae-kit:specify`. F: nhắc rằng tài liệu một mình chưa phải lời khách — nên có ít nhất một transcript xác nhận (T<n>) trước G1; vẫn có thể `/ae-kit:specify` nếu người chấp nhận R chỉ có nguồn F. C: người mở `spec/discovery-$0.md`, đổi `?` → `decided | debt | ignore` cho từng O, trả lời Q ngay trong bảng nếu được; rồi `/ae-kit:specify`. O `decided` loại tech → người (hoặc replan) chép vào `docs/product/tech.md`; O `decided` loại rule → `/ae-kit:ratchet` với nguồn `[C<n> O<m>]`.
