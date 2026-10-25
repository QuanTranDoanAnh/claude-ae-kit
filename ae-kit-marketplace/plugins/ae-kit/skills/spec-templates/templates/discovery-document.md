# Discovery — {{SOURCE_ID}} (tài liệu: {{DOC_TYPE}})

Nguồn: `intake/{{SOURCE_ID}}-{{SLUG}}.{{EXT}}` (bản trích: `intake/{{SOURCE_ID}}-{{SLUG}}.extracted.md`) · tác giả/nguồn: {{AUTHOR}} · ngày tài liệu: {{DOC_DATE}} · origin: {{ORIGIN}} · authority: {{AUTHORITY}} · trust: {{TRUST}}
<!-- Metadata trên PHẢI khớp intake/sources.yaml (scripts/sources.py). Tài liệu là BẰNG CHỨNG về điều ai đó đã viết,
     không phải sự thật về điều khách muốn hôm nay: SRS/BRD khách tự viết thường là wishlist, có thể lỗi thời, có thể
     do người không có thẩm quyền viết. Agent chỉ TRÍCH và HỎI — không "nâng cấp" câu trong SRS thành requirement. -->

## 0. Cấu trúc tài liệu (mục nào có, mục nào trống / TBD)
<!-- Liệt kê heading cấp 1–2 của tài liệu với số dòng/số statement trích được. Mục có tiêu đề nhưng rỗng, "TBD", "sẽ bổ sung"
     → một Q ở mục 3 (khoảng trống đã được chính tài liệu thừa nhận). -->
| § | Tiêu đề | Số statement | Ghi chú (trống / TBD / chỉ có tiêu đề) |
|---|---------|--------------|-----------------------------------------|

## 1. Statements (tài liệu nói gì — trích dẫn, không diễn giải)
<!-- Mỗi statement: mã S<n>, đoạn trích ngắn sát nghĩa, vị trí (§ của tài liệu + mã riêng nếu có, ví dụ "§3.2 FR-012"; PDF: trang).
     Câu đã ở dạng "shall/phải" trong SRS vẫn là STATEMENT (claim của tác giả), chưa phải R của dự án.
     Loại: goal / constraint / pain / example / out-of-scope. Ghi chú rời rạc (notes) không có chủ ngữ → trích nguyên văn, mơ hồ → Q. -->
| ID | Trích dẫn / diễn đạt sát nghĩa | Vị trí | Loại |
|----|-------------------------------|--------|------|
| S1 | ... | §3.2 FR-012 | goal / constraint / pain / example / out-of-scope |

## 2. Thuật ngữ trong tài liệu (glossary nháp)
<!-- Giữ nghĩa tài liệu dùng, kể cả khi khác với transcript — reconcile sẽ so. -->
| Thuật ngữ | Tài liệu dùng theo nghĩa | Vị trí |
|-----------|--------------------------|--------|

## 3. Open Questions (BẮT BUỘC)
<!-- Nguồn Q của tài liệu: mục trống/TBD (mục 0) · câu mơ hồ / ≥2 cách hiểu · câu "shall" không kiểm chứng được ·
     điều chỉ tài liệu nói mà chưa ai xác nhận bằng lời (sẽ là claim `single` khi reconcile — hỏi khách xác nhận nếu trust ≠ high).
     Cột Nhãn do NGƯỜI điền trước gate 1: send · assume · defer · prototype. gates.py compute G1 đếm Q chưa nhãn. -->
| ID | Câu hỏi cho khách | Vì sao quan trọng | Giả định mặc định nếu không có câu trả lời | Sau Q | Nhãn |
|----|-------------------|-------------------|--------------------------------------------|-------|------|
| Q1 | ... | ... | A1: ... | | |

## 4. Mâu thuẫn / mơ hồ NỘI BỘ tài liệu
<!-- Hai chỗ trong cùng tài liệu nói ngược nhau (mục tiêu §1 vs FR §3), hoặc bảng vs văn bản. Mâu thuẫn với nguồn KHÁC → spec/claims.md (reconcile). -->

## 5. Những gì tài liệu KHÔNG nói
<!-- Checklist tối thiểu — đăng nhập/phân quyền, dữ liệu cũ/migration, đa ngôn ngữ, mobile, hiệu năng/khối lượng, audit/log,
     tích hợp hệ thống khác, ai vận hành, ngân sách/thời hạn — và: AI ĐÃ VIẾT tài liệu này, ngày nào, đã được khách chốt chưa. -->
