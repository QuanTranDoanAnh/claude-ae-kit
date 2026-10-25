#!/usr/bin/env python3
"""
ae-kit tracker.py — chiếu spec/tasks.md lên issue tracker. spec/tasks.md LÀ nguồn sự thật; issue chỉ là bản chiếu.

Cấu hình: .ae-kit/tracker (dòng 1: none | github; các dòng sau tuỳ chọn `labels: a, b`, `repo: owner/name`).
Chỉ hỗ trợ GitHub qua `gh` CLI (đã đăng nhập). Không phụ thuộc thư viện ngoài.

Lệnh:
  status                 in chế độ tracker và số task đã/chưa có issue
  plan [--sprint N]      dry-run: task nào sẽ tạo / cập nhật / đóng, không gọi gh
  push [--sprint N]      tạo issue cho task chưa có `Issue:`, cập nhật issue của task đã có; ghi `Issue: #n` vào tasks.md
  sync [--sprint N]      đóng issue của task đã [x] (kèm comment link eval nếu có); không mở lại
  link T<x> <n>          gắn tay issue #n cho task T<x> (ghi Issue: vào tasks.md)
Exit code: 0 ok · 1 lỗi cấu hình/file · 3 tracker = none (bỏ qua, không phải lỗi).
Biến môi trường: AE_GH=<lệnh gh thay thế> (để test), CLAUDE_PROJECT_DIR.
"""
import os, re, sys, subprocess, tempfile, json

def _find_root():
    cands = []
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env: cands.append(env)
    cwd = os.getcwd(); cands.append(cwd)
    d = cwd
    for _ in range(4):
        d = os.path.dirname(d)
        if d and d != cands[-1]: cands.append(d)
    for c in cands:
        if os.path.exists(os.path.join(c, "spec", "tasks.md")): return c
    return cwd
ROOT = _find_root()
TASKS = os.path.join(ROOT, "spec", "tasks.md")
CFG = os.path.join(ROOT, ".ae-kit", "tracker")
GH = os.environ.get("AE_GH", "gh").split()

# ---------- cấu hình ----------
def config():
    cfg = {"mode": "none", "labels": ["ae-kit"], "repo": None}
    if not os.path.exists(CFG): return cfg
    lines = [l.strip() for l in open(CFG, encoding="utf-8") if l.strip() and not l.strip().startswith("#")]
    if lines: cfg["mode"] = lines[0].lower()
    for l in lines[1:]:
        k, _, v = l.partition(":")
        if k.strip() == "labels": cfg["labels"] = [x.strip() for x in v.split(",") if x.strip()]
        if k.strip() == "repo": cfg["repo"] = v.strip()
    return cfg

# ---------- đọc tasks.md ----------
def _read(p):
    try: return open(os.path.join(ROOT, p), encoding="utf-8").read()
    except FileNotFoundError: return ""

def req_text():
    """{R1.1: 'WHEN ..., the system SHALL ...'} từ spec/requirements.md"""
    out = {}
    for m in re.finditer(r"^\|\s*([RN]\d+(?:\.\d+)?)\s*\|\s*([^|]*?)\s*\|", _read("spec/requirements.md"), re.M):
        out[m.group(1)] = m.group(2).strip()
    for m in re.finditer(r"^\|\s*(I\d+)\s*\|\s*([^|]*?)\s*\|", _read("spec/design.md"), re.M):
        out[m.group(1)] = m.group(2).strip()
    return out

def parse_tasks(text):
    """Trả về list task theo thứ tự xuất hiện, kèm sprint và vị trí (start, end) của block trong text."""
    tasks, sprint = [], None
    for m in re.finditer(r"^## ([^\n]*)|^- \[([ x])\] (T\d+)[^\n]*(?:\n(?!- \[|## )[^\n]*)*", text, re.M):
        if m.group(1) is not None:
            sm = re.match(r"Sprint (\d+)", m.group(1).strip())
            sprint = int(sm.group(1)) if sm else None  # heading khác (Backlog…) → ngoài sprint
            continue
        if sprint is None: continue  # Backlog hoặc ngoài sprint → bỏ
        blk = m.group(0)
        head = blk.split("\n", 1)[0]
        tid = m.group(3)
        title_m = re.match(r"- \[[ x]\] T\d+\s*[—-]\s*(.*?)\s*(?:↔\s*(.*))?$", head)
        title = (title_m.group(1) if title_m else head).strip()
        refs = re.findall(r"\b[RNI]\d+(?:\.\d+)?\b", title_m.group(2) or "") if title_m else []
        def line(key):
            mm = re.search(rf"^\s+{key}:\s*(.*)$", blk, re.M)
            return mm.group(1).strip() if mm else ""
        issue = re.search(r"#(\d+)", line("Issue"))
        tasks.append({"id": tid, "done": m.group(2) == "x", "title": title, "refs": refs, "sprint": sprint,
                      "done_cmd": line("Done"), "files": line("Files"), "kind": line("Loại") or "feature",
                      "depends": re.findall(r"T\d+", line("Depends")), "issue": int(issue.group(1)) if issue else None,
                      "span": (m.start(), m.end()), "block": blk})
    return tasks

def write_issue_line(text, task, n):
    """Chèn/thay `Issue: #n` vào cuối block của task; trả text mới."""
    blk = task["block"]
    if re.search(r"^\s+Issue:", blk, re.M):
        new = re.sub(r"^(\s+Issue:\s*).*$", rf"\g<1>#{n}", blk, count=1, flags=re.M)
    else:
        indent = re.search(r"^(\s+)\S", blk, re.M)
        pad = indent.group(1) if indent else "      "
        new = blk.rstrip("\n") + f"\n{pad}Issue: #{n}"
    s, e = task["span"]
    return text[:s] + new + text[e:]

# ---------- nội dung issue ----------
def issue_title(t): return f"{t['id']} — {t['title']}"

def issue_body(t, byid, rtext):
    lines = [f"**Sprint {t['sprint']}** · ↔ {', '.join(t['refs']) or '—'} · Loại: `{t['kind']}`", ""]
    for r in t["refs"]:
        if r in rtext: lines.append(f"- **{r}**: {rtext[r]}")
    if any(r in rtext for r in t["refs"]): lines.append("")
    lines += [f"**Done:** {t['done_cmd'] or '—'}", "", f"**Files:** `{t['files'] or '—'}`", ""]
    if t["depends"]:
        deps = []
        for d in t["depends"]:
            dt = byid.get(d)
            deps.append(f"#{dt['issue']} ({d})" if dt and dt.get("issue") else d)
        lines += ["**Blocked by:** " + ", ".join(deps), ""]
    lines += ["---", "Nguồn sự thật: `spec/tasks.md` (ae-kit). Issue này là bản chiếu; đổi task thì sửa tasks.md rồi chạy `/ae-kit:publish`. Trạng thái gate: `spec/gates.yaml`."]
    return "\n".join(lines) + "\n"

# ---------- gh ----------
def gh(args, cfg, check=True):
    cmd = GH + list(args)
    if cfg.get("repo") and args and args[0] in ("issue", "label"): cmd += ["--repo", cfg["repo"]]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.stderr.write(f"gh lỗi: {' '.join(cmd)}\n{r.stderr}\n"); sys.exit(1)
    return r

def ensure_labels(cfg, labels):
    for l in labels:
        gh(["label", "create", l, "--force", "--color", "6f42c1", "--description", "ae-kit"], cfg, check=False)

def _bodyfile(body):
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8"); f.write(body); f.close(); return f.name

# ---------- lệnh ----------
def select(tasks, sprint):
    return [t for t in tasks if sprint is None or t["sprint"] == sprint]

def cmd_status(cfg, tasks, sprint):
    sel = select(tasks, sprint)
    linked = [t for t in sel if t["issue"]]
    print(f"tracker: {cfg['mode']}" + (f" · repo {cfg['repo']}" if cfg["repo"] else "") + f" · labels {','.join(cfg['labels'])}")
    print(f"task: {len(sel)} · có issue: {len(linked)} · chưa: {len(sel) - len(linked)} · done: {sum(1 for t in sel if t['done'])}")
    return 0

def cmd_plan(cfg, tasks, sprint, dry=True):
    sel = select(tasks, sprint)
    byid = {t["id"]: t for t in tasks}
    rtext = req_text()
    create = [t for t in sel if not t["issue"]]
    update = [t for t in sel if t["issue"]]
    close = [t for t in sel if t["issue"] and t["done"]]
    print(f"plan (sprint {sprint if sprint else 'tất cả'}): tạo {len(create)} · cập nhật {len(update)} · sẽ đóng khi sync {len(close)}")
    for t in create: print(f"  + {issue_title(t)}  [{', '.join(cfg['labels'])}, sprint-{t['sprint']}]" + (f"  blocked by {', '.join(t['depends'])}" if t["depends"] else ""))
    for t in update: print(f"  ~ #{t['issue']} {issue_title(t)}")
    for t in close: print(f"  x #{t['issue']} {t['id']} (đã [x])")
    if dry and create:
        print("\n--- body mẫu (" + create[0]["id"] + ") ---"); print(issue_body(create[0], byid, rtext))
    return 0

def cmd_push(cfg, tasks, sprint):
    if cfg["mode"] != "github": print("tracker = none — bỏ qua. Bật: `echo github > .ae-kit/tracker` (cần `gh auth login`)."); return 3
    sel = select(tasks, sprint)
    byid = {t["id"]: t for t in tasks}
    rtext = req_text()
    sprints = sorted({t["sprint"] for t in sel})
    ensure_labels(cfg, cfg["labels"] + [f"sprint-{s}" for s in sprints])
    text = open(TASKS, encoding="utf-8").read()
    created = updated = 0
    # tạo theo thứ tự phụ thuộc (blocker trước) để Blocked by có số issue thật
    for t in sel:
        labels = []
        for l in cfg["labels"] + [f"sprint-{t['sprint']}"]: labels += ["--label", l]
        if t["issue"]:
            bf = _bodyfile(issue_body(t, byid, rtext))
            gh(["issue", "edit", str(t["issue"]), "--title", issue_title(t), "--body-file", bf], cfg); os.unlink(bf)
            updated += 1
        else:
            bf = _bodyfile(issue_body(t, byid, rtext))
            r = gh(["issue", "create", "--title", issue_title(t), "--body-file", bf] + labels, cfg); os.unlink(bf)
            m = re.search(r"/issues/(\d+)\s*$", r.stdout.strip()) or re.search(r"#(\d+)", r.stdout)
            if not m: sys.stderr.write(f"không đọc được số issue từ output gh: {r.stdout!r}\n"); sys.exit(1)
            n = int(m.group(1)); t["issue"] = n; created += 1
            # ghi ngay vào tasks.md (parse lại span vì text đã đổi)
            tasks_now = parse_tasks(text); tn = next(x for x in tasks_now if x["id"] == t["id"])
            text = write_issue_line(text, tn, n)
            open(TASKS, "w", encoding="utf-8").write(text)
    # vòng 2: task vừa tạo có thể là blocker của task tạo trước nó → cập nhật body cho đủ số issue
    tasks2 = parse_tasks(open(TASKS, encoding="utf-8").read()); byid2 = {t["id"]: t for t in tasks2}
    for t in select(tasks2, sprint):
        if t["depends"] and t["issue"]:
            bf = _bodyfile(issue_body(t, byid2, rtext)); gh(["issue", "edit", str(t["issue"]), "--body-file", bf], cfg); os.unlink(bf)
    print(f"push: tạo {created} · cập nhật {updated} · Issue: đã ghi vào spec/tasks.md")
    return 0

def cmd_sync(cfg, tasks, sprint):
    if cfg["mode"] != "github": print("tracker = none — bỏ qua."); return 3
    sel = [t for t in select(tasks, sprint) if t["issue"] and t["done"]]
    ev = None
    if sprint:
        import glob
        fs = sorted(glob.glob(os.path.join(ROOT, "spec", f"eval-sprint-{sprint}-r*.md")))
        fs = [f for f in fs if not re.search(r"-p\d+\.md$", f)]
        if fs: ev = os.path.relpath(fs[-1], ROOT)
    n = 0
    for t in sel:
        r = gh(["issue", "view", str(t["issue"]), "--json", "state"], cfg, check=False)
        try: state = json.loads(r.stdout).get("state", "")
        except Exception: state = ""
        if state.upper() == "CLOSED": continue
        comment = f"{t['id']} đã [x] trong spec/tasks.md" + (f" · evaluation: `{ev}`" if ev else "")
        gh(["issue", "close", str(t["issue"]), "--comment", comment], cfg); n += 1
    print(f"sync: đóng {n} issue" + (f" (sprint {sprint})" if sprint else ""))
    return 0

def cmd_link(cfg, tasks, tid, n):
    t = next((x for x in tasks if x["id"] == tid), None)
    if not t: print(f"không có task {tid}"); return 1
    text = open(TASKS, encoding="utf-8").read()
    open(TASKS, "w", encoding="utf-8").write(write_issue_line(text, t, int(n)))
    print(f"{tid} ↔ #{n}"); return 0

def main(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return 0
    cmd, args = argv[0], argv[1:]
    sprint = None
    if "--sprint" in args:
        i = args.index("--sprint"); sprint = int(args[i + 1]); del args[i:i + 2]
    if not os.path.exists(TASKS): sys.stderr.write(f"không có {TASKS} — chạy /ae-kit:plan trước.\n"); return 1
    cfg = config(); tasks = parse_tasks(open(TASKS, encoding="utf-8").read())
    if cmd == "status": return cmd_status(cfg, tasks, sprint)
    if cmd == "plan": return cmd_plan(cfg, tasks, sprint)
    if cmd == "push": return cmd_push(cfg, tasks, sprint)
    if cmd == "sync": return cmd_sync(cfg, tasks, sprint)
    if cmd == "link": return cmd_link(cfg, tasks, args[0], args[1])
    print(f"lệnh không biết: {cmd}"); return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
