# Prototype — {{PROJECT_NAME}} — phiên bản hiện tại P{{V}}

<!-- Prototype là ARTIFACT SPEC để khách phản ứng, KHÔNG phải mã sản phẩm. Nằm trong spec/prototype/P<v>/ (HTML tĩnh, screenshot, hoặc link).
     /ae-kit:next-task bị cấm import/copy từ đây. Muốn tái dùng layout → ghi D<n> trong spec/design.md.
     gates.py compute GP kiểm: mọi R accepted có màn hình HOẶC khai ở "R không có UI"; mọi S có ≥1 R; luồng task đầu ≥2 S;
     file trong dấu ` tồn tại trong spec/prototype/; có approval-P<v>.md. -->

Phiên bản: P{{V}} · ngày {{DATE}} · công cụ: {{TOOL}} (Claude Design / HTML tĩnh / Figma) · mức độ: {{FIDELITY}} (wireframe / click-through / visual)

## 1. Màn hình
<!-- Một dòng một màn hình. Cột ↔ R: requirement mà màn hình này phục vụ — màn hình không ↔ R nào là scope creep, GP đỏ.
     Trạng thái: liệt kê đủ các trạng thái agent hay quên: rỗng · lỗi · đang tải · không có quyền · offline (ghi "n/a" nếu thật sự không có). -->
| ID | Màn hình | ↔ R | File / link | Trạng thái đã dựng | Q trả lời (nhãn prototype) |
|----|----------|-----|-------------|--------------------|----------------------------|
| S1 | | R1.1 | `P{{V}}/s1-....html` | rỗng · lỗi · đang tải | Q3 |

## 2. Luồng task đầu (vertical slice — phải click được từ đầu đến cuối)
S1 → S2 → S3

## 3. Luồng khác (tuỳ chọn)
- ...

## R không có UI
<!-- Liệt kê mã R accepted KHÔNG có màn hình (API, batch, tích hợp, N*). Khai ở đây để GP không đòi màn hình. -->
- 

## Lịch sử phiên bản
| P | Ngày | Thay đổi so với bản trước | Nguồn (T<n> §m / F<n> §m) |
|---|------|---------------------------|-----------------|
| P1 | | bản đầu | |
