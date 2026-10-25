---
name: principle-test-behavior-not-implementation
description: Test khẳng định điều người dùng của code quan sát được qua seam công khai, để test fail khi hành vi hỏng và vẫn pass khi chỉ đổi bên trong. Đọc khi viết, sửa hoặc xoá bất kỳ test nào, và khi chọn seam trong sprint contract.
---

# Test hành vi, không test cài đặt

**Khi áp dụng:** mọi lần chạm vào test; bước Seam của `/ae-kit:contract`; khi muốn mock.

**Làm gì**
1. Chọn **seam**: bề mặt công khai cao nhất mà vẫn chạy được trong CI (API → service → hàm thuần). Seam đã ghi trong bảng Chốt của contract là seam phải dùng; cần seam khác → hỏi người, không tự mở.
2. Tên test đọc như một dòng spec: `"từ chối đặt lịch trùng slot (R2.3)"`, không phải `"gọi repo.save một lần"`.
3. Giá trị kỳ vọng đến từ nguồn độc lập (spec, ví dụ khách đưa, số tính tay), không tính lại bằng cùng công thức với code.
4. Mock chỉ ở biên ngoài hệ thống (API bên thứ ba, đồng hồ, random). Không mock collaborator nội bộ.
5. Test bị refactor làm vỡ nhưng hành vi không đổi → test sai, sửa test; hành vi đổi mà test không vỡ → thiếu test.

**Dấu hiệu vi phạm:** `expect(fn).toHaveBeenCalledWith(...)` cho hàm nội bộ; snapshot không ai đọc; `expect(add(a,b)).toBe(a+b)`.

Nguồn: phỏng theo pstack "Test Behavior, Not Implementation" và skill `tdd` của mattpocock/skills (MIT) — xem NOTICE.md.
