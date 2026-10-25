---
name: intake
description: Trích xuất nguồn thành spec/discovery-*.md — T<n> là transcript trao đổi với khách (intake/T<n>-transcript.md), C<n> là codebase hiện có (brownfield). Chỉ TRÍCH XUẤT và ĐẶT CÂU HỎI, không suy diễn requirement. Bước đầu tiên của quy trình.
disable-model-invocation: true
argument-hint: "<T<n> | C<n>>"
allowed-tools: Read Write Edit Glob Grep Bash(ls *) Bash(git *) Bash(wc *) Bash(bash *)
---

Nguồn `$0`. Nếu trống: liệt kê transcript trong `intake/` và hỏi; nhắc rằng codebase cũ dùng `C1`.
Template ở `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/templates/`. Cách hỏi theo vòng: `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/references/grilling.md` (đọc trước khi trình bày Q).

## Nguyên tắc cốt lõi (áp dụng cho cả T và C)
Bạn đang làm việc với **lời của khách** hoặc **dấu vết của người đi trước**. Nhiệm vụ của bạn là **làm lộ ra những gì người cần quyết định**, không phải thay họ quyết định. Mọi chỗ trống là một CÂU HỎI, không phải chỗ để điền giả định hợp lý. Tuyệt đối KHÔNG viết requirement ("SHALL"), KHÔNG đề xuất giải pháp, KHÔNG chọn stack, KHÔNG suy diễn lý do ("có lẽ họ chọn X vì…" là cấm).

Phân biệt **sự thật** và **quyết định** (grilling.md §1): sự thật tra cứu được (file, lệnh, schema, transcript) thì tự tra và ghi thành statement/quan sát có bằng chứng; chỉ quyết định mới thành Q. Mỗi Q ghi cột **Sau Q** nếu nó chỉ có nghĩa sau khi một Q khác được trả lời.

## Nhánh T — transcript khách (`$0` bắt đầu bằng T)
Xử lý `intake/$0-transcript.md`.
1. Đọc toàn bộ transcript. Đánh số đoạn (§1, §2, …) theo lượt nói hoặc theo đoạn tự nhiên nếu chưa đánh số; nếu phải đánh số, ghi phiên bản đã đánh số vào `intake/$0-transcript.numbered.md` (KHÔNG sửa file gốc).
2. Tạo `spec/discovery-$0.md` từ template `discovery.md`:
   - **Statements**: mỗi điều khách nói có giá trị requirement → một dòng S<n>, trích dẫn sát nghĩa (không "làm đẹp"), vị trí §, loại (goal / constraint / pain / example / out-of-scope).
   - **Glossary nháp**: thuật ngữ nội bộ của khách, theo nghĩa khách dùng.
   - **Open Questions**: với mỗi khoảng trống, mơ hồ, hoặc chỗ có ≥2 cách hiểu → một câu hỏi cụ thể cho khách, kèm "vì sao quan trọng" và "giả định mặc định A<n> nếu không được trả lời". Cột **Nhãn để trống** — người điền `send | assume | defer | prototype` trước gate 1 (`prototype` = câu "nên trông/hoạt động thế nào", trả lời bằng màn hình ở `/ae-kit:prototype` thay vì bằng chữ). Đây là OUTPUT CHÍNH.
   - **Mâu thuẫn**: hai statement nói ngược nhau.
   - **Những gì khách KHÔNG nói**: checklist tối thiểu — đăng nhập/phân quyền, dữ liệu cũ/migration, đa ngôn ngữ, mobile, hiệu năng/khối lượng, audit/log, tích hợp hệ thống khác, ai vận hành, ngân sách/thời hạn.
3. Nếu đây là transcript trả lời cho câu hỏi của transcript trước (T2 trả lời Q của T1): ghi rõ mỗi câu trả lời giải quyết Q nào, A nào được xác nhận/bác bỏ, Q nào còn mở.
4. Nếu đây là transcript **buổi demo prototype** (người nói vậy, hoặc transcript nhắc P<v>/S<n>): với mỗi S<n> được nhắc, ghi statement kết luận (duyệt / duyệt có sửa / làm lại) kèm §; điều khách xin THÊM → statement loại goal + Q/S tương ứng (không viết requirement); câu khách xác nhận "đây là mô hình" → một statement riêng (approval cần). Sau đó nhắc `/ae-kit:prototype approve P<v> $0`.

## Nhánh C — codebase hiện có (`$0` bắt đầu bằng C)
1. Đọc **có giới hạn**, theo thứ tự: `README*`, manifest (`package.json` / `pyproject.toml` / `pom.xml` / `go.mod` / `Cargo.toml`), cấu trúc thư mục 2 cấp (`ls`), schema DB (`prisma/*.prisma`, `migrations/`, `*.sql`), cấu hình CI (`.github/workflows`, `.gitlab-ci.yml`), lint/format config, thư mục test (đếm file; chạy test nếu `tech.md`/manifest có lệnh chuẩn VÀ người đồng ý). Code nguồn: chỉ `Grep` theo mẫu (handler/route, try/catch, `TODO|FIXME|HACK`, hằng số magic, `any`, `console.log`) và `Read` tối đa 10 file chọn có chủ đích (entry point, model lõi, file bị TODO nhiều nhất). KHÔNG đọc toàn bộ repo.
2. Tạo `spec/discovery-$0.md` từ template `discovery-codebase.md`:
   - **Quan sát O<n>**: mỗi dòng BẮT BUỘC có bằng chứng (file:dòng, hoặc đếm "14/14 bảng"). Loại: tech / convention / rule / debt / documented (quyết định đã ghi trong README/docs). Cột Đề xuất: phân loại bạn nghĩ hợp lý. Cột **Nhãn = `?`** cho mọi dòng — chỉ người đổi thành `decided | debt | ignore`.
   - **Câu hỏi Q<n>**: mỗi O không tự giải thích được → đúng một câu, kèm giả định mặc định A<n>. Cột Nhãn để trống.
   - **Những gì codebase KHÔNG nói**: bắt buộc (người dùng, lý do stack, feature bỏ dở, môi trường thật).
   - **Số liệu**: O, Q, test pass/fail, TODO.
3. Chạy `bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" set G1_spec.checks.observed_classified false` (còn O nhãn `?`).

## Vòng hỏi (cả hai nhánh) — sau khi file discovery đã ghi
1. Tính frontier (Q chưa nhãn, mọi "Sau Q" đã có nhãn). Trình bày **vòng 1** đúng định dạng grilling.md §3: mỗi Q kèm "vì sao quan trọng" và `➡️ Đề xuất: A<n>`; nêu số Q chờ vòng sau. Tối đa 7 Q/vòng.
2. Chờ người trả lời. Ghi nhãn/giả định vào bảng Q của `spec/discovery-$0.md` theo bảng grilling.md §4 (chỉ `Edit` cột Nhãn và cột Giả định; brownfield: thêm cột Nhãn của O đi kèm khi người `yes`). Tính lại frontier, trình bày vòng tiếp.
3. Dừng khi frontier rỗng hoặc người nói dừng. Q chưa nhãn vẫn nằm trong file; G1 sẽ đếm.

## Kết thúc (cả hai nhánh)
1. Cập nhật `spec/progress.md` mục "Trạng thái hiện tại": nguồn nào đã intake, số Q mở / đã nhãn (send/assume/defer).
2. Tóm tắt cho người dùng: số statement/quan sát, số câu hỏi, danh sách Q nhãn `send` sẵn sàng gửi khách.
3. Bước tiếp theo:
   - T: gửi Open Questions cho khách; câu trả lời → `intake/T<n+1>-transcript.md` rồi `/ae-kit:intake T<n+1>`; đủ thông tin → `/ae-kit:specify`. Nhắc điền cột Nhãn cho Q.
   - C: người mở `spec/discovery-$0.md`, đổi `?` → `decided | debt | ignore` cho từng O, trả lời Q ngay trong bảng nếu được; rồi `/ae-kit:specify`. O `decided` loại tech → người (hoặc replan) chép vào `docs/product/tech.md`; O `decided` loại rule → `/ae-kit:ratchet` với nguồn `[C<n> O<m>]`.
