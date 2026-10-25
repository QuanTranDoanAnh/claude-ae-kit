# Claims — đối chiếu chéo nguồn — {{PROJECT_NAME}}

Nguồn đã đối chiếu: {{SOURCE_IDS}}
Ngày: {{DATE}} · thứ tự ưu tiên khi mâu thuẫn (đề xuất, từ `sources.py precedence`): {{PRECEDENCE}}

<!-- Một CLAIM = một điều về sản phẩm mà ít nhất một nguồn nói, viết lại trung lập (một câu, KHÔNG "SHALL", không giải pháp).
     Cột Nguồn: mã statement + vị trí, ví dụ `T1 S3 (§14); F1 S7 (§3.2 FR-012); C1 O4`. gates.py compute G1 đọc mã `T1 S3`.
     Trạng thái: corroborated (≥2 nguồn đồng ý) · single (một nguồn) · conflict (nguồn nói ngược nhau — phải có Giải quyết).
     Đề xuất: cách giải quyết agent đề xuất theo precedence (conflict) hoặc câu hỏi xác nhận (single, nguồn trust ≠ high) — là A, chưa phải quyết định.
     Giải quyết: NGƯỜI điền (qua vòng hỏi của /ae-kit:reconcile): "T1 §14 thắng (người quyết <ngày>: khách nói sau)" · "send Q12 (discovery-T2)" · "defer".
     Dòng conflict trống Giải quyết → G1 đỏ (claims_reconciled). Mọi S loại goal/constraint/out-of-scope phải thuộc ≥1 claim. -->

| ID | Claim (trung lập, một câu) | Nguồn | Trạng thái | Đề xuất | Giải quyết |
|----|----------------------------|-------|------------|---------|------------|
| CL1 | ... | T1 S3 (§14); F1 S7 (§3.2) | corroborated | | |
| CL2 | ... | F1 S12 (§5.1) | single | hỏi khách xác nhận → Q<n> | |
| CL3 | ... — T1 nói bỏ, F1 vẫn có | T1 S9 (§31) ⟂ F1 S4 (§4.3) | conflict | T1 §31 thắng (mới hơn, decision-maker) | |

## Thuật ngữ lệch nghĩa giữa các nguồn
<!-- Cùng một từ, nguồn A dùng nghĩa X, nguồn B nghĩa Y → đề xuất tách/thống nhất; specify ghi vào Glossary với nguồn. -->
| Thuật ngữ | Nguồn A | Nguồn B | Đề xuất | Giải quyết |
|-----------|---------|---------|---------|------------|

## Khoảng trống chung (không nguồn nào nói)
<!-- Giao của mục "Những gì ... KHÔNG nói" của mọi discovery. Mỗi dòng → đã có Q ở discovery nào? Nếu chưa → thêm Q vào discovery của nguồn mới nhất. -->
-
