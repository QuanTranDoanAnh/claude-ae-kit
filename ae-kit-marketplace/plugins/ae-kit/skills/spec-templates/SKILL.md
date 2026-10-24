---
name: spec-templates
description: Bộ template artifact của quy trình ae-kit (CLAUDE.md constitution, discovery, requirements EARS, design, tasks, sprint-contract, progress, eval-report). Các skill khác tham chiếu tới đây; không gọi trực tiếp.
user-invocable: false
---

Các template nằm trong `${CLAUDE_SKILL_DIR}/templates/`:

| File | Dùng ở bước | Ghi vào project |
|------|-------------|-----------------|
| CLAUDE.md | init | `CLAUDE.md` |
| discovery.md | intake | `spec/discovery-T<n>.md` |
| requirements.md | specify | `spec/requirements.md` |
| design.md | design | `spec/design.md` |
| tasks.md | plan | `spec/tasks.md` |
| sprint-contract.md | contract | `spec/sprint-<N>.contract.md` |
| progress.md | init / next-task | `spec/progress.md` |
| eval-report.md | evaluate | `spec/eval-sprint-<N>-r<k>.md` |

Quy ước chung của mọi artifact:
- Placeholder dạng `{{NAME}}` phải được thay hết; không để sót.
- Mọi requirement mang tag nguồn gốc `[src: T<n> §<m>]` hoặc `[src: A<n>]`.
- Artifact là file trong repo, không phải nội dung chat. Luôn ghi file rồi mới tóm tắt.
