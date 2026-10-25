# Playbook: bugfix

Mục tiêu: lỗi không tái hiện được nữa, có test regression mang tên lỗi, và nguyên nhân gốc được sửa ở nơi nó phát sinh (`ae-kit:principle-fix-root-causes`).

1. **Tái hiện trước khi sửa.** Viết test (tại seam đã chốt) hoặc script tái hiện đúng lỗi như mô tả trong task/R. Chạy — phải FAIL theo đúng cách lỗi mô tả. Không tái hiện được → DỪNG, ghi "Câu hỏi cần người quyết": điều kiện nào còn thiếu (dữ liệu, môi trường, trình tự).
2. **Lần ngược chuỗi**: triệu chứng ← hàm ← dữ liệu/trạng thái sai ← nơi tạo ra nó. Ghi chuỗi vào progress.md. Dùng Grep/Read có chủ đích; không đọc cả repo.
3. **Kiểm tra guard định thêm**: trạng thái mà guard xử lý có hợp lệ theo `spec/design.md` không? Không hợp lệ → sửa nơi tạo ra nó (hoặc ép invariant ở biên theo `ae-kit:principle-boundary-discipline`), không chỉ chặn ở nơi nhận.
4. **Sửa ở mắt xích đầu tiên** sai. Một fix cho một nguyên nhân; thấy phải sửa hai chỗ → nghi ngờ chuỗi lần ngược chưa đủ sâu.
5. Chạy lại test tái hiện: FAIL → PASS. Chạy bộ test đầy đủ (lệnh trong `docs/product/tech.md` "Test đầy đủ") để chắc không vỡ chỗ khác.
6. Fix lần 2 cho cùng lỗi vẫn fail → DỪNG, đọc `ae-kit:principle-attack-the-premise`, viết tiền đề ra và kiểm trực tiếp trước khi sửa lần 3.
7. **Chứng minh**: `Done:` pass; dán output. Đổi tên test regression theo lỗi (`<module>.<lỗi>.test.*`).
8. Lỗi do agent không biết quy ước / do thiếu invariant / do thiếu check cơ học → thêm dòng vào "Đề xuất ratchet" trong progress.md (nêu mức dự kiến: CLAUDE.md / test / hook / trigger principle).

Spec: bugfix thường KHÔNG đổi spec. Nếu lỗi là do spec sai → không sửa code cho khớp spec sai; ghi "Câu hỏi cần người quyết" và dừng.
