#!/usr/bin/env python3
"""
ae-kit gates.py — logic quality gate TẤT ĐỊNH (không để LLM tự sửa YAML).

File trạng thái: spec/gates.yaml (schema cố định, xem template). Không phụ thuộc PyYAML:
parser tối giản cho YAML dạng key/value lồng nhau + list inline `[a, b]`.

Lệnh:
  show                         in checklist 5 gate (dùng bởi /ae-kit:status và hook SessionStart)
  short                        in 1 dòng: G1 ✓  G2 ✗  G3 ·  G4 ·  G5 ·
  get <path>                   ví dụ: get G1_spec.status
  set <path> <value>           value: true|false|null|<số>|<chuỗi>  (chỉ cho skill ghi ô máy)
  incr <path>                  tăng số (rounds, retries); tự chuyển blocked khi vượt max_*
  compute G1|GP|G2|G4|G5       tính lại ô máy từ artifact thật và ghi vào gates.yaml
  approve G1|GP|G2|G5 <who> [--force "<lý do>"]
                               duyệt tay; từ chối nếu còn ô máy chưa true (trừ --force)
  pass G3|G4                   đặt gate máy sang passed (sau khi mọi ô true) — gọi từ contract/evaluate
  panel [N] [k]                tổng hợp TẤT ĐỊNH các báo cáo evaluator của panel đa model
                               (spec/eval-sprint-N-r<k>-p<i>.md) thành spec/eval-sprint-N-r<k>.md,
                               tính Verdict theo G4_evidence.panel.min_agree, ghi checks.panel_agree
  next                         in đúng một lệnh /ae-kit:... nên chạy tiếp
  new-sprint                   current_sprint += 1, reset G3/G4/G5
Gate GP (Prototype, khách duyệt) nằm giữa G1 và G2; dự án không có UI: `set GP_prototype.status n/a`.
Exit code: 0 ok · 1 lỗi tham số/file · 2 gate không đạt (để skill dừng).
"""
import os, re, sys, glob, subprocess, datetime, json

def _find_root():
    """Thứ tự: CLAUDE_PROJECT_DIR → cwd → cha của cwd (tối đa 4 cấp); chọn nơi đầu tiên có spec/gates.yaml,
    nếu không có thì cwd (để init tạo mới ở đúng chỗ người đang đứng)."""
    cands = []
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env: cands.append(env)
    cwd = os.getcwd(); cands.append(cwd)
    d = cwd
    for _ in range(4):
        d = os.path.dirname(d)
        if d and d != cands[-1]: cands.append(d)
    for c in cands:
        if os.path.exists(os.path.join(c, "spec", "gates.yaml")): return c
    return cwd
ROOT = _find_root()
GATES = os.path.join(ROOT, "spec", "gates.yaml")
ORDER = ["G1_spec", "GP_prototype", "G2_plan", "G3_contract", "G4_evidence", "G5_merge"]
HUMAN = {"G1_spec", "GP_prototype", "G2_plan", "G5_merge"}

def _status(d, g):
    """Trạng thái gate; GP thiếu trong gates.yaml cũ (v0.3) → n/a. n/a được coi là đã qua khi xét thứ tự."""
    if g not in d: return "n/a" if g == "GP_prototype" else "pending"
    return d.get(g, {}).get("status", "pending")

def _ok_prev(d, g):
    return _status(d, g) in ("passed", "n/a")

# ---------- YAML tối giản ----------
def _scalar(s):
    s = s.strip()
    if s == "" or s == "null" or s == "~": return None
    if s == "true": return True
    if s == "false": return False
    if re.fullmatch(r"-?\d+", s): return int(s)
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [] if not inner else [_scalar(x) for x in _split_list(inner)]
    if (s[0] == s[-1]) and s[0] in "\"'": return s[1:-1]
    return s

def _split_list(inner):
    out, cur, q = [], "", None
    for ch in inner:
        if q:
            cur += ch
            if ch == q: q = None
        elif ch in "\"'":
            q = ch; cur += ch
        elif ch == ",":
            out.append(cur); cur = ""
        else:
            cur += ch
    if cur.strip(): out.append(cur)
    return out

def load():
    if not os.path.exists(GATES):
        sys.stderr.write(f"gates.yaml không có ở {GATES} — chạy /ae-kit:init trong thư mục dự án (hoặc copy template).\n"); sys.exit(1)
    header, data, stack = [], {}, [(-1, None)]
    for raw in open(GATES, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            if not data: header.append(line)
            continue
        # bỏ comment cuối dòng (ngoài chuỗi)
        body = re.sub(r"\s+#.*$", "", line)
        indent = len(body) - len(body.lstrip())
        key, _, val = body.strip().partition(":")
        while stack and stack[-1][0] >= indent: stack.pop()
        parent = stack[-1][1] if stack and stack[-1][1] is not None else data
        if val.strip() == "":
            parent[key] = {}
            stack.append((indent, parent[key]))
        else:
            parent[key] = _scalar(val)
    return header, data

def _dump(d, indent=0):
    out = []
    for k, v in d.items():
        pad = "  " * indent
        if isinstance(v, dict):
            out.append(f"{pad}{k}:"); out.extend(_dump(v, indent + 1))
        else:
            out.append(f"{pad}{k}: {_fmt(v)}")
    return out

def _fmt(v):
    if v is None: return "null"
    if v is True: return "true"
    if v is False: return "false"
    if isinstance(v, list): return "[" + ", ".join(_fmt(x) for x in v) + "]"
    if isinstance(v, int): return str(v)
    s = str(v)
    return f'"{s}"' if re.search(r"[:#\[\]{},]|^\s|\s$", s) or s in ("true","false","null") else s

def save(header, data):
    lines = [h for h in header if h.strip()]  # giữ comment đầu file
    txt = "\n".join(lines + ([""] if lines else []) + _dump(data)) + "\n"
    open(GATES, "w", encoding="utf-8").write(txt)

def getp(d, path):
    for p in path.split("."):
        if not isinstance(d, dict) or p not in d: return None
        d = d[p]
    return d

def setp(d, path, val):
    parts = path.split(".")
    for p in parts[:-1]:
        d = d.setdefault(p, {})
    d[parts[-1]] = val

def today(): return datetime.date.today().isoformat()

# ---------- compute ----------
def _read(p):
    try: return open(os.path.join(ROOT, p), encoding="utf-8").read()
    except FileNotFoundError: return ""

def _latest(pattern):
    fs = sorted(glob.glob(os.path.join(ROOT, pattern)), key=os.path.getmtime)
    return fs[-1] if fs else None

def _req_fingerprint():
    """Dấu vân tay các dòng R/N accepted (nội dung + trạng thái) — để GP phát hiện spec đổi sau khi khách duyệt."""
    import hashlib
    rows = re.findall(r"^\|\s*[RN]\d+(?:\.\d+)?\s*\|.*\|\s*$", _read("spec/requirements.md"), re.M)
    return hashlib.sha1("\n".join(r.strip() for r in rows).encode("utf-8")).hexdigest()[:12]

def req_ids(text, accepted_only=False):
    ids = set()
    for m in re.finditer(r"^\|\s*([RN]\d+(?:\.\d+)?)\s*\|.*?\|\s*([a-z]+)\s*\|\s*$", text, re.M):
        if not accepted_only or m.group(2) in ("accepted", "implemented", "verified"):
            ids.add(m.group(1))
    return ids

def compute(data, gate):
    c = data.setdefault(gate, {}).setdefault("checks", {})
    notes = []
    if gate == "G1_spec":
        req = _read("spec/requirements.md")
        lint = _latest("spec/lint-*.md")
        lint_txt = open(lint, encoding="utf-8").read() if lint else ""
        c["lint_clean"] = bool(lint) and not re.search(r"^\|[^\n]*\|\s*ERROR\s*\|", lint_txt, re.M)
        if not lint: notes.append("chưa có spec/lint-*.md → /ae-kit:lint-spec")
        proposed = len(re.findall(r"^\|\s*[RN]\d+(?:\.\d+)?\s*\|.*?\|\s*proposed\s*\|\s*$", req, re.M))
        c["all_R_accepted"] = bool(req) and proposed == 0
        if proposed: notes.append(f"{proposed} R/N còn proposed")
        unl = 0
        for f in glob.glob(os.path.join(ROOT, "spec", "discovery-*.md")):
            for m in re.finditer(r"^\|\s*Q\d+\s*\|(.*)\|\s*$", open(f, encoding="utf-8").read(), re.M):
                if not re.search(r"\|\s*(send|assume|defer|prototype)\s*\|\s*$", m.group(0)): unl += 1
        c["open_q_classified"] = unl == 0
        if unl: notes.append(f"{unl} câu hỏi Q chưa có nhãn send/assume/defer")
        uno = 0
        for f in glob.glob(os.path.join(ROOT, "spec", "discovery-C*.md")):
            uno += len(re.findall(r"^\|\s*O\d+\s*\|.*\|\s*\?\s*\|\s*$", open(f, encoding="utf-8").read(), re.M))
        c["observed_classified"] = uno == 0
        if uno: notes.append(f"{uno} quan sát O chưa phân loại (brownfield)")
        if lint: data[gate]["evidence"] = os.path.relpath(lint, ROOT)
    elif gate == "GP_prototype":
        req = _read("spec/requirements.md")
        accepted = req_ids(req, accepted_only=True)
        scr = _read("spec/prototype/screens.md")
        if not scr:
            notes.append("chưa có spec/prototype/screens.md → /ae-kit:prototype")
        rows = re.findall(r"^\|\s*(S\d+)\s*\|([^\n]*)$", scr, re.M)
        covered, no_r = set(), []
        for sid, rest in rows:
            cells = [c.strip() for c in rest.split("|")]
            ids = set(re.findall(r"\b[RN]\d+(?:\.\d+)?\b", cells[1] if len(cells) > 1 else ""))
            if not ids: no_r.append(sid)
            covered |= ids
        noui = re.search(r"^## (?:\d+[.)]?\s*)?R không có UI[^\n]*\n([\s\S]*?)(?=^## |\Z)", scr, re.M)
        declared = set(re.findall(r"\b[RN]\d+(?:\.\d+)?\b", noui.group(1))) if noui else set()
        unclassified = sorted(accepted - covered - declared)
        c["every_R_has_screen_or_declared"] = bool(rows) and not unclassified
        if unclassified: notes.append("R chưa có màn hình và chưa khai 'không có UI': " + ", ".join(unclassified))
        c["every_screen_has_R"] = bool(rows) and not no_r
        if no_r: notes.append("màn hình không ↔ R nào (scope creep?): " + ", ".join(no_r))
        flow = re.search(r"^## (?:\d+[.)]?\s*)?Luồng task đầu[^\n]*\n([\s\S]*?)(?=^## |\Z)", scr, re.M)
        flow_ids = re.findall(r"\bS\d+\b", flow.group(1)) if flow else []
        sids = {sid for sid, _ in rows}
        missing_s = [x for x in flow_ids if x not in sids]
        c["first_slice_flow"] = len(flow_ids) >= 2 and not missing_s
        if len(flow_ids) < 2: notes.append("mục 'Luồng task đầu' cần ≥ 2 màn hình theo thứ tự click")
        if missing_s: notes.append("luồng trỏ tới màn hình không có trong bảng: " + ", ".join(missing_s))
        files_missing = []
        for sid, rest in rows:
            m = re.search(r"`([^`]+)`", rest)
            if m and not os.path.exists(os.path.join(ROOT, "spec", "prototype", m.group(1))) and not m.group(1).startswith(("http://", "https://")):
                files_missing.append(f"{sid}:{m.group(1)}")
        c["screen_files_exist"] = bool(rows) and not files_missing
        if files_missing: notes.append("file màn hình không tồn tại: " + ", ".join(files_missing))
        ap = _latest("spec/prototype/approval-P*.md")
        if ap:
            at = open(ap, encoding="utf-8").read()
            pv = re.search(r"^Prototype:\s*(P\d+)", at, re.M)
            tr = re.search(r"^Transcript:\s*(T\d+)", at, re.M)
            conf = re.search(r"^Xác nhận mô hình:\s*(yes|có)", at, re.M | re.I)
            ok = bool(pv and tr and conf)
            if tr and not os.path.exists(os.path.join(ROOT, "spec", f"discovery-{tr.group(1)}.md")):
                ok = False; notes.append(f"approval trỏ tới {tr.group(1)} nhưng chưa có spec/discovery-{tr.group(1)}.md → /ae-kit:intake {tr.group(1)}")
            if not pv: notes.append("approval thiếu dòng `Prototype: P<v>`")
            if not tr: notes.append("approval thiếu dòng `Transcript: T<n>` (buổi duyệt phải là một transcript)")
            if not conf: notes.append("approval thiếu `Xác nhận mô hình: yes` (khách đã được nói rõ đây là mô hình, không phải phần mềm)")
            if ok and data[gate].get("stale_approval") == os.path.relpath(ap, ROOT):
                ok = False; notes.append(f"approval {os.path.basename(ap)} đã cũ (spec đổi sau khi khách duyệt) → cần approval mới (P<v+1> hoặc buổi xác nhận lại T<n>)")
            c["approval_recorded"] = ok
            unl = 0
            if tr and os.path.exists(os.path.join(ROOT, "spec", f"discovery-{tr.group(1)}.md")):
                for m in re.finditer(r"^\|\s*Q\d+\s*\|(.*)\|\s*$", open(os.path.join(ROOT, "spec", f"discovery-{tr.group(1)}.md"), encoding="utf-8").read(), re.M):
                    if not re.search(r"\|\s*(send|assume|defer|prototype)\s*\|\s*$", m.group(0)): unl += 1
            c["demo_q_classified"] = unl == 0
            if unl: notes.append(f"{unl} câu hỏi Q phát sinh ở buổi demo chưa có nhãn")
            if ok: data[gate]["evidence"] = os.path.relpath(ap, ROOT)
        else:
            c["approval_recorded"] = False; c["demo_q_classified"] = False
            notes.append("chưa có spec/prototype/approval-P<v>.md (khách chưa duyệt)")
        # drift: spec đổi sau khi khách duyệt → về pending
        fp = _req_fingerprint()
        if data[gate].get("status") == "passed" and data[gate].get("req_fingerprint") and data[gate]["req_fingerprint"] != fp:
            c["approval_recorded"] = False
            data[gate]["stale_approval"] = data[gate].get("evidence")
            notes.append("requirements.md đã đổi sau khi khách duyệt prototype → cần demo lại hoặc khách xác nhận lại (approval mới)")
    elif gate == "G2_plan":
        req = _read("spec/requirements.md"); tasks = _read("spec/tasks.md")
        accepted = req_ids(req, accepted_only=True)
        blocks = re.findall(r"^- \[[ x]\] (T\d+)[^\n]*(?:\n(?!- \[)[^\n]*)*", tasks, re.M)
        task_blocks = re.findall(r"(^- \[[ x]\] T\d+[\s\S]*?)(?=^- \[[ x]\] T\d+|^## |\Z)", tasks, re.M)
        covered, missing_r, missing_done, missing_files = set(), [], [], []
        for b in task_blocks:
            tid = re.match(r"- \[[ x]\] (T\d+)", b).group(1)
            m = re.search(r"↔\s*([^\n]+)", b)
            ids = set(re.findall(r"\b[RNI]\d+(?:\.\d+)?\b", m.group(1))) if m else set()
            if not ids: missing_r.append(tid)
            covered |= ids
            if not re.search(r"^\s+Done:\s*\S", b, re.M): missing_done.append(tid)
            if not re.search(r"^\s+Files:\s*\S", b, re.M): missing_files.append(tid)
        uncovered = sorted(accepted - covered)
        c["every_R_has_task"] = bool(task_blocks) and not uncovered
        c["every_task_has_R"] = bool(task_blocks) and not missing_r
        c["every_task_has_done"] = bool(task_blocks) and not missing_done and not missing_files
        first = task_blocks[0] if task_blocks else ""
        c["first_task_e2e"] = bool(re.search(r"(?i)e2e|end-to-end|xuyên|vertical", first))
        bb = []
        if uncovered: bb += [f"{r} chưa có task" for r in uncovered]
        bb += [f"{t} không ↔ R nào" for t in missing_r]
        bb += [f"{t} thiếu Done:" for t in missing_done]
        bb += [f"{t} thiếu Files:" for t in missing_files]
        if not c["first_task_e2e"]: bb.append("task đầu chưa ghi rõ là vertical slice/e2e")
        data[gate]["blocked_by"] = bb
        notes += bb
        if tasks: data[gate]["evidence"] = "spec/tasks.md"
    elif gate == "G4_evidence":
        cmdf = os.path.join(ROOT, ".ae-kit", "check.cmd")
        if os.path.exists(cmdf):
            cmd = open(cmdf, encoding="utf-8").readline().strip()
            r = subprocess.run(["bash", "-c", cmd], cwd=ROOT, capture_output=True, text=True)
            c["check_cmd"] = "pass" if r.returncode == 0 else "fail"
            if r.returncode: notes.append("check.cmd FAIL:\n" + (r.stdout + r.stderr)[-1500:])
        else:
            c["check_cmd"] = "n/a"; notes.append(".ae-kit/check.cmd không có")
        tech = _read("docs/product/tech.md")
        m = re.search(r"^- E2E:\s*`([^`]+)`", tech, re.M)
        if m and m.group(1).strip():
            r = subprocess.run(["bash", "-c", m.group(1).strip()], cwd=ROOT, capture_output=True, text=True)
            c["e2e"] = "pass" if r.returncode == 0 else "fail"
            if r.returncode: notes.append("E2E FAIL:\n" + (r.stdout + r.stderr)[-1500:])
        else:
            c["e2e"] = "n/a"
        n = data[gate].get("sprint") or data.get("current_sprint")
        ev = _latest_synth(n)
        if ev:
            txt = open(ev, encoding="utf-8").read()
            c["evaluator_pass_per_R"] = bool(re.search(r"^Verdict:\s*\**PASS", txt, re.M))
            data[gate]["evidence"] = os.path.relpath(ev, ROOT)
            if not c["evaluator_pass_per_R"]: notes.append(f"evaluator FAIL: {os.path.basename(ev)}")
        else:
            notes.append("chưa có eval-sprint-*.md → /ae-kit:evaluate")
        models = _panel_models(data)
        if not models:
            c["panel_agree"] = "n/a"
        else:
            rounds = _eval_rounds(n)
            kp = max([k for k in rounds if rounds[k]["panel"]] or [0])
            ks = max([k for k in rounds if rounds[k]["synth"]] or [0])
            if kp == 0 or kp > ks or c.get("panel_agree") not in (True, False):
                # panel bật nhưng vòng mới nhất chưa được tổng hợp (chưa chạy `gates.py panel`)
                c["panel_agree"] = False
                notes.append(f"panel {len(models)} model bật nhưng vòng mới nhất chưa tổng hợp → `gates.py panel {n}` sau khi mọi evaluator xong")
    elif gate == "G5_merge":
        tasks = _read("spec/tasks.md")
        n = data[gate].get("sprint") or data.get("current_sprint")
        sprint_blk = re.search(rf"^## Sprint {n}\b[\s\S]*?(?=^## |\Z)", tasks, re.M)
        allowed = set()
        if sprint_blk:
            for m in re.finditer(r"^\s+Files:\s*([^\n]+)", sprint_blk.group(0), re.M):
                allowed |= {x.strip() for x in m.group(1).split(",") if x.strip()}
        base = os.environ.get("AE_BASE_BRANCH")
        cands = [base] if base else ["main", "master", "develop"]
        r = None
        for b in cands:
            r = subprocess.run(["git", "diff", "--name-only", f"{b}...HEAD"], cwd=ROOT, capture_output=True, text=True)
            if r.returncode == 0: base = b; break
        changed = [x for x in r.stdout.split("\n") if x.strip()] if r.returncode == 0 else []
        if r.returncode != 0:
            notes.append("git diff <base>...HEAD thất bại — đặt AE_BASE_BRANCH=<nhánh gốc> (đã thử main, master, develop)")
        def ok(f):
            if f.startswith("spec/") or f.startswith("docs/") or f in ("CLAUDE.md",): return True
            return any(f == a or (a.endswith("/") and f.startswith(a)) or (a.endswith("*") and f.startswith(a[:-1])) for a in allowed)
        outside = [f for f in changed if not ok(f)]
        c["no_file_outside_task_scope"] = r.returncode == 0 and not outside
        if outside: notes.append("file ngoài phạm vi task: " + ", ".join(outside))
        code_changed = [f for f in changed if not (f.startswith("spec/") or f.startswith("docs/") or f.endswith(".md"))]
        spec_changed = [f for f in changed if f.startswith("spec/")]
        if code_changed and not spec_changed:
            c["spec_diff_present_if_behavior_changed"] = None
            notes.append("code đổi nhưng spec/ không đổi — xác nhận 'không đổi hành vi' khi approve, hoặc cập nhật spec")
        else:
            c["spec_diff_present_if_behavior_changed"] = True
    return notes

# ---------- panel đa model (G4 tầng 2) ----------
def _panel_models(d):
    m = getp(d, "G4_evidence.panel.models")
    return [str(x) for x in m] if isinstance(m, list) else []

def _eval_rounds(n):
    """{k: {"synth": path|None, "panel": {i: path}}} cho sprint n."""
    rounds = {}
    for f in glob.glob(os.path.join(ROOT, "spec", f"eval-sprint-{n}-r*.md")):
        m = re.search(rf"eval-sprint-{n}-r(\d+)(?:-p(\d+))?\.md$", os.path.basename(f))
        if not m: continue
        k = int(m.group(1)); r = rounds.setdefault(k, {"synth": None, "panel": {}})
        if m.group(2): r["panel"][int(m.group(2))] = f
        else: r["synth"] = f
    return rounds

def _latest_synth(n):
    rounds = _eval_rounds(n)
    ks = [k for k in sorted(rounds) if rounds[k]["synth"]]
    return rounds[ks[-1]]["synth"] if ks else None

def _parse_eval(path):
    txt = open(path, encoding="utf-8").read()
    v = re.search(r"^Verdict:\s*\**\s*(PASS|FAIL)", txt, re.M)
    model = re.search(r"^Model:\s*(\S+)", txt, re.M)
    rows = {}
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*\**(PASS|FAIL)\**\s*\|", txt, re.M):
        crit = m.group(1).strip()
        if crit.lower() in ("criterion", "tiêu chí", "---") or crit.startswith("-"): continue
        rows[crit] = {"kind": m.group(2).strip().lower(), "result": m.group(3)}
    ratchet = re.search(r"^## Đề xuất ratchet[^\n]*\n([\s\S]*?)(?=^## |\Z)", txt, re.M)
    lines = [l for l in (ratchet.group(1).split("\n") if ratchet else []) if l.strip().startswith("- ") and l.strip() != "- ..."]
    return {"verdict": v.group(1) if v else None, "model": model.group(1) if model else "?", "rows": rows, "ratchet": lines}

def panel(d, n=None, k=None):
    n = n or d.get("G4_evidence", {}).get("sprint") or d.get("current_sprint")
    models = _panel_models(d)
    if not models:
        print("G4_evidence.panel.models rỗng — không có panel; evaluator đơn ghi thẳng spec/eval-sprint-N-r<k>.md."); return 1
    rounds = _eval_rounds(n)
    ks = [kk for kk in sorted(rounds) if rounds[kk]["panel"]]
    if not ks: print(f"chưa có spec/eval-sprint-{n}-r<k>-p<i>.md nào"); return 1
    k = int(k) if k else ks[-1]
    files = rounds.get(k, {}).get("panel", {})
    reports = {i: _parse_eval(p) for i, p in sorted(files.items())}
    expected = len(models)
    if len(reports) < expected:
        print(f"panel chưa đủ: {len(reports)}/{expected} báo cáo cho sprint {n} vòng {k} (chờ evaluator còn lại)"); return 2
    missing_v = [i for i, r in reports.items() if not r["verdict"]]
    if missing_v: print("báo cáo thiếu dòng `Verdict:` : " + ", ".join(f"p{i}" for i in missing_v)); return 2
    min_agree = getp(d, "G4_evidence.panel.min_agree") or expected
    n_pass = sum(1 for r in reports.values() if r["verdict"] == "PASS")
    crits = []
    for r in reports.values():
        for c in r["rows"]:
            if c not in crits: crits.append(c)
    hard_fail, disagree = [], []
    for c in crits:
        res = {i: r["rows"].get(c, {}).get("result", "—") for i, r in reports.items()}
        kinds = {r["rows"].get(c, {}).get("kind", "") for r in reports.values() if c in r["rows"]}
        fails = [i for i, x in res.items() if x == "FAIL"]
        hard = bool(re.match(r"^I\d+", c)) or any(("invariant" in kd) or ("cứng" in kd) for kd in kinds)
        if fails and hard: hard_fail.append((c, fails))
        if fails and len(fails) < len(reports): disagree.append((c, res))
    verdict = "PASS" if (n_pass >= min_agree and not hard_fail) else "FAIL"
    # viết báo cáo tổng hợp — tất định, không có lời giải thích của generator
    out = [f"# Evaluation — Sprint {n} — vòng {k} (panel {len(reports)} model)", "",
           f"Verdict: **{verdict}**  (tổng hợp bởi gates.py panel: {n_pass}/{len(reports)} PASS, cần ≥ {min_agree}; invariant/ngưỡng cứng FAIL bởi bất kỳ model nào → FAIL)", "",
           "| Evaluator | Model | Verdict | Báo cáo |", "|---|---|---|---|"]
    for i, r in reports.items():
        out.append(f"| p{i} | {r['model']} | {r['verdict']} | {os.path.relpath(files[i], ROOT)} |")
    out += ["", "## Tiêu chí × model", "", "| Criterion | " + " | ".join(f"p{i}" for i in reports) + " | Kết luận |", "|---|" + "---|" * len(reports) + "---|"]
    for c in crits:
        res = [reports[i]["rows"].get(c, {}).get("result", "—") for i in reports]
        concl = "FAIL" if "FAIL" in res else "PASS"
        if "FAIL" in res and "PASS" in res: concl += " (bất đồng)"
        out.append(f"| {c} | " + " | ".join(res) + f" | {concl} |")
    out += ["", "## Bất đồng (người xem ở G5)"]
    out += [f"- {c}: " + ", ".join(f"p{i}={x}" for i, x in res.items()) for c, res in disagree] or ["- (không)"]
    if hard_fail:
        out += ["", "## Invariant / ngưỡng cứng FAIL"] + [f"- {c}: FAIL bởi " + ", ".join(f"p{i}" for i in fs) for c, fs in hard_fail]
    out += ["", "## Đề xuất ratchet (gộp từ mọi evaluator, chưa khử trùng lặp)"]
    seen = set()
    for r in reports.values():
        for l in r["ratchet"]:
            if l.strip() not in seen: seen.add(l.strip()); out.append(l.strip())
    if not seen: out.append("- (không)")
    synth = os.path.join(ROOT, "spec", f"eval-sprint-{n}-r{k}.md")
    open(synth, "w", encoding="utf-8").write("\n".join(out) + "\n")
    setp(d, "G4_evidence.checks.panel_agree", n_pass >= min_agree)
    setp(d, "G4_evidence.panel.last", f"sprint {n} r{k}: {n_pass}/{len(reports)} PASS, {len(disagree)} bất đồng, {len(hard_fail)} hard FAIL")
    print(f"panel sprint {n} vòng {k}: Verdict {verdict} ({n_pass}/{len(reports)} PASS, cần ≥ {min_agree}) → {os.path.relpath(synth, ROOT)}")
    for c, res in disagree: print(f"  - bất đồng {c}: " + ", ".join(f"p{i}={x}" for i, x in res.items()))
    for c, fs in hard_fail: print(f"  - hard FAIL {c} bởi " + ", ".join(f"p{i}" for i in fs))
    return 0 if verdict == "PASS" else 2

def all_true(d, gate):
    chk = d.get(gate, {}).get("checks", {})
    return all(v is True or v == "pass" or v == "n/a" for v in chk.values()) and bool(chk)

def failing(d, gate):
    return [k for k, v in d.get(gate, {}).get("checks", {}).items() if not (v is True or v == "pass" or v == "n/a")]

# ---------- hiển thị ----------
SYM = {"passed": "[✓]", "blocked": "[✗]", "pending": "[ ]"}
NEXT = {
    "G1_spec": lambda d: "/ae-kit:lint-spec" if not d["G1_spec"].get("evidence") else ("/ae-kit:approve G1" if all_true(d, "G1_spec") else "/ae-kit:lint-spec (sửa ô đỏ rồi chạy lại)"),
    "GP_prototype": lambda d: "/ae-kit:prototype" if not os.path.exists(os.path.join(ROOT, "spec", "prototype", "screens.md")) else ("/ae-kit:approve GP \"<tên khách>\"" if all_true(d, "GP_prototype") else "/ae-kit:prototype (sửa ô đỏ; demo cho khách; /ae-kit:intake T<n> buổi duyệt)"),
    "G2_plan": lambda d: "/ae-kit:approve G2" if all_true(d, "G2_plan") else "/ae-kit:plan",
    "G3_contract": lambda d: f"/ae-kit:contract {d.get('current_sprint') or 1}",
    "G4_evidence": lambda d: "/ae-kit:next-task (nếu còn task) rồi /ae-kit:evaluate " + str(d.get("current_sprint") or 1),
    "G5_merge": lambda d: "/ae-kit:approve G5",
}

def next_cmd(d):
    for g in ORDER:
        st = _status(d, g)
        if st == "n/a": continue
        if st == "blocked":
            if g == "G4_evidence": return "G4 BLOCKED (vượt retry) — người quyết: sửa spec / chia nhỏ task / /ae-kit:ratchet, rồi `gates.py set G4_evidence.status pending`"
            if g == "G3_contract": return "G3 BLOCKED (vượt rounds) — người chốt tiêu chí tranh cãi trong contract, rồi `gates.py set G3_contract.status pending`"
            return NEXT[g](d)
        if st != "passed": return NEXT[g](d)
    return "/ae-kit:replan (sprint đã merge) hoặc /ae-kit:ratchet nếu sprint có lỗi"

def show(d):
    proj = d.get("project", "?"); sp = d.get("current_sprint", 0)
    br = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip() or "-"
    print(f"ae-kit status — {proj} · sprint {sp} · branch {br}\n")
    prev_ok = True
    for g in ORDER:
        gd = d.get(g, {}); st = _status(d, g)
        sym = SYM.get(st, "[ ]")
        if st == "pending" and prev_ok: sym = "[~]"
        label = g.split("_")[0] + " " + g.split("_")[1].capitalize()
        extra = ""
        if st == "n/a":
            print(f"[–] {label:<14} n/a (dự án không có UI hoặc gates.yaml v0.3)"); prev_ok = True; continue
        if st == "passed": extra = f"passed {gd.get('approved_at','')} ({gd.get('approved_by','auto')})"
        elif st == "blocked": extra = "BLOCKED  " + "; ".join(gd.get("blocked_by") or failing(d, g))
        else:
            f = failing(d, g)
            extra = ("chờ " + ", ".join(f)) if f else "pending"
            if g == "G3_contract": extra += f"  rounds {gd.get('rounds',0)}/{gd.get('max_rounds',3)}"
            if g == "G4_evidence":
                extra += f"  retries {gd.get('retries',0)}/{gd.get('max_retries',3)}"
                pm = _panel_models(d)
                extra += f"  panel {','.join(pm)} ≥{getp(d,'G4_evidence.panel.min_agree') or len(pm)}" if pm else "  panel off"
        print(f"{sym} {label:<14} {extra}")
        prev_ok = st == "passed"
    print()
    # Tầng luật
    cl = _read("CLAUDE.md")
    body = cl.split("## Ratchet log")[0]
    rules = [l for l in body.split("\n") if l.startswith("- ")]
    nosrc = [l for l in rules if not re.search(r"\[(harness|ratchet #\d+|[NID]\d+(?:\.\d+)?|C\d+ O\d+)\]\s*$", l)]
    print(f"CLAUDE.md: {len(cl.splitlines())}/40 dòng · {len(nosrc)} dòng luật thiếu [nguồn]" + ("  → /ae-kit:ratchet --audit" if nosrc else ""))
    uno = sum(len(re.findall(r"^\|\s*O\d+\s*\|.*\|\s*\?\s*\|\s*$", open(f, encoding="utf-8").read(), re.M)) for f in glob.glob(os.path.join(ROOT, "spec", "discovery-C*.md")))
    if glob.glob(os.path.join(ROOT, "spec", "discovery-C*.md")): print(f"Brownfield: {uno} O chưa phân loại")
    rm = _read("docs/product/roadmap.md")
    rows = re.findall(r"^\|\s*\d+[^|]*\|[^|]*\|[^|]*\|\s*(planned|in-progress|done|dropped)\s*\|", rm, re.M)
    if rows: print(f"Roadmap: {rows.count('done')}/{len(rows)} feature done")
    pg = _read("spec/progress.md")
    qsec = re.search(r"## Câu hỏi cần người quyết\s*([\s\S]*?)(?=^## |\Z)", pg, re.M)
    if qsec:
        q = [l for l in qsec.group(1).split("\n") if l.strip().startswith("- ") and l.strip() != "- ..."]
        print(f"Hỏi người đang mở: {len(q)}  (spec/progress.md)")
    print(f"Bước tiếp theo: {next_cmd(d)}")

def short(d):
    s = []
    for g in ORDER:
        st = _status(d, g)
        s.append(g.split("_")[0] + " " + {"passed": "✓", "blocked": "✗ BLOCKED", "n/a": "–"}.get(st, "·"))
    print("ae-kit gates: " + "  ".join(s) + f"  → {next_cmd(d)}")

# ---------- main ----------
def main(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return 0
    cmd, args = argv[0], argv[1:]
    header, d = load()
    if cmd == "show": show(d); return 0
    if cmd == "short": short(d); return 0
    if cmd == "next": print(next_cmd(d)); return 0
    if cmd == "get": print(_fmt(getp(d, args[0]))); return 0
    if cmd == "set":
        setp(d, args[0], _scalar(args[1])); save(header, d); print(f"{args[0]} = {args[1]}"); return 0
    if cmd == "incr":
        v = (getp(d, args[0]) or 0) + 1; setp(d, args[0], v)
        gate = args[0].split(".")[0]; mx = getp(d, gate + ".max_rounds") or getp(d, gate + ".max_retries")
        if mx and v >= mx: setp(d, gate + ".status", "blocked"); print(f"{gate} BLOCKED: {v}/{mx}")
        save(header, d); print(f"{args[0]} = {v}"); return 0
    if cmd == "compute":
        g = _gate(args[0])
        if g == "GP_prototype" and _status(d, g) == "n/a":
            print("GP n/a — không tính (bật bằng `set GP_prototype.status pending`)"); return 0
        notes = compute(d, g)
        f = failing(d, g)
        if f and d[g].get("status") == "passed":
            d[g]["status"] = "pending"; d[g].pop("approved_by", None); d[g].pop("approved_at", None)
            notes.append(f"{g} đã passed trước đó nhưng artifact đã đổi → về pending, cần duyệt lại (chống spec drift)")
        save(header, d)
        print(f"{g}: " + ("tất cả ô xanh" if not f else "ô đỏ: " + ", ".join(f)))
        for n in notes: print("  - " + n)
        return 0 if not f else 2
    if cmd == "panel":
        rc = panel(d, args[0] if args else None, args[1] if len(args) > 1 else None)
        save(header, d); return rc
    if cmd == "pass":
        g = _gate(args[0])
        if g in HUMAN: print(f"{g} là gate người duyệt — dùng approve"); return 1
        f = failing(d, g)
        if f: print(f"{g} chưa đạt: " + ", ".join(f)); return 2
        d[g]["status"] = "passed"; d[g]["approved_at"] = today(); save(header, d); print(f"{g} passed"); return 0
    if cmd == "approve":
        g = _gate(args[0]); who = args[1] if len(args) > 1 else "unknown"
        force = None
        if "--force" in args: force = args[args.index("--force") + 1] if args.index("--force") + 1 < len(args) else "no reason"
        if g not in HUMAN: print(f"{g} là gate máy — dùng pass"); return 1
        idx = ORDER.index(g)
        if idx > 0 and not _ok_prev(d, ORDER[idx-1]):
            print(f"Gate trước ({ORDER[idx-1]}) chưa passed."); return 2
        if g == "GP_prototype" and _status(d, g) == "n/a":
            print("GP đang n/a (dự án không có UI) — `gates.py set GP_prototype.status pending` nếu muốn bật."); return 1
        if g == "GP_prototype" and who in ("unknown", ""):
            print("approve GP cần tên khách hàng/người đại diện đã duyệt: `approve GP \"<tên>\"`."); return 1
        f = failing(d, g)
        if f and not force:
            print(f"KHÔNG duyệt {g}: ô máy chưa xanh → " + ", ".join(f)); print("Sửa rồi chạy lại, hoặc --force \"<lý do>\"."); return 2
        d[g]["status"] = "passed"; d[g]["approved_by"] = who; d[g]["approved_at"] = today()
        if g == "GP_prototype": d[g]["req_fingerprint"] = _req_fingerprint(); d[g].pop("stale_approval", None)
        if force: d[g]["forced"] = force
        save(header, d); print(f"{g} passed by {who}" + (f" (FORCED: {force})" if force else "")); return 0
    if cmd == "new-sprint":
        if d.get("G5_merge", {}).get("status") != "passed" and "--force" not in args:
            print("G5 chưa passed — không mở sprint mới (dùng --force nếu cố ý bỏ sprint)."); return 2
        n = (d.get("current_sprint") or 0) + 1; d["current_sprint"] = n
        for g, keys in (("G3_contract", {"reviewer_agreed": False, "criteria_observable": False}),
                        ("G4_evidence", {"check_cmd": None, "e2e": None, "evaluator_pass_per_R": None, "panel_agree": None}),
                        ("G5_merge", {"diff_within_contract": None, "spec_diff_present_if_behavior_changed": None, "no_file_outside_task_scope": None})):
            d[g].update({"sprint": n, "status": "pending", "checks": keys, "evidence": None})
            d[g].pop("approved_by", None); d[g].pop("approved_at", None); d[g].pop("forced", None)
            if "rounds" in d[g]: d[g]["rounds"] = 0
            if "retries" in d[g]: d[g]["retries"] = 0
            if isinstance(d[g].get("panel"), dict): d[g]["panel"].pop("last", None)
        save(header, d); print(f"sprint {n}"); return 0
    print(f"lệnh không biết: {cmd}"); return 1

def _gate(s):
    s = s.upper()
    for g in ORDER:
        if g.startswith(s + "_") or g == s: return g
    sys.stderr.write(f"gate không hợp lệ: {s}\n"); sys.exit(1)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
