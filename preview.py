"""Render a rough layout preview of chapters (panels, banner, quests, dep lines).

    python questgen/preview.py 10_stone_age [more ...]   -> questgen/_stage/preview_<key>.png
Run `build.py --stage --only ...` first (same QGEN_STAGE env) so panel/banner PNGs exist in _stage/textures.

Set QPREVIEW_SCREEN=29,55 to also render what the player actually sees: a 1460x1050 quest view at
GUI scale 4, with the map at 29 (and 55) screen px per quest unit, the screen-space tiled background,
item icons in the nodes and no quest titles (FTB only shows them on hover)
-> preview_screen<ppu>_<key>.png
"""
import math
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.argv = [sys.argv[0], "--check", "--only", ",".join(sys.argv[1:])]
import build  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

build.load_chapters()
U = 48
TEX = build.SROOT / "textures"
SCREEN = [int(v) for v in os.environ.get("QPREVIEW_SCREEN", "").split(",") if v.strip()]


def _poly(shape, cx, cy, r):
    if shape == "diamond":
        return [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    if shape in ("hexagon", "pentagon", "octagon"):
        n = {"hexagon": 6, "pentagon": 5, "octagon": 8}[shape]
        off = -math.pi / 2 + (math.pi / n if n == 8 else 0)
        return [(cx + r * math.cos(off + 2 * math.pi * k / n), cy + r * math.sin(off + 2 * math.pi * k / n))
                for k in range(n)]
    if shape == "gear":
        return [(cx + (r if k % 4 in (1, 2) else r * 0.8) * math.cos(k * math.pi / 24),
                 cy + (r if k % 4 in (1, 2) else r * 0.8) * math.sin(k * math.pi / 24)) for k in range(48)]
    if shape in ("square", "rsquare"):
        rr = r * 0.9
        return [(cx - rr, cy - rr), (cx + rr, cy - rr), (cx + rr, cy + rr), (cx - rr, cy + rr)]
    if shape == "heart":
        return [(cx, cy + r), (cx - r, cy - r * 0.1), (cx - r * 0.5, cy - r * 0.8), (cx, cy - r * 0.35),
                (cx + r * 0.5, cy - r * 0.8), (cx + r, cy - r * 0.1)]
    return [(cx + r * math.cos(k * math.pi / 16), cy + r * math.sin(k * math.pi / 16)) for k in range(32)]


def _icon_tex(icon):
    import artlib
    iid = icon if isinstance(icon, str) else (icon or {}).get("id") if isinstance(icon, dict) else None
    if not iid or ":" not in iid:
        return None
    ns, path = iid.split(":", 1)
    for cand in (f"{ns}:item/{path}", f"{ns}:block/{path}", f"{ns}:item/{path.split('/')[-1]}",
                 f"{ns}:block/{path.split('/')[-1]}"):
        if artlib.has_tex(cand):
            return artlib.tex(cand)
    return None


def render_screen(ch, imgs, ppu, gui=4, vw=1460, vh=1050):
    """Approximate the in-game quest view: what the player actually sees."""
    import artlib
    qs = list(ch.quests.values())
    cx = (min(q.x for q in qs) + max(q.x for q in qs)) / 2
    cy = (min(q.y for q in qs) + max(q.y for q in qs)) / 2
    can = Image.new("RGBA", (vw, vh), (24, 24, 28, 255))
    bg = TEX / f"{ch.key}_bg.png"
    if ch.key in build.STYLES and bg.exists():
        t = Image.open(bg).convert("RGBA")
        side = int(build.STYLES[ch.key]["background"].get("tile_size", 32) * artlib.GRID * gui)
        t = t.resize((side, side), Image.NEAREST)
        for x in range(0, vw, side):
            for y in range(0, vh, side):
                can.alpha_composite(t, (x, y))
    S = lambda x, y: (int(vw / 2 + (x - cx) * ppu), int(vh / 2 + (y - cy) * ppu))  # noqa: E731
    for im in sorted(imgs, key=lambda i: i.get("order", 0)):
        f = TEX / im["image"].split("/")[-1]
        if not f.exists():
            continue
        w, h = int(im["width"] * ppu), int(im["height"] * ppu)
        if w < 2 or h < 2:
            continue
        pic = Image.open(f).convert("RGBA").resize((w, h), Image.BILINEAR)
        x, y = S(im["x"] - im["width"] / 2, im["y"] - im["height"] / 2)
        layer = Image.new("RGBA", can.size, (0, 0, 0, 0))
        layer.paste(pic, (x, y))
        can.alpha_composite(layer)
    dr = ImageDraw.Draw(can)
    lw = max(2, int(0.17 * ppu * 0.6))
    for q in qs:
        if q.hide_lines:
            continue
        for d in q.deps:
            if ":" in d:
                continue
            o = ch.quests[d]
            dr.line([S(o.x, o.y), S(q.x, q.y)], fill=(204, 163, 163, 180), width=lw)
    default = build.STYLES[ch.key]["shapes"]["normal"] if ch.key in build.STYLES else "circle"
    for q in qs:
        shape = build.styled_shape(ch, q.shape) or default
        r = q.size / 2 * ppu * 0.95
        px, py = S(q.x, q.y)
        dr.polygon(_poly(shape, px, py, r), fill=(48, 48, 54, 235), outline=(210, 210, 210, 255))
        ic = _icon_tex(build.icon_of(q.icon))
        if ic is not None:
            s = max(4, int(r * 1.15))
            ic = ic.crop((0, 0, ic.size[0], ic.size[0])).resize((s, s), Image.NEAREST)
            can.alpha_composite(ic, (int(px - s / 2), int(py - s / 2)))
    return can


for ch in build.CHAPTERS.values():
    imgs = build.chapter_images(ch, write=False)
    xs = [i["x"] - i["width"] / 2 for i in imgs] + [q.x - q.size for q in ch.quests.values()]
    ys = [i["y"] - i["height"] / 2 for i in imgs] + [q.y - q.size for q in ch.quests.values()]
    xe = [i["x"] + i["width"] / 2 for i in imgs] + [q.x + q.size for q in ch.quests.values()]
    ye = [i["y"] + i["height"] / 2 for i in imgs] + [q.y + q.size for q in ch.quests.values()]
    ox, oy = min(xs) - 1, min(ys) - 1
    W, H = int((max(xe) - ox + 1) * U), int((max(ye) - oy + 1) * U)
    canvas = Image.new("RGBA", (W, H), (24, 24, 28, 255))
    bg = TEX / f"{ch.key}_bg.png"
    if ch.key in build.STYLES and bg.exists():  # screen-space tiled background, approximated
        import artlib
        tile = Image.open(bg).convert("RGBA")
        # FTB's default zoom shows roughly 24 GUI px per quest unit; tile_size is GUI px per block
        gui_px = build.STYLES[ch.key]["background"].get("tile_size", 48)
        cell = max(4, int(U * gui_px / 24))
        tile = tile.resize((cell * artlib.GRID, cell * artlib.GRID), Image.NEAREST)
        for tx in range(0, W, tile.size[0]):
            for ty in range(0, H, tile.size[1]):
                canvas.alpha_composite(tile, (tx, ty))
    P = lambda x, y: (int((x - ox) * U), int((y - oy) * U))  # noqa: E731
    for im in sorted(imgs, key=lambda i: i.get("order", 0)):
        f = TEX / im["image"].split("/")[-1]
        if not f.exists():
            continue
        pic = Image.open(f).convert("RGBA").resize((int(im["width"] * U), int(im["height"] * U)))
        canvas.alpha_composite(pic, P(im["x"] - im["width"] / 2, im["y"] - im["height"] / 2))
    dr = ImageDraw.Draw(canvas)
    for q in ch.quests.values():
        if q.hide_lines:
            continue
        for d in q.deps:
            if ":" in d:
                continue
            o = ch.quests[d]
            dr.line([P(o.x, o.y), P(q.x, q.y)], fill=(200, 200, 200, 160), width=2)
    fnt = build.font(11, "hei")
    default = build.STYLES[ch.key]["shapes"]["normal"] if ch.key in build.STYLES else "circle"
    for q in ch.quests.values():
        r = q.size / 2 * U * 0.9
        cx, cy = P(q.x, q.y)
        col = (120, 120, 140) if q.optional else (220, 200, 140)
        shape = build.styled_shape(ch, q.shape) or default
        kw = dict(fill=(40, 40, 50), outline=col)
        if shape == "diamond":
            dr.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], **kw)
        elif shape in ("hexagon", "pentagon", "octagon"):
            n = {"hexagon": 6, "pentagon": 5, "octagon": 8}[shape]
            dr.regular_polygon((cx, cy, r), n, rotation=0 if n != 8 else 22.5, **kw)
        elif shape == "gear":
            pts = [(cx + (r if k % 4 in (1, 2) else r * 0.8) * math.cos(k * math.pi / 24),
                    cy + (r if k % 4 in (1, 2) else r * 0.8) * math.sin(k * math.pi / 24)) for k in range(48)]
            dr.polygon(pts, **kw)
        elif shape in ("square", "rsquare"):
            rr = r * 0.88
            dr.rounded_rectangle([cx - rr, cy - rr, cx + rr, cy + rr], int(rr * 0.35) if shape == "rsquare" else 0,
                                 width=2, **kw)
        elif shape == "heart":
            dr.polygon([(cx, cy + r), (cx - r, cy - r * 0.1), (cx - r * 0.5, cy - r * 0.8), (cx, cy - r * 0.35),
                        (cx + r * 0.5, cy - r * 0.8), (cx + r, cy - r * 0.1)], **kw)
        else:
            dr.ellipse([cx - r, cy - r, cx + r, cy + r], width=2, **kw)
        tw = dr.textlength(q.title, font=fnt)
        dr.text((cx - tw / 2, cy + r + 2), q.title, font=fnt, fill=(255, 255, 255))
    out = build.SROOT / f"preview_{ch.key}.png"
    canvas.convert("RGB").save(out)
    print(out)
    for ppu in SCREEN:
        out = build.SROOT / f"preview_screen{ppu}_{ch.key}.png"
        render_screen(ch, imgs, ppu).convert("RGB").save(out)
        print(out)
