# NOTICE — nguồn ý tưởng của bên thứ ba

ae-kit © Albert Tran, MIT. Một số thành phần phỏng theo ý tưởng từ các dự án MIT khác; nội dung được viết lại bằng tiếng Việt và cắt gọn cho ae-kit, không sao chép nguyên văn.

| Thành phần ae-kit | Phỏng theo | Tác giả / giấy phép |
|---|---|---|
| `skills/principle-*` (tầng principle có điều kiện), bảng trigger trong `skills/principles` | Các skill `principle-*` và cơ chế nạp theo trigger của **pstack** | Lauren Tan (poteto), MIT — https://github.com/cursor/plugins/tree/main/pstack ; bản port pstack-claude của Michael Denyer, MIT — https://github.com/michael-denyer/pstack-claude |
| Panel evaluator đa model (`gates.py panel`, skill `evaluate` 2a) | Skill `interrogate` (review đa model, tín hiệu từ sự đa dạng model) của pstack | như trên |
| Vòng hỏi theo frontier, mỗi câu kèm đề xuất, `yes` chấp nhận (`references/grilling.md`) | Skill `grilling` / `grill-me` của **Skills for Real Engineers** | Matt Pocock, MIT — https://github.com/mattpocock/skills |
| Seam trong sprint contract, `references/tdd.md`, expand–contract cho refactor rộng | Skill `tdd`, `to-tickets`, `code-review` của Skills for Real Engineers | như trên |
| Xuất task ra issue tracker, giữ spec/ là nguồn sự thật (`scripts/tracker.py`) | Cách `to-tickets` publish ticket lên tracker | như trên |

Hai bản MIT gốc yêu cầu giữ thông báo bản quyền khi sao chép mã; ae-kit không sao chép mã hay văn bản gốc, bảng này tồn tại để ghi nhận nguồn ý tưởng.
