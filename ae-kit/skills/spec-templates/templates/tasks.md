# Tasks — {{PROJECT_NAME}}

<!-- Vertical slice, depth-first, mỗi task có done-condition KIỂM CHỨNG ĐƯỢC bằng lệnh.
     Thứ tự = thứ tự phụ thuộc. Logic lõi trước UI.
     Mỗi task BẮT BUỘC có 3 dòng: ↔ (R/I), Done:, Files: — gates.py compute G2 kiểm 3 dòng này.
     Files: danh sách file/thư mục dự kiến đụng (hỗ trợ `dir/` và `prefix*`); approve G5 so với git diff. -->

## Sprint 1 — {{tên sprint}}
- [ ] T1 — {{việc}} (vertical slice: UI → API → DB)  ↔ R1.1, I1
      Done: `{{lệnh}}` pass; {{mô tả bằng chứng}}
      Files: src/api/..., src/db/..., test/...
- [ ] T2 — {{việc}}  ↔ R1.2
      Done: ...
      Files: ...
      Depends: T1

## Sprint 2 — ...

## Backlog (ngoài scope hiện tại — KHÔNG làm nếu chưa được kéo lên)
- ...
