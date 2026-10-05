"""Scan mod jars + kubejs + resourcepacks for item ids and zh_cn names.

Output: questgen/registry.json  {"items": {id: name_or_empty}, "lang": {key: text}}
"""
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "registry.json"

MODEL_RE = re.compile(r"^assets/([a-z0-9_.\-]+)/models/item/(.+)\.json$")
LANG_RE = re.compile(r"^assets/([a-z0-9_.\-]+)/lang/(zh_cn|en_us)\.json$")

items: dict[str, str] = {}
lang_zh: dict[str, str] = {}
lang_en: dict[str, str] = {}


def load_lang(text: str, target: dict):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # some mods ship lang with comments / trailing commas
        try:
            cleaned = re.sub(r"//.*", "", text)
            cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
            data = json.loads(cleaned)
        except Exception:
            return
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, str):
                target[k] = v


def scan_zip(path: Path):
    try:
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                m = MODEL_RE.match(name)
                if m:
                    items.setdefault(f"{m.group(1)}:{m.group(2)}", "")
                    continue
                m = LANG_RE.match(name)
                if m:
                    raw = z.read(name).decode("utf-8", errors="ignore")
                    load_lang(raw, lang_zh if m.group(2) == "zh_cn" else lang_en)
    except zipfile.BadZipFile:
        pass


def scan_dir(base: Path):
    for p in base.rglob("*.json"):
        rel = p.relative_to(base).as_posix()
        m = MODEL_RE.match(rel)
        if m:
            items.setdefault(f"{m.group(1)}:{m.group(2)}", "")
            continue
        m = LANG_RE.match(rel)
        if m:
            load_lang(p.read_text("utf-8", errors="ignore"), lang_zh if m.group(2) == "zh_cn" else lang_en)


for jar in sorted((ROOT / "mods").glob("*.jar")):
    scan_zip(jar)
    # nested jars (jar-in-jar) e.g. mekanism generators, create addons
    try:
        with zipfile.ZipFile(jar) as z:
            for name in z.namelist():
                if name.startswith("META-INF/jarjar/") and name.endswith(".jar"):
                    tmp = OUT.parent / "_nested.jar"
                    tmp.write_bytes(z.read(name))
                    scan_zip(tmp)
                    tmp.unlink()
    except zipfile.BadZipFile:
        pass

# vanilla client jar
for v in ROOT.glob("*.jar"):
    scan_zip(v)

scan_dir(ROOT / "kubejs")
for rp in (ROOT / "resourcepacks").iterdir():
    if rp.is_dir():
        scan_dir(rp)
    elif rp.suffix == ".zip":
        scan_zip(rp)

# kubejs startup-registered items may have no model file: parse custom_item.js
for js in (ROOT / "kubejs" / "startup_scripts").glob("*.js"):
    for m in re.finditer(r"\.create\(\s*['\"]([a-z0-9_:/]+)['\"]", js.read_text("utf-8", errors="ignore")):
        iid = m.group(1) if ":" in m.group(1) else f"kubejs:{m.group(1)}"
        items.setdefault(iid, "")


def name_of(iid: str) -> str:
    ns, path = iid.split(":", 1)
    key_tail = path.replace("/", ".")
    for prefix in ("item", "block"):
        k = f"{prefix}.{ns}.{key_tail}"
        if k in lang_zh:
            return lang_zh[k]
    for prefix in ("item", "block"):
        k = f"{prefix}.{ns}.{key_tail}"
        if k in lang_en:
            return lang_en[k]
    return ""


for iid in items:
    items[iid] = name_of(iid)

# ids that only appear as lang keys (code-generated models etc.) -> "probable"
probable: dict[str, str] = {}
KEY_RE = re.compile(r"^(item|block)\.([a-z0-9_]+)\.([a-z0-9_.]+)$")
for src in (lang_en, lang_zh):
    for k in src:
        m = KEY_RE.match(k)
        if m:
            iid = f"{m.group(2)}:{m.group(3).replace('.', '/')}"
            if iid not in items and iid not in probable:
                probable[iid] = lang_zh.get(k) or lang_en.get(k, "")

# item tags from data/*/tags/items/**.json (jars) + kubejs tags.js event.add('ns:tag', ...)
TAG_RE = re.compile(r"^data/([a-z0-9_.\-]+)/tags/items/(.+)\.json$")
tags: set[str] = set()
for jar in sorted((ROOT / "mods").glob("*.jar")):
    try:
        with zipfile.ZipFile(jar) as z:
            for n in z.namelist():
                m = TAG_RE.match(n)
                if m:
                    tags.add(f"{m.group(1)}:{m.group(2)}")
    except zipfile.BadZipFile:
        pass
for js in (ROOT / "kubejs" / "server_scripts").rglob("*.js"):
    for m in re.finditer(r"\.add\(\s*['\"]([a-z0-9_.\-]+:[a-z0-9_/.\-]+)['\"]", js.read_text("utf-8", errors="ignore")):
        tags.add(m.group(1))
for p in (ROOT / "kubejs" / "data").rglob("*.json"):
    m = TAG_RE.match(p.relative_to(ROOT / "kubejs").as_posix())
    if m:
        tags.add(f"{m.group(1)}:{m.group(2)}")

# items hidden from JEI by the pack (usually disabled / unobtainable): explicit ids in hide.js
hidden: list[str] = []
hide_js = ROOT / "kubejs" / "client_scripts" / "hide.js"
if hide_js.exists():
    src = hide_js.read_text("utf-8", errors="ignore")
    src = re.sub(r"//.*", "", src)
    start = src.find("JEIEvents.hideItems")
    if start >= 0:
        hidden = sorted(set(re.findall(r"['\"]([a-z0-9_.\-]+:[a-z0-9_/.\-]+)['\"]", src[start:])))

OUT.write_text(json.dumps({"items": dict(sorted(items.items())), "probable": dict(sorted(probable.items())),
                           "tags": sorted(tags), "hidden": hidden}, ensure_ascii=False, indent=0), "utf-8")
print(len(hidden), "hidden")
print(len(items), "items;", len(probable), "probable;", len(tags), "tags")
