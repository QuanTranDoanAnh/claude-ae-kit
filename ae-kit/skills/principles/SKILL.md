---
name: principles
description: Tầng thứ ba của constitution — luật CÓ ĐIỀU KIỆN, nạp theo tình huống (không phải luật bất biến trong CLAUDE.md, không phải context sản phẩm trong docs/product). Liệt kê bảng trigger → principle và cách thêm trigger riêng cho project (.ae-kit/principles.md). Dùng để tra "tình huống này nên đọc principle nào".
disable-model-invocation: true
allowed-tools: Read Glob Grep
---

Ba tầng constitution của ae-kit:

| Tầng | Ở đâu | Khi nạp | Ai sửa |
|------|-------|---------|--------|
| Luật bất biến | `CLAUDE.md` (≤ 40 dòng) | mọi turn | `/ae-kit:ratchet` |
| Context sản phẩm | `docs/product/*.md` | khi task cần | `/ae-kit:replan` |
| **Principle có điều kiện** | `ae-kit:principle-*` + trigger riêng `.ae-kit/principles.md` | khi tình huống khớp trigger | plugin; project thêm trigger qua ratchet mức 4 |

Lý do có tầng này: một luật chỉ đúng trong tình huống (khi refactor, khi sửa bug) mà đưa vào CLAUDE.md sẽ chiếm chú ý ở mọi turn khác. Principle được đọc đủ dài khi cần, và không tồn tại khi không cần.

## Bảng trigger mặc định (plugin)
| Khi | Đọc skill |
|-----|-----------|
| Sắp thêm abstraction, lớp, tham số, file mới; diff phình; refactor | `ae-kit:principle-laziness-protocol` |
| Task có trạng thái, ≥ 3 nhánh if trên cùng một thứ, shape lặp nhiều file | `ae-kit:principle-model-the-domain` |
| Viết validation, xử lý lỗi, adapter, tích hợp ngoài, ép invariant | `ae-kit:principle-boundary-discipline` |
| Trước khi đánh `[x]`, commit, hoặc nói "xong" | `ae-kit:principle-prove-it-works` |
| Task `Loại: bugfix`; evaluator FAIL; sắp thêm null-check | `ae-kit:principle-fix-root-causes` |
| Cùng tiêu chí FAIL ≥ 2 vòng; `Done:` fail ≥ 3 lượt cùng cách | `ae-kit:principle-attack-the-premise` |
| Viết/sửa/xoá test; chọn seam trong contract | `ae-kit:principle-test-behavior-not-implementation` |
| Task `Loại: refactor`; debt phase 0; `Files:` > 5; migration | `ae-kit:principle-sequence-verifiable-units` |
| Đầu next-task; phải đọc > 10 file; output lệnh dài | `ae-kit:principle-guard-the-context-window` |
| Chạy ratchet; CLAUDE.md gần 40 dòng; đề xuất ratchet lặp ý | `ae-kit:principle-encode-lessons-in-structure` |

## Trigger riêng của project
File `.ae-kit/principles.md` (tạo bởi init, nối thêm bởi `/ae-kit:ratchet` mức 4), mỗi dòng:
```
| <khi nào> | <ae-kit:principle-… hoặc đường dẫn skill riêng .claude/skills/…> | [ratchet #n] |
```
`/ae-kit:next-task` đọc file này ở bước khởi động và khớp với task hiện tại. Dòng không có `[nguồn]` bị bỏ qua (cùng luật với CLAUDE.md).

## Quy tắc dùng
- Đọc **toàn bộ** leaf trước khi nói đã áp dụng. Trong nhật ký progress.md, nêu principle nào đã *đổi* quyết định gì; principle đọc mà không đổi gì thì không kể.
- Principle không thay thế gate: nó giúp qua gate ít retry hơn, không bỏ được gate nào.
- Thấy mình muốn viết principle mới cho project → đó là ratchet mức 4 (trigger) hoặc một skill riêng trong `.claude/skills/`, không phải dòng CLAUDE.md.

Các leaf `principle-*` phỏng theo pstack của Lauren Tan (MIT, qua bản port pstack-claude), diễn đạt lại và cắt về đúng những gì ae-kit cần; xem `NOTICE.md`.
