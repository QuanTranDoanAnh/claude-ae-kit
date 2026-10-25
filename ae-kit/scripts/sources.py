#!/usr/bin/env python3
"""
ae-kit sources.py — manifest nguồn đầu vào TẤT ĐỊNH (intake/sources.yaml). v0.5.

Mỗi nguồn đã intake (T<n> transcript · F<n> file tài liệu · C<n> codebase) phải có một mục với metadata;
reconcile dùng metadata để ĐỀ XUẤT cách giải quyết mâu thuẫn (precedence), gates.py compute G1 đếm nguồn thiếu
metadata (ô sources_registered). Agent không sửa sources.yaml tay — đi qua script này.

Lệnh:
  init                         quét intake/ (T*/F*) + spec/discovery-C*.md, thêm mục còn thiếu với `?`; không đụng mục đã có
  add <ID> [key=value ...]     thêm/sửa một nguồn. key: type path origin date author authority trust note
                               ví dụ: add F1 type=srs path=F1-srs-v0.3.docx origin=customer date=2026-09-05 \\
                                      author="Phòng IT khách" authority=stakeholder trust=medium
  set <ID> <key> <value>       sửa một trường
  list                         bảng nguồn + trạng thái (đã intake? đủ metadata?)
  check                        exit 2 nếu còn nguồn đã intake mà thiếu metadata / `?`, hoặc path không tồn tại
  precedence                   in thứ tự ưu tiên mặc định khi mâu thuẫn (để reconcile đề xuất, KHÔNG tự quyết)

Giá trị hợp lệ:
  type       transcript | srs | brd | rfp | notes | email | spec-legacy | codebase | other
  origin     customer | vendor | internal | third-party
  authority  decision-maker | stakeholder | end-user | unknown      (ai đứng sau nguồn này)
  trust      high | medium | low                                     (bạn đánh giá; SRS khách tự viết thường medium)
  date       YYYY-MM-DD (ngày của nguồn: buổi nói chuyện / phiên bản tài liệu / commit)
Thứ tự ưu tiên mặc định khi hai nguồn mâu thuẫn (có thể ghi đè bằng `precedence: [T2, T1, F1]` ở đầu sources.yaml):
  1. nguồn mới hơn (date)  2. authority decision-maker > stakeholder > end-user > unknown
  3. transcript > tài liệu > codebase (lời nói sau cùng của khách thắng văn bản cũ)  4. trust cao hơn.
Exit code: 0 ok · 1 lỗi tham số · 2 check không đạt.
"""
import os, re, sys, glob, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gates import ROOT, load_yaml, save_yaml, _fmt, discovery_ids  # noqa: E402

SOURCES = os.path.join(ROOT, "intake", "sources.yaml")
KIND = "TFC"
KEYS = ("type", "path", "origin", "date", "author", "authority", "trust", "note")
REQUIRED = ("type", "origin", "date", "authority")
VALID = {
    "type": {"transcript", "srs", "brd", "rfp", "notes", "email", "spec-legacy", "codebase", "other"},
    "origin": {"customer", "vendor", "internal", "third-party"},
    "authority": {"decision-maker", "stakeholder", "end-user", "unknown"},
    "trust": {"high", "medium", "low"},
}
HEADER = [
    "# intake/sources.yaml — manifest nguồn đầu vào (v0.5). Sửa qua scripts/sources.py, không sửa tay.",
    "# Mỗi nguồn đã intake (T<n> transcript · F<n> file tài liệu · C<n> codebase) phải có một mục.",
    "# origin: customer|vendor|internal|third-party · authority: decision-maker|stakeholder|end-user|unknown · trust: high|medium|low",
    "# precedence: [T2, T1, F1] (tuỳ chọn) — ghi đè thứ tự ưu tiên mặc định khi reconcile đề xuất giải quyết mâu thuẫn.",
]

def _load():
    if not os.path.exists(SOURCES): return list(HEADER), {}
    h, d = load_yaml(SOURCES)
    return (h or list(HEADER)), d

def _save(h, d):
    os.makedirs(os.path.dirname(SOURCES), exist_ok=True)
    # giữ thứ tự: precedence (nếu có) → nguồn theo chữ rồi số
    out = {}
    if "precedence" in d: out["precedence"] = d["precedence"]
    for k in sorted([k for k in d if re.fullmatch(rf"[{KIND}]\d+", k)], key=lambda s: (s[0], int(s[1:]))):
        out[k] = {kk: d[k].get(kk, "?") for kk in KEYS if kk in d[k] or kk in REQUIRED or kk == "path"}
    for k, v in d.items():
        if k not in out: out[k] = v
    save_yaml(SOURCES, h, out)

def _intake_files():
    """{ID: path tương đối trong intake/} từ intake/T*-*.md | F*-* (bỏ bản .numbered/.extracted)."""
    found = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "intake", "*"))):
        b = os.path.basename(f)
        m = re.match(r"^([TF]\d+)[-_]", b)
        if not m or b.endswith((".numbered.md", ".extracted.md")) or b.lower() in ("readme.md", "sources.yaml"): continue
        found.setdefault(m.group(1), b)
    return found

def _guess_type(i, path):
    if i.startswith("T"): return "transcript"
    if i.startswith("C"): return "codebase"
    p = (path or "").lower()
    for k in ("srs", "brd", "rfp", "email", "note"):
        if k in p: return "notes" if k == "note" else k
    return "?"

def _git_date():
    r = subprocess.run(["git", "log", "-1", "--format=%cs"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip() or "?"

def cmd_init(h, d):
    files = _intake_files()
    ids = sorted(set(files) | set(discovery_ids()), key=lambda s: (s[0], int(s[1:])))
    added = []
    for i in ids:
        if i in d: continue
        path = files.get(i, "." if i.startswith("C") else "?")
        d[i] = {"type": _guess_type(i, path), "path": path, "origin": "internal" if i.startswith("C") else "?",
                "date": _git_date() if i.startswith("C") else "?", "author": "?",
                "authority": "unknown" if i.startswith("C") else "?", "trust": "?"}
        added.append(i)
    _save(h, d)
    print(f"sources.yaml: thêm {len(added)} nguồn " + (", ".join(added) if added else "(không có mới)") + f" → {os.path.relpath(SOURCES, ROOT)}")
    miss = _missing(d)
    if miss: print("Cần điền (`sources.py set <ID> <key> <value>`): " + "; ".join(f"{i}: {', '.join(ks)}" for i, ks in miss))
    return 0

def _validate(key, val):
    if key in VALID and val not in VALID[key] and val != "?":
        sys.stderr.write(f"{key}={val} không hợp lệ; chọn: {', '.join(sorted(VALID[key]))}\n"); sys.exit(1)
    if key == "date" and val != "?" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", val):
        sys.stderr.write("date phải là YYYY-MM-DD\n"); sys.exit(1)

def cmd_add(h, d, i, kvs):
    if not re.fullmatch(rf"[{KIND}]\d+", i): sys.stderr.write(f"ID không hợp lệ: {i} (T<n> | F<n> | C<n>)\n"); return 1
    e = d.setdefault(i, {})
    for kv in kvs:
        k, _, v = kv.partition("=")
        if k not in KEYS: sys.stderr.write(f"key không biết: {k} (chọn: {', '.join(KEYS)})\n"); return 1
        _validate(k, v); e[k] = v
    if "type" not in e: e["type"] = _guess_type(i, e.get("path"))
    if "path" not in e: e["path"] = _intake_files().get(i, "." if i.startswith("C") else "?")
    for k in REQUIRED: e.setdefault(k, "?")
    _save(h, d); print(f"{i}: " + ", ".join(f"{k}={_fmt(e[k])}" for k in KEYS if k in e)); return 0

def cmd_set(h, d, i, k, v):
    if i not in d: sys.stderr.write(f"{i} chưa có — dùng `add {i} ...` hoặc `init`\n"); return 1
    if k not in KEYS: sys.stderr.write(f"key không biết: {k}\n"); return 1
    _validate(k, v); d[i][k] = v; _save(h, d); print(f"{i}.{k} = {v}"); return 0

def _missing(d):
    out = []
    for i in discovery_ids():
        e = d.get(i)
        if e is None: out.append((i, ["chưa có mục"])); continue
        ks = [k for k in REQUIRED if e.get(k) in (None, "", "?")]
        if ks: out.append((i, ks))
    return out

def cmd_list(h, d):
    disc = set(discovery_ids()); files = _intake_files()
    ids = sorted(set(d) - {"precedence"} | disc | set(files), key=lambda s: (s[0], int(s[1:])) if re.fullmatch(rf"[{KIND}]\d+", s) else ("Z", 0))
    print(f"{'ID':<4} {'type':<11} {'origin':<11} {'date':<11} {'authority':<15} {'trust':<7} {'intake':<7} {'discovery':<10} path")
    for i in ids:
        e = d.get(i, {})
        print(f"{i:<4} {str(e.get('type','-')):<11} {str(e.get('origin','-')):<11} {str(e.get('date','-')):<11} {str(e.get('authority','-')):<15} "
              f"{str(e.get('trust','-')):<7} {('có' if i in files or i.startswith('C') else '—'):<7} {('có' if i in disc else '—'):<10} {e.get('path','-')}")
    if "precedence" in d: print(f"precedence (ghi đè): {_fmt(d['precedence'])}")
    miss = _missing(d)
    if miss: print("Thiếu metadata: " + "; ".join(f"{i}: {', '.join(ks)}" for i, ks in miss))
    return 0

def cmd_check(h, d):
    rc = 0
    miss = _missing(d)
    for i, ks in miss: print(f"✗ {i}: thiếu " + ", ".join(ks)); rc = 2
    for i, e in d.items():
        if i == "precedence" or not isinstance(e, dict): continue
        p = e.get("path")
        if p and p not in ("?", ".") and not os.path.exists(os.path.join(ROOT, "intake", p)):
            print(f"✗ {i}: intake/{p} không tồn tại"); rc = 2
    for i in _intake_files():
        if i not in d: print(f"✗ {i}: có file trong intake/ nhưng chưa đăng ký → sources.py init"); rc = 2
    print("sources.yaml: " + ("OK" if rc == 0 else "chưa đạt"))
    return rc

RANK_AUTH = {"decision-maker": 0, "stakeholder": 1, "end-user": 2, "unknown": 3}
RANK_KIND = {"T": 0, "F": 1, "C": 2}
RANK_TRUST = {"high": 0, "medium": 1, "low": 2}

def precedence(d):
    """Thứ tự nguồn thắng khi mâu thuẫn (đầu danh sách thắng). Ghi đè bởi d['precedence'] nếu có."""
    ids = [k for k in d if re.fullmatch(rf"[{KIND}]\d+", k)]
    ov = d.get("precedence")
    if isinstance(ov, list) and ov:
        ov = [str(x) for x in ov]
        return ov + [i for i in sorted(ids) if i not in ov]
    def key(i):
        e = d[i]
        date = str(e.get("date") or "0000-00-00")
        return (date if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) else "0000-00-00",
                -RANK_AUTH.get(str(e.get("authority")), 3), -RANK_KIND[i[0]], -RANK_TRUST.get(str(e.get("trust")), 2))
    return sorted(ids, key=key, reverse=True)

def cmd_precedence(h, d):
    order = precedence(d)
    print("Thứ tự ưu tiên khi mâu thuẫn (đề xuất cho reconcile; người quyết): " + " > ".join(order))
    for i in order:
        e = d.get(i, {})
        print(f"  {i}: {e.get('date','?')} · {e.get('authority','?')} · {e.get('type','?')} · trust {e.get('trust','?')}")
    return 0

def main(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return 0
    cmd, args = argv[0], argv[1:]
    h, d = _load()
    if cmd == "init": return cmd_init(h, d)
    if cmd == "add": return cmd_add(h, d, args[0], args[1:]) if args else 1
    if cmd == "set": return cmd_set(h, d, *args[:3]) if len(args) >= 3 else 1
    if cmd == "list": return cmd_list(h, d)
    if cmd == "check": return cmd_check(h, d)
    if cmd == "precedence": return cmd_precedence(h, d)
    print(f"lệnh không biết: {cmd}"); return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
