---
name: design
description: Từ spec/requirements.md đã accepted (G1 passed), viết spec/design.md high-level — entities, hợp đồng giao diện, invariants (ép xuống đúng tầng), quyết định kiến trúc, ánh xạ acceptance criteria. Không đặc tả thuật toán. Đề xuất luật từ invariant qua progress.md, không tự ghi CLAUDE.md.
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash(bash *)
---

Tạo `spec/design.md` từ template `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/templates/design.md`, dựa trên `spec/requirements.md`, `CLAUDE.md` và `docs/product/tech.md`.

## Điều kiện vào
Chạy `bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" get G1_spec.status`. Nếu không phải `passed` → DỪNG, in: "G1 chưa passed — chạy `/ae-kit:lint-spec` rồi `/ae-kit:approve G1`". Sau đó `get GP_prototype.status`: `pending`/`blocked` → DỪNG: "Khách chưa duyệt prototype — `/ae-kit:prototype`"; `n/a` → bỏ mục 4b; `passed` → mục 4b bắt buộc. Người có thể nói "cứ làm" → tiếp tục nhưng ghi dòng cảnh báo đầu design.md: `<!-- thiết kế trên spec chưa qua G1 -->`.

## Mức chi tiết — có chủ đích
Spec này nói **cấu trúc và hợp đồng**, không nói thuật toán. Lý do: nếu đặc tả implementation sớm mà sai, lỗi sẽ lan xuống toàn bộ build. Để generator tự tìm đường đi bên trong hợp đồng.
- Entities: tên, field, kiểu, trạng thái. Không ORM code.
- Interfaces: endpoint/event/route với input, output, mã lỗi, và ↔ R nào.
- **Invariants**: điều luôn đúng. Với mỗi I*, ghi rõ **bảo đảm ở tầng nào** (DB constraint / domain / API). Mặc định: bất biến về tính duy nhất, toàn vẹn, tiền, thời gian → ép xuống DB hoặc transaction, không chỉ check ở application code.
- Quyết định thiết kế: mỗi D* có lý do và phương án đã loại. Nếu D* chọn thư viện/pattern **khác** với `docs/product/tech.md` → nêu rõ và ghi vào `spec/progress.md` mục "Đề xuất ratchet" một dòng `- replan tech.md: <thay đổi> — [D<n>]` để `/ae-kit:replan` cập nhật tầng context.
- **UX (mục 4b, khi GP passed)**: đọc `spec/prototype/screens.md` và `approval-P<v>.md`; ghi luồng theo S<n> đã duyệt, trạng thái bắt buộc có cho từng luồng (rỗng/lỗi/đang tải/không có quyền/offline — ghi `n/a` có chủ đích chứ không bỏ trống), ràng buộc i18n/a11y/thiết bị/quyền, và dòng "Tái dùng từ prototype": mặc định KHÔNG; muốn tái dùng → một D<n> nêu phần nào, vì sao. Màn hình khách "duyệt có sửa" → ghi sửa gì (§m) ngay tại dòng luồng.
- Ánh xạ AC ↔ R ↔ cách verify: mọi R accepted phải xuất hiện trong ít nhất một AC. AC của R có UI: cách verify là e2e + screenshot khớp S<n>.

## Invariant → luật (không tự ghi CLAUDE.md)
Với mỗi I* mà agent dễ vi phạm khi implement (timezone, idempotency, uniqueness, tiền), viết vào `spec/progress.md` mục "Đề xuất ratchet" một dòng theo định dạng luật: `- <luật>. — <lý do> — [I<n>]`. Người duyệt qua `/ae-kit:ratchet`. KHÔNG sửa `CLAUDE.md` trong skill này.

## Kết thúc
Liệt kê: các R không có AC nào cover (phải = 0), các I* và tầng bảo đảm, 3 quyết định D* cần người dùng xác nhận nhất, số dòng đã thêm vào "Đề xuất ratchet". Nhắc bước tiếp: `/ae-kit:plan`.
