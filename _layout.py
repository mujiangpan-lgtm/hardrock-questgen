"""Temp layout helper (delete when done).
python questgen/_layout.py <stem>                 show section boxes
python questgen/_layout.py <stem> S dx dy [S dx dy ...]   shift whole section(s) S (1-based index)
python questgen/_layout.py <stem> q:key x y ...   set absolute position of one quest
"""
import re, sys, io, importlib.util, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import qlib

stem = sys.argv[1]
path = HERE / "chapters" / f"{stem}.py"


def load():
    qlib.CHAPTERS.clear()
    spec = importlib.util.spec_from_file_location("c", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.ch


def num(v):
    v = round(v, 3)
    return str(int(v)) if v == int(v) else str(v)


def sbox(s):
    qs = [ch.quests[k] for k in s.keys if k in ch.quests]
    return (min(q.x - q.size / 2 for q in qs) - s.pad, min(q.y - q.size / 2 for q in qs) - s.pad - 0.9,
            max(q.x + q.size / 2 for q in qs) + s.pad, max(q.y + q.size / 2 for q in qs) + s.pad)


ch = load()
src = path.read_text("utf-8")
args = sys.argv[2:]
moves = {}
def local_deps(k):
    return [d for d in ch.quests[k].deps if ":" not in d and d in ch.quests]


def reach(k, seen=None):
    seen = set() if seen is None else seen
    for d in local_deps(k):
        if d not in seen:
            seen.add(d)
            reach(d, seen)
    return seen


# redundant deps (implied transitively) -> report
for k in ch.quests:
    ds = local_deps(k)
    for d in ds:
        if any(d in reach(o) for o in ds if o != d):
            print(f"  REDUNDANT {k} -> {d}")

if args and args[0] == "auto":
    # layered layout per section, then pack: "auto 1,2/3,4/5 [gap] [dy]"
    gap = float(args[2]) if len(args) > 2 else 0.8
    step_y = float(args[3]) if len(args) > 3 else 2.0
    for s in ch.sections:
        ks = [k for k in s.keys if k in ch.quests]
        depth = {}

        def dep_of(k):
            if k not in depth:
                depth[k] = 0
                ds = [d for d in local_deps(k) if d in ks]
                depth[k] = 1 + max((dep_of(d) for d in ds), default=-1)
            return depth[k]
        for k in ks:
            dep_of(k)
        cols = {}
        for k in ks:
            cols.setdefault(depth[k], []).append(k)
        cx = 0.0
        for c in sorted(cols):
            members = cols[c]
            # order a column by the mean y of its parents (reduces crossings)
            def py(k):
                ps = [d for d in local_deps(k) if d in ks and d in ch.quests]
                return sum(ch.quests[p].y for p in ps) / len(ps) if ps else ks.index(k)
            if c > 0:
                members.sort(key=py)
            maxr = 3
            for j in range(0, len(members), maxr):
                chunk = members[j:j + maxr]
                n = len(chunk)
                for i, k in enumerate(chunk):
                    ch.quests[k].x = cx
                    ch.quests[k].y = (i - (n - 1) / 2) * step_y
                cx += 2.2
    args = ["pack"] + args[1:2] + [str(gap)]

if args and args[0] == "pack":
    # pack sections into rows: "pack 1,2/3,4/5 [gap]" (rows separated by /)
    rows = [[int(i) for i in r.split(",")] for r in args[1].split("/")]
    gap = float(args[2]) if len(args) > 2 else 0.6
    args = []
    y = 0.0
    for row in rows:
        x, h = 0.0, 0.0
        for i in row:
            s = ch.sections[i - 1]
            bx0, by0, bx1, by1 = sbox(s)
            dx, dy = x - bx0, y - by0
            for k in s.keys:
                q = ch.quests[k]
                moves[k] = (q.x + dx, q.y + dy)
            x += (bx1 - bx0) + gap
            h = max(h, by1 - by0)
        y += h + gap
while args:
    a, dx, dy = args[0], float(args[1]), float(args[2])
    args = args[3:]
    if a.startswith("q:"):
        q = ch.quests[a[2:]]
        moves[a[2:]] = (dx, dy)
    else:
        for k in ch.sections[int(a) - 1].keys:
            q = ch.quests[k]
            moves[k] = (q.x + dx, q.y + dy)
for k, (x, y) in moves.items():
    pat = re.compile(r'(ch\.quest\(\s*"' + re.escape(k) + r'"\s*,\s*)([-\d.]+)(\s*,\s*)([-\d.]+)')
    src, n = pat.subn(lambda m: m.group(1) + num(x) + m.group(3) + num(y), src)
    assert n == 1, (k, n)
if moves:
    path.write_text(src, "utf-8")
    ch = load()

import os
lim = float(os.environ.get("HIDE_LONG", "0"))
if lim:
    src = path.read_text("utf-8")
    sec = {k: i for i, s in enumerate(ch.sections) for k in s.keys}
    for k, q in ch.quests.items():
        long = [d for d in local_deps(k) if sec.get(d) != sec.get(k) and
                ((ch.quests[d].x - q.x) ** 2 + (ch.quests[d].y - q.y) ** 2) ** .5 > lim]
        if long and not q.hide_lines:
            print(f"  HIDE {k} (long edge from {','.join(long)})")
            pat = re.compile(r'(ch\.quest\(\s*"' + re.escape(k) + r'"\s*,[^\n]*?)\)?$', re.M)
            m = re.search(r'ch\.quest\(\s*"' + re.escape(k) + r'"\s*,', src)
            # insert right after the opening 'ch.quest("key",' line's title arg: append kw at end of first line
            eol = src.index("\n", m.start())
            line = src[m.start():eol]
            src = src[:eol] + (" hide_lines=True," if line.rstrip().endswith(",") else "") + src[eol:]
            assert line.rstrip().endswith(","), line
    path.write_text(src, "utf-8")
    ch = load()

boxes = []
for i, s in enumerate(ch.sections, 1):
    qs = [ch.quests[k] for k in s.keys if k in ch.quests]
    x0 = min(q.x - q.size / 2 for q in qs) - s.pad
    x1 = max(q.x + q.size / 2 for q in qs) + s.pad
    y0 = min(q.y - q.size / 2 for q in qs) - s.pad - 0.9
    y1 = max(q.y + q.size / 2 for q in qs) + s.pad
    boxes.append((i, s.title, x0, y0, x1, y1))
    print(f"S{i} {s.title}: x {x0:.2f}..{x1:.2f}  y {y0:.2f}..{y1:.2f}  ({len(qs)} q)")
    print("    " + "  ".join(f"{q.key}({num(q.x)},{num(q.y)})" for q in qs))
for i, a in enumerate(boxes):
    for b in boxes[i + 1:]:
        if a[2] < b[4] and b[2] < a[4] and a[3] < b[5] and b[3] < a[5]:
            print(f"  OVERLAP S{a[0]} / S{b[0]}")
missing = set(ch.quests) - {k for s in ch.sections for k in s.keys}
if missing:
    print("  not in a section:", missing)
