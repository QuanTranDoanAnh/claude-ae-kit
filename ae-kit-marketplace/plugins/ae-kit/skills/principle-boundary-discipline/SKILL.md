---
name: principle-boundary-discipline
description: Kiểm tra và chuyển đổi dữ liệu ở biên hệ thống (HTTP, DB, file, API ngoài), tin vào type bên trong, giữ logic nghiệp vụ thuần. Đọc khi viết validation, xử lý lỗi, adapter cho framework hoặc tích hợp hệ thống ngoài.
---

# Kỷ luật biên (Boundary Discipline)

**Khi áp dụng:** handler HTTP, job đọc file/queue, gọi API ngoài, đọc/ghi DB, parse cấu hình.

**Làm gì**
1. Xác định biên: chỗ dữ liệu từ *ngoài* đi vào. Ở đó parse + validate **một lần** thành type nội bộ. Lỗi ở biên → trả lỗi có cấu trúc; không để dữ liệu "có thể sai" lọt vào trong.
2. Bên trong biên: không kiểm tra lại cái đã kiểm; hàm nghiệp vụ nhận type đã hợp lệ, không nhận `string`/`dict` thô.
3. Logic nghiệp vụ không import framework, không gọi I/O trực tiếp — nhận dữ liệu, trả kết quả; I/O ở lớp ngoài. Đây là seam test tốt nhất (xem `references/tdd.md` của next-task).
4. Invariant của `spec/design.md` được ép ở **đúng tầng** design đã ghi (DB constraint / service / UI); không ép hai nơi cùng lúc trừ khi design nói vậy.

**Dấu hiệu vi phạm:** `if (!user) throw` ở 5 hàm liên tiếp; hàm tính tiền nhận `req.body`; validate ở UI nhưng API không.

Nguồn: phỏng theo pstack "Boundary Discipline" (MIT) — xem NOTICE.md.
