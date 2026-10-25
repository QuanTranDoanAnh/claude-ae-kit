# Prototype approval — P{{V}}

<!-- Bản ghi khách duyệt prototype. gates.py compute GP đọc 3 dòng đầu (đúng chính tả). Buổi duyệt PHẢI được ghi thành transcript
     intake/T<n>-transcript.md và chạy /ae-kit:intake T<n> — mọi điều khách nói tại đó có [src: T<n> §m] như bình thường. -->

Prototype: P{{V}}
Transcript: T{{N}}
Xác nhận mô hình: yes   <!-- khách đã được nói rõ: đây là mô hình để chốt yêu cầu, không phải phần mềm; tiến độ thật tính theo sprint -->

Ngày: {{DATE}} · Người duyệt (phía khách): {{CUSTOMER}} · Ghi nhận (phía mình): {{CONSULTANT}}
Commit/hash của P{{V}}: {{HASH}}

## Màn hình đã duyệt
| S | Kết luận | Ghi chú của khách (→ T{{N}} §) |
|---|----------|--------------------------------|
| S1 | duyệt / duyệt có sửa / làm lại | §4 |

## Điều khách yêu cầu THÊM tại buổi demo (không đưa thẳng vào prototype — đi qua intake → Q/R)
- (ghi §m; intake T{{N}} sẽ tạo Q/S tương ứng)

## Điều kiện duyệt
- Mọi S trong "Luồng task đầu" của screens.md: duyệt hoặc duyệt có sửa.
- "Làm lại" bất kỳ S nào trong luồng đầu → chưa duyệt; dựng P{{V}}+1 rồi demo lại.
