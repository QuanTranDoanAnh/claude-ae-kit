---
name: prototype
description: Gate GP — dựng prototype UI/UX (click-through) từ requirements đã accepted để KHÁCH HÀNG phản ứng và duyệt trước khi plan/code. Tạo spec/prototype/P<v>/ + screens.md (S<n> ↔ R), kịch bản demo, sau demo ghi approval-P<v>.md và đưa buổi duyệt vào intake như một transcript. Prototype là artifact spec, không phải mã sản phẩm. Dự án không có UI → bỏ qua (GP n/a).
disable-model-invocation: true
argument-hint: "[new | demo | approve <P<v>> <T<n>>]"
allowed-tools: Read Write Edit Glob Grep Bash(bash *) Bash(ls *) Bash(mkdir *) Bash(git *) Bash(date *) Bash(cp *) Agent
---

`G=bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py"` (viết tắt `$G`). Template: `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/templates/{screens.md,approval.md}`. Cách hỏi theo vòng: `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/references/grilling.md`.

## Điều kiện vào
- `$G get G1_spec.status` = `passed`. Không → DỪNG: "Prototype dựng trên spec đã accepted — `/ae-kit:approve G1` trước." (Ngoại lệ: người nói "dựng wireframe để hỏi khách" trước G1 → cho phép, nhưng ghi `<!-- pre-G1 -->` đầu screens.md và không được approve GP.)
- `$G get GP_prototype.status` = `n/a` → DỪNG: "Dự án khai không có UI. Bật bằng `gates.py set GP_prototype.status pending`."

## Ba nguyên tắc (không thương lượng)
1. **Prototype là artifact spec.** Nằm trong `spec/prototype/P<v>/`. HTML tĩnh + dữ liệu giả, hoặc export từ Claude Design, hoặc Figma link + screenshot. KHÔNG backend, KHÔNG DB, KHÔNG dùng stack sản phẩm. `/ae-kit:next-task` bị cấm import/copy từ đây; tái dùng layout là quyết định tường minh `D<n>` trong `spec/design.md`.
2. **Mọi màn hình trả lời một R.** Màn hình không ↔ R nào là scope creep và làm GP đỏ. Khách xin thêm tại demo → đi qua transcript → intake → Q/R, không đưa thẳng vào prototype.
3. **Khách phản ứng với thứ thật, không với chữ.** Q nhãn `prototype` trong discovery là những câu "nên trông/hoạt động thế nào" — chúng được trả lời bằng màn hình, không bằng email.

## `$0` = `new` (hoặc trống) — dựng P<v>
1. Thu thập: R accepted trong `spec/requirements.md`; Q nhãn `prototype` trong `spec/discovery-*.md`; glossary; `docs/product/mission.md` (cho ai). Brownfield: luật UI đã `decided` trong `discovery-C<n>` (design system, component library) — prototype phải theo.
2. Phân loại R: có UI / không có UI. Trình bày cho người dùng một vòng grilling: đề xuất danh sách màn hình S<n> ↔ R, luồng task đầu, mức độ (wireframe / click-through / visual; đề xuất click-through cho lần đầu), công cụ. `yes` = chấp nhận. Không dựng gì trước khi người chốt danh sách.
3. v = phiên bản mới (P1 nếu chưa có). Tạo `spec/prototype/P<v>/` và từng màn hình theo danh sách; mỗi màn hình có đủ trạng thái cột "Trạng thái đã dựng" (rỗng / lỗi / đang tải / không có quyền tối thiểu); dữ liệu giả dùng ví dụ thật của khách trong transcript nếu có (đã che PII). Click-through: link giữa các màn hình theo luồng.
   - Khi có Claude Design trong phiên: dựng ở đó, xuất HTML vào `P<v>/`; vẫn ghi screens.md như thường.
   - Có thể giao từng màn hình cho subagent (file riêng, không chồng); bạn tự kiểm luồng click bằng cách mở từng file.
4. Ghi `spec/prototype/screens.md` từ template (lần sau: cập nhật, giữ lịch sử phiên bản). Điền "R không có UI" cho mọi R còn lại — GP đếm.
5. Viết kịch bản demo `spec/prototype/demo-P<v>.md`: thứ tự màn hình, với mỗi S câu hỏi cụ thể để hỏi khách (lấy từ Q nhãn `prototype` + ranh giới chưa chốt), và câu mở đầu bắt buộc: *"Đây là mô hình để chốt yêu cầu, không phải phần mềm; tiến độ thật tính theo sprint."* Nhắc ghi âm/ghi biên bản có sự đồng ý của khách.
6. `$G compute GP`. Dán output. Kết thúc: "Demo P<v> cho khách theo `demo-P<v>.md`; sau buổi demo: đặt transcript vào `intake/T<n>-transcript.md`, chạy `/ae-kit:intake T<n>` rồi `/ae-kit:prototype approve P<v> T<n>`."

## `$0` = `demo` — chuẩn bị/ôn lại buổi demo
In `demo-P<v>.md` mới nhất, luồng task đầu, và các Q còn mở. Không dựng gì.

## `$0` = `approve P<v> T<n>` — ghi nhận sau buổi demo
1. Điều kiện: `spec/discovery-T<n>.md` tồn tại (buổi demo đã qua intake). Không → DỪNG: "Chạy `/ae-kit:intake T<n>` trước — phản ứng của khách phải có nguồn §m."
2. Đọc discovery-T<n>: statement nào là kết luận về từng S (duyệt / duyệt có sửa / làm lại), statement nào là yêu cầu THÊM. Trình bày bảng cho người dùng xác nhận (một vòng grilling).
3. Ghi `spec/prototype/approval-P<v>.md` từ template: 3 dòng đầu đúng chính tả (`Prototype:`, `Transcript:`, `Xác nhận mô hình: yes` — chỉ ghi `yes` nếu transcript có câu khách xác nhận; không có → `no` và GP đỏ, hỏi khách bổ sung), bảng S ↔ kết luận ↔ §, mục "yêu cầu THÊM" trỏ § (không sửa prototype ở đây).
4. "Làm lại" bất kỳ S nào trong luồng task đầu → in: "Chưa duyệt được. Dựng P<v+1> (`/ae-kit:prototype new`) rồi demo lại." Ghi dòng vào Lịch sử phiên bản của screens.md.
5. Yêu cầu THÊM / sửa R → nhắc: `/ae-kit:specify` (R mới có `[src: T<n> §m]`) → `/ae-kit:lint-spec` → `/ae-kit:approve G1` lại; GP sẽ tự về pending nếu requirements đổi sau khi duyệt (drift guard) — đó là đúng, khách phải thấy lại.
6. `$G compute GP`. Mọi ô xanh → in: "Chạy `/ae-kit:approve GP \"<tên khách>\"`" (approve ghi `req_fingerprint`). Còn đỏ → liệt kê.

## Sau GP
`/ae-kit:design` (mục UX tham chiếu S<n> đã duyệt) → `/ae-kit:plan`. Contract của sprint có UI phải có seam `e2e` và tiêu chí "khớp S<n>" với bằng chứng screenshot.
