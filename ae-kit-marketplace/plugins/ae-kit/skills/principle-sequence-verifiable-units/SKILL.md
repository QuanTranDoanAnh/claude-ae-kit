---
name: principle-sequence-verifiable-units
description: Chia việc nhiều bước (migration, sửa hàng loạt, refactor rộng) thành các đơn vị nhỏ, mỗi đơn vị kết thúc bằng một kiểm tra chạy được và một commit, theo thứ tự tự chứng minh. Đọc trong playbook refactor, task phase 0 (debt), và khi một task đụng > 5 file.
---

# Xếp việc thành đơn vị kiểm chứng được

**Khi áp dụng:** `Loại: refactor`; task debt phase 0; task có `Files:` dài; migration dữ liệu.

**Làm gì**
1. Trước khi sửa: chạy bộ kiểm tra (`.ae-kit/check.cmd` + test đầy đủ) và ghi kết quả làm **mốc xanh**.
2. Chia thành các bước mà *sau mỗi bước* mốc vẫn xanh. Không được có bước "giữa chừng mọi thứ đỏ".
3. Đổi rộng (đổi tên cột, đổi kiểu một symbol dùng khắp nơi) → **expand → migrate theo lô → contract**: thêm dạng mới cạnh dạng cũ; chuyển caller từng lô theo blast radius; xoá dạng cũ khi không còn caller. Mỗi lô một commit.
4. Mỗi bước: sửa → chạy kiểm tra → commit với message nêu bước. Bước fail → quay về commit trước, không chồng fix lên đỏ.
5. Thứ tự giao nộp phải để người review đọc commit theo thứ tự mà thấy nó tự chứng minh.

**Dấu hiệu vi phạm:** một commit 40 file; "sẽ fix test sau"; API cũ và mới cùng sống vô thời hạn (quên bước contract).

Nguồn: phỏng theo pstack "Sequence Work into Verifiable Units" và quy tắc expand–contract trong `to-tickets` của mattpocock/skills (MIT) — xem NOTICE.md.
