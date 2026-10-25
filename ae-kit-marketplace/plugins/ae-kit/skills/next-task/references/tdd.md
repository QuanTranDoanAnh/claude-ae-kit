# Quy tắc test trong ae-kit (red → green tại seam đã chốt)

**Seam** = bề mặt công khai mà test quan sát hành vi, không chạm bên trong. Seam của sprint được chốt ở G3 (cột Seam, bảng Chốt của `spec/sprint-N.contract.md`). Ưu tiên seam cao nhất còn chạy được trong CI; càng ít seam càng tốt. Seam mới → quyết định của người ở contract, không phải của next-task.

**Vòng lặp**
1. Red trước green: test fail trước vì *thiếu hành vi*, không phải vì lỗi cú pháp/import.
2. Một slice một lần: một seam, một test, một cài đặt tối thiểu. Không viết sẵn 10 test rồi code một lượt (test hàng loạt mô tả hành vi tưởng tượng).
3. Refactor không nằm trong vòng red–green; nó là bước dọn cuối task (feature) hoặc là task `Loại: refactor`.

**Test tốt**
- Tên test = một dòng spec kèm mã R/I: `"từ chối đặt lịch trùng slot (R2.3)"`.
- Khẳng định điều người dùng của code thấy; đổi cài đặt bên trong không làm vỡ test.
- Giá trị kỳ vọng từ nguồn độc lập (spec, ví dụ khách, tính tay) — không tính lại bằng công thức của code.
- Mock chỉ ở biên ngoài hệ thống (API bên thứ ba, đồng hồ, random, mạng). Không mock collaborator nội bộ.
- Thử biên: `=`, `±1`, rỗng, trùng, song song, timezone/DST, unicode, dữ liệu lớn — đúng như evaluator (G4) sẽ thử.

**Cấm**
- Comment-out hoặc skip test để pass. Sửa hoặc xoá có lý do ghi trong progress.md.
- Test tautology (`expect(f(a)).toBe(f(a))`), snapshot không ai đọc, `toHaveBeenCalledWith` lên hàm nội bộ.
- Test ở seam chưa chốt.

Phỏng theo skill `tdd` của mattpocock/skills (MIT) và pstack "Test Behavior, Not Implementation"; xem NOTICE.md.
