---
name: contract
description: Thương lượng sprint contract cho sprint N — generator đề xuất "done là gì / verify bằng gì", contract-reviewer phản biện, người dùng chốt. Chạy TRƯỚC khi viết dòng code nào của sprint.
disable-model-invocation: true
argument-hint: "<sprint-number>"
allowed-tools: Read Write Glob Grep Agent
---

Sprint `$0` (nếu trống: sprint đầu tiên còn task `[ ]` trong `spec/tasks.md`).

## Bước 1 — Generator đề xuất (chính bạn)
Tạo `spec/sprint-$0.contract.md` từ template sprint-contract. Điền mục "Generator đề xuất":
- Sẽ build gì (theo task của sprint).
- Verify bằng gì: lệnh cụ thể + kỳ vọng cụ thể.
- Giả định đang dựa vào: liệt kê thẳng thắn, kể cả giả định "hiển nhiên".

## Bước 2 — Evaluator phản biện
Gọi subagent `ae-kit:contract-reviewer` lên file contract. Nó sẽ điền mục "Evaluator phản biện" (Thiếu / Cần chốt / Yêu cầu thêm) và đề xuất bảng Chốt dự thảo.

## Bước 3 — Người dùng là trọng tài
Trình bày các mục "Cần chốt" dưới dạng câu hỏi lựa chọn (A/B kèm hệ quả). Chờ người dùng quyết. Ghi quyết định vào bảng "Chốt", đặt ngưỡng cứng cho mọi tiêu chí liên quan invariant. Ghi budget vòng fix (mặc định 3).

Không bắt đầu implement trong lệnh này. Kết thúc: "Contract đã chốt. Chạy `/ae-kit:next-task` để bắt đầu."
