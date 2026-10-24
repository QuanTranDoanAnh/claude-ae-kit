---
name: spec-templates
description: Bộ template artifact của quy trình ae-kit (CLAUDE.md constitution tầng luật, docs/product tầng context, gates.yaml, discovery T/C, requirements EARS, design, tasks, sprint-contract, progress, eval-report). Các skill khác tham chiếu tới đây; không gọi trực tiếp.
user-invocable: false
---

Các template nằm trong `${CLAUDE_SKILL_DIR}/templates/`:

| File | Dùng ở bước | Ghi vào project | Tầng |
|------|-------------|-----------------|------|
| CLAUDE.md | init | `CLAUDE.md` | luật (≤ 40 dòng, chỉ ratchet sửa) |
| mission.md, tech.md, roadmap.md | init / replan | `docs/product/*.md` | product context (replan sửa) |
| gates.yaml | init | `spec/gates.yaml` | trạng thái gate (chỉ `scripts/gates.py` ghi) |
| discovery.md | intake T<n> | `spec/discovery-T<n>.md` | spec |
| discovery-codebase.md | intake C<n> (brownfield) | `spec/discovery-C<n>.md` | spec |
| requirements.md | specify | `spec/requirements.md` | spec |
| design.md | design | `spec/design.md` | spec |
| tasks.md | plan | `spec/tasks.md` | spec |
| sprint-contract.md | contract | `spec/sprint-<N>.contract.md` | spec |
| progress.md | init / next-task | `spec/progress.md` | handoff |
| eval-report.md | evaluate | `spec/eval-sprint-<N>-r<k>.md` | spec |

Quy ước chung của mọi artifact:
- Placeholder dạng `{{NAME}}` phải được thay hết; không để sót.
- Mọi requirement mang tag nguồn gốc `[src: T<n> §<m>]`, `[src: A<n>]` hoặc `[src: C<n> O<m>]`.
- Mọi dòng luật trong CLAUDE.md kết thúc bằng `[<nguồn>]`: `[harness]`, `[ratchet #n]`, `[N<n>]`, `[I<n>]`, `[C<n> O<m>]`.
- Artifact là file trong repo, không phải nội dung chat. Luôn ghi file rồi mới tóm tắt.
- Trạng thái gate chỉ đổi qua `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gates.py" ...`, không sửa `gates.yaml` tay.
