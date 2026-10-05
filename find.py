"""Search the registry:  python questgen/find.py <regex> [<regex> ...]
                        python questgen/find.py --tag <regex> ...

Matches item ids + localized names (items marked '?' come only from lang keys).
With --tag, searches item tags instead. Prints up to 40 hits per pattern.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
raw = json.loads((Path(__file__).resolve().parent / "registry.json").read_text("utf-8"))
args = sys.argv[1:]
if args and args[0] == "--tag":
    for pat in args[1:]:
        rx = re.compile(pat)
        hits = [t for t in raw["tags"] if rx.search(t)]
        print(f"## #{pat}  ({len(hits)} hits)")
        for t in hits[:40]:
            print("  #" + t)
    sys.exit()
for pat in args:
    rx = re.compile(pat)
    hits = [(k, v, "") for k, v in raw["items"].items() if rx.search(k) or rx.search(v)]
    hits += [(k, v, "?") for k, v in raw.get("probable", {}).items() if rx.search(k) or rx.search(v)]
    print(f"## {pat}  ({len(hits)} hits)")
    for k, v, m in hits[:40]:
        print(f"  {m}{k}  {v}")
