# Playbook: refactor

Mục tiêu: cấu trúc đổi, hành vi quan sát được KHÔNG đổi, bộ kiểm tra xanh ở mọi commit (`ae-kit:principle-sequence-verifiable-units`, `ae-kit:principle-laziness-protocol`).

1. **Mốc xanh**: chạy `.ae-kit/check.cmd` và test đầy đủ TRƯỚC khi sửa. Đỏ sẵn → DỪNG, báo người (refactor trên nền đỏ không chứng minh được gì); hoặc task phải đổi thành bugfix.
2. **Khoá hành vi**: các tiêu chí trong bảng Chốt của contract cho task này phải có test tại seam đã chốt. Thiếu test cho hành vi sắp bị đụng → viết test đặc tả hành vi HIỆN TẠI trước (test phải PASS trên code cũ), rồi mới refactor.
3. **Xoá trước, thêm sau**: code chết, wrapper một nơi gọi, tham số không dùng. Mỗi lần xoá → chạy kiểm tra → commit.
4. **Đổi rộng** (đổi tên symbol/cột dùng khắp nơi) → expand → migrate theo lô (theo thư mục/package) → contract (xoá dạng cũ). Mỗi lô một commit, xanh giữa các lô.
5. Mỗi bước: sửa → kiểm tra → commit `T<x> (bước k/n): <bước>`. Bước fail → quay về commit trước; không chồng fix lên đỏ.
6. **Không** đổi hành vi, không thêm feature, không sửa test để "cho khớp" (test vỡ mà hành vi không đổi → test gắn với cài đặt, sửa test theo `ae-kit:principle-test-behavior-not-implementation` và ghi vào progress.md).
7. **Chứng minh**: `Done:` pass; test đầy đủ xanh; diff chỉ trong `Files:`.

Spec: refactor KHÔNG được làm đổi `spec/requirements.md`/`design.md`. Ở G5, câu "không đổi hành vi?" trả lời "có" là mong đợi; nếu bạn thấy cần đổi spec, task này không còn là refactor → dừng và hỏi.
