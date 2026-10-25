---
name: principle-attack-the-premise
description: Hai lần sửa liên tiếp cùng dựa trên một giả thuyết đều thất bại → giả thuyết sai; viết nó ra và kiểm tra trực tiếp trước khi sửa lần ba. Đọc khi evaluator FAIL cùng tiêu chí ≥ 2 vòng, hoặc Done: fail ≥ 2 lượt cùng cách.
---

# Tấn công tiền đề (Attack the Premise)

**Khi áp dụng:** vòng fix thứ 2 trở đi cho cùng tiêu chí (G4 retries), hoặc lượt chạy `Done:` thứ 3 fail cùng một cách.

**Làm gì**
1. DỪNG sửa. Viết vào `spec/progress.md`: "Hai fix vừa rồi cùng giả định: <tiền đề>."
2. Thiết kế một kiểm tra *trực tiếp* cho tiền đề (log giá trị, test tối giản, chạy lệnh cô lập). Không phải một fix nữa.
3. Tiền đề sai → fix mới phải xuất phát từ quan sát mới, ghi rõ. Tiền đề đúng → vấn đề nằm ở chỗ khác; mở rộng chuỗi lần ngược (principle-fix-root-causes).
4. Sắp hết budget retry (`gates.py get G4_evidence.retries`) mà tiền đề chưa rõ → ghi "Câu hỏi cần người quyết" ngay, đừng đốt retry cuối.

**Dấu hiệu vi phạm:** "thử thêm một cách nữa"; đổi tham số ngẫu nhiên; sửa test cho khớp code.

Nguồn: phỏng theo pstack "Attack the Premise" (MIT) — xem NOTICE.md.
