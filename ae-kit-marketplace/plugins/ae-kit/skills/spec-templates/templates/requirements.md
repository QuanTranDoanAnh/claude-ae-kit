# Requirements — {{PROJECT_NAME}}

Cú pháp EARS. Mỗi dòng: mã, câu EARS, tag nguồn gốc, trạng thái.
- `[src: T1 §12]` = khách nói (transcript T1, đoạn 12)
- `[src: A3]` = giả định A3 trong discovery, CHƯA được khách xác nhận
- Trạng thái: `proposed` → `accepted` (khách/bạn duyệt) → `implemented` → `verified`

Mẫu EARS:
- Ubiquitous: `The system SHALL ...`
- Event: `WHEN <sự kiện>, the system SHALL ...`
- State: `WHILE <trạng thái>, the system SHALL ...`
- Unwanted: `IF <điều kiện lỗi>, THEN the system SHALL ...`
- Optional: `WHERE <tính năng có>, the system SHALL ...`

## R1. {{Nhóm chức năng 1}}
| ID | Requirement | Src | Status |
|----|-------------|-----|--------|
| R1.1 | WHEN ..., the system SHALL ... | T1 §4 | proposed |
| R1.2 | IF ..., THEN the system SHALL ... | A2 | proposed |

## R2. {{Nhóm chức năng 2}}

## Non-functional
| ID | Requirement | Src | Status |
|----|-------------|-----|--------|
| N1 | The system SHALL ... (hiệu năng / bảo mật / i18n / audit) | | |

## Non-goals (v1) — KHÔNG làm
<!-- Quan trọng ngang requirements. Mỗi dòng có lý do. -->
- ...

## Glossary
| Thuật ngữ | Định nghĩa thống nhất | Src |
|-----------|----------------------|-----|
