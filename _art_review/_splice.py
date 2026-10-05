"""Replace whole motif functions in artlib.py with the versions in a file:
python _art_review/_splice.py newfuncs.py   (each top-level def replaces the same-named def)"""
import re
import sys

src = open("artlib.py", encoding="utf-8").read()
new = open(sys.argv[1], encoding="utf-8").read()
blocks = re.split(r"\n(?=def )", "\n" + new.strip() + "\n")
for b in blocks:
    b = b.strip("\n")
    if not b.startswith("def "):
        continue
    name = b.split("(")[0][4:]
    a = src.index(f"\ndef {name}(") + 1
    m = re.search(r"\n(?=(def |_DECOR = |[A-Z_]+ = |# ----))", src[a + 1:])
    e = a + 1 + m.start() + 1
    src = src[:a] + b + "\n\n\n" + src[e:].lstrip("\n")
    print("replaced", name)
open("artlib.py", "w", encoding="utf-8", newline="\n").write(src)
