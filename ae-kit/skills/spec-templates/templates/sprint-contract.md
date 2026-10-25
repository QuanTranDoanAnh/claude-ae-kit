# Sprint Contract — Sprint {{N}}

Scope: T{{a}}–T{{b}}  ·  Requirements: {{R-list}}  ·  Invariants: {{I-list}}

## Generator đề xuất
**Sẽ build:**
- ...

**Sẽ verify bằng:**
- `lệnh` → kỳ vọng ...

**Giả định tôi đang dựa vào:**
- ...

## Evaluator phản biện
<!-- Thiếu gì? Ranh giới nào chưa chốt (≥ hay >)? Edge case nào bị bỏ? Test nào chưa đủ sâu? -->
- Thiếu: ...
- Cần chốt: ...
- Yêu cầu thêm: ...

## Seam (nơi test quan sát hành vi — chốt ở đây, next-task không được mở seam mới)
<!-- Ưu tiên seam cao nhất còn chạy được trong CI; càng ít seam càng tốt. Dạng: e2e (Playwright) · api (HTTP) · service <module> · cli · unit <hàm thuần>. -->
| Seam | Loại | Gồm những gì / bỏ qua những gì | Prior art (test tương tự có sẵn) |
|------|------|--------------------------------|----------------------------------|
| S1 | | | |

## Chốt (cả hai đồng ý — đây là định nghĩa DONE của sprint)
| # | Tiêu chí done | Seam | Cách verify | Ngưỡng |
|---|---------------|------|-------------|--------|
| 1 | | S1 | | cứng / mềm |

Budget: tối đa {{3}} vòng fix. Vượt budget → dừng, báo người.
