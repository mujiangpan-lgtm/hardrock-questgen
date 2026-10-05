"""Prove that a stage build changed only the given chapters' art.

    python tools/check_unchanged.py <stage dir> <chapter key>[,<key>...]

Compares every generated texture and theme line of the OTHER chapters in <stage dir> with the live
pack (kubejs/assets/...). Exit code 1 and a list of differences if anything else changed.
"""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
stage = HERE / sys.argv[1]
keys = sys.argv[2].split(",")
live_tex = HERE.parent / "kubejs" / "assets" / "kubejs" / "textures" / "quests"
live_theme = HERE.parent / "kubejs" / "assets" / "ftbquests" / "ftb_quests_theme.txt"


def mine(name):
    return any(name.startswith(k + "_") for k in keys)


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


bad = []
st = {p.name: p for p in (stage / "textures").glob("*.png")}
lv = {p.name: p for p in live_tex.glob("*.png")}
for n in sorted(set(st) | set(lv)):
    if mine(n):
        continue
    if n not in st or n not in lv:
        bad.append(f"only in {'live' if n in lv else 'stage'}: {n}")
    elif md5(st[n]) != md5(lv[n]):
        bad.append(f"changed: {n}")
a = {x for x in live_theme.read_text("utf-8").splitlines() if not any(k in x for k in keys)}
b = {x for x in (stage / "ftb_quests_theme.txt").read_text("utf-8").splitlines() if not any(k in x for k in keys)}
bad += [f"theme line changed: {x}" for x in sorted(a ^ b)]
print("\n".join(bad) if bad else f"OK: all other chapters' textures ({len([n for n in st if not mine(n)])}) and theme lines identical to live")
sys.exit(1 if bad else 0)
