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

## 5. Quyết định thiết kế (ADR rút gọn)
| ID | Quyết định | Lý do | Thay thế đã cân nhắc |
|----|------------|-------|----------------------|
| D1 | ... | ... | ... |

## 6. Ánh xạ Acceptance Criteria
| AC | ↔ Requirements | Cách verify (test / Playwright / script) |
|----|----------------|------------------------------------------|
| AC1 | R1.1–R1.3 | |
