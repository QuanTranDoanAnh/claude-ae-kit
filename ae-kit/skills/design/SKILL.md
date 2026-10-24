---
name: design
description: Từ spec/requirements.md đã accepted, viết spec/design.md high-level — entities, hợp đồng giao diện, invariants (ép xuống đúng tầng), quyết định kiến trúc, ánh xạ acceptance criteria. Không đặc tả thuật toán.
disable-model-invocation: true
allowed-tools: Read Write Glob Grep
---

Tạo `spec/design.md` từ template `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/templates/design.md`, dựa trên `spec/requirements.md` và `CLAUDE.md`.

## Trước khi viết
- Đếm số R còn `proposed`. Nếu > 0, cảnh báo người dùng và hỏi có tiếp tục không (thiết kế trên requirement chưa duyệt sẽ phải làm lại).

## Mức chi tiết — có chủ đích
Spec này nói **cấu trúc và hợp đồng**, không nói thuật toán. Lý do: nếu đặc tả implementation sớm mà sai, lỗi sẽ lan xuống toàn bộ build. Để generator tự tìm đường đi bên trong hợp đồng.
- Entities: tên, field, kiểu, trạng thái. Không ORM code.
- Interfaces: endpoint/event/route với input, output, mã lỗi, và ↔ R nào.
- **Invariants**: điều luôn đúng. Với mỗi I*, ghi rõ **bảo đảm ở tầng nào** (DB constraint / domain / API). Mặc định: bất biến về tính duy nhất, toàn vẹn, tiền, thời gian → ép xuống DB hoặc transaction, không chỉ check ở application code.
- Quyết định thiết kế: mỗi D* có lý do và phương án đã loại. Đây là chỗ kiến trúc sư để lại dấu vết cho người sau.
- Ánh xạ AC ↔ R ↔ cách verify: mọi R accepted phải xuất hiện trong ít nhất một AC.

## Kết thúc
Liệt kê: các R không có AC nào cover (phải = 0), các I* và tầng bảo đảm, 3 quyết định D* cần người dùng xác nhận nhất. Nhắc bước tiếp: `/ae-kit:plan`.
