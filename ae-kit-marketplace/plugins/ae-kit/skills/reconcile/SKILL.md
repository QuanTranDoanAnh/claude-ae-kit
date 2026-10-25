---
name: reconcile
description: Đối chiếu chéo mọi spec/discovery-*.md (T transcript, F tài liệu, C codebase) thành spec/claims.md — mỗi claim ghi nguồn nào nói, trùng khớp (corroborated) / một nguồn (single) / mâu thuẫn (conflict). Mâu thuẫn → câu hỏi theo vòng frontier với đề xuất theo precedence (sources.py), người quyết. Bắt buộc khi có ≥2 nguồn, chạy trước /ae-kit:specify và chạy lại mỗi khi có nguồn mới. Không viết requirement.
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash(bash *)
---

`$S` = `bash "${CLAUDE_PLUGIN_ROOT}/scripts/py" "${CLAUDE_PLUGIN_ROOT}/scripts/sources.py"` · `$G` = `… scripts/gates.py`. Template `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/templates/claims.md`. Cách hỏi: `${CLAUDE_PLUGIN_ROOT}/skills/spec-templates/references/grilling.md`.

## Vì sao có bước này
Transcript, SRS khách gửi, ghi chú, và codebase cũ hiếm khi đồng ý với nhau; chỗ chúng mâu thuẫn chính là chỗ khách **chưa nghĩ kỹ** — và là câu hỏi đáng giá nhất. Specify không được tự chọn phe; reconcile làm lộ mâu thuẫn, đề xuất theo thứ tự ưu tiên của nguồn, và để người quyết. Claim là **mô tả trung lập**, chưa phải requirement.

## Điều kiện vào
1. `$S check` phải OK (mọi nguồn đã intake có metadata). Thiếu → DỪNG, in lệnh `sources.py set …` cần chạy.
2. ≥ 2 file `spec/discovery-*.md`. Chỉ 1 → DỪNG: "không cần reconcile; `/ae-kit:specify`".

## Các bước
1. Đọc `intake/sources.yaml` và `$S precedence` (thứ tự ưu tiên đề xuất). Đọc toàn bộ `spec/discovery-*.md`. Nếu `spec/claims.md` đã có: giữ nguyên mã CL và mọi dòng đã có **Giải quyết**; chỉ thêm/sửa cho nguồn mới hoặc statement mới (ghi `(updated from <ID>)`).
2. **Gom claim.** Với mỗi statement S (T/F) loại goal / constraint / out-of-scope, và mỗi O (C) nhãn `decided`/`debt`/`?` loại rule/documented/debt (bỏ `ignore`): tìm statement/O ở nguồn khác nói về **cùng một điều**. Một claim = một câu trung lập (không "SHALL", không giải pháp, không gộp hai điều). Cột Nguồn ghi mã + vị trí: `T1 S3 (§14); F1 S7 (§3.2 FR-012); C1 O4`. **Mọi S loại goal/constraint/out-of-scope phải thuộc ≥1 claim** (G1 đếm); pain/example chỉ gắn nếu làm rõ claim.
3. **Phân loại:**
   - `corroborated` — ≥2 nguồn độc lập đồng ý (F2 thay thế F1 không tính là 2 nguồn).
   - `single` — một nguồn. Nếu nguồn đó `trust` ≠ high hoặc authority ≠ decision-maker → cột Đề xuất: "hỏi khách xác nhận → Q<n>" (Q sẽ thêm ở bước 5). Nguồn trust high → Đề xuất để trống.
   - `conflict` — nguồn nói ngược nhau (có/không, số khác nhau, phạm vi khác nhau, cùng từ khác nghĩa). Cột Đề xuất: nguồn thắng theo precedence + lý do một câu ("T2 §9 thắng: mới hơn, decision-maker"). Codebase (C) nói ngược lời khách → vẫn là conflict (code cũ có thể là tai nạn lịch sử), đề xuất theo precedence (C xếp sau).
   - Nguồn F ghi `note: superseded by F<k>` → S của nó chỉ dùng để phát hiện điều **bị bỏ** giữa hai phiên bản (→ conflict F1 ⟂ F2, đề xuất F2 thắng).
4. **Thuật ngữ lệch nghĩa** giữa glossary của các discovery → bảng riêng, đề xuất tách/thống nhất. **Khoảng trống chung** = giao của các mục "KHÔNG nói" → mỗi dòng chưa có Q nào → thêm Q vào discovery của nguồn **mới nhất** (bảng Open Questions, Nhãn trống).
5. Ghi `spec/claims.md` (dòng `Nguồn đã đối chiếu:` liệt kê **mọi** ID discovery). Với mỗi conflict và mỗi single cần xác nhận → thêm một Q vào `spec/discovery-<nguồn mới nhất>.md` (chỉ `Edit` bảng Open Questions; Q ghi "CL<n>" trong cột Vì sao quan trọng; A<n> = Đề xuất của claim).
6. **Vòng hỏi** (grilling.md §3) — frontier = claim conflict chưa Giải quyết, rồi single cần xác nhận; tối đa 7/vòng, conflict trước. Mỗi mục: hai (hoặc nhiều) phía trích nguyên văn kèm nguồn/ngày/authority, `➡️ Đề xuất:` theo precedence, `yes` = chấp nhận. Người trả lời → ghi cột **Giải quyết** của claims.md (`"<nguồn> thắng (người quyết <ngày>: <lý do>)"` · `send Q<n> (discovery-<ID>)` · `defer`) **và** cột Nhãn của Q tương ứng trong discovery theo grilling.md §4. Chỉ reconcile ghi cột Giải quyết; conflict `send` coi như giải quyết tạm bằng A mặc định cho tới khi transcript trả lời về (intake T<n+1> sẽ nhắc chạy lại reconcile).
7. Dừng khi frontier rỗng hoặc người dừng. Conflict chưa Giải quyết vẫn nằm trong file; G1 đếm (`claims_reconciled`).

## Không được
- Không viết `spec/requirements.md`, không sửa Statements/O, không tự điền Giải quyết (kể cả khi precedence "rõ ràng" — ngày tháng không phải thẩm quyền).
- Không xoá claim; claim bị khách rút lại → conflict đã giải quyết, specify sẽ đưa vào Non-goals.
- Không gộp nhiều điều vào một claim để giảm conflict.

## Kết thúc
1. Chạy `$G compute G1` (chỉ để ghi `sources_registered` / `claims_reconciled`; các ô khác sẽ đỏ cho tới lint) — dán output.
2. Tóm tắt: số claim theo trạng thái, số conflict đã/chưa giải quyết, Q `send` mới sinh (sẵn sàng gửi khách), thuật ngữ lệch nghĩa.
3. Bước tiếp theo: conflict chưa giải quyết → gửi Q cho khách rồi `/ae-kit:intake T<n+1>` và chạy lại `/ae-kit:reconcile`; hết conflict → `/ae-kit:specify` (lần đầu) hoặc `/ae-kit:specify` + `/ae-kit:lint-spec` lại (requirements đã có và nguồn mới đổi claim).
