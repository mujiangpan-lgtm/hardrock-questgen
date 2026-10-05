"""Build FTB Quests SNBT + decorative PNGs from questgen/chapters/*.py.

    python questgen/build.py          # validate + write
    python questgen/build.py --check  # validate only
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import qlib  # noqa: E402
from qlib import B, D, L, Fl, CHAPTERS, ERRORS, WARNINGS, THEMES, Item, Task, Reward, hid  # noqa: E402

ROOT = HERE.parent
STAGE = "--stage" in sys.argv  # write into questgen/_stage instead of the live pack
SROOT = HERE / os.environ.get("QGEN_STAGE", "_stage")
QDIR = (SROOT / "quests") if STAGE else ROOT / "config" / "ftbquests" / "quests"
TEX_DIR = (SROOT / "textures") if STAGE else ROOT / "kubejs" / "assets" / "kubejs" / "textures" / "quests"
TEX_NS = "kubejs:textures/quests/"
# FTB Quests theme override: per-chapter tiled backgrounds (selector = chapter id)
THEME_FILE = (SROOT / "ftb_quests_theme.txt") if STAGE else ROOT / "kubejs" / "assets" / "ftbquests" / "ftb_quests_theme.txt"

try:  # per-chapter art direction; chapters without an entry keep the classic look
    from art_styles import STYLES  # noqa: E402
except ImportError:
    STYLES = {}
# ... plus one JSON file per chapter in questgen/art_styles.d/<chapter key>.json (overrides art_styles.py)
for _f in sorted((HERE / "art_styles.d").glob("*.json")):
    try:
        import json as _json
        STYLES[_f.stem] = _json.loads(_f.read_text("utf-8"))
    except ValueError as _e:  # a half-written file must not break other chapters' builds
        WARNINGS.append(f"art style {_f.name} skipped: {_e}")

GROUPS = [
    ("survival", "生存之道"),
    ("ages", "金属时代"),
    ("industry", "工业革命"),
    ("frontier", "远方与星辰"),
]

PX = 48  # pixels per quest-grid unit for generated panels


# ---------------------------------------------------------------- SNBT writer
def _key(k: str) -> str:
    return k if all(c.isalnum() or c in "_-.+" for c in k) else '"' + k.replace('"', '\\"') + '"'


def _str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def snbt(v, ind=0) -> str:
    t = "\t"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, D):
        return f"{round(float(v), 4)!r}d"
    if isinstance(v, Fl):
        return f"{float(v)!r}f"
    if isinstance(v, L):
        return f"{int(v)}L"
    if isinstance(v, B):
        return f"{int(v)}b"
    if isinstance(v, float):
        return f"{v!r}d"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return _str(v)
    if isinstance(v, dict):
        if not v:
            return "{ }"
        lines = [f"{t * (ind + 1)}{_key(k)}: {snbt(v[k], ind + 1)}" for k in sorted(v)]
        return "{\n" + "\n".join(lines) + f"\n{t * ind}}}"
    if isinstance(v, (list, tuple)):
        if not v:
            return "[ ]"
        if all(isinstance(x, str) for x in v) and len(v) == 1:
            return f"[{snbt(v[0])}]"
        lines = [f"{t * (ind + 1)}{snbt(x, ind + 1)}" for x in v]
        return "[\n" + "\n".join(lines) + f"\n{t * ind}]"
    raise TypeError(type(v))


# ---------------------------------------------------------------- serialization
def icon_of(icon):
    if icon is None:
        return None
    if isinstance(icon, Item):
        return icon.stack()
    qlib._check(icon)
    return icon


def ser_task(ch, q, i, t) -> dict:
    tid = hid("task", ch.key, q.key, str(i))
    if isinstance(t, Item):
        d = {"id": tid, "type": "item", "item": t.stack()}
        if t.count > 1:
            d["count"] = L(t.count)
        if t.title:
            d["title"] = t.title
        if t.consume:
            d["consume_items"] = True
        return d
    if isinstance(t, Task):
        return {"id": tid, **t.data}
    raise TypeError(f"{ch.key}:{q.key} bad task {t!r}")


def ser_reward(ch, q, i, r) -> dict:
    rid = hid("reward", ch.key, q.key, str(i))
    if isinstance(r, Item):
        d = {"id": rid, "type": "item", "item": r.stack()}
        if r.count > 1:
            d["count"] = r.count
        return d
    if isinstance(r, Reward):
        return {"id": rid, **r.data}
    raise TypeError(f"{ch.key}:{q.key} bad reward {r!r}")


def styled_shape(ch, shape):
    """Chapter art styles give each quest role (normal/milestone/optional/gate) its own shape."""
    st = STYLES.get(ch.key)
    if not st:
        return shape
    import artlib
    role = artlib.ROLE_OF_SHAPE.get(shape)
    if role is None:  # an explicit non-role shape stays as written
        return shape
    mapped = st["shapes"][role]
    return None if role == "normal" else mapped  # normal quests inherit default_quest_shape


def ser_quest(ch, q) -> dict:
    d = {"id": ch.qid(q.key), "title": q.title, "x": D(q.x), "y": D(q.y)}
    if q.subtitle:
        d["subtitle"] = q.subtitle
    desc = []
    for line in q.desc:
        desc.extend(line.split("\n"))
    st = STYLES.get(ch.key)
    if st:  # key terms (&6) take the chapter's own colour
        hx = "&" + st["palette"]["text_key_hex"]
        desc = [ln.replace("&6", hx) for ln in desc]
    if desc:
        d["description"] = desc
    ic = icon_of(q.icon)
    if ic:
        d["icon"] = ic
    shape = styled_shape(ch, q.shape)
    if shape:
        d["shape"] = shape
    if q.size != 1.0:
        d["size"] = D(q.size)
    if q.optional:
        d["optional"] = True
    if q.deps:
        d["dependencies"] = [ch.qid(r) for r in q.deps]
        if q.any_dep and len(q.deps) > 1:
            d["dependency_requirement"] = "one_completed"
    if q.hide_lines:
        d["hide_dependency_lines"] = True
    if not q.tasks:
        ERRORS.append(f"{ch.key}:{q.key} has no tasks")
    d["tasks"] = [ser_task(ch, q, i, t) for i, t in enumerate(q.tasks)]
    if q.rewards:
        d["rewards"] = [ser_reward(ch, q, i, r) for i, r in enumerate(q.rewards)]
    return d


# ---------------------------------------------------------------- images
def font(size, kind="kai"):
    from PIL import ImageFont
    f = {"kai": "simkai.ttf", "bold": "msyhbd.ttc", "hei": "msyh.ttc"}[kind]
    p = Path(f"C:/Windows/Fonts/{f}")
    return ImageFont.truetype(str(p if p.exists() else _noto(kind)), size)


_NOTO = {"kai": ("NotoSerifCJK-Regular", "NotoSerifSC-Regular", "NotoSansCJK-Regular"),
         "bold": ("NotoSansCJK-Bold", "NotoSansSC-Bold", "NotoSansCJK-Regular"),
         "hei": ("NotoSansCJK-Regular", "NotoSansSC-Regular")}


def _noto(kind):
    """Machines without the Windows fonts (cloud previews): a Noto CJK font from the system font dirs."""
    found = {p.stem: p for d in ("/usr/share/fonts", "/usr/local/share/fonts", str(Path.home() / ".fonts"))
             for p in Path(d).rglob("*") if p.suffix in (".ttc", ".otf", ".ttf")}
    for stem in _NOTO[kind]:
        if stem in found:
            return found[stem]
    sys.exit("no CJK font: install fonts-noto-cjk (apt) or put a Noto Sans/Serif CJK font into ~/.fonts")


def chapter_colors(ch):
    st = STYLES.get(ch.key)
    if st:
        return tuple(st["palette"]["panel_fill"]), tuple(st["palette"]["accent"])
    return THEMES[ch.theme]


def draw_panel(path: Path, w_units, h_units, header_units, title, colors):
    from PIL import Image, ImageDraw
    fill, accent = colors
    W, H, HH = int(w_units * PX), int(h_units * PX), int(header_units * PX)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    r = 18
    dr.rounded_rectangle([2, 2, W - 3, H - 3], r, fill=fill + (150,), outline=accent + (170,), width=3)
    # header band: vertical gradient
    band = Image.new("RGBA", (W, HH), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    for yy in range(HH):
        a = int(150 * (1 - yy / HH) + 40)
        bd.line([(0, yy), (W, yy)], fill=accent + (a // 3,))
    mask = Image.new("L", (W, HH), 0)
    ImageDraw.Draw(mask).rounded_rectangle([4, 4, W - 5, HH + r], r - 2, fill=255)
    img.paste(band, (0, 0), mask)
    dr.line([(r, HH), (W - r, HH)], fill=accent + (200,), width=2)
    # title: full size with diamond ornaments if it fits; else drop the ornaments and use the full width;
    # if it would still shrink below a readable size, set "第N节" small above the name (two lines)
    full, min_fs = int(HH * 0.55), int(HH * 0.44)

    def fit(text, room, cap):
        fs = cap
        while fs > 10 and dr.textlength(text, font=font(fs, "bold")) > room:
            fs -= 1
        return fs

    lines = [(title, full)]
    ornaments = dr.textlength(title, font=font(full, "bold")) <= W - 2 * (r + 22)
    if not ornaments:
        fs1 = fit(title, W - 2 * 12, full)
        lines = [(title, fs1)]
        if fs1 < min_fs and "·" in title:
            head, name = (t.strip() for t in title.split("·", 1))
            fs_b = fit(name, W - 2 * 12, int(HH * 0.5))
            fs_a = min(int(HH * 0.36), fs_b)
            if fs_b > fs1:
                lines = [(head, fs_a), (name, fs_b)]
    if ornaments:
        for cx in (r + 6, W - r - 6):
            cy = HH // 2
            dr.polygon([(cx, cy - 7), (cx + 7, cy), (cx, cy + 7), (cx - 7, cy)], fill=accent + (230,))
    boxes = [dr.textbbox((0, 0), t, font=font(fs, "bold")) for t, fs in lines]
    gap = 1
    total = sum(b[3] - b[1] for b in boxes) + gap * (len(lines) - 1)
    y = (HH - total) / 2 + (1 if len(lines) == 1 else 0)
    for (t, fs), b in zip(lines, boxes):
        f = font(fs, "bold")
        tx, ty = (W - (b[2] - b[0])) / 2 - b[0], y - b[1]
        if ornaments:  # unchanged placement for titles that always fitted
            tx, ty = (W - dr.textlength(t, font=f)) / 2, HH * 0.18
        dr.text((tx + 2, ty + 2), t, font=f, fill=(0, 0, 0, 160))
        dr.text((tx, ty), t, font=f, fill=accent + (255,))
        y += b[3] - b[1] + gap
    img.save(path)


def draw_banner(path: Path, title, subtitle, theme):
    from PIL import Image, ImageDraw
    fill, accent = THEMES[theme]
    W, H = 1280, 256
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    # horizontal fade ribbon
    for xx in range(W):
        k = 1 - abs(xx - W / 2) / (W / 2)
        a = int(210 * min(1, k * 1.6))
        dr.line([(xx, 40), (xx, H - 40)], fill=fill + (a,))
        if k > 0.04:
            dr.point((xx, 40), fill=accent + (int(255 * min(1, k * 1.5)),))
            dr.point((xx, 41), fill=accent + (int(255 * min(1, k * 1.5)),))
            dr.point((xx, H - 41), fill=accent + (int(255 * min(1, k * 1.5)),))
            dr.point((xx, H - 42), fill=accent + (int(255 * min(1, k * 1.5)),))
    ft = font(92, "kai")
    tw = dr.textlength(title, font=ft)
    tx, ty = (W - tw) / 2, 52
    for ox, oy in ((3, 3), (2, 2)):
        dr.text((tx + ox, ty + oy), title, font=ft, fill=(0, 0, 0, 170))
    dr.text((tx, ty), title, font=ft, fill=accent + (255,))
    # side ornaments
    for side in (-1, 1):
        cx = W / 2 + side * (tw / 2 + 50)
        cy = ty + 50
        dr.polygon([(cx, cy - 12), (cx + 12, cy), (cx, cy + 12), (cx - 12, cy)], fill=accent + (240,))
        x2 = cx + side * 160
        dr.line([(cx + side * 16, cy), (x2, cy)], fill=accent + (200,), width=3)
    if subtitle:
        fs = font(34, "hei")
        sw = dr.textlength(subtitle, font=fs)
        dr.text(((W - sw) / 2, 160), subtitle, font=fs, fill=(235, 230, 220, 230))
    img.save(path)


def quest_bounds(qs):
    xs0 = [q.x - q.size / 2 for q in qs]
    xs1 = [q.x + q.size / 2 for q in qs]
    ys0 = [q.y - q.size / 2 for q in qs]
    ys1 = [q.y + q.size / 2 for q in qs]
    return min(xs0), min(ys0), max(xs1), max(ys1)


def chapter_images(ch, write: bool) -> list[dict]:
    imgs = []
    if not ch.quests:
        return imgs
    x0, y0, x1, y1 = quest_bounds(ch.quests.values())
    header = 0.9
    top = y0
    pb = (x0, y0, x1, y1)  # content box including section panels (for decorations only)
    for si, s in enumerate(ch.sections):
        missing = [k for k in s.keys if k not in ch.quests]
        if missing:
            ERRORS.append(f"{ch.key}: section '{s.title}' unknown keys {missing}")
            continue
        sx0, sy0, sx1, sy1 = quest_bounds([ch.quests[k] for k in s.keys])
        sx0 -= s.pad; sx1 += s.pad; sy1 += s.pad; sy0 -= s.pad + header
        top = min(top, sy0)
        w, h = sx1 - sx0, sy1 - sy0
        fname = f"{ch.key}_s{si}.png"
        if write:
            draw_panel(TEX_DIR / fname, w, h, header, s.title, chapter_colors(ch))
        imgs.append({"image": TEX_NS + fname, "x": D((sx0 + sx1) / 2), "y": D((sy0 + sy1) / 2),
                     "width": D(w), "height": D(h), "rotation": D(0), "order": -10})
        pb = (min(pb[0], sx0), min(pb[1], sy0), max(pb[2], sx1), max(pb[3], sy1))
    # banner centered over content (styled banners carry icons and art, so they are larger)
    st = STYLES.get(ch.key)
    bw = 20.0 if st else 10.0
    bh = bw / 5
    fname = f"{ch.key}_banner.png"
    bx, by = (x0 + x1) / 2, top - bh / 2 - 0.2
    if write:
        if st:
            import artlib
            artlib.banner(TEX_DIR / fname, ch.title, ch.subtitle[0] if ch.subtitle else "", st, font, ch.key)
        else:
            draw_banner(TEX_DIR / fname, ch.title, ch.subtitle[0] if ch.subtitle else "", ch.theme)
    imgs.append({"image": TEX_NS + fname, "x": D(bx), "y": D(by),
                 "width": D(bw), "height": D(bh), "rotation": D(0), "order": -5})
    if st:
        content = (pb[0], min(pb[1], by - bh / 2), pb[2], pb[3])
        imgs.extend(chapter_decor(ch, st, content, (bx, by, bw, bh), write))
        if st.get("scene"):
            import artlib
            qx0, qy0, qx1, qy1 = quest_bounds(ch.quests.values())
            scx, scy, sw, sh = artlib.scene_box(content, st["scene"], ((qx0 + qx1) / 2, (qy0 + qy1) / 2))
            fname = f"{ch.key}_scene.png"
            if write:
                artlib.scene(TEX_DIR / fname, st["scene"], sw, sh, f"{ch.key}:scene")
            imgs.append({"image": TEX_NS + fname, "x": D(scx), "y": D(scy), "width": D(sw), "height": D(sh),
                         "rotation": D(0), "order": -30})
    imgs.extend(ch.extra_images)
    return imgs


def chapter_decor(ch, st, bounds, banner_box, write) -> list[dict]:
    """Large, faint map-space decorations behind panels and banner (art_styles 'decor')."""
    import artlib
    out = []
    for i, dc in enumerate(st.get("decor", [])):
        w, h = artlib.decor_size(dc["motif"], dc["size_units"])
        cx, cy = artlib.anchor_center(dc["anchor"], bounds, banner_box, w, h)
        fname = f"{ch.key}_d{i}.png"
        if write:
            artlib.decor(TEX_DIR / fname, dc["motif"], w, h, dc["color"], dc["alpha"], f"{ch.key}:{i}")
        out.append({"image": TEX_NS + fname, "x": D(cx), "y": D(cy), "width": D(w), "height": D(h),
                    "rotation": D(0), "order": -20 + i})
    return out


def write_backgrounds_and_theme(write: bool):
    """Tiled chapter backgrounds go through the FTB Quests theme file, selected by chapter id."""
    styled = [ch for ch in CHAPTERS.values() if ch.key in STYLES]
    if not write:
        return
    import artlib
    lines = ["# Generated by questgen/build.py from questgen/art_styles.py - do not edit by hand.",
             "# One section per chapter: [<chapter id>] -> tiled background for that chapter.", ""]
    for ch in styled:
        st = STYLES[ch.key]
        fname = f"{ch.key}_bg.png"
        artlib.background_tile(st["background"], ch.key).save(TEX_DIR / fname)
        tile = artlib.GRID * int(st["background"].get("tile_size", 48))
        lines += [f"[{hid('chapter', ch.key)}]",
                  f"background: {TEX_NS}{fname}; color=#FFFFFFFF; tile_size={tile}", ""]
    THEME_FILE.parent.mkdir(parents=True, exist_ok=True)
    if styled:
        THEME_FILE.write_text("\n".join(lines), "utf-8")
    elif THEME_FILE.exists():
        THEME_FILE.unlink()


# ---------------------------------------------------------------- validation
def validate():
    all_ids = {}
    for ch in CHAPTERS.values():
        for q in ch.quests.values():
            all_ids[(ch.key, q.key)] = q
    for ch in CHAPTERS.values():
        if ch.group and ch.group not in dict(GROUPS):
            ERRORS.append(f"{ch.key}: unknown group {ch.group}")
        if ch.key != "00_welcome":
            for k in ("start", "finale"):
                if k not in ch.quests:
                    ERRORS.append(f"{ch.key}: missing contract quest key '{k}'")
        # section panels must not overlap each other
        boxes = []
        for s in ch.sections:
            if all(k in ch.quests for k in s.keys):
                bx0, by0, bx1, by1 = quest_bounds([ch.quests[k] for k in s.keys])
                boxes.append((s.title, bx0 - s.pad, by0 - s.pad - 0.9, bx1 + s.pad, by1 + s.pad))
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    ERRORS.append(f"{ch.key}: section panels overlap '{a[0]}' / '{b[0]}'")
        qs = list(ch.quests.values())
        for q in qs:
            for r in q.deps:
                ck, qk = r.split(":", 1) if ":" in r else (ch.key, r)
                # in --only mode other chapters aren't loaded: accept their contract keys
                if ONLY and ck not in CHAPTERS:
                    if qk not in ("start", "finale"):
                        WARNINGS.append(f"{ch.key}:{q.key} -> {r} (chapter not loaded, unchecked)")
                    continue
                if (ck, qk) not in all_ids:
                    ERRORS.append(f"{ch.key}:{q.key} unknown dependency {r}")
        for i, a in enumerate(qs):
            for b in qs[i + 1:]:
                if math.hypot(a.x - b.x, a.y - b.y) < (a.size + b.size) / 2 * 0.95:
                    ERRORS.append(f"{ch.key}: quests overlap {a.key} / {b.key}")
    # cycle check
    graph = {(ck, qk): [tuple(r.split(":", 1)) if ":" in r else (ck, r) for r in q.deps]
             for (ck, qk), q in all_ids.items()}
    state = {}

    def dfs(n, stack):
        state[n] = 1
        for m in graph.get(n, []):
            if state.get(m) == 1:
                ERRORS.append(f"dependency cycle: {' -> '.join(':'.join(s) for s in stack + [m])}")
            elif m in graph and not state.get(m):
                dfs(m, stack + [m])
        state[n] = 2

    for n in graph:
        if not state.get(n):
            dfs(n, [n])
    # chapter art styles: every texture must exist, every value inside the vocabulary
    styled = [k for k in STYLES if k in CHAPTERS]
    if styled:
        import artlib
        for k in styled:
            ERRORS.extend(artlib.validate(STYLES[k], k))


# ---------------------------------------------------------------- main
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None


def load_chapters():
    for p in sorted((HERE / "chapters").glob("*.py")):
        if ONLY and p.stem not in ONLY:
            continue
        spec = importlib.util.spec_from_file_location(f"chapters.{p.stem}", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)


def main():
    write = "--check" not in sys.argv
    if ONLY and write and not STAGE:
        sys.exit("--only requires --check or --stage (a live write would drop other chapters)")
    load_chapters()
    validate()
    gid = {k: hid("group", k) for k, _ in GROUPS}
    out = {}
    if write:
        TEX_DIR.mkdir(parents=True, exist_ok=True)
        for old in TEX_DIR.glob("*.png"):
            old.unlink()
    for ch in CHAPTERS.values():
        quests = [ser_quest(ch, q) for q in ch.quests.values()]
        d = {
            "id": hid("chapter", ch.key), "filename": ch.key, "title": ch.title,
            "group": gid.get(ch.group, ""), "order_index": ch.order,
            "icon": icon_of(ch.icon),
            "default_quest_shape": STYLES[ch.key]["shapes"]["normal"] if ch.key in STYLES else ch.default_shape,
            "default_hide_dependency_lines": False, "quest_links": [],
            "images": chapter_images(ch, write), "quests": quests,
        }
        if ch.subtitle:
            d["subtitle"] = ch.subtitle
        if ch.autofocus:
            d["autofocus_id"] = ch.qid(ch.autofocus)
        out[ch.key] = d
    for w in WARNINGS:
        print("WARN", w)
    if ERRORS:
        for e in sorted(set(ERRORS)):
            print("ERROR", e)
        print(f"{len(set(ERRORS))} errors")
        sys.exit(1)
    nq = sum(len(c.quests) for c in CHAPTERS.values())
    print(f"OK: {len(CHAPTERS)} chapters, {nq} quests")
    if not write:
        return
    write_backgrounds_and_theme(write)
    cdir = QDIR / "chapters"
    cdir.mkdir(parents=True, exist_ok=True)
    for old in cdir.glob("*.snbt"):
        old.unlink()
    for k, d in out.items():
        (cdir / f"{k}.snbt").write_text(snbt(d) + "\n", "utf-8")
    groups = {"chapter_groups": [{"id": gid[k], "title": t} for k, t in GROUPS]}
    (QDIR / "chapter_groups.snbt").write_text(snbt(groups) + "\n", "utf-8")
    data = {
        "default_autoclaim_rewards": "disabled", "default_consume_items": False,
        "default_quest_disable_jei": False, "default_quest_shape": "circle",
        "default_reward_team": True, "detection_delay": 5, "disable_gui": False,
        "drop_book_on_death": False, "drop_loot_crates": False, "emergency_items_cooldown": 300,
        "grid_scale": D(0.5), "hide_excluded_quests": False, "icon": "tfc:stone/axe/sedimentary",
        "lock_message": "&7完成前置任务后解锁", "loot_crate_no_drop": {"boss": 0, "monster": 600, "passive": 4000},
        "pause_game": False, "progression_mode": "flexible", "show_lock_icons": True,
        "title": "&6HardRock &7· &f群峦求生录", "version": 13,
    }
    (QDIR / "data.snbt").write_text(snbt(data) + "\n", "utf-8")
    print("written to", QDIR)


if __name__ == "__main__":
    main()
