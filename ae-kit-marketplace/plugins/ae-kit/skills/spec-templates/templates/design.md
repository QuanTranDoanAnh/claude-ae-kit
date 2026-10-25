# Design — {{PROJECT_NAME}}

<!-- High-level có chủ đích. Nói CẤU TRÚC và HỢP ĐỒNG, không nói thuật toán.
     Lý do: nếu spec chi tiết hoá implementation sớm mà sai, lỗi lan xuống toàn bộ build. -->

## 1. Context & ràng buộc kiến trúc
- Stack: ...
- Deploy: ...
- Tích hợp bên ngoài: ...

## 2. Entities (domain model)
```
Entity { field: type, ... }  — mô tả 1 dòng, trạng thái nếu có
```

## 3. Hợp đồng giao diện (API / events / UI routes)
| Interface | Input | Output | Lỗi | ↔ R |
|-----------|-------|--------|-----|-----|
| GET /api/... | | | | R1.1 |

## 4. Invariants (bất biến) — evaluator CHẤM THEO ĐÂY, ngưỡng cứng
<!-- Điều luôn đúng bất kể đường đi nào. Nêu rõ được bảo đảm ở TẦNG nào (DB / domain / API). -->
| ID | Bất biến | Bảo đảm ở tầng | ↔ R |
|----|----------|----------------|-----|
| I1 | ... | DB (unique index) | R2.2 |

## 4b. UX (chỉ dự án có UI — tham chiếu prototype đã khách duyệt ở GP)
<!-- Nguồn: spec/prototype/screens.md P<v> đã duyệt + approval-P<v>.md. Không vẽ lại màn hình ở đây; nói LUỒNG, TRẠNG THÁI, RÀNG BUỘC.
     Mỗi dòng ↔ R; trạng thái là nơi agent hay bỏ sót nhất → evaluator chấm theo bảng này + screenshot so với S<n>. -->
Prototype duyệt: P{{V}} (approval-P{{V}}.md) · Design system / component library: {{DS}} (nguồn: D<n> hoặc [C<n> O<m>])

| Luồng | Màn hình (S<n>) | Trạng thái bắt buộc có | Ràng buộc (i18n / a11y / thiết bị / quyền) | ↔ R |
|-------|-----------------|------------------------|--------------------------------------------|-----|
| Đặt lịch | S1 → S2 → S3 | rỗng · lỗi · đang tải · không có quyền | mobile-first; vi/en | R1.1–R1.3 |

Tái dùng từ prototype: KHÔNG (mặc định) / D<n>: ... (nêu rõ phần nào, vì sao)

## 5. Quyết định thiết kế (ADR rút gọn)
| ID | Quyết định | Lý do | Thay thế đã cân nhắc |
|----|------------|-------|----------------------|
| D1 | ... | ... | ... |

## 6. Ánh xạ Acceptance Criteria
| AC | ↔ Requirements | Cách verify (test / Playwright / script) |
|----|----------------|------------------------------------------|
| AC1 | R1.1–R1.3 | |
