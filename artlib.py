"""Chapter art for the quest book: themed tiled backgrounds, banners and map decorations.

The base material is real Minecraft pixel art read straight from the installed jars, so every
chapter can be dressed in the blocks and items of its own era. Atmosphere (glows, silhouettes,
planets, cogs ...) is drawn procedurally on top. build.py calls this module; the per-chapter
specs live in art_styles.py. Nothing in here is hand-edited art.
"""
from __future__ import annotations

import inspect
import io
import math
import random
import zipfile
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent

SHAPES = {"circle", "square", "rsquare", "diamond", "pentagon", "hexagon", "octagon", "gear", "heart"}
BG_OVERLAYS = {"none", "speckle", "starfield", "blueprint_grid", "strata", "gear_ghosts", "nebula"}
BANNER_MOTIFS = {"mountains", "strata", "cogs", "planet_rings", "starfield", "nebula", "flames", "none"}
ANCHORS = {"top_left", "top_right", "bottom_left", "bottom_right", "behind_banner", "left_edge", "right_edge",
           "center"}
# role of a quest, derived from the shape the chapter source gives it
ROLE_OF_SHAPE = {None: "normal", "circle": "normal", "hexagon": "milestone", "diamond": "optional", "gear": "gate"}

CELL, TEXEL, GRID = 16, 2, 8          # background tile: 8x8 blocks, each texel drawn 2x2 px -> 256 px
BW, BH = 1600, 320                    # banner, shown as 10 x 2 grid units
DECOR_PX = 64                         # decoration pixels per grid unit


# ---------------------------------------------------------------- textures from jars
_INDEX: dict | None = None
# extracted textures for machines without the pack (see CLOUD_TASK.md); unused when the jars are present
PACKDATA = Path(__file__).resolve().parent / "_packdata" / "textures"


def _index() -> dict:
    global _INDEX
    if _INDEX is None:
        idx = {}
        jars = sorted((ROOT / "mods").glob("*.jar")) + sorted(ROOT.glob("*.jar"))
        for j in jars:
            try:
                z = zipfile.ZipFile(j)
            except zipfile.BadZipFile:
                continue
            with z:
                for n in z.namelist():
                    if n.startswith("assets/") and n.endswith(".png") and "/textures/" in n:
                        ns, rest = n[7:].split("/textures/", 1)
                        idx.setdefault(f"{ns}:{rest[:-4]}", (j, n))
        if not jars and PACKDATA.is_dir():  # no pack here (cloud): block/item textures extracted from the jars
            for p in PACKDATA.rglob("*.png"):
                ns, *rest = p.relative_to(PACKDATA).parts
                idx.setdefault(f"{ns}:{'/'.join(rest)[:-4]}", (None, p))
        _INDEX = idx
    return _INDEX


def has_tex(asset: str) -> bool:
    return asset in _index()


@lru_cache(None)
def tex(asset: str) -> Image.Image:
    """Texture by 'namespace:path' (path under assets/<ns>/textures/, no .png). First frame only."""
    if asset not in _index():
        raise KeyError(f"texture not found in any jar: {asset}")
    j, n = _index()[asset]
    if j is None:
        im = Image.open(n).convert("RGBA")
    else:
        with zipfile.ZipFile(j) as z:
            im = Image.open(io.BytesIO(z.read(n))).convert("RGBA")
    w, h = im.size
    if h > w and h % w == 0:  # animated strip
        im = im.crop((0, 0, w, w))
    return im


def _cell(asset: str, back=(12, 13, 14)) -> Image.Image:
    t = tex(asset)
    if t.size != (CELL, CELL):
        t = t.resize((CELL, CELL), Image.NEAREST)
    base = Image.new("RGBA", t.size, back + (255,))
    base.alpha_composite(t)
    return base.convert("RGB")


# ---------------------------------------------------------------- colour helpers
def _arr(img) -> np.ndarray:
    return np.asarray(img, dtype=np.float32) / 255.0


def _img(a: np.ndarray, mode="RGB") -> Image.Image:
    return Image.fromarray(np.clip(a * 255 + 0.5, 0, 255).astype(np.uint8), mode)


def _mix(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def _periodic_noise(size, cells, rng, octaves=3) -> np.ndarray:
    """Seamless smooth noise in [0,1], size x size, tiling on both axes."""
    acc = np.zeros((size, size), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        c = cells * (2 ** o)
        g = np.array([[rng.random() for _ in range(c)] for _ in range(c)], np.float32)
        big = np.tile(g, (3, 3))
        im = Image.fromarray((big * 255).astype(np.uint8), "L").resize((size * 3, size * 3), Image.BICUBIC)
        a = np.asarray(im, np.float32)[size:2 * size, size:2 * size] / 255.0
        acc += a * amp
        tot += amp
        amp *= 0.5
    acc /= tot
    acc -= acc.min()
    return acc / max(acc.max(), 1e-6)


def _wrap_copies(x, y, r, size):
    for dx in (-size, 0, size):
        for dy in (-size, 0, size):
            if -r <= x + dx <= size + r and -r <= y + dy <= size + r:
                yield x + dx, y + dy


def _gear_poly(cx, cy, r, teeth, depth=0.18, rot=0.0):
    pts = []
    n = teeth * 4
    for i in range(n):
        a = rot + 2 * math.pi * i / n
        rr = r if (i % 4) in (1, 2) else r * (1 - depth)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


# ---------------------------------------------------------------- background tile
LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)


def _process(a: np.ndarray, sat, tint) -> np.ndarray:
    """Desaturate around Rec.709 luma, then multiply by the tint (both on 0..1 sRGB)."""
    g = (a @ LUMA)[..., None]
    a = g + sat * (a - g)
    if tint:
        a = a * (np.array(tint, np.float32) / 255.0)
    return a


def _compress(a: np.ndarray, target_sd) -> np.ndarray:
    m = a.reshape(-1, 3).mean(0)
    sd = float((a @ LUMA).std())
    f = min(1.0, target_sd / max(sd, 1e-6))
    return m + (a - m) * f


def background_tile(spec: dict, seed: str) -> Image.Image:
    """Seamless dark tile: 8x8 blocks (128 texels), every texture normalised to the same mean
    luma so nothing checkerboards, contrast squeezed so white text stays readable on top,
    overlay drawn at texel resolution with wrap-around, then nearest-upscaled (TEXEL px/texel)."""
    rng = random.Random(seed)
    sat, tint = float(spec.get("saturation", 0.6)), spec.get("tint")
    target = float(spec.get("target_brightness", 0.15))
    tiles = [(t["asset"], max(1, int(t.get("weight", 1)))) for t in spec["tiles"]]
    proc = {}
    for asset, _ in tiles:
        a = _process(_arr(_cell(asset)), sat, tint)
        proc[asset] = a * (target / max(float((a @ LUMA).mean()), 1e-4))
    n = CELL * GRID
    a = np.zeros((n, n, 3), np.float32)
    for gy in range(GRID):
        for gx in range(GRID):
            asset = rng.choices([t for t, _ in tiles], [w for _, w in tiles])[0]
            a[gy * CELL:(gy + 1) * CELL, gx * CELL:(gx + 1) * CELL] = proc[asset]
    a *= target / max(float((a @ LUMA).mean()), 1e-4)
    a = np.clip(_compress(a, float(spec.get("contrast_sd", 0.022))), 0, 1)
    a = _texel_overlay(a, spec.get("overlay") or {"type": "none", "density": 0}, rng)
    img = _img(np.clip(a, 0, 1))
    img = img.resize((n * TEXEL, n * TEXEL), Image.NEAREST)
    return _bg_overlay_hi(img, spec.get("overlay") or {}, rng)


def _texel_overlay(a, ov, rng) -> np.ndarray:
    """Pixel-scale overlays (1 texel = 1 dot), wrap-safe by construction."""
    kind, dens = ov.get("type", "none"), float(ov.get("density", 0))
    col = np.array(ov.get("color") or (255, 255, 255), np.float32) / 255.0
    n = a.shape[0]
    if kind == "speckle":  # 1.0 = 0.7 % of texels; 60 % ember colour at 35 %, 40 % soot
        for _ in range(int(n * n * 0.007 * dens)):
            y, x = rng.randrange(n), rng.randrange(n)
            if rng.random() < 0.6:
                a[y, x] = a[y, x] * 0.65 + col * 0.35
            else:
                a[y, x] = a[y, x] * 0.4
    elif kind == "starfield":  # 1.0 = 2 % of texels, single pixels at alpha 0.35-0.8
        for _ in range(int(n * n * 0.02 * dens)):
            y, x = rng.randrange(n), rng.randrange(n)
            al = rng.uniform(0.35, 0.8) * (0.5 + 0.5 * rng.random() ** 2)
            a[y, x] = a[y, x] * (1 - al) + col * al
    elif kind == "strata":
        for _ in range(int(3 + dens * 6)):
            y0, m, ph = rng.uniform(0, n), rng.choice((1, 2)), rng.uniform(0, 6.28)
            amp, k = rng.uniform(1, 4), rng.choice((0.85, 1.12))
            for x in range(n):
                y = int(y0 + amp * math.sin(2 * math.pi * m * x / n + ph)) % n
                a[y, x] *= k
    elif kind == "blueprint_grid":
        al = 0.05 + 0.12 * dens
        for k in range(0, n, CELL):
            a[k, :] = a[k, :] * (1 - al) + col * al
            a[:, k] = a[:, k] * (1 - al) + col * al
    elif kind == "nebula":
        noise = _periodic_noise(n, 3, rng)
        al = ((np.clip(noise - 0.35, 0, 1) / 0.65) ** 1.6 * 0.5 * dens)[..., None]
        a = a * (1 - al) + col * al
    return a


def _bg_overlay_hi(img, ov, rng) -> Image.Image:
    """Line-art overlays drawn after upscaling (smoother outlines)."""
    if ov.get("type") != "gear_ghosts":
        return img
    dens = float(ov.get("density", 0.5))
    col = tuple(ov.get("color") or (255, 255, 255))
    size = img.size[0]
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    al = int(255 * 0.10)  # 1.0 = 6 wrapped outlines per tile, 8-12 teeth, line alpha 0.10
    for _ in range(max(1, round(6 * dens))):
        x, y, r = rng.uniform(0, size), rng.uniform(0, size), rng.uniform(size * 0.08, size * 0.2)
        teeth, rot = rng.choice((8, 10, 12)), rng.random()
        for X, Y in _wrap_copies(x, y, r + 4, size):
            d.polygon(_gear_poly(X, Y, r, teeth, rot=rot), outline=col + (al,))
            d.ellipse([X - r * 0.35, Y - r * 0.35, X + r * 0.35, Y + r * 0.35], outline=col + (al,))
    out = img.convert("RGBA")
    out.alpha_composite(lay)
    return out.convert("RGB")


# ---------------------------------------------------------------- banner
def _ribbon_mask(w, h) -> Image.Image:
    x = np.linspace(-1, 1, w, dtype=np.float32)
    kx = np.clip((1 - np.abs(x)) * 1.7, 0, 1)
    y = np.arange(h, dtype=np.float32)
    feather = 16.0
    ky = np.clip(np.minimum(y, h - 1 - y) / feather, 0, 1)
    return _img(np.outer(ky, kx) * 0.94, "L")


def _icon(asset, scale) -> Image.Image:
    t = tex(asset)
    if t.size != (CELL, CELL):
        t = t.resize((CELL, CELL), Image.NEAREST)
    return t.resize((CELL * scale, CELL * scale), Image.NEAREST)


def _glow_of(img_rgba, color, radius, strength=1.0) -> Image.Image:
    a = img_rgba.getchannel("A").filter(ImageFilter.GaussianBlur(radius))
    if strength != 1.0:
        a = a.point(lambda v: min(255, int(v * strength)))
    g = Image.new("RGBA", img_rgba.size, tuple(color) + (0,))
    g.putalpha(a)
    return g


def banner(path: Path, title: str, subtitle: str, style: dict, font, seed: str):
    pal, b = style["palette"], style["banner"]
    fill, accent, glow = tuple(pal["panel_fill"]), tuple(pal["accent"]), tuple(pal["glow"])
    rng = random.Random(seed + ":banner")
    img = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    top, bot = 54, BH - 54
    rh = bot - top
    # ribbon of the chapter's own block texture
    ca = _process(_arr(_cell(b["ribbon_asset"])), 0.75, style["background"].get("tint"))
    ca = ca * (0.22 / max(float((ca @ LUMA).mean()), 1e-4))
    ca = np.clip(_compress(ca, 0.045), 0, 1)
    scale = 8
    tile = _img(ca).resize((CELL * scale, CELL * scale), Image.NEAREST)
    rib = Image.new("RGB", (BW, rh))
    for x in range(0, BW, tile.size[0]):
        for y in range(0, rh, tile.size[1]):
            rib.paste(tile, (x, y))
    mask = _ribbon_mask(BW, rh)
    layer = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    rl = rib.convert("RGBA")
    rl.putalpha(mask)
    layer.paste(rl, (0, top))
    img.alpha_composite(layer)
    full_mask = Image.new("L", (BW, BH), 0)
    full_mask.paste(mask, (0, top))
    # procedural motif, clipped to the ribbon
    mot = _banner_motif(b.get("motif", "none"), tuple(b.get("motif_color") or accent), top, bot, rng)
    mot.putalpha(ImageChops.multiply(mot.getchannel("A"), full_mask))
    img.alpha_composite(mot)
    # title metrics
    probe = ImageDraw.Draw(img)
    n_icons = min(3, max(len(b.get("icons_left", [])), len(b.get("icons_right", []))))
    room = BW - 2 * (150 + 125 * n_icons)
    fs = 104
    ft = font(fs, "kai")
    tw = probe.textlength(title, font=ft)
    while tw > room and fs > 56:
        fs -= 4
        ft = font(fs, "kai")
        tw = probe.textlength(title, font=ft)
    tx, ty = (BW - tw) / 2, top + 10 + (104 - fs) * 0.5
    # soft light behind the title
    gl = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    ImageDraw.Draw(gl).ellipse([BW / 2 - tw / 2 - 120, top + 18, BW / 2 + tw / 2 + 120, bot - 18], fill=glow + (120,))
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(42)))
    # accent rules
    d = ImageDraw.Draw(img)
    for xx in range(BW):
        k = 1 - abs(xx - BW / 2) / (BW / 2)
        if k <= 0.03:
            continue
        a = int(255 * min(1, k * 1.5))
        for yy in (top, top + 1, bot - 1, bot - 2):
            d.point((xx, yy), fill=accent + (a,))
    # item icons with shadow and glow
    cy = (top + bot) / 2 - 6
    for side, key in ((-1, "icons_left"), (1, "icons_right")):
        for i, asset in enumerate(b.get(key, [])[:3]):
            ic = _icon(asset, 6)
            s = ic.size[0]
            cx = BW / 2 + side * (tw / 2 + 95 + i * 125)
            x, y = int(cx - s / 2), int(cy - s / 2)
            sh = Image.new("RGBA", ic.size, (0, 0, 0, 0))
            sh.putalpha(ic.getchannel("A").point(lambda v: int(v * 0.6)))
            pad = 24
            canvas = Image.new("RGBA", (s + 2 * pad, s + 2 * pad), (0, 0, 0, 0))
            canvas.alpha_composite(sh, (pad + 6, pad + 7))
            canvas = canvas.filter(ImageFilter.GaussianBlur(4))
            gpad = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            gpad.alpha_composite(ic, (pad, pad))
            canvas.alpha_composite(_glow_of(gpad, glow, 10, 0.55))
            canvas.alpha_composite(ic, (pad, pad))
            img.alpha_composite(canvas, (x - pad, y - pad))
    # diamonds between title and icons
    for side in (-1, 1):
        dx = BW / 2 + side * (tw / 2 + 38)
        dy = ty + fs * 0.55
        d.polygon([(dx, dy - 10), (dx + 10, dy), (dx, dy + 10), (dx - 10, dy)], fill=accent + (235,))
    # title: glow, shadow, gradient fill
    tm = Image.new("L", (BW, BH), 0)
    ImageDraw.Draw(tm).text((tx, ty), title, font=ft, fill=255)
    tg = Image.new("RGBA", (BW, BH), glow + (0,))
    tg.putalpha(tm.filter(ImageFilter.GaussianBlur(9)).point(lambda v: min(255, int(v * 1.1))))
    img.alpha_composite(tg)
    shadow = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    shadow.putalpha(ImageChops.offset(tm, 3, 4).point(lambda v: int(v * 0.7)))
    img.alpha_composite(shadow)
    grad = np.zeros((BH, BW, 4), np.float32)
    hi, lo = np.array(_mix(accent, (255, 255, 255), 0.7), np.float32), np.array(accent, np.float32)
    t = np.clip((np.arange(BH, dtype=np.float32) - ty) / max(fs, 1), 0, 1)[:, None]
    grad[..., :3] = (hi * (1 - t) + lo * t)[:, None, :].repeat(BW, 1) / 255.0
    grad[..., 3] = _arr(tm)
    img.alpha_composite(_img(grad, "RGBA"))
    if subtitle:
        fs2 = font(36, "hei")
        sw = d.textlength(subtitle, font=fs2)
        sy = bot - 62
        d.text(((BW - sw) / 2 + 2, sy + 2), subtitle, font=fs2, fill=(0, 0, 0, 150))
        d.text(((BW - sw) / 2, sy), subtitle, font=fs2, fill=(238, 232, 222, 240))
    img.save(path)


def _banner_motif(kind, color, top, bot, rng) -> Image.Image:
    lay = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    if kind == "mountains":
        for layer_i, (base, amp, a) in enumerate(((bot - 20, 70, 55), (bot - 6, 50, 85))):
            pts = _ridge(BW, base, amp, rng)
            d.polygon(pts + [(BW, bot), (0, bot)], fill=color + (a,))
    elif kind == "strata":
        for i in range(6):
            y0 = top + 20 + i * (bot - top - 30) / 6
            m, ph, amp = rng.choice((1, 2, 3)), rng.uniform(0, 6.28), rng.uniform(4, 12)
            pts = [(x, y0 + amp * math.sin(2 * math.pi * m * x / BW + ph)) for x in range(0, BW + 8, 8)]
            d.line(pts, fill=color + (rng.randint(30, 60),), width=rng.randint(3, 8))
    elif kind == "cogs":
        for side in (-1, 1):
            for r, ox, oy, teeth in ((120, 150, 30, 14), (70, 300, -40, 10)):
                cx, cy = BW / 2 + side * (BW / 2 - ox), (top + bot) / 2 + oy
                d.polygon(_gear_poly(cx, cy, r, teeth, rot=rng.random()), fill=color + (60,))
                d.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32], fill=(0, 0, 0, 0))
    elif kind == "planet_rings":
        R = 900
        cx, cy = BW / 2, bot + R - 70
        d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=color + (40,))
        d.ellipse([cx - R - 6, cy - R - 6, cx + R + 6, cy + R + 6], outline=color + (110,), width=3)
        d.ellipse([60, top + 70, BW - 60, bot + 40], outline=color + (55,), width=4)
        lay = _stars_into(lay, color, 70, top, bot, rng)
    elif kind == "starfield":
        lay = _stars_into(lay, color, 160, top, bot, rng)
    elif kind == "nebula":
        n = _periodic_noise(256, 4, rng)
        im = Image.fromarray((n * 255).astype(np.uint8), "L").resize((BW, BH), Image.BICUBIC)
        a = np.asarray(im, np.float32) / 255.0
        a = (np.clip(a - 0.3, 0, 1) / 0.7) ** 1.5 * 0.55
        rgba = np.zeros((BH, BW, 4), np.float32)
        rgba[..., :3] = np.array(color, np.float32) / 255.0
        rgba[..., 3] = a
        lay = _img(rgba, "RGBA")
        lay = _stars_into(lay, (255, 255, 255), 90, top, bot, rng)
    elif kind == "flames":
        for _ in range(26):
            x = rng.uniform(0, BW)
            h = rng.uniform(40, 120)
            w = rng.uniform(16, 40)
            d.polygon([(x - w, bot), (x, bot - h), (x + w, bot)], fill=color + (rng.randint(30, 70),))
        lay = lay.filter(ImageFilter.GaussianBlur(6))
    return lay


def _ridge(w, base, amp, rng, n=9):
    xs = np.linspace(0, w, n)
    ys = [base - rng.uniform(0.2, 1.0) * amp for _ in xs]
    pts = []
    for (x0, y0), (x1, y1) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
        for t in np.linspace(0, 1, 8, endpoint=False):
            pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + rng.uniform(-4, 4)))
    pts.append((w, ys[-1]))
    return pts


def _stars_into(lay, color, n, top, bot, rng):
    d = ImageDraw.Draw(lay)
    for _ in range(n):
        x, y = rng.uniform(0, BW), rng.uniform(top, bot)
        b = rng.random() ** 2
        a = int(70 + 185 * b)
        if rng.random() < 0.08:
            d.line([(x - 6, y), (x + 6, y)], fill=tuple(color) + (a // 2,))
            d.line([(x, y - 6), (x, y + 6)], fill=tuple(color) + (a // 2,))
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=tuple(color) + (a,))
        else:
            d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=tuple(color) + (a,))
    return lay


# ---------------------------------------------------------------- map decorations
DECOR_ASPECT = {"mountain_range": 3.0, "strata_band": 4.0}


def decor_size(motif, size_units):
    asp = DECOR_ASPECT.get(motif, 1.0)
    return size_units, size_units / asp


def decor(path: Path, motif: str, w_units, h_units, color, alpha, seed: str):
    rng = random.Random(seed)
    W = max(32, min(1600, int(w_units * DECOR_PX)))
    H = max(32, min(1600, int(h_units * DECOR_PX)))
    color = tuple(color)
    img = _DECOR[motif](W, H, color, rng)
    a = img.getchannel("A").point(lambda v: int(v * max(0.0, min(1.0, alpha))))
    img.putalpha(a)
    img.save(path)


def _ss(W, H):
    return Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))


def _down(img, W, H):
    return img.resize((W, H), Image.LANCZOS)


def _shade(img, strength=0.45, outline=0.55):
    """Give a flat silhouette volume: light from the top-left, darker rim, so it sits with pixel art."""
    W, H = img.size
    a = np.asarray(img, np.float32) / 255
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    g = 1 + strength * (0.5 - (x / max(W, 1) * 0.5 + y / max(H, 1) * 0.5)) * 2
    rgb = a[..., :3] * g[..., None]
    al = Image.fromarray((a[..., 3] * 255).astype(np.uint8), "L")
    rad = max(1, int(min(W, H) * 0.012)) * 2 + 1
    inner = np.asarray(al.filter(ImageFilter.MinFilter(rad)), np.float32) / 255
    rim = np.clip(a[..., 3] - inner, 0, 1)[..., None]
    rgb = rgb * (1 - rim * outline)
    out = np.concatenate([np.clip(rgb, 0, 1), a[..., 3:4]], axis=2)
    return _img(out, "RGBA")


def _d_cog(W, H, color, rng, teeth=None):
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    r = min(W, H) * 0.98
    cx, cy = W, H
    d.polygon(_gear_poly(cx, cy, r, teeth or rng.choice((10, 12, 14)), rot=rng.random()), fill=color + (255,))
    d.ellipse([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62], fill=_mix(color, (0, 0, 0), 0.35) + (255,))
    d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5], fill=color + (255,))
    for k in range(6):
        a = k * math.pi / 3 + 0.3
        x, y = cx + r * 0.33 * math.cos(a), cy + r * 0.33 * math.sin(a)
        d.ellipse([x - r * 0.08, y - r * 0.08, x + r * 0.08, y + r * 0.08], fill=(0, 0, 0, 0))
    d.ellipse([cx - r * 0.14, cy - r * 0.14, cx + r * 0.14, cy + r * 0.14], fill=(0, 0, 0, 0))
    return _shade(_down(im, W, H))


def _d_gear_cluster(W, H, color, rng):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s = min(W, H)
    for frac, ox, oy, t in ((0.62, 0.36, 0.38, 14), (0.42, 0.74, 0.62, 10), (0.3, 0.3, 0.82, 8)):
        g = _d_cog(int(s * frac), int(s * frac), color, rng, t)
        im.alpha_composite(g, (int(W * ox - g.size[0] / 2), int(H * oy - g.size[1] / 2)))
    return im


def _sphere(W, H, color, rng, bands=False, craters=False, atmo=True):
    s = min(W, H)
    r = s * 0.42
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    nx, ny = (x - W / 2) / r, (y - H / 2) / r
    rr = nx ** 2 + ny ** 2
    inside = rr <= 1
    nz = np.sqrt(np.clip(1 - rr, 0, 1))
    light = np.clip(-0.55 * nx - 0.6 * ny + 0.58 * nz, 0, 1)
    shade = 0.18 + 0.82 * light
    base = np.array(color, np.float32) / 255.0
    rgb = np.ones((H, W, 3), np.float32) * base
    if bands:
        n = _periodic_noise(64, 4, rng, 2)
        nb = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H)), np.float32) / 255
        stripe = 0.5 + 0.5 * np.sin(ny * 9 + nb * 3)
        rgb = rgb * (0.75 + 0.35 * stripe[..., None])
    if craters:
        cm = np.zeros((H, W), np.float32)
        for _ in range(14):
            cxp, cyp, cr = rng.uniform(-0.8, 0.8), rng.uniform(-0.8, 0.8), rng.uniform(0.05, 0.2)
            dd = np.sqrt((nx - cxp) ** 2 + (ny - cyp) ** 2)
            cm += np.clip(1 - dd / cr, 0, 1) * 0.5
        rgb = rgb * (1 - 0.35 * np.clip(cm, 0, 1)[..., None])
    rgb = rgb * shade[..., None]
    alpha = inside.astype(np.float32)
    edge = np.clip((1 - np.sqrt(rr)) * r / 1.5, 0, 1)
    alpha = alpha * edge
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = rgb
    out[..., 3] = alpha
    img = _img(out, "RGBA")
    if atmo:
        ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse([W / 2 - r - 4, H / 2 - r - 4, W / 2 + r + 4, H / 2 + r + 4],
                                     outline=_mix(color, (255, 255, 255), 0.4) + (200,), width=max(3, int(r * 0.05)))
        ring = ring.filter(ImageFilter.GaussianBlur(max(2, r * 0.05)))
        ring.alpha_composite(img)
        img = ring
    return img


def _d_planet(W, H, color, rng):
    return _sphere(W, H, color, rng, bands=True)


def _d_moon(W, H, color, rng):
    return _sphere(W, H, color, rng, craters=True, atmo=False)


def _d_ringed_planet(W, H, color, rng):
    s = min(W, H)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ring_col = _mix(color, (255, 255, 255), 0.3)
    back = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    db = ImageDraw.Draw(back)
    box = [W * 0.03, H / 2 - W * 0.11, W * 0.97, H / 2 + W * 0.11]
    for k, a in ((0, 200), (int(s * 0.035), 110)):
        db.ellipse([box[0] + k, box[1] + k * 0.25, box[2] - k, box[3] - k * 0.25], outline=ring_col + (a,),
                   width=max(3, int(s * 0.025)))
    upper = back.crop((0, 0, W, int(H / 2)))
    img.alpha_composite(upper, (0, 0))
    planet = _sphere(int(s * 0.8), int(s * 0.8), color, rng, bands=True)
    img.alpha_composite(planet, (int(W / 2 - planet.size[0] / 2), int(H / 2 - planet.size[1] / 2)))
    lower = back.crop((0, int(H / 2), W, H))
    img.alpha_composite(lower, (0, int(H / 2)))
    return img


def _d_nebula_glow(W, H, color, rng):
    n = _periodic_noise(128, 3, rng)
    im = Image.fromarray((n * 255).astype(np.uint8), "L").resize((W, H), Image.BICUBIC)
    a = np.asarray(im, np.float32) / 255
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    fall = np.clip(1 - np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2), 0, 1)
    a = (np.clip(a - 0.25, 0, 1) / 0.75) ** 1.3 * fall ** 0.8
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    out[..., 3] = a
    return _img(out, "RGBA").filter(ImageFilter.GaussianBlur(3))


def _d_soft_glow(W, H, color, rng):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    rr = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    out[..., 3] = np.clip(1 - rr, 0, 1) ** 2
    return _img(out, "RGBA")


def _d_mountain_range(W, H, color, rng):
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    for i, (base, amp, a) in enumerate(((H2 * 0.75, H2 * 0.55, 120), (H2 * 0.88, H2 * 0.45, 200), (H2 * 1.0, H2 * 0.3, 255))):
        pts = _ridge(W2, base, amp, rng, n=10)
        d.polygon(pts + [(W2, H2), (0, H2)], fill=_mix(color, (0, 0, 0), 0.25 * i) + (a,))
    im = _down(im, W, H)
    return _fade_sides(_fade_bottom(im))


def _fade_sides(im, frac=0.12):
    """Ramp alpha to zero over the outer `frac` of the width (no hard vertical cut at the ends)."""
    W, H = im.size
    x = np.minimum(np.arange(W), W - 1 - np.arange(W)).astype(np.float32) / max(1.0, W * frac)
    t = np.clip(x, 0, 1)
    g = t * t * (3 - 2 * t)
    a = np.asarray(im.getchannel("A"), np.float32) * g[None, :]
    im.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    return im


def _fade_bottom(im):
    W, H = im.size
    t = np.clip((1 - np.linspace(0, 1, H, dtype=np.float32)) / 0.4, 0, 1)
    g = t * t * (3 - 2 * t)  # smoothstep to zero over the bottom 40 %
    a = np.asarray(im.getchannel("A"), np.float32) * g[:, None]
    im.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    return im


def _d_strata_band(W, H, color, rng):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(7):
        y0 = H * (0.1 + 0.8 * i / 7)
        m, ph, amp = rng.choice((1, 2)), rng.uniform(0, 6.28), H * rng.uniform(0.02, 0.06)
        pts = [(x, y0 + amp * math.sin(2 * math.pi * m * x / W + ph)) for x in range(0, W + 6, 6)]
        d.line(pts, fill=_mix(color, (0, 0, 0), rng.uniform(0, 0.4)) + (rng.randint(120, 230),),
               width=max(2, int(H * rng.uniform(0.03, 0.08))))
    x = np.linspace(-1, 1, W, dtype=np.float32)
    fade = np.clip((1 - np.abs(x)) * 2.5, 0, 1)
    a = np.asarray(im.getchannel("A"), np.float32) * fade[None, :]
    im.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    return im


def _d_arrowhead(W, H, color, rng):
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    tip, base_y = (W2 * 0.5, H2 * 0.04), H2 * 0.78
    left, right = (W2 * 0.18, base_y), (W2 * 0.82, base_y)
    notch_l, notch_r, stem = (W2 * 0.36, H2 * 0.88), (W2 * 0.64, H2 * 0.88), (W2 * 0.5, H2 * 0.96)
    poly = [tip, right, notch_r, stem, notch_l, left]
    d.polygon(poly, fill=color + (255,))
    light, dark = _mix(color, (255, 255, 255), 0.12), _mix(color, (0, 0, 0), 0.3)
    for _ in range(9):  # knapping facets
        a = rng.uniform(0.1, 0.9)
        p0 = (left[0] + (tip[0] - left[0]) * a, left[1] + (tip[1] - left[1]) * a) if rng.random() < 0.5 else \
            (right[0] + (tip[0] - right[0]) * a, right[1] + (tip[1] - right[1]) * a)
        p1 = (W2 * 0.5 + rng.uniform(-0.05, 0.05) * W2, p0[1] + rng.uniform(0.05, 0.15) * H2)
        p2 = (p0[0] + (p1[0] - p0[0]) * 0.3, p1[1] + rng.uniform(0.05, 0.1) * H2)
        d.polygon([p0, p1, p2], fill=(light if rng.random() < 0.5 else dark) + (255,))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    im.putalpha(ImageChops.multiply(im.getchannel("A"), mask))
    return _down(im, W, H)


def _d_hand_print(W, H, color, rng):
    """Cave-art hand stencil: sprayed pigment with the hand left bare."""
    hand = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(hand)
    s = min(W, H)
    cx, cy = W / 2, H * 0.62
    d.ellipse([cx - s * 0.2, cy - s * 0.2, cx + s * 0.2, cy + s * 0.22], fill=255)
    for ang, ln, wd in ((-58, 0.3, 0.07), (-20, 0.4, 0.075), (0, 0.44, 0.075), (20, 0.4, 0.07), (45, 0.3, 0.065)):
        a = math.radians(ang - 90)
        x0, y0 = cx + math.cos(a) * s * 0.12, cy - s * 0.08 + math.sin(a) * s * 0.12
        x1, y1 = x0 + math.cos(a) * s * ln, y0 + math.sin(a) * s * ln
        d.line([(x0, y0), (x1, y1)], fill=255, width=int(s * wd * 2))
        d.ellipse([x1 - s * wd, y1 - s * wd, x1 + s * wd, y1 + s * wd], fill=255)
    if rng.random() < 0.5:
        hand = hand.transpose(Image.FLIP_LEFT_RIGHT)
    halo = hand.filter(ImageFilter.MaxFilter(int(s * 0.12) | 1)).filter(ImageFilter.GaussianBlur(s * 0.06))
    spray = np.asarray(halo, np.float32) / 255
    noise = np.random.default_rng(rng.randrange(1 << 30)).random(spray.shape).astype(np.float32)
    a = np.clip(spray * (0.55 + 0.6 * noise), 0, 1) * (1 - np.asarray(hand, np.float32) / 255)
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    out[..., 3] = a
    return _img(out, "RGBA")


def _d_star_cluster(W, H, color, rng):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(int(W * H / 1600) + 12):
        x, y = rng.gauss(W / 2, W / 5), rng.gauss(H / 2, H / 5)
        b = rng.random() ** 2
        a = int(90 + 165 * b)
        r = 1 + 2 * b
        if b > 0.75:
            d.line([(x - r * 4, y), (x + r * 4, y)], fill=color + (a // 2,))
            d.line([(x, y - r * 4), (x, y + r * 4)], fill=color + (a // 2,))
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (a,))
    g = im.filter(ImageFilter.GaussianBlur(3))
    g.alpha_composite(im)
    return g


def _d_orbit_ring(W, H, color, rng):
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    box = [W2 * 0.04, H2 * 0.3, W2 * 0.96, H2 * 0.7]
    d.ellipse(box, outline=color + (220,), width=max(2, int(min(W2, H2) * 0.008)))
    for _ in range(3):
        t = rng.uniform(0, 2 * math.pi)
        x = W2 / 2 + (box[2] - box[0]) / 2 * math.cos(t)
        y = H2 / 2 + (box[3] - box[1]) / 2 * math.sin(t)
        r = min(W2, H2) * rng.uniform(0.015, 0.03)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (255,))
    return _down(im, W, H)


def _d_sky_band(W, H, color, rng):
    """Horizontal band of coloured light (dusk sky, firelit haze, galactic glow)."""
    y = np.linspace(-1, 1, H, dtype=np.float32)
    x = np.linspace(-1, 1, W, dtype=np.float32)
    prof = np.exp(-(y / 0.45) ** 2)
    side = np.clip((1 - np.abs(x)) / 0.25, 0, 1)
    side = side * side * (3 - 2 * side)
    n = _periodic_noise(64, 3, rng, 2)
    nb = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    a = np.outer(prof, side) * (0.7 + 0.3 * nb)
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    out[..., 3] = a
    return _img(out, "RGBA")


def _d_embers(W, H, color, rng):
    """Rising sparks: denser and brighter towards the bottom."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(int(W * H / 1500) + 12):
        x = rng.uniform(0, W)
        y = H * (1 - rng.betavariate(1.2, 2.6))
        k = y / H
        r = rng.uniform(0.8, 2.4) * (0.6 + 0.6 * k)
        a = int(rng.uniform(90, 255) * (0.35 + 0.65 * k))
        c = _mix(color, (255, 236, 180), rng.random() * 0.5)
        d.ellipse([x - r, y - r, x + r, y + r], fill=c + (a,))
    g = im.filter(ImageFilter.GaussianBlur(4))
    g.alpha_composite(im)
    return g


def _d_milky_way(W, H, color, rng):
    """A band of dense small stars with a soft glow; rotate it into a diagonal when placing."""
    y = np.linspace(-1, 1, H, dtype=np.float32)
    x = np.linspace(-1, 1, W, dtype=np.float32)
    prof = np.exp(-(y / 0.42) ** 2)
    side = np.clip((1 - np.abs(x)) / 0.3, 0, 1)
    n = _periodic_noise(96, 4, rng, 3)
    nb = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    a = np.outer(prof, side) * np.clip(nb * 1.3 - 0.2, 0, 1) * 0.45
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    out[..., 3] = a
    im = _img(out, "RGBA").filter(ImageFilter.GaussianBlur(4))
    d = ImageDraw.Draw(im)
    for _ in range(int(W * H / 90)):
        px, py = rng.uniform(0, W), rng.gauss(H / 2, H / 5)
        if not 0 <= py < H:
            continue
        k = math.exp(-((py - H / 2) / (H * 0.25)) ** 2) * min(1, (1 - abs(px / W * 2 - 1)) / 0.3)
        if rng.random() > k:
            continue
        b = rng.random() ** 2
        c = _mix((255, 255, 255), color, rng.random() * 0.6)
        if b > 0.92:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=c + (int(200 * k) + 55,))
        else:
            d.point((px, py), fill=c + (int((90 + 165 * b) * k),))
    return im


def _d_comet(W, H, color, rng):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hx, hy = W * 0.86, H * 0.5
    tail = np.zeros((H, W), np.float32)
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    t = np.clip((hx - x) / (hx * 0.95), 0, 1)
    half = (H * 0.04) + (H * 0.32) * t
    inside = np.abs(y - hy) < half
    tail = np.where(inside & (x <= hx), (1 - t) ** 1.4 * (1 - np.abs(y - hy) / np.maximum(half, 1)), 0)
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    out[..., 3] = np.clip(tail, 0, 1) * 0.8
    im = _img(out, "RGBA").filter(ImageFilter.GaussianBlur(3))
    d = ImageDraw.Draw(im)
    r = H * 0.09
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([hx - r * 3, hy - r * 3, hx + r * 3, hy + r * 3], fill=color + (160,))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(r * 1.5)))
    d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=(255, 255, 255, 255))
    return im


def _d_shaft(W, H, color, rng):
    """A Create-style shaft (horizontal; rotate when placing): rod, segment rings, end caps."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    th = H2 * 0.38
    dark, light = _mix(color, (0, 0, 0), 0.35), _mix(color, (255, 255, 255), 0.25)
    d.rectangle([0, H2 / 2 - th / 2, W2, H2 / 2 + th / 2], fill=color + (255,))
    d.rectangle([0, H2 / 2 - th / 2, W2, H2 / 2 - th / 4], fill=light + (255,))
    step = H2 * 2.2
    x = step / 2
    while x < W2:
        d.rectangle([x - H2 * 0.08, H2 / 2 - th * 0.75, x + H2 * 0.08, H2 / 2 + th * 0.75], fill=dark + (255,))
        x += step
    for cx in (H2 * 0.4, W2 - H2 * 0.4):
        d.ellipse([cx - H2 * 0.4, H2 * 0.1, cx + H2 * 0.4, H2 * 0.9], fill=dark + (255,))
    return _down(im, W, H)


def _d_belt(W, H, color, rng):
    """A Create mechanical belt from the side: a solid rubber band with tread plates around two pulleys,
    an andesite frame inside the loop with bolts, and support legs."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    r = H2 * 0.4
    c1, c2 = (r + H2 * 0.06, H2 * 0.46), (W2 - r - H2 * 0.06, H2 * 0.46)
    rubber, tread = (38, 34, 32), (78, 72, 66)
    frame, fdk = color, _mix(color, (0, 0, 0), 0.4)
    bw = max(4, int(r * 0.28))
    for x in np.linspace(c1[0] + r * 1.2, c2[0] - r * 1.2, 3):  # legs
        d.rectangle([x - H2 * 0.04, c1[1], x + H2 * 0.04, H2], fill=fdk + (255,))
    # frame inside the loop
    _gpoly(im, [(c1[0], c1[1] - r + bw * 0.6), (c2[0], c2[1] - r + bw * 0.6), (c2[0], c2[1] + r - bw * 0.6),
                (c1[0], c1[1] + r - bw * 0.6)], _mix(frame, (255, 255, 255), 0.18), fdk)
    for x in np.arange(c1[0] + r * 0.9, c2[0] - r * 0.5, r * 1.6):
        for y in (c1[1] - r * 0.35, c1[1] + r * 0.35):
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=fdk + (255,))
    # rubber band: stadium outline + tread plates on both runs
    d.rounded_rectangle([c1[0] - r, c1[1] - r, c2[0] + r, c2[1] + r], radius=int(r), outline=rubber + (255,), width=bw)
    for y in (c1[1] - r + bw / 2, c1[1] + r - bw / 2):
        x = c1[0]
        while x < c2[0]:
            d.line([(x, y - bw * 0.35), (x, y + bw * 0.35)], fill=tread + (255,), width=max(2, bw // 4))
            x += bw * 1.1
    d.line([(c1[0], c1[1] - r + 2), (c2[0], c1[1] - r + 2)], fill=(110, 104, 96, 255), width=2)
    for cx, cy in (c1, c2):  # pulleys
        rr = r - bw * 0.9
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=_mix(frame, (0, 0, 0), 0.15) + (255,))
        d.ellipse([cx - rr * 0.8, cy - rr * 0.8, cx + rr * 0.8, cy + rr * 0.8],
                  fill=_mix(frame, (255, 255, 255), 0.12) + (255,))
        for k in range(6):
            a = k * math.pi / 3 + rng.uniform(0, 1)
            d.line([(cx, cy), (cx + rr * 0.75 * math.cos(a), cy + rr * 0.75 * math.sin(a))], fill=fdk + (255,),
                   width=max(2, bw // 3))
        d.rectangle([cx - rr * 0.18, cy - rr * 0.18, cx + rr * 0.18, cy + rr * 0.18], fill=fdk + (255,))
    return _shade(_down(im, W, H), 0.3, 0.3)


def _d_blueprint(W, H, color, rng):
    """Faint technical drawing: grid, gear outlines, construction circles and dimension lines."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    u = DECOR_PX
    for k in range(0, W, u):
        d.line([(k, 0), (k, H)], fill=color + (70 if (k // u) % 4 == 0 else 28,))
    for k in range(0, H, u):
        d.line([(0, k), (W, k)], fill=color + (70 if (k // u) % 4 == 0 else 28,))
    for _ in range(5):
        x, y, r = rng.uniform(0.1, 0.9) * W, rng.uniform(0.1, 0.9) * H, rng.uniform(1.5, 4) * u
        d.polygon(_gear_poly(x, y, r, rng.choice((10, 12, 16)), rot=rng.random()), outline=color + (150,))
        d.ellipse([x - r * 0.4, y - r * 0.4, x + r * 0.4, y + r * 0.4], outline=color + (120,))
        d.line([(x - r * 1.3, y), (x + r * 1.3, y)], fill=color + (90,))
        d.line([(x, y - r * 1.3), (x, y + r * 1.3)], fill=color + (90,))
    for _ in range(4):
        x0, y0 = rng.uniform(0.05, 0.6) * W, rng.uniform(0.1, 0.9) * H
        x1 = x0 + rng.uniform(4, 9) * u
        d.line([(x0, y0), (x1, y0)], fill=color + (130,))
        for xx, s in ((x0, 1), (x1, -1)):
            d.polygon([(xx, y0), (xx + s * 10, y0 - 4), (xx + s * 10, y0 + 4)], fill=color + (130,))
            d.line([(xx, y0 - 10), (xx, y0 + 10)], fill=color + (130,))
    return im


def _d_cave_painting(W, H, color, rng):
    """Ochre rock art: deer, a mammoth and hunters with spears, pigment-textured."""
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    s = min(W, H)
    lw = max(2, int(s * 0.018))

    def j(v):
        return v + rng.uniform(-s * 0.004, s * 0.004)

    def deer(cx, cy, k, face=1):
        bw, bh = s * 0.16 * k, s * 0.07 * k
        d.ellipse([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], fill=255)
        for lx in (-0.38, -0.2, 0.2, 0.38):
            x = cx + lx * bw
            d.line([(x, cy), (j(x - face * s * 0.01 * k), cy + s * 0.11 * k)], fill=255, width=lw)
        nx, ny = cx + face * bw * 0.45, cy - bh * 0.3
        hx, hy = nx + face * s * 0.05 * k, ny - s * 0.08 * k
        d.line([(nx, ny), (hx, hy)], fill=255, width=int(lw * 1.6))
        ex0, ex1 = sorted((hx - face * s * 0.018 * k, hx + face * s * 0.03 * k))
        d.ellipse([ex0, hy - s * 0.014 * k, ex1, hy + s * 0.014 * k], fill=255)
        for t in (-1, 1):
            ax, ay = hx - face * s * 0.005, hy - s * 0.01 * k
            d.line([(ax, ay), (j(ax + t * s * 0.03 * k), ay - s * 0.06 * k)], fill=255, width=lw)
            d.line([(ax + t * s * 0.015 * k, ay - s * 0.03 * k), (j(ax + t * s * 0.045 * k), ay - s * 0.045 * k)],
                   fill=255, width=lw)

    def mammoth(cx, cy, k):
        bw, bh = s * 0.26 * k, s * 0.16 * k
        d.ellipse([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], fill=255)
        d.ellipse([cx + bw * 0.25, cy - bh * 0.75, cx + bw * 0.62, cy - bh * 0.05], fill=255)
        for lx in (-0.3, -0.12, 0.15, 0.32):
            x = cx + lx * bw
            d.line([(x, cy), (x, cy + s * 0.12 * k)], fill=255, width=int(lw * 2.4))
        tx, ty = cx + bw * 0.58, cy - bh * 0.15
        d.line([(tx, ty), (tx + s * 0.03 * k, ty + s * 0.1 * k), (tx + s * 0.05 * k, ty + s * 0.12 * k)], fill=255,
               width=int(lw * 1.4))
        d.arc([tx - s * 0.02 * k, ty - s * 0.01 * k, tx + s * 0.09 * k, ty + s * 0.08 * k], 300, 120, fill=255,
              width=lw)

    def hunter(cx, cy, k, face=1):
        h = s * 0.16 * k
        d.ellipse([cx - h * 0.07, cy - h * 0.5 - h * 0.14, cx + h * 0.07, cy - h * 0.5], fill=255)
        d.line([(cx, cy - h * 0.5), (j(cx), cy)], fill=255, width=lw)
        d.line([(cx, cy), (j(cx - h * 0.15), cy + h * 0.4)], fill=255, width=lw)
        d.line([(cx, cy), (j(cx + h * 0.18), cy + h * 0.38)], fill=255, width=lw)
        d.line([(cx, cy - h * 0.35), (cx + face * h * 0.22, cy - h * 0.48)], fill=255, width=lw)
        d.line([(cx - face * h * 0.3, cy - h * 0.2), (cx + face * h * 0.55, cy - h * 0.62)], fill=255,
               width=max(1, lw - 1))

    mammoth(W * 0.28, H * 0.42, 1.2)
    deer(W * 0.66, H * 0.33, 1.0, -1)
    deer(W * 0.8, H * 0.55, 0.8, -1)
    hunter(W * 0.5, H * 0.62, 1.0, 1)
    hunter(W * 0.42, H * 0.7, 0.85, 1)
    hunter(W * 0.12, H * 0.68, 0.8, 1)
    a = np.asarray(im.filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    noise = np.random.default_rng(rng.randrange(1 << 30)).random(a.shape).astype(np.float32)
    a = a * (0.55 + 0.45 * noise)
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    out[..., 3] = a
    return _img(out, "RGBA")


def _teardrop(cx, base, width, height, sway, n=24):
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        y = base - t * height
        half = width / 2 * (1 - t) ** 0.85 * (0.55 + 0.45 * math.sin(math.pi * min(1.0, t * 1.4 + 0.25)))
        x = cx + sway * t * t
        left.append((x - half, y))
        right.append((x + half, y))
    return left + right[::-1]


def _d_campfire(W, H, color, rng):
    """A hearth: glow, ring of stones, crossed logs and three nested flame tongues."""
    im = _ss(W, H)
    W2, H2 = W * 2, H * 2
    halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([W2 * 0.08, H2 * 0.2, W2 * 0.92, H2 * 1.0], fill=color + (130,))
    im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(W2 * 0.1)))
    d = ImageDraw.Draw(im)
    stone = (92, 86, 82)
    for k in range(9):
        t = k / 8
        x = W2 * (0.14 + 0.72 * t)
        y = H2 * (0.93 - 0.05 * math.sin(math.pi * t))
        rw, rh = W2 * 0.06, H2 * 0.04
        d.ellipse([x - rw, y - rh, x + rw, y + rh], fill=_mix(stone, (0, 0, 0), rng.uniform(0, 0.35)) + (255,))
    wood, end = (70, 45, 28), (150, 104, 62)
    lw = int(W2 * 0.075)
    for (x0, y0, x1, y1) in ((0.2, 0.92, 0.62, 0.64), (0.8, 0.92, 0.38, 0.64), (0.3, 0.95, 0.72, 0.78),
                             (0.7, 0.95, 0.28, 0.78)):
        d.line([(W2 * x0, H2 * y0), (W2 * x1, H2 * y1)], fill=wood + (255,), width=lw)
        d.ellipse([W2 * x0 - lw / 2, H2 * y0 - lw / 2, W2 * x0 + lw / 2, H2 * y0 + lw / 2], fill=end + (255,))
    fl = Image.new("RGBA", im.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(fl)
    for wf, hf, c, a in ((0.5, 0.72, color, 200), (0.34, 0.56, _mix(color, (255, 200, 90), 0.5), 235),
                         (0.18, 0.38, _mix(color, (255, 245, 210), 0.8), 255)):
        fd.polygon(_teardrop(W2 * 0.5, H2 * 0.8, W2 * wf, H2 * hf, W2 * rng.uniform(-0.05, 0.05)), fill=c + (a,))
    im.alpha_composite(fl.filter(ImageFilter.GaussianBlur(2)))
    return _down(im, W, H)


def _d_water_wheel(W, H, color, rng):
    """Create-style water wheel from the side: two plank rims boxing 16 paddle boards, six planked
    spokes, an andesite hub with a square shaft, water pouring onto the top-left paddles with a splash,
    and a rippling channel underneath."""
    im = _ss(W, H)
    W2, H2 = W * 2, H * 2
    s = min(W2, H2)
    cx, cy = W2 / 2, H2 / 2
    ro, ri = s * 0.44, s * 0.31
    wood, dark, lite = color, _mix(color, (0, 0, 0), 0.45), _mix(color, (255, 236, 200), 0.3)
    axle = _mix(color, (124, 128, 132), 0.75)
    water = Image.new("RGBA", im.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(water)
    # channel under the wheel: a rippling band, lighter at the surface, dissolving at both ends
    chan = Image.new("RGBA", im.size, (0, 0, 0, 0))
    _gpoly(chan, [(cx - s * 0.5, H2 * 0.9), (cx + s * 0.5, H2 * 0.9), (cx + s * 0.5, H2), (cx - s * 0.5, H2)],
           (90, 150, 220), (40, 80, 150), a=170)
    water.alpha_composite(_fade_sides(chan, 0.22))
    for k in range(5):
        y = H2 * (0.915 + 0.017 * k)
        x0 = cx - s * 0.45 + rng.uniform(0, s * 0.1)
        while x0 < cx + s * 0.4:
            L = s * rng.uniform(0.04, 0.1)
            wd.line([(x0, y), (x0 + L, y)], fill=(200, 230, 255, 150 - 20 * k), width=2)
            x0 += L + s * rng.uniform(0.03, 0.08)
    # falling stream onto the top-left paddles
    sx0, sx1 = cx - s * 0.36, cx - s * 0.22
    _gpoly(water, [(sx0, 0), (sx1, 0), (sx1 + s * 0.02, cy - ro * 0.72), (sx0 + s * 0.02, cy - ro * 0.6)],
           (110, 165, 235), (70, 120, 205), horiz=True, a=200)
    for xx in np.linspace(sx0 + s * 0.02, sx1 - s * 0.02, 4):
        wd.line([(xx, s * 0.02), (xx + s * 0.015, cy - ro * 0.7)], fill=(205, 232, 255, 130), width=2)
    for _ in range(14):  # splash
        a = rng.uniform(math.pi * 1.05, math.pi * 1.55)
        r = ro * rng.uniform(0.95, 1.15)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        rr = s * rng.uniform(0.012, 0.03)
        wd.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(220, 240, 255, 170))
    im.alpha_composite(water.filter(ImageFilter.GaussianBlur(s * 0.004)))
    wheel = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(wheel)
    # back of the bucket ring in shadow
    d.ellipse([cx - ro, cy - ro, cx + ro, cy + ro], fill=_mix(color, (0, 0, 0), 0.62) + (255,))
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=(0, 0, 0, 0))
    # paddle boards between the rims
    n = 16
    t = s * 0.03
    for k in range(n):
        a = 2 * math.pi * k / n + 0.1
        ca, sa = math.cos(a), math.sin(a)
        p = [(cx + ca * ri - sa * t, cy + sa * ri + ca * t), (cx + ca * ro - sa * t, cy + sa * ro + ca * t),
             (cx + ca * ro + sa * t, cy + sa * ro - ca * t), (cx + ca * ri + sa * t, cy + sa * ri - ca * t)]
        lit = 0.5 + 0.5 * math.cos(a + math.pi * 0.75)  # boards facing the top-left light are lighter
        d.polygon(p, fill=_mix(dark, lite, lit) + (255,))
    # rims (plank rings with joints)
    for r, wdt in ((ro, s * 0.045), (ri, s * 0.035)):
        box = [cx - r - wdt / 2, cy - r - wdt / 2, cx + r + wdt / 2, cy + r + wdt / 2]
        d.ellipse(box, outline=wood + (255,), width=int(wdt))
        d.arc(box, 160, 290, fill=lite + (255,), width=max(2, int(wdt * 0.35)))
        for k in range(8):
            a = 2 * math.pi * k / 8 + 0.3
            d.line([(cx + math.cos(a) * (r - wdt / 2), cy + math.sin(a) * (r - wdt / 2)),
                    (cx + math.cos(a) * (r + wdt / 2), cy + math.sin(a) * (r + wdt / 2))], fill=dark + (255,), width=2)
    # planked spokes
    for k in range(6):
        a = 2 * math.pi * k / 6 + 0.26
        ca, sa = math.cos(a), math.sin(a)
        for o, c in ((-s * 0.018, wood), (s * 0.018, _mix(wood, (0, 0, 0), 0.2))):
            d.line([(cx + ca * s * 0.06 - sa * o, cy + sa * s * 0.06 + ca * o),
                    (cx + ca * ri - sa * o, cy + sa * ri + ca * o)], fill=c + (255,), width=int(s * 0.034))
    # andesite hub with a square shaft
    hub = [(cx + math.cos(a) * s * 0.085, cy + math.sin(a) * s * 0.085)
           for a in np.linspace(0, 2 * math.pi, 9)[:-1] + 0.39]
    _gpoly(wheel, hub, _mix(axle, (255, 255, 255), 0.25), _mix(axle, (0, 0, 0), 0.35))
    d.rectangle([cx - s * 0.03, cy - s * 0.03, cx + s * 0.03, cy + s * 0.03], fill=_mix(axle, (0, 0, 0), 0.55) + (255,))
    im.alpha_composite(wheel)
    return _shade(_down(im, W, H), 0.3, 0.3)


def _d_windmill_sails(W, H, color, rng):
    """Four windmill arms: wooden spars carrying cream sail panels with a lattice."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    s = min(W2, H2)
    cx, cy = W2 / 2, H2 / 2
    spar = _mix(color, (70, 50, 32), 0.65)
    sail = (226, 218, 196)
    for k in range(4):
        a = k * math.pi / 2
        ca, sa = math.cos(a), math.sin(a)
        nx, ny = -sa, ca

        def P(r, o):
            return cx + ca * r + nx * o, cy + sa * r + ny * o
        d.polygon([P(s * 0.14, s * 0.02), P(s * 0.48, s * 0.02), P(s * 0.48, s * 0.17), P(s * 0.14, s * 0.17)],
                  fill=sail + (255,))
        for t in (0.25, 0.36):
            d.line([P(s * t, s * 0.02), P(s * t, s * 0.17)], fill=spar + (255,), width=max(2, int(s * 0.008)))
        d.line([P(s * 0.14, s * 0.095), P(s * 0.48, s * 0.095)], fill=spar + (255,), width=max(2, int(s * 0.008)))
        d.line([P(s * 0.04, 0), P(s * 0.49, 0)], fill=spar + (255,), width=int(s * 0.03))
    d.ellipse([cx - s * 0.06, cy - s * 0.06, cx + s * 0.06, cy + s * 0.06], fill=(110, 114, 118, 255))
    return _shade(_down(im, W, H), 0.3, 0.35)


def _d_rocket(W, H, color, rng):
    """Upright rocket climbing on a bright exhaust plume (tilt it with the layer's rot)."""
    im = _ss(W, H)
    W2, H2 = W * 2, H * 2
    d = ImageDraw.Draw(im)
    steel = (226, 229, 238)
    bx0, bx1 = W2 * 0.3, W2 * 0.7
    plume = Image.new("RGBA", im.size, (0, 0, 0, 0))
    pd = ImageDraw.Draw(plume)
    for k in range(6):
        y = H2 * (0.74 + 0.04 * k)
        r = W2 * (0.12 + 0.045 * k)
        pd.ellipse([W2 / 2 - r + rng.uniform(-4, 4), y - r * 0.5, W2 / 2 + r, y + r * 0.5],
                   fill=(150, 150, 165, 46 - 6 * k))
    for wf, hf, c in ((0.36, 0.42, (255, 120, 40)), (0.24, 0.32, (255, 200, 90)), (0.12, 0.22, (255, 250, 230))):
        pts = _teardrop(W2 / 2, H2 * 0.54, W2 * wf, -H2 * hf, 0)
        pd.polygon(pts, fill=c + (235,))
    im.alpha_composite(plume.filter(ImageFilter.GaussianBlur(W2 * 0.025)))
    d.polygon([(W2 * 0.2, H2 * 0.5), (bx0, H2 * 0.36), (bx0, H2 * 0.52)], fill=color + (255,))
    d.polygon([(W2 * 0.8, H2 * 0.5), (bx1, H2 * 0.36), (bx1, H2 * 0.52)], fill=color + (255,))
    d.rectangle([bx0, H2 * 0.14, bx1, H2 * 0.5], fill=steel + (255,))
    for y in (0.22, 0.44):
        d.rectangle([bx0, H2 * y, bx1, H2 * (y + 0.025)], fill=color + (255,))
    d.polygon([(W2 / 2, H2 * 0.0), (W2 * 0.6, H2 * 0.05), (bx1, H2 * 0.14), (bx0, H2 * 0.14), (W2 * 0.4, H2 * 0.05)],
              fill=color + (255,))
    d.polygon([(W2 * 0.36, H2 * 0.5), (W2 * 0.64, H2 * 0.5), (W2 * 0.6, H2 * 0.55), (W2 * 0.4, H2 * 0.55)],
              fill=(70, 72, 80, 255))
    r = W2 * 0.07
    d.ellipse([W2 / 2 - r, H2 * 0.28 - r, W2 / 2 + r, H2 * 0.28 + r], fill=(60, 64, 80, 255))
    d.ellipse([W2 / 2 - r * 0.7, H2 * 0.28 - r * 0.7, W2 / 2 + r * 0.7, H2 * 0.28 + r * 0.7], fill=(150, 200, 255, 255))
    out = _down(im, W, H)
    body = out.crop((0, 0, W, int(H * 0.56)))
    out.paste(_shade(body, 0.5, 0.45), (0, 0))
    return out


def _d_planet_horizon(W, H, color, rng):
    """The curved limb of a planet with cloud bands, a lit crescent and a glowing atmosphere."""
    R = 1.2 * W
    cx, cy = W / 2, 0.2 * H + R
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    inside = dist <= R
    depth = np.clip(R - dist, 0, None)
    n = _periodic_noise(64, 3, rng, 3)
    nb = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, max(8, H // 3)), Image.BICUBIC)
                    .resize((W, H), Image.BICUBIC), np.float32) / 255
    shade = 0.25 + 0.75 * np.exp(-depth / (0.25 * H))
    side = 1 - 0.5 * np.abs(x / W * 2 - 1) ** 2
    rgb = (np.array(color, np.float32) / 255) * (0.8 + 0.35 * nb)[..., None] * (shade * side)[..., None]
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.clip(rgb, 0, 1)
    out[..., 3] = inside.astype(np.float32)
    planet = _img(out, "RGBA")
    atmo = np.exp(-np.abs(dist - R) / (0.035 * H)) * (dist > R - 0.06 * H)
    glow = np.zeros((H, W, 4), np.float32)
    glow[..., :3] = np.array(_mix(color, (190, 225, 255), 0.6), np.float32) / 255
    glow[..., 3] = np.clip(atmo * side, 0, 1) * 0.9
    img = _img(glow, "RGBA")
    img.alpha_composite(planet)
    return img


def _d_satellite(W, H, color, rng):
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    panel = (40, 58, 135)
    d.line([(W2 * 0.06, H2 / 2), (W2 * 0.94, H2 / 2)], fill=(150, 150, 160, 255), width=max(2, int(H2 * 0.03)))
    for x0 in (0.06, 0.64):
        d.rectangle([W2 * x0, H2 * 0.29, W2 * (x0 + 0.3), H2 * 0.71], fill=panel + (255,))
        for i in range(1, 4):
            xx = W2 * (x0 + 0.3 * i / 4)
            d.line([(xx, H2 * 0.29), (xx, H2 * 0.71)], fill=(120, 150, 230, 255), width=2)
        d.line([(W2 * x0, H2 / 2), (W2 * (x0 + 0.3), H2 / 2)], fill=(120, 150, 230, 255), width=2)
    d.rounded_rectangle([W2 * 0.37, H2 * 0.35, W2 * 0.63, H2 * 0.65], int(H2 * 0.05), fill=color + (255,))
    d.rectangle([W2 * 0.37, H2 * 0.47, W2 * 0.63, H2 * 0.53], fill=_mix(color, (0, 0, 0), 0.35) + (255,))
    for x in (0.44, 0.56):
        d.ellipse([W2 * x - H2 * 0.03, H2 * 0.4 - H2 * 0.03, W2 * x + H2 * 0.03, H2 * 0.4 + H2 * 0.03],
                  fill=(255, 220, 140, 255))
    d.ellipse([W2 * 0.5 - H2 * 0.025, H2 * 0.3 - H2 * 0.025, W2 * 0.5 + H2 * 0.025, H2 * 0.3 + H2 * 0.025],
              fill=(255, 60, 60, 255))
    return _shade(_down(im, W, H), 0.35, 0.3)


def _d_cave_painting_herd(W, H, color, rng):
    """Second rock-art frieze: bison struck by spears, archers, a row of tally dots."""
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    s = min(W, H)
    lw = max(2, int(s * 0.018))

    def bison(cx, cy, k):
        bw, bh = s * 0.22 * k, s * 0.1 * k
        d.ellipse([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], fill=255)
        d.ellipse([cx - bw * 0.55, cy - bh * 1.05, cx - bw * 0.05, cy + bh * 0.1], fill=255)
        d.ellipse([cx - bw * 0.72, cy - bh * 0.35, cx - bw * 0.42, cy + bh * 0.45], fill=255)
        d.line([(cx - bw * 0.62, cy - bh * 0.3), (cx - bw * 0.7, cy - bh * 0.75)], fill=255, width=lw)
        for lx in (-0.34, -0.18, 0.2, 0.36):
            x = cx + lx * bw
            d.line([(x, cy), (x + rng.uniform(-2, 2), cy + s * 0.09 * k)], fill=255, width=int(lw * 1.5))
        d.line([(cx + bw * 0.5, cy - bh * 0.1), (cx + bw * 0.62, cy + bh * 0.5)], fill=255, width=lw)
        d.line([(cx + bw * 0.05, cy - bh * 1.4), (cx - bw * 0.1, cy - bh * 0.2)], fill=255, width=max(1, lw - 1))

    def archer(cx, cy, k):
        h = s * 0.15 * k
        d.ellipse([cx - h * 0.07, cy - h * 0.64, cx + h * 0.07, cy - h * 0.5], fill=255)
        d.line([(cx, cy - h * 0.5), (cx, cy)], fill=255, width=lw)
        d.line([(cx, cy), (cx - h * 0.16, cy + h * 0.4)], fill=255, width=lw)
        d.line([(cx, cy), (cx + h * 0.16, cy + h * 0.4)], fill=255, width=lw)
        d.arc([cx - h * 0.45, cy - h * 0.62, cx - h * 0.05, cy - h * 0.08], 100, 260, fill=255, width=lw)
        d.line([(cx - h * 0.3, cy - h * 0.35), (cx + h * 0.15, cy - h * 0.35)], fill=255, width=max(1, lw - 1))

    bison(W * 0.3, H * 0.4, 1.0)
    bison(W * 0.55, H * 0.28, 0.8)
    bison(W * 0.45, H * 0.66, 0.9)
    archer(W * 0.8, H * 0.5, 1.0)
    archer(W * 0.88, H * 0.66, 0.85)
    for i in range(9):
        x = W * (0.2 + 0.05 * i)
        d.ellipse([x - lw, H * 0.9 - lw, x + lw, H * 0.9 + lw], fill=255)
    a = np.asarray(im.filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    noise = np.random.default_rng(rng.randrange(1 << 30)).random(a.shape).astype(np.float32)
    a = a * (0.55 + 0.45 * noise)
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    out[..., 3] = a
    return _img(out, "RGBA")


# ---- landscape & nature
def _d_tree_line(W, H, color, rng):
    """Forest silhouette band: two depths of conifers and round crowns, bottom dissolved."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    for depth, (a, base, hmax) in enumerate(((150, H2 * 0.95, 0.75), (255, H2 * 1.0, 0.6))):
        c = _mix(color, (0, 0, 0), 0.3 * depth)
        x = -rng.uniform(0, 40)
        while x < W2 + 40:
            h = H2 * rng.uniform(0.35, hmax)
            w = h * rng.uniform(0.28, 0.42)
            if rng.random() < 0.65:  # conifer: stacked triangles
                for k in range(3):
                    t = k / 3
                    d.polygon([(x, base - h + h * t * 0.55), (x - w * (0.5 + t * 0.5), base - h * (0.45 - t * 0.12)),
                               (x + w * (0.5 + t * 0.5), base - h * (0.45 - t * 0.12))], fill=c + (a,))
                d.rectangle([x - w * 0.08, base - h * 0.35, x + w * 0.08, base], fill=c + (a,))
            else:  # broadleaf crown
                d.ellipse([x - w * 0.9, base - h, x + w * 0.9, base - h * 0.35], fill=c + (a,))
                d.rectangle([x - w * 0.1, base - h * 0.45, x + w * 0.1, base], fill=c + (a,))
            x += w * rng.uniform(0.7, 1.2)
    return _fade_sides(_fade_bottom(_down(im, W, H)))


def _d_fireflies(W, H, color, rng):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(int(W * H / 2500) + 10):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        r = rng.uniform(1.2, 2.6)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (rng.randint(150, 255),))
    g = im.filter(ImageFilter.GaussianBlur(5))
    g.alpha_composite(im.filter(ImageFilter.GaussianBlur(2)))
    g.alpha_composite(im)
    return g


def _d_aurora(W, H, color, rng):
    """Curtains of light: a wavy ribbon with vertical streaks fading upwards."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    k1, k2, ph = rng.uniform(1.5, 3), rng.uniform(4, 7), rng.uniform(0, 6.28)
    base = H * (0.62 + 0.12 * np.sin(x / W * math.pi * k1 + ph) + 0.05 * np.sin(x / W * math.pi * k2))
    up = np.clip((base - y) / (H * 0.55), 0, 1)
    band = np.where(y <= base, (1 - up) ** 1.4, np.exp(-(y - base) / (H * 0.03)))
    streak = 0.6 + 0.4 * np.sin(x / W * math.pi * 60 + np.sin(x / W * 9) * 3) ** 2
    side = np.clip((1 - np.abs(x / W * 2 - 1)) / 0.25, 0, 1)
    a = band * streak * side * 0.85
    c2 = np.array(_mix(color, (150, 120, 255), 0.6), np.float32) / 255
    c1 = np.array(color, np.float32) / 255
    t = up[..., None]
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = c1 * (1 - t) + c2 * t
    out[..., 3] = a
    return _img(out, "RGBA").filter(ImageFilter.GaussianBlur(2))


def _d_snowfall(W, H, color, rng):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(int(W * H / 1100) + 20):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        r = rng.choice((1, 1, 1.5, 2, 2.5))
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (rng.randint(110, 230),))
    g = im.filter(ImageFilter.GaussianBlur(1.5))
    g.alpha_composite(im)
    return g


def _d_snowy_range(W, H, color, rng):
    """Mountain silhouettes with snow caps on the peaks."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    snow = _mix(color, (235, 242, 255), 0.75)
    for i, (base, amp) in enumerate(((H2 * 0.9, H2 * 0.75), (H2 * 1.0, H2 * 0.55))):
        xs = np.linspace(0, W2, 7)
        peaks = [(x, base - rng.uniform(0.45, 1.0) * amp) for x in xs]
        pts = []
        for (x0, y0), (x1, y1) in zip(peaks, peaks[1:]):
            mx = (x0 + x1) / 2
            pts += [(x0, y0), (mx, max(y0, y1) + amp * rng.uniform(0.2, 0.35))]
        pts.append(peaks[-1])
        c = _mix(color, (0, 0, 0), 0.25 * i)
        d.polygon(pts + [(W2, H2), (0, H2)], fill=c + (255,))
        for x, y in peaks:
            cap = amp * 0.16
            d.polygon([(x, y), (x - cap * 0.9, y + cap), (x - cap * 0.3, y + cap * 0.8), (x, y + cap * 1.1),
                       (x + cap * 0.4, y + cap * 0.75), (x + cap * 0.9, y + cap)], fill=snow + (255,))
    return _fade_sides(_fade_bottom(_shade(_down(im, W, H), 0.3, 0.2)))


def _d_sun(W, H, color, rng, rays=False):
    """A low sun: wide atmospheric bloom, a bright corona and a white-hot disc whose limb takes the
    colour. rays=true adds the old clip-art line rays (legacy look)."""
    s = min(W, H)
    r = s * 0.2
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((x - W / 2) ** 2 + (y - H / 2) ** 2)
    c = np.array(color, np.float32) / 255
    hot = np.array(_mix(color, (255, 252, 238), 0.85), np.float32) / 255
    bloom = np.clip(1 - d / (s * 0.5), 0, 1) ** 2.2 * 0.75
    corona = np.exp(-np.clip(d - r, 0, None) / (r * 0.35)) * 0.85
    disc = np.clip((r - d) / 1.5 + 0.5, 0, 1)
    limb = np.clip(d / r, 0, 1) ** 3
    a_glow = np.clip(bloom + corona * (1 - disc), 0, 1)
    out = np.zeros((H, W, 4), np.float32)
    rgb_glow = c * (1 - corona[..., None] * 0.5) + hot * (corona[..., None] * 0.5)
    rgb_disc = hot * (1 - limb[..., None] * 0.35) + c * (limb[..., None] * 0.35)
    out[..., :3] = rgb_glow * (1 - disc[..., None]) + rgb_disc * disc[..., None]
    out[..., 3] = np.clip(a_glow * (1 - disc) + disc, 0, 1)
    im = _img(out, "RGBA")
    if rays:
        dr = ImageDraw.Draw(im)
        for k in range(16):
            a = 2 * math.pi * k / 16
            dr.line([(W / 2 + math.cos(a) * r * 1.25, H / 2 + math.sin(a) * r * 1.25),
                     (W / 2 + math.cos(a) * r * (1.8 if k % 2 else 1.55),
                      H / 2 + math.sin(a) * r * (1.8 if k % 2 else 1.55))],
                    fill=_mix(color, (255, 255, 255), 0.4) + (200,), width=max(2, int(s * 0.012)))
    return im


def _d_falling_leaves(W, H, color, rng):
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    for _ in range(int(W * H / 2600) + 8):
        x, y = rng.uniform(0, W2), rng.uniform(0, H2)
        L = rng.uniform(8, 18)
        a = rng.uniform(0, math.pi)
        c = _mix(color, (0, 0, 0), rng.uniform(0, 0.35))
        pts = [(x + math.cos(a) * L, y + math.sin(a) * L), (x + math.cos(a + 1.9) * L * 0.4, y + math.sin(a + 1.9) * L * 0.4),
               (x - math.cos(a) * L, y - math.sin(a) * L), (x + math.cos(a - 1.2) * L * 0.4, y + math.sin(a - 1.2) * L * 0.4)]
        d.polygon(pts, fill=c + (rng.randint(170, 255),))
    return _down(im, W, H)


def _d_wheat_field(W, H, color, rng):
    """Rows of wheat stalks with ears, silhouetted against a low glow."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    for row, (base, hh, a) in enumerate(((H2 * 0.75, 0.45, 150), (H2 * 0.92, 0.55, 220), (H2 * 1.02, 0.6, 255))):
        c = _mix(color, (0, 0, 0), 0.22 * row)
        x = rng.uniform(0, 8)
        while x < W2:
            h = H2 * hh * rng.uniform(0.75, 1.0)
            lean = rng.uniform(-0.12, 0.12) * h
            tx, ty = x + lean, base - h
            d.line([(x, base), (tx, ty)], fill=c + (a,), width=max(2, int(W2 * 0.003)))
            for k in range(5):
                t = 0.05 + k * 0.045
                ex, ey = x + lean * (1 - t), base - h * (1 - t)
                d.ellipse([ex - 4, ey - 7, ex + 4, ey + 3], fill=_mix(c, (255, 230, 150), 0.25) + (a,))
            x += rng.uniform(9, 16)
    return _fade_bottom(_down(im, W, H))


# ---- industry
def _d_pipes(W, H, color, rng):
    """A run of thick pipes with elbows, flanges and a valve wheel."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    t = max(8, int(min(W2, H2) * 0.07))
    dark, light = _mix(color, (0, 0, 0), 0.4), _mix(color, (255, 255, 255), 0.25)
    for i in range(3):
        y = H2 * (0.25 + 0.25 * i) + rng.uniform(-10, 10)
        xb = W2 * rng.uniform(0.35, 0.75)
        d.line([(0, y), (xb, y)], fill=color + (255,), width=t)
        d.line([(0, y - t * 0.3), (xb, y - t * 0.3)], fill=light + (255,), width=max(2, t // 5))
        yb = H2 if i % 2 else 0
        d.line([(xb, y), (xb, yb)], fill=color + (255,), width=t)
        d.ellipse([xb - t * 0.75, y - t * 0.75, xb + t * 0.75, y + t * 0.75], fill=color + (255,))
        for fx in np.arange(W2 * 0.15, xb - t, W2 * 0.18):
            d.rectangle([fx - t * 0.2, y - t * 0.75, fx + t * 0.2, y + t * 0.75], fill=dark + (255,))
        vx = xb * 0.5
        _valve(d, vx, y, t, color)
    return _shade(_down(im, W, H), 0.4, 0.4)


def _valve(d, vx, y, t, color):
    """Gate valve on a pipe: bonnet, stem and a cast-iron handwheel (rim, spokes, hub) seen from the
    front, painted a dull oxide red only on the rim highlight (it used to be a bright red ring)."""
    iron = _mix(color, (40, 38, 36), 0.55)
    rim_hi = _mix(iron, (150, 70, 52), 0.45)
    d.rectangle([vx - t * 0.45, y - t * 0.95, vx + t * 0.45, y - t * 0.45], fill=_mix(color, (0, 0, 0), 0.3) + (255,))
    d.line([(vx, y - t * 0.5), (vx, y - t * 1.55)], fill=iron + (255,), width=max(2, int(t * 0.22)))
    cy, R = y - t * 1.65, t * 0.85
    rw = max(2, int(t * 0.2))
    d.ellipse([vx - R, cy - R * 0.32, vx + R, cy + R * 0.32], outline=iron + (255,), width=rw)
    d.arc([vx - R, cy - R * 0.32, vx + R, cy + R * 0.32], 190, 350, fill=rim_hi + (255,), width=max(1, rw // 2))
    for sx in (-1, 1):
        d.line([(vx, cy), (vx + sx * R * 0.92, cy)], fill=iron + (255,), width=max(1, rw // 2 + 1))
    d.ellipse([vx - t * 0.18, cy - t * 0.12, vx + t * 0.18, cy + t * 0.12], fill=_mix(iron, (255, 255, 255), 0.15) + (255,))


def _d_power_line(W, H, color, rng):
    """Lattice pylons with sagging cables."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    xs = [W2 * 0.12, W2 * 0.5, W2 * 0.88]
    lw = max(2, int(W2 * 0.004))
    for x in xs:
        top, base, hw = H2 * 0.12, H2, W2 * 0.05
        d.line([(x - hw, base), (x, top)], fill=color + (255,), width=lw * 2)
        d.line([(x + hw, base), (x, top)], fill=color + (255,), width=lw * 2)
        for k in range(6):
            y0 = top + (base - top) * k / 6
            y1 = top + (base - top) * (k + 1) / 6
            w0, w1 = hw * k / 6, hw * (k + 1) / 6
            d.line([(x - w0, y0), (x + w1, y1)], fill=color + (255,), width=lw)
            d.line([(x + w0, y0), (x - w1, y1)], fill=color + (255,), width=lw)
        for yy, arm in ((H2 * 0.2, W2 * 0.07), (H2 * 0.3, W2 * 0.055)):
            d.line([(x - arm, yy), (x + arm, yy)], fill=color + (255,), width=lw * 2)
    for yy, arm in ((H2 * 0.2, W2 * 0.07), (H2 * 0.3, W2 * 0.055)):
        for sgn in (-1, 1):
            for a, b in zip(xs, xs[1:]):
                pts = [(a + sgn * arm + (b - a) * t, yy + 4 + H2 * 0.08 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 30)]
                d.line(pts, fill=_mix(color, (0, 0, 0), 0.3) + (230,), width=lw)
    return _down(im, W, H)


def _d_smokestack(W, H, color, rng):
    """Brick chimneys with drifting smoke and a warm glow at their feet."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(smoke)
    stacks = [(0.3, 0.55, 0.11), (0.62, 0.38, 0.13)]
    for sx, top, sw in stacks:
        x, y = W * sx, H * top
        for k in range(14):
            r = W * (0.04 + 0.012 * k)
            sd.ellipse([x - r + k * W * 0.02, y - k * H * 0.03 - r, x + r + k * W * 0.02, y - k * H * 0.03 + r],
                       fill=(120, 116, 112, max(0, 60 - 4 * k)))
    im.alpha_composite(smoke.filter(ImageFilter.GaussianBlur(W * 0.015)))
    st = _ss(W, H)
    d = ImageDraw.Draw(st)
    for sx, top, sw in stacks:
        x0, x1 = W * 2 * (sx - sw / 2), W * 2 * (sx + sw / 2)
        d.polygon([(x0, H * 2), (x0 + (x1 - x0) * 0.08, H * 2 * top), (x1 - (x1 - x0) * 0.08, H * 2 * top), (x1, H * 2)],
                  fill=color + (255,))
        d.rectangle([x0 - 6, H * 2 * top - 10, x1 + 6, H * 2 * top + 10], fill=_mix(color, (0, 0, 0), 0.35) + (255,))
        for yy in np.arange(H * 2 * top + 30, H * 2, 26):
            d.line([(x0, yy), (x1, yy)], fill=_mix(color, (0, 0, 0), 0.25) + (255,), width=2)
    im.alpha_composite(_shade(_down(st, W, H), 0.35, 0.3))
    return _fade_bottom(im)


def _d_circuit(W, H, color, rng):
    """PCB traces: orthogonal tracks with 45-degree bends, pads and a couple of chips."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    g = max(6, int(DECOR_PX * 0.5))
    lw = max(2, g // 4)
    for _ in range(int(W * H / (g * g * 14)) + 6):
        x, y = rng.randrange(0, W // g) * g, rng.randrange(0, H // g) * g
        pts = [(x, y)]
        for _ in range(rng.randint(2, 5)):
            dx, dy = rng.choice(((1, 0), (0, 1), (-1, 0), (0, -1)))
            n = rng.randint(2, 6) * g
            x, y = x + dx * n, y + dy * n
            pts.append((x, y))
        d.line(pts, fill=color + (200,), width=lw)
        for px, py in (pts[0], pts[-1]):
            d.ellipse([px - lw * 1.6, py - lw * 1.6, px + lw * 1.6, py + lw * 1.6], outline=color + (230,), width=lw)
    for _ in range(3):
        x, y = rng.uniform(0.1, 0.8) * W, rng.uniform(0.1, 0.8) * H
        w, h = g * rng.randint(3, 5), g * rng.randint(2, 3)
        d.rectangle([x, y, x + w, y + h], fill=_mix(color, (0, 0, 0), 0.65) + (230,), outline=color + (230,), width=lw)
        for k in range(1, int(w / g)):
            d.line([(x + k * g, y), (x + k * g, y - g * 0.5)], fill=color + (200,), width=lw)
            d.line([(x + k * g, y + h), (x + k * g, y + h + g * 0.5)], fill=color + (200,), width=lw)
    g2 = im.filter(ImageFilter.GaussianBlur(3))
    g2.alpha_composite(im)
    return g2


def _bolt_path(x0, y0, x1, y1, rough, rng, depth=6):
    """Jagged path by midpoint displacement (natural lightning kinks at every scale)."""
    pts = [(x0, y0), (x1, y1)]
    for lvl in range(depth):
        out = [pts[0]]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            L = math.hypot(bx - ax, by - ay)
            nx, ny = -(by - ay) / max(L, 1e-6), (bx - ax) / max(L, 1e-6)
            o = rng.gauss(0, 1) * L * rough * (0.75 ** lvl)
            out += [((ax + bx) / 2 + nx * o, (ay + by) / 2 + ny * o), (bx, by)]
        pts = out
    return pts


def _d_lightning(W, H, color, rng, width=1.0, branches=1.0, flash=0.0):
    """A forked lightning strike: jagged main channel (top to bottom of the box), forks that split
    again, a white-hot tapering core, a coloured inner glow and a wide soft outer glow.
    width scales the bolt thickness (1 = bold, 0.5 = thin), branches the number of forks (0 = none),
    flash adds a cloud flash at the top (0..1)."""
    S = 2
    W2, H2 = W * S, H * S
    core_w = max(3.0, min(W2 * 0.05, H2 * 0.016) + 4) * float(width)

    def fit(pts, lo, hi):  # squeeze the horizontal wander into [lo, hi] of the box
        xs = [p[0] for p in pts]
        m0, m1 = min(xs), max(xs)
        if m0 >= lo and m1 <= hi:
            return pts
        f = min(1.0, (hi - lo) / max(m1 - m0, 1e-6))
        c = (m0 + m1) / 2
        sh = min(max(c, lo + (m1 - m0) * f / 2), hi - (m1 - m0) * f / 2)
        return [(sh + (x - c) * f, y) for x, y in pts]

    def walk(x, y, ey, step, jump, lo, hi):  # sharp-kinked random walk, then fine jaggies
        pts = [(x, y)]
        while y < ey:
            y = min(ey, y + step * rng.uniform(0.5, 1.3))
            x = min(max(x + rng.uniform(-1, 1) * jump, lo), hi)
            pts.append((x, y))
        out = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            out += _bolt_path(p[0], p[1], q[0], q[1], 0.12, rng, 3)[1:]
        return out

    main = walk(W2 * rng.uniform(0.42, 0.58), 0, H2 * 0.97, H2 * 0.075, W2 * 0.16, W2 * 0.22, W2 * 0.78)
    strokes = [(main, core_w, core_w * 0.6)]  # (points, width at start, width at end)

    def fork(pts, w, lvl):
        n = len(pts)
        cnt = int(round(rng.uniform(2.2, 3.2) * branches)) if lvl == 0 else int(rng.random() < 0.6 * branches)
        for j in range(cnt):
            lo_i, hi_i = int(n * (0.1 + 0.55 * j / max(cnt, 1))), int(n * (0.1 + 0.55 * (j + 1) / max(cnt, 1)))
            bx, by = pts[rng.randrange(lo_i, max(lo_i + 1, hi_i))]
            side = rng.choice((-1, 1))
            L = H2 * rng.uniform(0.24, 0.4) / (lvl + 1.4)
            ang = math.radians(rng.uniform(28, 50))
            dx = side * math.tan(ang) * L / max(1, L / (H2 * 0.075))
            sub = walk(bx, by, by + L, H2 * 0.05, abs(dx) * 0.9, -1e9, 1e9)
            sub = [(x + side * (y - by) * math.tan(ang) * 0.7, y) for x, y in sub]
            f = 1.0  # shrink sideways around the attachment point so the fork stays inside the box
            for x, _ in sub:
                if x < W2 * 0.1:
                    f = min(f, (bx - W2 * 0.1) / max(bx - x, 1e-6))
                elif x > W2 * 0.9:
                    f = min(f, (W2 * 0.9 - bx) / max(x - bx, 1e-6))
            sub = [(bx + (x - bx) * max(f, 0.0), y) for x, y in sub]
            strokes.append((sub, w * 0.5, max(1.4, w * 0.16)))
            if lvl < 1:
                fork(sub, w * 0.5, lvl + 1)

    if branches > 0:
        fork(main, core_w, 0)

    def draw(scale, col, a):
        lay = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for pts, w0, w1 in strokes:
            n = len(pts) - 1
            for j, (p, q) in enumerate(zip(pts, pts[1:])):
                w = max(1.0, (w0 + (w1 - w0) * j / max(n, 1)) * scale)
                d.line([p, q], fill=col + (a,), width=int(round(w)))
                d.ellipse([q[0] - w / 2, q[1] - w / 2, q[0] + w / 2, q[1] + w / 2], fill=col + (a,))
        return lay

    out = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    if flash:  # lit cloud base around the top of the channel: a soft radial blob, no edges
        y, x = np.mgrid[0:H2, 0:W2].astype(np.float32)
        r = np.sqrt(((x - main[0][0]) / (W2 * 0.46)) ** 2 + ((y - H2 * 0.03) / (H2 * 0.13)) ** 2)
        fl = np.zeros((H2, W2, 4), np.float32)
        fl[..., :3] = np.array(color, np.float32) / 255
        fl[..., 3] = np.clip(1 - r, 0, 1) ** 2 * 0.8 * min(1.0, float(flash))
        out.alpha_composite(_img(fl, "RGBA"))
    out.alpha_composite(draw(7.0, color, 125).filter(ImageFilter.GaussianBlur(core_w * 3.2)))
    out.alpha_composite(draw(3.0, _mix(color, (255, 255, 255), 0.25), 200).filter(ImageFilter.GaussianBlur(core_w * 0.9)))
    out.alpha_composite(draw(1.0, _mix(color, (255, 255, 255), 0.85), 255).filter(ImageFilter.GaussianBlur(0.6)))
    out = _fade_sides(out.resize((W, H), Image.LANCZOS), 0.1)  # glow never ends in a hard box edge
    t = np.clip(np.arange(H, dtype=np.float32) / max(1.0, H * 0.05), 0, 1)  # emerges from the cloud
    a = np.asarray(out.getchannel("A"), np.float32) * (t * t * (3 - 2 * t))[:, None]
    out.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    return out


def _d_heartbeat(W, H, color, rng, width=1.0):
    """An ECG trace across the band with a glow. width scales the line (0.4 = a faint ambient trace)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts, x = [], 0
    mid = H / 2
    while x < W:
        pts += [(x, mid), (x + W * 0.06, mid)]
        b = W * 0.06
        pts += [(x + b + W * 0.01, mid - H * 0.12), (x + b + W * 0.02, mid), (x + b + W * 0.03, mid + H * 0.1),
                (x + b + W * 0.045, mid - H * 0.42), (x + b + W * 0.06, mid + H * 0.3), (x + b + W * 0.07, mid),
                (x + b + W * 0.11, mid - H * 0.08), (x + b + W * 0.14, mid)]
        x += b + W * 0.2
    d.line(pts, fill=color + (255,), width=max(1, int(H * 0.04 * width)), joint="curve")
    g = im.filter(ImageFilter.GaussianBlur(max(3, H * 0.06)))
    g.alpha_composite(im)
    x = np.linspace(-1, 1, W, dtype=np.float32)
    fade = np.clip((1 - np.abs(x)) / 0.3, 0, 1)
    a = np.asarray(g.getchannel("A"), np.float32) * fade[None, :]
    g.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    return g


def _d_light_rays(W, H, color, rng, angle=60.0, spread=36.0, count=7, src=(0.0, 0.0)):
    """Soft shafts of light fanning out from a source point (window, sun, furnace mouth): gives a scene one
    visible light direction. src = source position in the box (fractions), angle = mean direction in
    degrees (0 = right, 90 = down), spread = fan width in degrees, count = number of shafts."""
    sx, sy = src[0] * W, src[1] * H
    L = math.hypot(W, H) * 1.05
    lay = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(lay)
    for k in range(int(count)):
        a = math.radians(angle + spread * ((k + rng.uniform(0.2, 0.8)) / max(count, 1) - 0.5))
        half = math.radians(rng.uniform(0.8, 2.2))
        d.polygon([(sx, sy), (sx + math.cos(a - half) * L, sy + math.sin(a - half) * L),
                   (sx + math.cos(a + half) * L, sy + math.sin(a + half) * L)], fill=int(rng.uniform(110, 230)))
    lay = lay.filter(ImageFilter.GaussianBlur(max(2, min(W, H) * 0.015)))
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    fall = np.clip(1 - np.sqrt((x - sx) ** 2 + (y - sy) ** 2) / L, 0, 1) ** 1.6
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    ex = np.clip(np.minimum(x, W - 1 - x) / (W * 0.15), 0, 1)
    ey = np.clip(np.minimum(y, H - 1 - y) / (H * 0.15), 0, 1)
    ex, ey = ex * ex * (3 - 2 * ex), ey * ey * (3 - 2 * ey)
    near = np.clip(np.sqrt((x - sx) ** 2 + (y - sy) ** 2) / (min(W, H) * 0.1), 0, 1)  # source stays visible
    edge = np.maximum(ex * ey, 1 - near)
    out[..., 3] = np.asarray(lay, np.float32) / 255 * fall * edge
    return _img(out, "RGBA")


# ---- maps & places
def _d_compass_rose(W, H, color, rng):
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    s = min(W, H) * 2
    cx, cy = W, H
    R = s * 0.46
    lw = max(2, int(s * 0.006))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=color + (220,), width=lw)
    d.ellipse([cx - R * 0.9, cy - R * 0.9, cx + R * 0.9, cy + R * 0.9], outline=color + (150,), width=lw)
    for k in range(72):
        a = 2 * math.pi * k / 72
        r0 = R * (0.82 if k % 9 == 0 else 0.86)
        d.line([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * R * 0.9, cy + math.sin(a) * R * 0.9)],
               fill=color + (200,), width=lw)
    dark = _mix(color, (0, 0, 0), 0.45)
    for k in range(8):
        a = -math.pi / 2 + k * math.pi / 4
        L = R * (0.82 if k % 2 == 0 else 0.5)
        wdt = R * (0.12 if k % 2 == 0 else 0.08)
        tip = (cx + math.cos(a) * L, cy + math.sin(a) * L)
        l = (cx + math.cos(a - math.pi / 2) * wdt, cy + math.sin(a - math.pi / 2) * wdt)
        r = (cx + math.cos(a + math.pi / 2) * wdt, cy + math.sin(a + math.pi / 2) * wdt)
        d.polygon([tip, l, (cx, cy)], fill=color + (255,))
        d.polygon([tip, r, (cx, cy)], fill=dark + (255,))
    d.ellipse([cx - R * 0.06, cy - R * 0.06, cx + R * 0.06, cy + R * 0.06], fill=color + (255,))
    return _down(im, W, H)


def _d_contour_map(W, H, color, rng):
    """Topographic contour lines from a smooth height field."""
    n = _periodic_noise(64, 2, rng, 3)
    h = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    levels = 12
    f = (h * levels) % 1.0
    line = np.clip(1 - np.minimum(f, 1 - f) / 0.06, 0, 1)
    major = ((np.floor(h * levels) % 4) == 0).astype(np.float32)
    a = line * (0.5 + 0.5 * major)
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    out[..., 3] = a
    return _img(out, "RGBA")


def _d_castle(W, H, color, rng):
    """Castle silhouette on a hill with towers, crenellations and a few lit windows."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    d.ellipse([-W2 * 0.2, H2 * 0.78, W2 * 1.2, H2 * 1.4], fill=color + (255,))
    towers = [(0.18, 0.38, 0.1), (0.38, 0.22, 0.12), (0.62, 0.3, 0.11), (0.82, 0.45, 0.09)]
    d.rectangle([W2 * 0.15, H2 * 0.52, W2 * 0.85, H2 * 0.9], fill=color + (255,))
    for tx, top, tw in towers:
        x0, x1 = W2 * (tx - tw / 2), W2 * (tx + tw / 2)
        d.rectangle([x0, H2 * top, x1, H2 * 0.9], fill=color + (255,))
        d.polygon([(x0 - W2 * 0.01, H2 * top), (x1 + W2 * 0.01, H2 * top), ((x0 + x1) / 2, H2 * (top - 0.14))],
                  fill=color + (255,))
        for k in range(3):
            wy = H2 * (top + 0.08 + k * 0.1)
            if rng.random() < 0.6 and wy < H2 * 0.85:
                d.rectangle([(x0 + x1) / 2 - W2 * 0.008, wy, (x0 + x1) / 2 + W2 * 0.008, wy + H2 * 0.035],
                            fill=(255, 210, 120, 255))
    for k in range(14):
        x = W2 * (0.15 + 0.05 * k)
        d.rectangle([x, H2 * 0.49, x + W2 * 0.025, H2 * 0.53], fill=color + (255,))
    return _down(im, W, H)


# ---- props requested by the art directors (round 4)
def _gpoly(im, pts, c0, c1, horiz=False, a=255):
    """Polygon filled with a linear gradient c0 -> c1 (top->bottom, or left->right): cheap volume."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, y0 = int(math.floor(min(xs))), int(math.floor(min(ys)))
    w, h = max(1, int(math.ceil(max(xs))) - x0 + 1), max(1, int(math.ceil(max(ys))) - y0 + 1)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon([(x - x0, y - y0) for x, y in pts], fill=a)
    n = w if horiz else h
    t = np.linspace(0, 1, n, dtype=np.float32)[:, None]
    ramp = (np.array(c0, np.float32) * (1 - t) + np.array(c1, np.float32) * t) / 255
    rgb = np.broadcast_to(ramp[None, :, :], (h, w, 3)) if horiz else np.broadcast_to(ramp[:, None, :], (h, w, 3))
    tile = np.concatenate([rgb, (np.asarray(mask, np.float32) / 255)[..., None]], axis=2)
    im.alpha_composite(_img(tile, "RGBA"), (x0, y0))


def _ellipse_shadow(im, cx, cy, rw, rh, a=0.55):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(0, 0, 0, int(255 * a)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(max(1.5, rh * 0.6))))


def _d_anvil(W, H, color, rng, hot=False):
    """Side-view blacksmith anvil (~2:1): tapered horn, face plate with a lit top edge and a shadowed
    overhang, hardy hole, a waist in shadow and arched feet on a contact shadow; lit from the top-left."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    lite, mid, dark, deep = (_mix(color, (255, 255, 255), 0.32), color, _mix(color, (0, 0, 0), 0.38),
                             _mix(color, (0, 0, 0), 0.62))
    fy, fh = H2 * 0.1, H2 * 0.21  # face plate
    _ellipse_shadow(im, W2 * 0.53, H2 * 0.965, W2 * 0.4, H2 * 0.035, 0.6)
    # feet: wide base with an arch cut between the front feet
    _gpoly(im, [(W2 * 0.27, H2 * 0.74), (W2 * 0.79, H2 * 0.74), (W2 * 0.9, H2 * 0.97), (W2 * 0.16, H2 * 0.97)],
           mid, dark)
    d.chord([W2 * 0.4, H2 * 0.84, W2 * 0.66, H2 * 1.1], 180, 360, fill=deep + (255,))
    d.line([(W2 * 0.27, H2 * 0.745), (W2 * 0.79, H2 * 0.745)], fill=lite + (255,), width=max(2, int(H2 * 0.02)))
    # waist (in the face's shadow, lit on the left)
    _gpoly(im, [(W2 * 0.34, fy + fh), (W2 * 0.8, fy + fh), (W2 * 0.68, H2 * 0.6), (W2 * 0.72, H2 * 0.75),
                (W2 * 0.33, H2 * 0.75), (W2 * 0.39, H2 * 0.6)], _mix(mid, (255, 255, 255), 0.08), deep, horiz=True)
    _gpoly(im, [(W2 * 0.34, fy + fh), (W2 * 0.8, fy + fh), (W2 * 0.78, fy + fh * 1.45), (W2 * 0.36, fy + fh * 1.45)],
           (0, 0, 0), dark, a=150)  # cast shadow under the face's overhang
    # horn: tapered cone, round underside
    horn = [(W2 * 0.33, fy), (W2 * 0.33, fy + fh * 1.0)] + [
        (W2 * (0.33 - 0.31 * t), fy + fh * (1.0 - 0.62 * t ** 0.8)) for t in np.linspace(0.05, 1, 12)]
    _gpoly(im, horn, lite, dark)
    # face plate: lit top surface, mid front, dark lower lip
    _gpoly(im, [(W2 * 0.32, fy), (W2 * 0.97, fy), (W2 * 0.97, fy + fh), (W2 * 0.32, fy + fh)], mid, dark)
    d.rectangle([W2 * 0.32, fy, W2 * 0.97, fy + fh * 0.2], fill=lite + (255,))
    d.line([(W2 * 0.04, fy + fh * 0.4), (W2 * 0.33, fy + 1)], fill=lite + (255,), width=max(2, int(fh * 0.1)))
    d.rectangle([W2 * 0.32, fy + fh * 0.88, W2 * 0.97, fy + fh], fill=deep + (255,))
    d.rectangle([W2 * 0.84, fy, W2 * 0.89, fy + fh * 0.2], fill=deep + (255,))  # hardy hole
    d.rectangle([W2 * 0.775, fy, W2 * 0.795, fy + fh * 0.2], fill=deep + (255,))  # pritchel hole
    out = _shade(_down(im, W, H), 0.25, 0.4)
    if hot:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        x0, x1, y = W * 0.45, W * 0.72, H * 0.06
        gd.rounded_rectangle([x0, y, x1, y + H * 0.06], radius=int(H * 0.03), fill=(255, 150, 50, 255))
        glow = g.filter(ImageFilter.GaussianBlur(max(3, W * 0.03)))
        for _ in range(14):
            sx, sy = rng.uniform(x0, x1), y - rng.uniform(0, H * 0.25)
            gd.ellipse([sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5], fill=(255, 210, 120, 255))
        glow.alpha_composite(g)
        out.alpha_composite(glow)
    return out


def _d_anvil_hot(W, H, color, rng):
    return _d_anvil(W, H, color, rng, hot=True)


def _d_tree(W, H, color, rng):
    """One complete tree inside its box (conifer if taller than 1.6:1, else broadleaf), 3 tones."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    trunk = _mix(color, (60, 40, 25), 0.6)
    tones = [_mix(color, (0, 0, 0), 0.35), color, _mix(color, (255, 255, 255), 0.18)]
    if H / max(W, 1) > 1.6:
        d.rectangle([W2 * 0.45, H2 * 0.78, W2 * 0.55, H2], fill=trunk + (255,))
        for k in range(5):
            t = k / 4
            top, base = H2 * (0.02 + t * 0.4), H2 * (0.28 + t * 0.54)
            half = W2 * (0.2 + 0.28 * t)
            d.polygon([(W2 / 2, top), (W2 / 2 - half, base), (W2 / 2 + half, base)], fill=tones[0] + (255,))
            d.polygon([(W2 / 2, top + 4), (W2 / 2 - half * 0.7, base - 2), (W2 / 2 + half * 0.15, base - 2)],
                      fill=tones[1] + (255,))
    else:
        d.polygon([(W2 * 0.46, H2), (W2 * 0.47, H2 * 0.5), (W2 * 0.53, H2 * 0.5), (W2 * 0.56, H2)], fill=trunk + (255,))
        d.line([(W2 * 0.5, H2 * 0.62), (W2 * 0.32, H2 * 0.45)], fill=trunk + (255,), width=int(W2 * 0.03))
        d.line([(W2 * 0.5, H2 * 0.58), (W2 * 0.68, H2 * 0.42)], fill=trunk + (255,), width=int(W2 * 0.03))
        for tone, sc in ((tones[0], 1.0), (tones[1], 0.8), (tones[2], 0.5)):
            for _ in range(7):
                cx, cy = W2 * rng.uniform(0.25, 0.75), H2 * rng.uniform(0.12, 0.45)
                r = W2 * rng.uniform(0.14, 0.24) * sc
                cx -= (1 - sc) * W2 * 0.06
                cy -= (1 - sc) * H2 * 0.05
                d.ellipse([cx - r, cy - r * 0.85, cx + r, cy + r * 0.85], fill=tone + (255,))
    return _down(im, W, H)


def _d_tower(W, H, color, rng):
    """A tall stone tower with crenellations, a conical roof and lit windows."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    x0, x1 = W2 * 0.27, W2 * 0.73
    bw = x1 - x0
    top = H2 * 0.27
    mortar = _mix(color, (0, 0, 0), 0.45)
    # round-tower shading across the width: lit left third, shadowed right edge
    def tone(u):  # u = 0..1 across the body
        return 1.12 - 0.55 * max(0.0, u - 0.25) ** 1.2 - 0.25 * max(0.0, 0.12 - u) * 4

    d.rectangle([x0, top, x1, H2], fill=mortar + (255,))
    bh = H2 * 0.042
    y, row = top + H2 * 0.012, 0
    while y < H2:  # staggered stone courses, each block its own tone
        x = x0 - (bw * 0.09 if row % 2 else 0)
        while x < x1:
            w = bw * rng.uniform(0.16, 0.26)
            u = ((x + w / 2) - x0) / bw
            c = tuple(int(v * tone(min(max(u, 0), 1)) * rng.uniform(0.9, 1.06)) for v in color)
            bx0, bx1 = max(x0, x + 2), min(x1, x + w - 2)
            if bx1 - bx0 >= 2:
                d.rectangle([bx0, y + 2, bx1, y + bh - 2], fill=c + (255,))
                d.line([(bx0, y + 2), (bx1, y + 2)], fill=_mix(c, (255, 255, 255), 0.18) + (255,), width=2)
            x += w
        y += bh
        row += 1
    # corbelled parapet with merlons
    py = top - H2 * 0.035
    _gpoly(im, [(x0 - W2 * 0.06, py), (x1 + W2 * 0.06, py), (x1 + W2 * 0.06, top + H2 * 0.01),
                (x0 - W2 * 0.06, top + H2 * 0.01)], _mix(color, (255, 255, 255), 0.12), _mix(color, (0, 0, 0), 0.4),
           horiz=True)
    for k in range(5):
        cx = x0 - W2 * 0.06 + (bw + W2 * 0.12) * (k + 0.5) / 5
        _gpoly(im, [(cx - W2 * 0.045, py - H2 * 0.045), (cx + W2 * 0.045, py - H2 * 0.045), (cx + W2 * 0.045, py),
                    (cx - W2 * 0.045, py)], _mix(color, (255, 255, 255), 0.15), _mix(color, (0, 0, 0), 0.3), horiz=True)
    for k in range(4):  # corbel shadows
        cx = x0 + bw * (k + 0.5) / 4
        d.polygon([(cx - W2 * 0.03, top + H2 * 0.01), (cx + W2 * 0.03, top + H2 * 0.01), (cx, top + H2 * 0.03)],
                  fill=_mix(color, (0, 0, 0), 0.55) + (255,))
    # slate cone roof, lit left
    rt = py - H2 * 0.045
    roof = [(x0 - W2 * 0.09, rt), (x1 + W2 * 0.09, rt), (W2 * 0.5, H2 * 0.005)]
    slate = _mix(color, (40, 44, 60), 0.55)
    _gpoly(im, roof, _mix(slate, (255, 255, 255), 0.2), _mix(slate, (0, 0, 0), 0.45), horiz=True)
    for t in np.linspace(0.2, 0.92, 6):
        yy = H2 * 0.005 + (rt - H2 * 0.005) * t
        half = (bw / 2 + W2 * 0.09) * t
        d.line([(W2 * 0.5 - half, yy), (W2 * 0.5 + half, yy)], fill=_mix(slate, (0, 0, 0), 0.35) + (200,), width=2)
    # arched windows: deep reveal, warm light, sill
    for wy in (0.42, 0.62):
        wx, ww, wh = W2 * 0.47, W2 * 0.11, H2 * 0.085
        d.rectangle([wx - ww / 2 - 4, H2 * wy - 4, wx + ww / 2 + 4, H2 * wy + wh + 4], fill=mortar + (255,))
        d.ellipse([wx - ww / 2 - 4, H2 * wy - ww / 2 - 4, wx + ww / 2 + 4, H2 * wy + ww / 2 + 4], fill=mortar + (255,))
        glow = [(wx - ww / 2, H2 * wy)] + [(wx - math.cos(a) * ww / 2, H2 * wy - math.sin(a) * ww / 2)
                                          for a in np.linspace(0, math.pi, 10)] + [(wx + ww / 2, H2 * wy + wh),
                                                                                   (wx - ww / 2, H2 * wy + wh)]
        _gpoly(im, glow, (255, 226, 160), (240, 150, 70))
        d.line([(wx, H2 * wy - ww / 2), (wx, H2 * wy + wh)], fill=mortar + (255,), width=max(2, int(W2 * 0.012)))
        d.rectangle([wx - ww / 2 - 6, H2 * wy + wh + 2, wx + ww / 2 + 6, H2 * wy + wh + 8],
                    fill=_mix(color, (255, 255, 255), 0.2) + (255,))
    # door
    dx, dw, dt = W2 * 0.5, W2 * 0.16, H2 * 0.86
    door = [(dx - dw / 2, H2)] + [(dx - math.cos(a) * dw / 2, dt - math.sin(a) * dw / 2)
                                  for a in np.linspace(0, math.pi, 10)] + [(dx + dw / 2, H2)]
    d.polygon(door, fill=mortar + (255,))
    _gpoly(im, [(x * 0.92 + dx * 0.08, y + (H2 - y) * 0.05) for x, y in door], (92, 64, 40), (52, 34, 22))
    out = _shade(_down(im, W, H), 0.25, 0.35)
    glow = Image.new("RGBA", out.size, (0, 0, 0, 0))  # windows spill a little light onto the stone
    gd = ImageDraw.Draw(glow)
    for wy in (0.42, 0.62):
        gd.ellipse([W * 0.47 - W * 0.14, H * wy - H * 0.03, W * 0.47 + W * 0.14, H * wy + H * 0.09],
                   fill=(255, 190, 110, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(max(2, W * 0.05)))
    glow.putalpha(ImageChops.multiply(glow.getchannel("A"), out.getchannel("A")))
    out.alpha_composite(glow)
    return out


def _d_pumpjack(W, H, color, rng):
    """Oil pumpjack: A-frame samson post, walking beam with horse head, crank and counterweight."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    dark, light = _mix(color, (0, 0, 0), 0.45), _mix(color, (255, 255, 255), 0.3)
    deep = _mix(color, (0, 0, 0), 0.65)
    lw = max(4, int(W2 * 0.022))
    _ellipse_shadow(im, W2 * 0.5, H2 * 0.975, W2 * 0.47, H2 * 0.03, 0.6)
    # skid and concrete pad
    _gpoly(im, [(W2 * 0.06, H2 * 0.9), (W2 * 0.95, H2 * 0.9), (W2 * 0.95, H2 * 0.975), (W2 * 0.06, H2 * 0.975)],
           light, dark)
    piv = (W2 * 0.5, H2 * 0.27)
    # wellhead under the horse head: stuffing box, tee and valves
    wx = W2 * 0.075
    d.line([(wx, H2 * 0.5), (wx, H2 * 0.9)], fill=_mix(color, (220, 220, 225), 0.6) + (255,), width=max(2, lw // 3))
    _gpoly(im, [(wx - W2 * 0.025, H2 * 0.78), (wx + W2 * 0.025, H2 * 0.78), (wx + W2 * 0.025, H2 * 0.9),
                (wx - W2 * 0.025, H2 * 0.9)], light, deep, horiz=True)
    d.rectangle([wx - W2 * 0.05, H2 * 0.83, wx + W2 * 0.05, H2 * 0.855], fill=dark + (255,))
    # samson post: A-frame of two legs with braces (rear leg darker)
    for (bx, c, wdt) in ((W2 * 0.6, dark, lw), (W2 * 0.39, color, lw)):
        d.line([(bx, H2 * 0.9), piv], fill=c + (255,), width=wdt)
    d.line([(W2 * 0.39, H2 * 0.9), piv], fill=light + (255,), width=max(2, lw // 3))
    for yy in (0.48, 0.68):
        t = (H2 * yy - piv[1]) / (H2 * 0.9 - piv[1])
        d.line([(piv[0] - (piv[0] - W2 * 0.39) * t, H2 * yy), (piv[0] + (W2 * 0.6 - piv[0]) * t, H2 * yy)],
               fill=color + (255,), width=max(2, lw // 2))
    # gearbox, crank and counterweight on the right
    cx, cy = W2 * 0.8, H2 * 0.66
    _gpoly(im, [(W2 * 0.72, H2 * 0.72), (W2 * 0.9, H2 * 0.72), (W2 * 0.92, H2 * 0.9), (W2 * 0.7, H2 * 0.9)],
           light, dark)
    ang = math.radians(rng.uniform(-30, 30))
    crank = (cx + math.cos(ang - math.pi / 2) * W2 * 0.09, cy + math.sin(ang - math.pi / 2) * W2 * 0.09)
    R = W2 * 0.13  # counterweight: heavy sector opposite the crank pin
    cw = [(cx, cy)] + [(cx + math.cos(a) * R, cy + math.sin(a) * R) for a in
                       np.linspace(ang + math.pi / 2 - 0.75, ang + math.pi / 2 + 0.75, 14)]
    _gpoly(im, cw, _mix(color, (150, 60, 40), 0.25), deep)
    d.line([(cx, cy), crank], fill=dark + (255,), width=lw)
    d.ellipse([cx - lw, cy - lw, cx + lw, cy + lw], fill=light + (255,))
    # walking beam (I-beam: lit top flange, dark web) from horse head to equalizer
    bl, br = (W2 * 0.14, H2 * 0.24), (W2 * 0.82, H2 * 0.3)
    bt = H2 * 0.05
    _gpoly(im, [(bl[0], bl[1] - bt / 2), (br[0], br[1] - bt / 2), (br[0], br[1] + bt / 2), (bl[0], bl[1] + bt / 2)],
           light, deep)
    d.line([(bl[0], bl[1] - bt / 2), (br[0], br[1] - bt / 2)], fill=_mix(light, (255, 255, 255), 0.3) + (255,),
           width=max(2, int(bt * 0.18)))
    # pitman arm from the equalizer down to the crank pin
    d.line([(br[0] - W2 * 0.01, br[1]), crank], fill=color + (255,), width=max(3, int(lw * 0.8)))
    d.line([(br[0] - W2 * 0.015, br[1]), (crank[0] - W2 * 0.005, crank[1])], fill=light + (255,),
           width=max(1, lw // 4))
    # horse head: a curved plate whose face is an arc around the pivot
    r_out = math.hypot(piv[0] - W2 * 0.03, piv[1] - bl[1])
    r_in = r_out - W2 * 0.07
    a0 = math.atan2(bl[1] - piv[1], W2 * 0.03 - piv[0])
    arc = [(piv[0] + math.cos(a0 + s) * r_out, piv[1] + math.sin(a0 + s) * r_out) for s in np.linspace(0.2, -0.26, 12)]
    back = [(piv[0] + math.cos(a0 + s) * r_in, piv[1] + math.sin(a0 + s) * r_in) for s in np.linspace(-0.16, 0.12, 6)]
    _gpoly(im, arc + back, light, dark)
    d.line(arc, fill=_mix(light, (255, 255, 255), 0.25) + (255,), width=max(2, lw // 3))
    # bridle: cables from the bottom of the head straight down to the polished rod
    hb = arc[-1]
    d.line([(hb[0], hb[1]), (wx, H2 * 0.5)], fill=deep + (255,), width=max(2, lw // 4))
    d.line([(wx - W2 * 0.012, H2 * 0.5), (wx + W2 * 0.012, H2 * 0.5)], fill=deep + (255,), width=max(3, lw // 2))
    # saddle bearing on the pivot
    d.ellipse([piv[0] - lw * 1.3, piv[1] - lw * 0.6, piv[0] + lw * 1.3, piv[1] + lw * 1.6], fill=dark + (255,))
    d.ellipse([piv[0] - lw * 0.5, piv[1], piv[0] + lw * 0.5, piv[1] + lw], fill=light + (255,))
    return _shade(_down(im, W, H), 0.25, 0.3)


def _d_plank_shelf(W, H, color, rng):
    """A flat wooden plank (square ends): light top edge, darker underside, soft shadow below."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([W * 0.02, H * 0.55, W * 0.98, H * 0.95], fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(max(2, H * 0.15))))
    d = ImageDraw.Draw(im)
    d.rectangle([0, H * 0.15, W - 1, H * 0.6], fill=color + (255,))
    d.rectangle([0, H * 0.15, W - 1, H * 0.24], fill=_mix(color, (255, 255, 255), 0.25) + (255,))
    d.rectangle([0, H * 0.52, W - 1, H * 0.6], fill=_mix(color, (0, 0, 0), 0.35) + (255,))
    for x in np.arange(W * 0.12, W, W * 0.23):
        d.line([(x, H * 0.26), (x + W * 0.04, H * 0.5)], fill=_mix(color, (0, 0, 0), 0.18) + (255,), width=1)
    return im


def _d_hanging_cord(W, H, color, rng):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = W / 2
    lw = max(2, int(W * 0.08))
    d.line([(cx, 0), (cx, H * 0.88)], fill=color + (255,), width=lw)
    for y in np.arange(4, H * 0.88, lw * 2.5):
        d.line([(cx - lw / 2, y), (cx + lw / 2, y + lw)], fill=_mix(color, (0, 0, 0), 0.35) + (255,), width=1)
    d.ellipse([cx - lw * 1.4, H * 0.04, cx + lw * 1.4, H * 0.04 + lw * 2.4], fill=_mix(color, (0, 0, 0), 0.2) + (255,))
    d.arc([cx - W * 0.3, H * 0.84, cx + W * 0.3, H * 0.99], 0, 200, fill=(150, 150, 156, 255), width=lw)
    return im


def _d_livestock(W, H, color, rng):
    """Farm animals on a grassy ground line, lit from the top-left: two cows with patches, a woolly
    sheep and a chicken, each with a contact shadow. color = the cows' coat."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    g = H2 * 0.92
    s = H2
    hide = color
    patch = _mix(color, (40, 30, 24), 0.62)
    belly = _mix(color, (0, 0, 0), 0.32)
    back = _mix(color, (255, 255, 255), 0.25)

    def shadow(x, w):
        _ellipse_shadow(im, x, g + s * 0.005, w, s * 0.025, 0.55)

    def cow(x, k, face=1):
        bw, bh = s * 0.5 * k, s * 0.25 * k
        y = g - s * 0.2 * k - bh / 2
        shadow(x, bw * 0.62)
        def leg(lx, c, top=y):
            d.rounded_rectangle([x + lx * bw - s * 0.022 * k, top, x + lx * bw + s * 0.022 * k, g],
                                radius=int(s * 0.01), fill=c + (255,))
        for lx in (-0.3, 0.3):  # far legs in shadow
            leg(lx, belly)
        body = Image.new("RGBA", im.size, (0, 0, 0, 0))  # gradient body with patches, clipped to a rounded hull
        _gpoly(body, [(x - bw / 2, y - bh / 2), (x + bw / 2, y - bh / 2), (x + bw / 2, y + bh / 2),
                      (x - bw / 2, y + bh / 2)], back, belly)
        bd = ImageDraw.Draw(body)
        for _ in range(3):
            px, py = x + rng.uniform(-0.35, 0.3) * bw, y + rng.uniform(-0.4, 0.2) * bh
            r = bh * rng.uniform(0.22, 0.38)
            bd.ellipse([px - r * 1.3, py - r, px + r * 1.3, py + r], fill=patch + (255,))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], radius=int(bh * 0.4),
                                               fill=255)
        body.putalpha(ImageChops.multiply(body.getchannel("A"), mask))
        im.alpha_composite(body)
        for lx in (-0.38, 0.22):  # near legs
            leg(lx, _mix(hide, (0, 0, 0), 0.15), y + bh * 0.3)
            d.rectangle([x + lx * bw - s * 0.022 * k, g - s * 0.025 * k, x + lx * bw + s * 0.022 * k, g],
                        fill=(40, 32, 28, 255))
        d.ellipse([x - bw * 0.05, y + bh * 0.38, x + bw * 0.12, y + bh * 0.62], fill=(222, 170, 160, 255))  # udder
        hx = x + face * bw * 0.56
        head = [(hx - face * s * 0.05 * k, y - bh * 0.5), (hx + face * s * 0.08 * k, y - bh * 0.32),
                (hx + face * s * 0.1 * k, y + bh * 0.12), (hx - face * s * 0.02 * k, y + bh * 0.18)]
        _gpoly(im, head, back, belly)
        mx = hx + face * s * 0.075 * k
        d.ellipse([mx - s * 0.035 * k, y - bh * 0.02, mx + s * 0.035 * k, y + bh * 0.2], fill=(214, 168, 150, 255))
        d.ellipse([hx + face * s * 0.02 * k - 3, y - bh * 0.3 - 3, hx + face * s * 0.02 * k + 3, y - bh * 0.3 + 3],
                  fill=(20, 16, 14, 255))
        d.line([(hx - face * s * 0.02 * k, y - bh * 0.48), (hx - face * s * 0.005 * k, y - bh * 0.72)],
               fill=(230, 222, 200, 255), width=max(2, int(s * 0.012)))  # horn
        d.polygon([(hx - face * s * 0.05 * k, y - bh * 0.42), (hx - face * s * 0.11 * k, y - bh * 0.5),
                   (hx - face * s * 0.05 * k, y - bh * 0.3)], fill=belly + (255,))  # ear
        tx = x - face * bw / 2
        d.line([(tx, y - bh * 0.35), (tx - face * bw * 0.06, y + bh * 0.45)], fill=belly + (255,),
               width=max(2, int(s * 0.01)))
        d.ellipse([tx - face * bw * 0.06 - 4, y + bh * 0.4, tx - face * bw * 0.06 + 4, y + bh * 0.58],
                  fill=patch + (255,))

    def sheep(x, k):
        y = g - s * 0.27 * k
        wool, wool_dk = _mix(color, (246, 242, 232), 0.8), _mix(color, (150, 140, 128), 0.6)
        shadow(x, s * 0.2 * k)
        for lx in (-0.1, 0.1):
            d.rectangle([x + lx * s * k - 3, y + s * 0.07 * k, x + lx * s * k + 3, g], fill=(46, 40, 38, 255))
        puffs = [(rng.uniform(-0.17, 0.17) * s * k, rng.uniform(-0.07, 0.05) * s * k) for _ in range(8)]
        r = s * 0.09 * k
        for ox, oy in puffs:  # shadow side first, lit puffs offset up-left on top
            d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r], fill=wool_dk + (255,))
        for ox, oy in puffs:
            d.ellipse([x + ox - r * 0.85 - 3, y + oy - r * 0.85 - 4, x + ox + r * 0.7 - 3, y + oy + r * 0.7 - 4],
                      fill=wool + (255,))
        d.ellipse([x + s * 0.17 * k, y - s * 0.12 * k, x + s * 0.29 * k, y + s * 0.0], fill=(52, 44, 40, 255))
        d.ellipse([x + s * 0.24 * k - 2, y - s * 0.08 * k - 2, x + s * 0.24 * k + 2, y - s * 0.08 * k + 2],
                  fill=(230, 220, 200, 255))

    def chicken(x, k):
        y = g - s * 0.12 * k
        body, bdk = _mix(color, (250, 246, 236), 0.75), _mix(color, (170, 160, 150), 0.6)
        shadow(x, s * 0.08 * k)
        d.line([(x - s * 0.01 * k, y + s * 0.03 * k), (x - s * 0.01 * k, g)], fill=(230, 160, 60, 255), width=3)
        d.line([(x + s * 0.02 * k, y + s * 0.03 * k), (x + s * 0.025 * k, g)], fill=(230, 160, 60, 255), width=3)
        d.polygon([(x - s * 0.07 * k, y - s * 0.04 * k), (x - s * 0.15 * k, y - s * 0.14 * k), (x - s * 0.1 * k, y)],
                  fill=bdk + (255,))
        d.ellipse([x - s * 0.08 * k, y - s * 0.07 * k, x + s * 0.06 * k, y + s * 0.05 * k], fill=bdk + (255,))
        d.ellipse([x - s * 0.075 * k, y - s * 0.075 * k, x + s * 0.05 * k, y + s * 0.03 * k], fill=body + (255,))
        d.ellipse([x + s * 0.03 * k, y - s * 0.14 * k, x + s * 0.09 * k, y - s * 0.07 * k], fill=body + (255,))
        d.polygon([(x + s * 0.045 * k, y - s * 0.14 * k), (x + s * 0.06 * k, y - s * 0.17 * k),
                   (x + s * 0.075 * k, y - s * 0.14 * k)], fill=(200, 40, 36, 255))
        d.polygon([(x + s * 0.09 * k, y - s * 0.115 * k), (x + s * 0.115 * k, y - s * 0.105 * k),
                   (x + s * 0.09 * k, y - s * 0.095 * k)], fill=(236, 170, 60, 255))

    ground = _mix(color, (60, 80, 40), 0.55)
    d.line([(0, g), (W2, g)], fill=_mix(ground, (0, 0, 0), 0.25) + (220,), width=max(2, int(H2 * 0.018)))
    cow(W2 * 0.2, 1.0, 1)
    sheep(W2 * 0.48, 0.9)
    cow(W2 * 0.72, 0.85, -1)
    chicken(W2 * 0.9, 0.9)
    x = rng.uniform(0, 10)
    while x < W2:  # grass tufts along the ground line
        h = H2 * rng.uniform(0.02, 0.05)
        c = _mix(ground, (255, 255, 255), rng.uniform(0, 0.2))
        for dx in (-4, 0, 4):
            d.line([(x, g + 2), (x + dx * 1.5, g - h)], fill=c + (255,), width=2)
        x += rng.uniform(14, 34)
    return _down(im, W, H)


def _d_mine_entrance(W, H, color, rng):
    """Timber mine portal: two posts, a lintel, a dark opening and plank grain."""
    im = _ss(W, H)
    d = ImageDraw.Draw(im)
    W2, H2 = W * 2, H * 2
    lite, dark, deep = _mix(color, (255, 255, 255), 0.25), _mix(color, (0, 0, 0), 0.4), _mix(color, (0, 0, 0), 0.65)
    # tunnel: dark gradient towards a vanishing point, receding inner frames, rails, lantern glow deep inside
    ox0, ox1, oy0 = W2 * 0.18, W2 * 0.82, H2 * 0.18
    vx, vy = W2 * 0.52, H2 * 0.6
    _gpoly(im, [(ox0, oy0), (ox1, oy0), (ox1, H2), (ox0, H2)], (34, 28, 24), (16, 13, 12))
    lamp = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(lamp).ellipse([vx - W2 * 0.16, vy - H2 * 0.16, vx + W2 * 0.16, vy + H2 * 0.14],
                                 fill=(255, 170, 80, 120))
    im.alpha_composite(lamp.filter(ImageFilter.GaussianBlur(W2 * 0.06)))
    for t in (0.45, 0.7, 0.86):  # inner frames get smaller and darker with depth
        fx0, fx1 = ox0 + (vx - ox0) * t, ox1 + (vx - ox1) * t
        fy0, fy1 = oy0 + (vy - oy0) * t, H2 + (vy - H2) * t * 0.55
        c = _mix(color, (20, 16, 14), 0.35 + 0.5 * t)
        pw = max(2, int(W2 * 0.05 * (1 - t)))
        d.rectangle([fx0, fy0, fx0 + pw, fy1], fill=c + (255,))
        d.rectangle([fx1 - pw, fy0, fx1, fy1], fill=c + (255,))
        d.rectangle([fx0, fy0, fx1, fy0 + pw], fill=c + (255,))
    d.ellipse([vx - W2 * 0.012, vy - H2 * 0.05, vx + W2 * 0.012, vy - H2 * 0.02], fill=(255, 214, 140, 255))
    rail = _mix(color, (150, 150, 160), 0.6)
    for k in range(6):  # sleepers
        t = k / 6
        y = H2 - (H2 - (vy + H2 * 0.04)) * t ** 0.8
        half = W2 * 0.2 * (1 - t * 0.85)
        d.line([(vx - half, y), (vx + half, y)], fill=_mix(color, (0, 0, 0), 0.3 + 0.4 * t) + (255,),
               width=max(2, int(H2 * 0.02 * (1 - t))))
    for s in (-1, 1):
        d.line([(vx + s * W2 * 0.13, H2), (vx + s * W2 * 0.02, vy + H2 * 0.04)], fill=rail + (255,),
               width=max(2, int(W2 * 0.01)))
    # timber portal: posts with grain, lintel, corner knee braces, lit from the top-left
    post = W2 * 0.12
    for x, lit in ((W2 * 0.1, True), (W2 * 0.9 - post, False)):
        _gpoly(im, [(x, H2 * 0.12), (x + post, H2 * 0.12), (x + post, H2), (x, H2)],
               lite if lit else color, color if lit else deep, horiz=True)
        for y in np.arange(H2 * 0.2, H2, H2 * rng.uniform(0.07, 0.1)):
            d.line([(x + post * 0.18, y), (x + post * 0.75, y + 5)], fill=dark + (200,), width=2)
    _gpoly(im, [(W2 * 0.04, H2 * 0.03), (W2 * 0.96, H2 * 0.03), (W2 * 0.96, H2 * 0.18), (W2 * 0.04, H2 * 0.18)],
           lite, dark)
    d.line([(W2 * 0.04, H2 * 0.04), (W2 * 0.96, H2 * 0.04)], fill=_mix(lite, (255, 255, 255), 0.25) + (255,), width=3)
    for x in (W2 * 0.06, W2 * 0.94):  # log ends
        d.ellipse([x - W2 * 0.035, H2 * 0.06, x + W2 * 0.035, H2 * 0.15], fill=_mix(color, (210, 170, 120), 0.5) + (255,))
        d.ellipse([x - W2 * 0.015, H2 * 0.09, x + W2 * 0.015, H2 * 0.12], fill=dark + (255,))
    for x0_, s in ((W2 * 0.22, 1), (W2 * 0.78, -1)):
        d.polygon([(x0_, H2 * 0.18), (x0_ + s * W2 * 0.1, H2 * 0.18), (x0_, H2 * 0.3)], fill=dark + (255,))
    return _shade(_down(im, W, H), 0.2, 0.3)


_DECOR = {
    "anvil": _d_anvil, "anvil_hot": _d_anvil_hot, "tree": _d_tree, "tower": _d_tower, "pumpjack": _d_pumpjack,
    "plank_shelf": _d_plank_shelf, "hanging_cord": _d_hanging_cord, "livestock": _d_livestock,
    "mine_entrance": _d_mine_entrance,
    "tree_line": _d_tree_line, "fireflies": _d_fireflies, "aurora": _d_aurora, "snowfall": _d_snowfall,
    "snowy_range": _d_snowy_range, "sun": _d_sun, "falling_leaves": _d_falling_leaves, "wheat_field": _d_wheat_field,
    "pipes": _d_pipes, "power_line": _d_power_line, "smokestack": _d_smokestack, "circuit": _d_circuit,
    "lightning": _d_lightning, "heartbeat": _d_heartbeat, "light_rays": _d_light_rays, "compass_rose": _d_compass_rose,
    "contour_map": _d_contour_map, "castle": _d_castle,
    "campfire": _d_campfire, "water_wheel": _d_water_wheel, "windmill_sails": _d_windmill_sails,
    "rocket": _d_rocket, "planet_horizon": _d_planet_horizon, "satellite": _d_satellite,
    "cave_painting_herd": _d_cave_painting_herd,
    "cog": _d_cog, "gear_cluster": _d_gear_cluster, "planet": _d_planet, "ringed_planet": _d_ringed_planet,
    "moon": _d_moon, "nebula_glow": _d_nebula_glow, "mountain_range": _d_mountain_range,
    "strata_band": _d_strata_band, "arrowhead": _d_arrowhead, "hand_print": _d_hand_print,
    "star_cluster": _d_star_cluster, "orbit_ring": _d_orbit_ring, "soft_glow": _d_soft_glow,
    "sky_band": _d_sky_band, "embers": _d_embers, "milky_way": _d_milky_way, "comet": _d_comet,
    "shaft": _d_shaft, "belt": _d_belt, "blueprint": _d_blueprint, "cave_painting": _d_cave_painting,
}
# ---------------------------------------------------------------- create chapter: pixel Create parts
# (additive block: pixel cogwheel / water wheel / windmill sails / shaft / belt / water / steam, all drawn on a
#  coarse k-px texel grid from real Create / Minecraft texels so they sit with the `blocks` and sprites)
def _cx_wood(w, h, ox=0, oy=0, name="minecraft:block/spruce_planks"):
    """Real plank texels (Create's wood) tiled into an (h, w, 3) float array."""
    try:
        t = np.asarray(tex(name), np.float32)[..., :3] / 255
    except Exception:  # pragma: no cover - texture missing
        t = np.tile(np.array([112, 82, 46], np.float32) / 255, (16, 16, 1))
    return t[(np.arange(h)[:, None] + oy) % t.shape[0], (np.arange(w)[None, :] + ox) % t.shape[1]]


def _cx_finish(col, mask, k, W, H, depth=2, outline=0.5, side=0.5):
    """(h, w, 3) colours + (h, w) mask -> RGBA W x H: extruded thickness toward the lower right, dark one-texel
    outline, one-texel highlight on the lit (upper-left) inner edge, nearest-upscaled by k."""
    h, w = mask.shape
    col = np.clip(col, 0, 1).copy()
    full = mask.copy()
    scol = np.zeros_like(col)
    for d in range(1, depth + 1):
        for ox, oy in ((d, d), (d, d - 1), (d - 1, d)):
            m = _shift(mask.astype(np.uint8), ox, oy).astype(bool) & ~full
            if m.any():
                for c in range(3):
                    scol[..., c] = np.where(m, _shift(col[..., c], ox, oy) * side, scol[..., c])
                full |= m
    ext = full & ~mask
    col = np.where(ext[..., None], scol, col)
    up = _shift(full.astype(np.uint8), 0, 1).astype(bool)      # cell above is solid
    lf = _shift(full.astype(np.uint8), 1, 0).astype(bool)
    dn = _shift(full.astype(np.uint8), 0, -1).astype(bool)
    rt = _shift(full.astype(np.uint8), -1, 0).astype(bool)
    edge = full & ~(up & lf & dn & rt)
    hi = mask & ~edge & (_shift(edge.astype(np.uint8), 0, 1).astype(bool)
                         | _shift(edge.astype(np.uint8), 1, 0).astype(bool))
    col = np.where(hi[..., None], col * 1.16, col)
    col = np.where(edge[..., None], col * (1 - outline * 0.76), col)
    out = np.zeros((h, w, 4), np.float32)
    out[..., :3] = np.clip(col, 0, 1)
    out[..., 3] = full.astype(np.float32)
    im = _img(out, "RGBA").resize((w * k, h * k), Image.NEAREST)
    res = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    res.paste(im, (0, 0))
    return res


def _cx_grid(W, H, k):
    k = max(2, int(k))
    return k, max(8, W // k), max(8, H // k)


def _d_create_cog(W, H, color, rng, teeth=12, phase=0.0, k=4, hub=(118, 122, 118), depth=2, holes=0, metal=False,
                  hole_w=0.28):
    """Pixel Create cogwheel seen face-on: plank body with a lighter rim and teeth (real spruce texels tinted
    by `color`, default wood (112,82,46); `metal` true = flat `color` metal with plank grain), andesite hub with a
    dark axle square, thickness shown as a dark side. `teeth` count, `phase` (0..1 of a tooth pitch; use it to mesh neighbours), `k` px per texel (match the
    scene texel), `holes` N > 0 cuts N window holes between hub and rim (large cogs / flywheels; `hole_w` 0.2-0.4 = hole
    width as a fraction of the sector), `depth` side texels. `teeth` 0 with `phase` 0.25 = smooth flywheel disc."""
    k, w, h = _cx_grid(W, H, k)
    cx, cy = (w - depth) / 2, (h - depth) / 2
    R = min(w - depth, h - depth) / 2 - 0.3
    td = max(2.0, round(R * 0.2))
    Rb = R - td
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = x + 0.5 - cx, y + 0.5 - cy
    r = np.hypot(dx, dy)
    th = np.arctan2(dy, dx)
    fr = (th / (2 * np.pi) * teeth + phase) % 1.0
    taper = np.clip((r - Rb) / td, 0, 1)
    tooth = np.abs(fr - 0.25) < (0.27 - 0.09 * taper)
    mask = (r <= Rb + 0.5) | ((r <= R) & tooth)
    Rh = max(3.2, R * 0.3)
    if holes:
        sec = (th / (2 * np.pi) * holes + 0.5) % 1.0
        mask &= ~((r > Rh + 2.2) & (r < Rb - 2.6) & (np.abs(sec - 0.5) < hole_w))
    grain = _cx_wood(w, h, int(phase * 7), 3)
    if metal:
        col = np.array(color, np.float32) / 255 * (grain.mean(axis=2, keepdims=True) / 0.34)
    else:
        col = grain * (np.array(color, np.float32) / np.array([112, 82, 46], np.float32))
    col = np.where(((r > Rb + 0.5))[..., None], col * 1.12, col)                       # teeth
    col = np.where(((r > Rb - 1.5) & (r <= Rb + 0.5))[..., None], col * 1.22, col)     # rim band
    if R > 10:
        col = np.where(((r > Rb - 3.2) & (r <= Rb - 1.5))[..., None], col * 0.74, col)  # groove inside the rim
    col = np.where(((r > Rh) & (r <= Rh + 1.3))[..., None], col * 0.55, col)           # shadow ring round the hub
    g = np.clip(1.12 - 0.3 * (dx + dy) / (2 * Rh), 0.7, 1.25)[..., None]
    hubc = np.array(hub, np.float32) / 255 * g
    hubc = np.where(((r > Rh - 1.0))[..., None], hubc * 0.8, hubc)
    col = np.where((r <= Rh)[..., None], hubc, col)
    ax = max(1.0, R * 0.08)
    col = np.where(((r <= ax * 2.3) & (r <= Rh))[..., None], col * 0.8, col)       # socket round the axle
    axle = (np.abs(dx) <= ax) & (np.abs(dy) <= ax)
    col = np.where(axle[..., None], np.array([0.22, 0.23, 0.22], np.float32), col)
    col = np.where((axle & (dx < 0) & (dy < 0))[..., None], np.array([0.36, 0.37, 0.36], np.float32), col)
    return _cx_finish(col, mask, k, W, H, depth)


def _d_create_wheel(W, H, color, rng, blades=12, spokes=8, phase=0.0, k=4, depth=2, hub=(92, 94, 92), ring=False,
                    paddles=True, lip=True, metal=False, rim=0.1, spoke_w=0.058):
    """Pixel Create water wheel, face-on: boarded rim, radial paddle boards with a hooked lip (`lip`), wooden
    spokes (`spoke_w` = width as a fraction of the radius) + optional inner `ring`, steel hub (real spruce /
    stripped-log texels). `blades` paddles, `spokes` beams, `phase` 0..1 of a blade pitch (rotation), `k` px per
    texel, `color` = wood tint (default (112,82,46)), `rim` = rim thickness / radius. `paddles` false drops the
    paddles and `metal` true uses flat `color` metal: together a flywheel."""
    k, w, h = _cx_grid(W, H, k)
    cx, cy = (w - depth) / 2, (h - depth) / 2
    R = min(w - depth, h - depth) / 2 - 0.3
    pl = max(3.0, R * 0.2) if paddles else 0.0   # paddle length beyond the rim
    Rr = R - pl                        # rim outer radius
    rt = max(3.0, R * rim)             # rim thickness
    Rh = max(4.2, R * 0.14)
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = x + 0.5 - cx, y + 0.5 - cy
    r = np.hypot(dx, dy)
    th = np.arctan2(dy, dx)
    pitch = 2 * np.pi / blades
    dth = ((th - phase * pitch + pitch / 2) % pitch) - pitch / 2
    arc = np.abs(dth) * r
    pw = max(2.4, R * 0.115)
    rimm = (r <= Rr) & (r > Rr - rt)
    pad = (r > Rr - rt * 0.5) & (r <= R) & (arc <= pw) if paddles else np.zeros_like(rimm)
    if paddles and lip:  # hooked tip: a bucket lip reaching sideways at the end of every paddle
        pad = pad | ((r > R - 2.3) & (r <= R) & (dth * r > pw - 0.6) & (dth * r <= pw + 3.0))
    sp = 2 * np.pi / spokes
    ds = ((th - phase * pitch + sp / 2) % sp) - sp / 2
    sw = max(2.0, R * spoke_w)
    spoke = (np.abs(ds) * r <= sw) & (r > Rh * 0.6) & (r <= Rr - rt * 0.5)
    ringm = ring & (r > R * 0.5) & (r <= R * 0.5 + max(1.6, R * 0.05))
    mask = rimm | pad | spoke | ringm | (r <= Rh)
    if metal:
        base = np.array(color, np.float32) / 255
        plank = base * (_cx_wood(w, h, 2, 5).mean(axis=2, keepdims=True) / 0.34)
        log = base * (_cx_wood(w, h, 5, 1, "minecraft:block/stripped_spruce_log").mean(axis=2, keepdims=True) / 0.36)
    else:
        tint = np.array(color, np.float32) / np.array([112, 82, 46], np.float32)
        plank = _cx_wood(w, h, 2, 5) * tint
        log = _cx_wood(w, h, 5, 1, "minecraft:block/stripped_spruce_log") * tint
    board = (np.floor((th - phase * pitch) / pitch + 0.5).astype(np.int32) % 2)[..., None]
    col = plank * 0.96
    col = np.where(rimm[..., None], plank * np.where(board == 1, 0.88, 1.04), col)
    col = np.where(pad[..., None], log * 1.2, col)
    col = np.where((pad & (r > R - 1.2))[..., None], col * 0.8, col)
    col = np.where((spoke | ringm)[..., None] & ~rimm[..., None] & ~pad[..., None], plank * 1.0, col)
    gh = np.clip(1.1 - 0.3 * (dx + dy) / (2 * Rh), 0.7, 1.2)[..., None]
    hubc = np.array(hub, np.float32) / 255 * gh
    hubc = np.where((r > Rh - 1.0)[..., None], hubc * 0.78, hubc)
    col = np.where((r <= Rh)[..., None], hubc, col)
    ax = max(1.0, R * 0.06)
    axle = (np.abs(dx) <= ax) & (np.abs(dy) <= ax)
    col = np.where(axle[..., None], np.array([0.2, 0.21, 0.2], np.float32), col)
    col = np.where((axle & (dx < 0) & (dy < 0))[..., None], np.array([0.38, 0.39, 0.38], np.float32), col)
    return _cx_finish(col, mask, k, W, H, depth)


def _d_create_sails(W, H, color, rng, arms=4, ang=20.0, k=4, depth=2, hub_r=0.2):
    """Pixel windmill sails seen face-on: `arms` wooden beams radiating from the centre, each with a canvas sail
    (colour `color`, default off-white (226,222,208)) on its trailing side with a wooden lattice. `ang` degrees (not `rot`),
    `hub_r` fraction of the radius left empty for a hub block drawn on top (a `blocks` bearing)."""
    k, w, h = _cx_grid(W, H, k)
    cx, cy = (w - depth) / 2, (h - depth) / 2
    R = min(w - depth, h - depth) / 2 - 0.3
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = x + 0.5 - cx, y + 0.5 - cy
    mask = np.zeros((h, w), bool)
    col = np.zeros((h, w, 3), np.float32)
    beam_c = _cx_wood(w, h, 4, 2, "minecraft:block/stripped_spruce_log") * 0.86
    cloth = np.array(color, np.float32) / 255
    lat = np.array([0.40, 0.29, 0.17], np.float32)
    sw = R * 0.3
    for i in range(arms):
        a = math.radians(ang) + i * 2 * math.pi / arms
        u = dx * math.cos(a) + dy * math.sin(a)
        v = -dx * math.sin(a) + dy * math.cos(a)
        beam = (np.abs(v) <= 2.0) & (u > R * hub_r * 0.5) & (u <= R)
        sail = (v > 1.9) & (v <= 1.9 + sw) & (u > R * hub_r + 1.0) & (u <= R - 0.5)
        t = np.clip((v - 1.9) / max(sw, 1), 0, 1)
        fold = np.where((np.floor((v - 1.9) / 2.6).astype(np.int32) % 2) == 0, 1.05, 0.93)
        cc = cloth * (fold * (1.0 - 0.14 * t))[..., None]
        batten = ((u - R * hub_r) % 7.0) < 1.0
        rail = (v > 1.9 + sw - 1.0) | (v <= 2.9) | (u > R - 1.6) | (u <= R * hub_r + 2.0)
        latt = sail & (batten | rail)
        cc = np.where(latt[..., None], lat * (1.12 - 0.3 * t)[..., None], cc)
        bshade = (1.18 - 0.28 * np.clip((v + 2.0) / 4.0, 0, 1))[..., None]      # lit upper edge of the beam
        m = beam | sail
        col = np.where(m[..., None], np.where(beam[..., None], beam_c * bshade, cc), col)
        mask |= m
    return _cx_finish(col, mask, k, W, H, depth)


def _d_create_shaft(W, H, color, rng, k=4, thick=5, joints=16, depth=1):
    """Pixel Create shaft (horizontal; `rot` 90 for vertical): a rod of `thick` texels (outline included) in
    `color` with a lit upper half, a darker lower half and a collar every `joints` texels (one block)."""
    k, w, h = _cx_grid(W, H, k)
    mask = np.zeros((h, w), bool)
    col = np.zeros((h, w, 3), np.float32)
    c = np.array(color, np.float32) / 255
    t0 = max(1, (h - depth - thick) // 2)
    for j in range(thick):
        row = t0 + j
        if 0 <= row < h:
            f = 1.0 + 0.3 * (1 - 2.0 * j / max(1, thick - 1)) * 0.8
            mask[row, :] = True
            col[row, :] = c * f
    for xx in range(joints // 2, w - 1, joints):
        for dxx in (0, 1):
            for row in (t0 - 1, t0 + thick):
                if 0 <= row < h:
                    mask[row, xx + dxx] = True
                    col[row, xx + dxx] = c * (0.55 if row == t0 + thick else 0.85)
            for j in range(thick):
                if 0 <= t0 + j < h:
                    col[t0 + j, xx + dxx] = c * (0.58 if dxx else 0.8)
    return _cx_finish(col, mask, k, W, H, depth)


def _d_create_belt(W, H, color, rng, k=4, thick=10, legs=3, scroll=0):
    """Pixel Create mechanical belt from the side: a thick dark rubber loop with lit tread ticks on the top run,
    an andesite plate (`color`, default (130,135,132)) with bolts inside the loop, end pulleys, and `legs`
    support legs down to the image bottom. `thick` = belt height in texels, `scroll` shifts the tread ticks."""
    k, w, h = _cx_grid(W, H, k)
    rb = thick / 2.0
    band = 3.0
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    px, py = x + 0.5, y + 0.5
    nx = np.clip(px, rb, w - rb)
    dist = np.hypot(px - nx, py - rb)
    loop = (dist <= rb) & (py <= thick)
    inner = dist <= rb - band
    mask = loop.copy()
    rub = np.array([48, 44, 38], np.float32) / 255
    tickc = np.array([104, 94, 76], np.float32) / 255
    pl = np.array(color, np.float32) / 255
    col = np.broadcast_to(rub, (h, w, 3)).copy()
    topband = loop & ~inner & (py < rb)
    tick = topband & (((x + scroll) % 4) < 2)
    col = np.where(tick[..., None], tickc, col)
    col = np.where((topband & (py < 1.2))[..., None], tickc * 1.08, col)
    col = np.where((loop & ~inner & (py >= rb))[..., None], rub * 0.75, col)
    plate = pl * np.clip(1.1 - 0.3 * (py - band) / thick, 0.7, 1.15)[..., None] * 0.82
    col = np.where(inner[..., None], plate, col)
    bolt = inner & (np.abs(py - rb) < 0.7) & (((x - rb) % 12) < 1.3)
    col = np.where(bolt[..., None], pl * 0.45, col)
    for cxp in (rb, w - rb):   # pulleys
        pr = np.hypot(px - cxp, py - rb)
        col = np.where((pr <= rb - band - 0.2)[..., None], pl * 1.12, col)
        col = np.where((pr <= 1.3)[..., None], np.array([0.2, 0.2, 0.2], np.float32), col)
    lw = 5
    for j in range(legs):
        lx = int(rb + 3 + j * (w - 2 * rb - 6 - lw) / max(1, legs - 1)) if legs > 1 else int(w / 2 - lw / 2)
        for yy in range(int(thick - 1), h):
            for xx in range(lx, lx + lw):
                if 0 <= xx < w and yy < h and not loop[yy, xx]:
                    mask[yy, xx] = True
                    col[yy, xx] = pl * (0.58 if xx >= lx + lw - 1 else (0.95 if xx == lx else 0.76))
    return _cx_finish(col, mask, k, W, H, depth=1)


def _d_create_water(W, H, color, rng, k=4, pool=1.0, fall=None, fall_w=7, foam=1, splash=None):
    """Pixel water: a pool filling the bottom `pool` fraction of the box (rippled surface, foam row, darker
    depth, light dashes) and optionally a waterfall column at x fraction `fall` (`fall_w` texels wide) pouring
    from the top into the pool. `color` = mid water colour (default (52,112,188)). Use alpha ~0.85. `foam` = number
    of light foam rows along the surface (default 1), `splash` = optional list of x fractions where a few white
    droplets jump above the surface (paddle tips)."""
    k, w, h = _cx_grid(W, H, k)
    c = np.array(color, np.float32) / 255
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    ys = int(round(h * (1 - pool)))
    wave = np.round(np.sin(x * 0.33 + 1.3) * 0.9 + np.sin(x * 0.11) * 0.8)
    body = (y >= (ys + wave)) & (pool > 0)
    t = np.clip((y - ys) / max(h - ys, 1), 0, 1)[..., None]
    col = c * (1.12 - 0.5 * t)
    nz = np.array([[rng.random() for _ in range(w)] for _ in range(h)], np.float32)
    dash = body & (y > ys + 2) & (nz > 0.93)
    col = np.where(dash[..., None], np.minimum(c * 1.45, 1), col)
    foam_m = body & (y <= ys + wave + 0.9)
    col = np.where(foam_m[..., None], np.array([0.78, 0.9, 0.97], np.float32), col)
    mask = body.copy()
    if foam and foam > 1:   # a second, broken foam row below the first (every other texel)
        f2 = body & (y > ys + wave + 0.9) & (y <= ys + wave + 1.9) & (((x.astype(np.int32) + int(ys)) % 3) != 0)
        col = np.where(f2[..., None], np.array([0.6, 0.76, 0.9], np.float32), col)
    for sx in (splash or []):   # droplets leaping off the surface
        cxs = int(round(float(sx) * w))
        for ddx, ddy in ((0, -2), (-1, -3), (1, -3), (0, -4), (-2, -2), (2, -2)):
            xx, yy = cxs + ddx, int(ys) + ddy
            if 0 <= xx < w and 0 <= yy < h and not body[yy, xx]:
                col[yy, xx] = np.array([0.84, 0.93, 0.98], np.float32)
                mask[yy, xx] = True
    if fall is not None:
        fx = fall * w
        fm = (np.abs(x + 0.5 - fx) <= fall_w / 2) & (y < (ys + 2 if pool > 0 else h))
        streak = ((x.astype(np.int32) + (y.astype(np.int32) // 3) * (x.astype(np.int32) % 2)) % 3 == 0)
        fc = c * 1.2
        fc = np.broadcast_to(fc, (h, w, 3)).copy()
        fc = np.where(streak[..., None], np.minimum(fc * 1.35, 1), fc)
        fc = np.where((np.abs(x + 0.5 - fx) > fall_w / 2 - 1)[..., None], c * 0.8, fc)
        col = np.where(fm[..., None], fc, col)
        mask |= fm
        splash = (np.abs(x + 0.5 - fx) <= fall_w / 2 + 2) & (np.abs(y - ys) <= 1.2) & (nz > 0.35)
        col = np.where(splash[..., None], np.array([0.85, 0.93, 0.98], np.float32), col)
        mask |= splash & (pool > 0)
    out = np.zeros((h, w, 4), np.float32)
    out[..., :3] = np.clip(col, 0, 1)
    out[..., 3] = mask.astype(np.float32)
    im = _img(out, "RGBA").resize((w * k, h * k), Image.NEAREST)
    res = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    res.paste(im, (0, 0))
    return res


def _d_create_steam(W, H, color, rng, k=4, puffs=8, drift=0.3):
    """A rising plume of pixel steam puffs: small and dense at the bottom, large and faint at the top, three
    tones (lit upper-left, shaded lower-right). `color` = base tone (default (226,230,236)); use layer alpha
    ~0.5. `drift` leans the plume sideways (-1..1)."""
    k, w, h = _cx_grid(W, H, k)
    base = np.array(color, np.float32) / 255
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    out = np.zeros((h, w, 4), np.float32)
    rmax = w * 0.26
    order = []
    for j in range(puffs):
        t = j / max(1, puffs - 1)
        rad = 2.2 + (rmax - 2.2) * (t ** 0.85) * rng.uniform(0.8, 1.1)
        cy = max(rad + 1, h * 0.92 - t * h * 0.8 - rng.uniform(0, h * 0.03))
        cx = w * (0.5 + drift * 0.3 * t) + rng.uniform(-1, 1) * w * 0.1 * (0.3 + t)
        cx = min(max(cx, rad + 1), w - rad - 1)
        order.append((t, cx, cy, rad, 0.95 - 0.6 * t))
    for t, cx, cy, rad, al in sorted(order, reverse=True):  # high faint puffs first, low dense ones over them
        for sub in range(3):
            ox = (sub - 1) * rad * 0.62
            oy = 0.28 * rad if sub != 1 else 0.0
            rr = rad * (1.0 if sub == 1 else 0.66)
            d = np.hypot(x + 0.5 - (cx + ox), y + 0.5 - (cy + oy))
            m = d <= rr
            if not m.any():
                continue
            lit = ((x + 0.5 - (cx + ox)) + (y + 0.5 - (cy + oy))) / max(rr, 1)
            tone = np.where(lit < -0.5, 1.08, np.where(lit > 0.55, 0.84, 0.97))[..., None] * base
            out[..., :3] = np.where(m[..., None], np.clip(tone, 0, 1), out[..., :3])
            out[..., 3] = np.where(m, al, out[..., 3])
    im = _img(out, "RGBA").resize((w * k, h * k), Image.NEAREST)
    res = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    res.paste(im, (0, 0))
    return res


_DECOR.update({"create_cog": _d_create_cog, "create_wheel": _d_create_wheel, "create_sails": _d_create_sails,
               "create_shaft": _d_create_shaft, "create_belt": _d_create_belt, "create_water": _d_create_water,
               "create_steam": _d_create_steam})


# ---------------------------------------------------------------- space chapter motifs (round 2: pixel sky bodies, rocket, gantry, atlas crops)
# All drawn on a coarse grid of `k` canvas px per texel and NEAREST-upscaled, so they share the scene texel.
def _sp_h3(a, b, c, seed):
    n = ((a * 73856093) ^ (b * 19349663) ^ (c * 83492791) ^ ((seed * 2654435761) & 0xFFFFFFFF)) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF).astype(np.float32) / 65535.0


def _sp_noise3(x, y, z, seed):
    xi, yi, zi = (np.floor(v).astype(np.int64) for v in (x, y, z))
    sx, sy, sz = ((v - np.floor(v)) for v in (x, y, z))
    sx, sy, sz = (f * f * (3 - 2 * f) for f in (sx, sy, sz))

    def c(dx, dy, dz):
        return _sp_h3(xi + dx, yi + dy, zi + dz, seed)

    def lerp(a, b, t):
        return a + (b - a) * t

    x00, x10 = lerp(c(0, 0, 0), c(1, 0, 0), sx), lerp(c(0, 1, 0), c(1, 1, 0), sx)
    x01, x11 = lerp(c(0, 0, 1), c(1, 0, 1), sx), lerp(c(0, 1, 1), c(1, 1, 1), sx)
    return lerp(lerp(x00, x10, sy), lerp(x01, x11, sy), sz)


def _sp_fbm(p, scale, seed, octaves=4):
    x, y, z = p[..., 0] * scale, p[..., 1] * scale, p[..., 2] * scale
    acc, tot, amp = 0.0, 0.0, 0.5
    for o in range(octaves):
        acc = acc + amp * _sp_noise3(x + o * 17.3, y - o * 9.1, z + o * 5.7, seed + o)
        tot += amp
        amp *= 0.5
        x, y, z = x * 2.03, y * 2.03, z * 2.03
    return acc / tot


def _sp_ramp(t, stops):
    """Piecewise-linear colour ramp: t array in 0..1, stops = [(pos, (r, g, b)), ...] -> (..., 3) in 0..1."""
    pos = [s[0] for s in stops]
    cols = np.array([s[1] for s in stops], np.float32) / 255.0
    return np.stack([np.interp(t, pos, cols[:, i]) for i in range(3)], -1).astype(np.float32)


def _sp_mix(a, b, m):
    """a * (1 - m) + b * m; b is an (r, g, b) tuple in 0..255 or an array in 0..1."""
    b = np.asarray(b, np.float32) / 255.0 if isinstance(b, tuple) else np.asarray(b, np.float32)
    m = np.asarray(m, np.float32)
    if m.ndim == a.ndim - 1:
        m = m[..., None]
    return a * (1 - m) + b * m


def _d_space_planet(W, H, color, rng, k=5, kind="moon", sun=(0.7, -0.6), r=None, ring=False, tilt=-16.0, seed=1):
    """Pixel-art planet on a k-px texel grid, lit from `sun` ([dx, dy] towards the light, y down) in 5 hard
    tone steps with a little 2x2 dither at the terminator. kind: earth | moon | mercury | mars | venus |
    glacio | gas (gas uses `color` as its base hue; ring=true adds a tilted ring, canvas should be wide).
    r = planet radius in texels (default: fills the box; with ring default is the box width / 4.2)."""
    k = max(1, int(k))
    Wt, Ht = max(6, W // k), max(6, H // k)
    R = float(r) if r else (Wt / 4.2 if ring else min(Wt, Ht) / 2.0)
    cx, cy = Wt / 2.0, Ht / 2.0
    ys, xs = np.mgrid[0:Ht, 0:Wt].astype(np.float32)
    u, v = (xs + 0.5 - cx) / R, (ys + 0.5 - cy) / R
    r2 = u * u + v * v
    inside = r2 <= 1.0
    z = np.sqrt(np.clip(1 - r2, 0, 1))
    n = np.stack([u, v, z], -1)
    ta = math.radians(tilt)
    q = np.stack([u * math.cos(ta) - v * math.sin(ta), u * math.sin(ta) + v * math.cos(ta), z], -1)  # unit, for terrain
    sd = int(seed)
    L = np.array([sun[0], sun[1], 0.55], np.float32)
    L /= np.linalg.norm(L)
    lam = n @ L
    py = q[..., 1]
    if kind == "earth":
        h = _sp_fbm(q + sd, 1.7, sd, 4)
        ocean = _sp_ramp(np.clip((0.5 - h) / 0.22, 0, 1), [(0, (62, 124, 208)), (1, (22, 58, 142))])
        elev = np.clip((h - 0.5) / 0.18, 0, 1)
        land = _sp_ramp(elev, [(0, (72, 150, 70)), (0.55, (118, 152, 72)), (1, (156, 124, 82))])
        alb = np.where((h > 0.5)[..., None], land, ocean)
        cl = _sp_fbm((q + 5.5 + sd) * np.array([1.0, 2.6, 1.0], np.float32), 3.0, sd + 11, 3)
        alb = _sp_mix(alb, (246, 249, 253), np.where(cl > 0.6, 0.78, 0.0))
        alb = _sp_mix(alb, (238, 246, 253), np.where(np.abs(py) > 0.87 + 0.07 * (h - 0.5), 1.0, 0.0))
        alb = _sp_mix(alb, (140, 196, 255), np.clip((r2 - 0.78) / 0.22, 0, 1) * 0.55)
    elif kind in ("moon", "mercury"):
        lo, hi = ((98, 102, 122), (176, 180, 196)) if kind == "moon" else ((112, 74, 104), (184, 132, 160))
        h = _sp_fbm(q + sd, 2.4, sd, 3)
        alb = _sp_ramp(h, [(0, lo), (1, hi)])
        mar = _sp_fbm(q + 3.1 + sd, 0.95, sd + 3, 2)
        alb = _sp_mix(alb, lo, np.where(mar < 0.44, 0.55, 0.0))
        cr = random.Random(f"crater{sd}{kind}")
        for _ in range(20 if kind == "mercury" else 15):
            c = np.array([cr.uniform(-1, 1), cr.uniform(-1, 1), cr.uniform(-0.2, 1)], np.float32)
            c /= np.linalg.norm(c)
            rad = cr.uniform(0.07, 0.26)
            ang = np.arccos(np.clip(q @ c, -1, 1))
            alb = np.where((ang < rad * 0.8)[..., None], alb * 0.78, alb)
            alb = np.where(((ang >= rad * 0.8) & (ang < rad))[..., None], np.minimum(alb * 1.2 + 0.03, 1.0), alb)
    elif kind == "mars":
        h = _sp_fbm(q + sd, 2.1, sd, 4)
        alb = _sp_ramp(h, [(0, (112, 56, 38)), (0.5, (176, 90, 50)), (1, (222, 148, 92))])
        mar = _sp_fbm(q + 2.2 + sd, 1.1, sd + 5, 2)
        alb = _sp_mix(alb, (92, 46, 36), np.where(mar < 0.4, 0.5, 0.0))
        alb = _sp_mix(alb, (244, 230, 226), np.where(np.abs(py) > 0.9 + 0.05 * (h - 0.5), 1.0, 0.0))
    elif kind == "venus":
        s = py * 6.0 + (_sp_fbm(q + sd, 2.0, sd, 3) - 0.5) * 3.4
        alb = _sp_ramp(0.5 + 0.5 * np.sin(s * math.pi), [(0, (204, 146, 78)), (0.55, (234, 182, 106)), (1, (250, 218, 152))])
        alb = _sp_mix(alb, (255, 224, 160), np.clip((r2 - 0.8) / 0.2, 0, 1) * 0.35)
    elif kind == "glacio":
        h = _sp_fbm(q + sd, 2.6, sd, 4)
        alb = _sp_ramp(h, [(0, (146, 158, 214)), (0.5, (190, 198, 240)), (1, (232, 238, 255))])
        crack = np.abs(_sp_fbm(q + 8.8 + sd, 2.2, sd + 9, 3) - 0.5) < 0.028
        alb = _sp_mix(alb, (104, 116, 190), np.where(crack, 0.7, 0.0))
        alb = _sp_mix(alb, (130, 232, 244), np.clip((r2 - 0.78) / 0.22, 0, 1) * 0.5)
    else:  # gas giant in `color`
        base = np.array(color, np.float32) / 255.0
        s = py * 7.5 + (_sp_fbm(q + sd, 1.6, sd, 3) - 0.5) * 1.8
        t = 0.5 + 0.5 * np.sin(s * math.pi)
        dk, lt = base * 0.62, np.minimum(base * 0.7 + 0.3, 1.0)
        alb = np.where((t < 0.5)[..., None], _sp_mix(dk + 0 * q, base, t * 2), _sp_mix(base + 0 * q, lt, (t - 0.5) * 2))
        spot = ((u - 0.28) / 0.3) ** 2 + ((v - 0.34) / 0.14) ** 2 < 1
        alb = _sp_mix(alb, dk * 0.8, np.where(spot, 0.7, 0.0))
    # five hard tone steps + 2x2 dither at the terminator, cool ambient on the night side
    bay = np.array([[0, 2], [3, 1]], np.float32) / 4 - 0.375
    dith = bay[ys.astype(int) % 2, xs.astype(int) % 2]
    lev = np.digitize(lam + dith * 0.12, [0.02, 0.28, 0.54, 0.82])
    ramp = np.array([0.30, 0.56, 0.80, 1.0, 1.15], np.float32)
    rgb = alb * ramp[lev][..., None]
    rgb = np.where((lev == 0)[..., None], alb * np.array([0.27, 0.30, 0.46], np.float32) + 0.015, rgb)
    out = np.zeros((Ht, Wt, 4), np.float32)
    out[..., :3] = np.clip(rgb, 0, 1)
    out[..., 3] = inside.astype(np.float32)
    if ring:
        rc, rs = math.cos(math.radians(-tilt * 0.5)), math.sin(math.radians(-tilt * 0.5))
        xr = (xs + 0.5 - cx) * rc - (ys + 0.5 - cy) * rs
        yr = (xs + 0.5 - cx) * rs + (ys + 0.5 - cy) * rc
        a_out = 2.15 * R
        b_out = a_out * 0.27
        e2 = (xr / a_out) ** 2 + (yr / b_out) ** 2
        band = (e2 <= 1.0) & (e2 >= (1.5 * R / a_out) ** 2)
        gap = (e2 > 0.7) & (e2 < 0.77)
        band &= ~gap
        tcol = np.clip((e2 - 0.45) / 0.55, 0, 1)
        rcol = _sp_ramp(tcol, [(0, (214, 196, 248)), (0.5, (170, 150, 226)), (1, (226, 212, 252))])
        sh = 0.62 + 0.38 * np.clip(0.5 + 0.5 * ((xs - cx) * sun[0] + (ys - cy) * sun[1]) / (a_out * 0.7), 0, 1)
        rcol = rcol * sh[..., None]
        front = band & (yr > 0)
        back = band & (yr <= 0) & ~inside
        out[back, :3], out[back, 3] = rcol[back], 1.0
        out[front, :3], out[front, 3] = rcol[front], 1.0
    img = Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")
    return img.resize((Wt * k, Ht * k), Image.NEAREST)


def _d_space_rocket(W, H, color, rng, k=5, side=1, window=True):
    """Pixel rocket standing upright on a k-px texel grid (nose cone in `color`, white steel body, one
    porthole, swept side fins, engine bell). side = +1 / -1: the light comes from the right / left."""
    k = max(1, int(k))
    Wt, Ht = max(12, W // k), max(30, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    bw = max(6, (int(Wt * 0.46) // 2) * 2)
    x0 = (Wt - bw) // 2
    cxf = x0 + bw / 2.0
    E = max(5, Ht // 12)
    N = int(Ht * 0.27)
    body_end = Ht - E  # first engine row
    steel = np.array([(88, 94, 124), (132, 140, 170), (178, 186, 208), (216, 222, 238), (248, 250, 255)], np.float32) / 255
    base = np.array(color, np.float32) / 255
    red = np.array([base * m for m in (0.40, 0.62, 0.84, 1.0, 1.22)], np.float32).clip(0, 1)

    def lev_of(jc, sd=side):  # jc = texel centre column
        t = np.clip((jc - cxf) / (bw / 2.0), -1, 1)
        nz = math.sqrt(max(0.0, 1 - t * t))
        return int(np.digitize(t * 0.8 * sd + nz * 0.6, [-0.25, 0.15, 0.5, 0.82]))

    def put(y, x, c, a=1.0):
        if 0 <= y < Ht and 0 <= x < Wt:
            img[y, x, :3], img[y, x, 3] = c, a

    # nose cone: elliptical ogive
    for y in range(N):
        t = (y + 0.5) / N
        hw = max(1.0, (bw / 2.0) * math.sqrt(max(0.0, 1 - (1 - t) ** 2)))
        for j in range(Wt):
            if abs(j + 0.5 - cxf) < hw:
                lv = lev_of(j + 0.5)
                if y == 0:
                    lv = min(4, lv + 1)
                put(y, j, red[lv])
    # body
    for y in range(N, body_end):
        rr = y - N
        for j in range(x0, x0 + bw):
            lv = lev_of(j + 0.5)
            col = steel[lv]
            if rr == 0:
                col = steel[max(0, lv - 2)]
            elif rr in (5, 6, 7):
                col = red[lv]
            elif rr >= 12 and (rr - 12) % 13 == 0:
                col = steel[max(0, lv - 2)]  # panel seam
            elif rr >= 13 and (rr - 13) % 13 == 0:
                col = steel[min(4, lv + 1)]  # lit lip under the seam
            elif body_end - y <= 4:
                col = steel[max(0, lv - 1)]  # skirt
            put(y, j, col)
    # porthole
    if window:
        wy, wx = N + 17, cxf
        for yy in range(int(wy) - 4, int(wy) + 4):
            for xx in range(int(wx) - 4, int(wx) + 4):
                dcx, dcy = (xx + 0.5) - wx, (yy + 0.5) - wy
                d = math.hypot(dcx, dcy)
                if d <= 3.1:
                    if d > 2.3:
                        put(yy, xx, np.array((56, 62, 84), np.float32) / 255 if dcx * side < 0 else np.array((120, 128, 156), np.float32) / 255)
                    else:
                        g = 0.5 + 0.5 * np.clip((-dcx * side * 0.55 - dcy * 0.55) / 2.2, -1, 1)
                        put(yy, xx, (np.array((34, 86, 172), np.float32) * (1 - g) + np.array((130, 206, 255), np.float32) * g) / 255)
        put(int(wy) - 2, int(wx) + (1 if side > 0 else -2), np.array((232, 250, 255), np.float32) / 255)
    # fins
    fw = x0 - 1
    fh = max(10, int(Ht * 0.27))
    ft, fb = body_end - fh, body_end + 1
    for s in (-1, 1):
        lvf = 3 if s == side else 1
        for c in range(fw):
            jx = x0 - 1 - c if s < 0 else x0 + bw + c
            top = ft + int(c * (fh * 0.55) / max(1, fw - 1))
            for y in range(top, fb + 1):
                lv = lvf
                if y == top:
                    lv = min(4, lvf + 1)
                if c == fw - 1:
                    lv = max(0, lvf - 1)
                put(y, jx, red[lv])
    # engine bell + collar
    for i in range(E):
        y = body_end + i
        wdt = int(round(bw * 0.58 + (bw * 0.34) * i / max(1, E - 1)))
        wdt += wdt % 2
        xa = int(round(cxf - wdt / 2.0))
        for j in range(xa, xa + wdt):
            t = np.clip((j + 0.5 - cxf) / (wdt / 2.0), -1, 1)
            lv = int(np.digitize(t * 0.8 * side + math.sqrt(max(0, 1 - t * t)) * 0.6, [-0.25, 0.15, 0.5, 0.82]))
            c = np.array([(44, 46, 60), (62, 66, 84), (84, 90, 112), (112, 120, 146), (150, 158, 184)], np.float32)[lv] / 255
            if i == E - 1:
                c = np.array((150, 70, 34), np.float32) / 255 if lv < 3 else np.array((255, 170, 80), np.float32) / 255
            put(y, j, c)
    out = Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")
    return out.resize((Wt * k, Ht * k), Image.NEAREST)


def _d_space_gantry(W, H, color, rng, k=5, arm_len=8, arms=(0.3, 0.62), side=1, beacon=True):
    """Launch-tower lattice on a k-px texel grid: two legs, X-braces, hazard-striped foot, beacon on top and
    service arms reaching `arm_len` texels to the right (towards the rocket) at the given height fractions."""
    k = max(1, int(k))
    Wt, Ht = max(10, W // k), max(20, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    tw = Wt - int(arm_len)

    def put(y, x, c, a=1.0):
        if 0 <= y < Ht and 0 <= x < Wt:
            img[y, x, :3], img[y, x, 3] = np.array(c, np.float32) / 255, a

    leg_d, leg_m, leg_l = (70, 76, 98), (112, 120, 144), (164, 172, 196)
    top0 = 6 if beacon else 0
    foot = 7
    for y in range(top0, Ht):
        for j in (0, 1, tw - 2, tw - 1):
            lit = (j == tw - 1) if side > 0 else (j == 0)
            shd = (j == 0) if side > 0 else (j == tw - 1)
            put(y, j, leg_l if lit else (leg_d if shd else leg_m))
    seg = max(8, int(tw * 1.5))
    y = Ht - foot - 1
    while y - seg >= top0:  # X-braces between rungs
        for i in range(seg):
            f = i / max(1, seg - 1)
            xa = 2 + int(round(f * (tw - 5)))
            put(y - i, xa, (86, 92, 114))
            put(y - i, tw - 3 - int(round(f * (tw - 5))), (86, 92, 114))
        for j in range(2, tw - 2):
            put(y, j, (126, 134, 158))
        y -= seg
    for j in range(2, tw - 2):
        put(top0, j, (150, 158, 182))
    for yy in range(Ht - foot, Ht):  # hazard stripes on the foot
        for j in range(tw):
            put(yy, j, (236, 196, 44) if ((j + yy) // 2) % 2 == 0 else (34, 34, 42))
    if beacon:
        for dy in range(2):
            for dx in range(2):
                put(top0 - 3 + dy, tw // 2 - 1 + dx, (206, 178, 255))
        for yy in range(top0 - 2, top0):
            put(yy, tw // 2 - 1, (150, 158, 182))
        put(top0 - 4, tw // 2, (255, 255, 255))
    for fr in arms:  # service arms
        ay = int(top0 + fr * (Ht - top0 - foot))
        for j in range(tw, Wt):
            put(ay, j, (178, 186, 208))
            put(ay + 1, j, (116, 124, 148))
            put(ay + 2, j, (70, 76, 98))
        for i in range(5):  # strut under the arm
            put(ay + 3 + i, tw + 4 - i, (86, 92, 114))
        for dy in range(-2, 4):  # clamp at the tip
            put(ay + dy, Wt - 1, (212, 70, 52) if dy == -2 else (60, 64, 84))
    out = Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")
    return out.resize((Wt * k, Ht * k), Image.NEAREST)


def _d_space_crop(W, H, color, rng, asset="", box=None, k=5, flip=False):
    """A sub-rectangle `box` = [x0, y0, x1, y1] (texture pixels) of any texture / model atlas, pixel-scaled by k."""
    t = tex(asset)
    if box:
        t = t.crop(tuple(int(v) for v in box))
    if flip:
        t = t.transpose(Image.FLIP_LEFT_RIGHT)
    k = max(1, int(k))
    return t.resize((t.size[0] * k, t.size[1] * k), Image.NEAREST)


def _sp_put(img, y, x, c, a=1.0):
    Ht, Wt = img.shape[:2]
    if 0 <= y < Ht and 0 <= x < Wt:
        img[y, x, :3], img[y, x, 3] = np.array(c, np.float32) / 255.0, a


def _sp_up(img, k):
    out = Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")
    return out.resize((img.shape[1] * k, img.shape[0] * k), Image.NEAREST)


_SP_ASTRO = {
    "W": (232, 236, 248), "w": (190, 196, 218), "s": (132, 140, 172), "V": (26, 34, 66), "v": (58, 98, 178),
    "h": (176, 218, 255), "G": (240, 190, 70), "r": (214, 64, 56), "b": (70, 120, 210), "k": (62, 66, 86),
    "K": (84, 88, 110),
}
_SP_ASTRO_ROWS = [
    "...wWWWWs...",
    "..wWWWWWWs..",
    ".wWVVVVVVWs.",
    ".wWVhhvVVWs.",
    ".wWVhvvVVWs.",
    ".wWVvvVVVWs.",
    ".wWVVVVVVWs.",
    "..wWWWWWWs..",
    "...wGGGGs...",
    "swwWWWWWWwss",
    "swwWWWWWWwss",
    "swwWrWWbWwss",
    "swwWWWWWWwss",
    "swwWGGGGWwss",
    "kkwWWWWWWwkk",
    "..wWWWWWWs..",
    "..wWWswWWs..",
    "..wWWswWWs..",
    "..wWWswWWs..",
    "..wWWswWWs..",
    "..wWWswWWs..",
    "..swWswsWs..",
    "..swWswsWs..",
    ".kKKKskKKKk.",
    ".kKKKskKKKk.",
]


def _d_space_astronaut(W, H, color, rng, k=5, flag=True, side=1, emblem="square"):
    """Pixel astronaut (white suit, dark visor with highlight, chest lights, boots) 12 x 25 texels; with
    flag=true a flag in `color` is planted beside it (canvas should be >= 20 texels wide, 25 tall).
    side = -1 mirrors the whole figure."""
    k = max(1, int(k))
    Wt, Ht = max(14, W // k), max(26, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    ox, oy = 0, Ht - len(_SP_ASTRO_ROWS)
    for y, row in enumerate(_SP_ASTRO_ROWS):
        for x, ch in enumerate(row):
            if ch != ".":
                _sp_put(img, oy + y, ox + x, _SP_ASTRO[ch])
    if flag and Wt >= 20:
        px = 14
        for y in range(Ht - 1, Ht - 25, -1):  # pole
            _sp_put(img, y, px, (176, 180, 196))
            _sp_put(img, y, px + 1, (112, 116, 136))
        base = np.array(color, np.float32)
        top = Ht - 24
        for y in range(top, top + 8):  # cloth, folds shaded in vertical bands
            for x in range(px + 2, min(Wt, px + 13)):
                sh = 1.0 if (y - top) < 4 else 0.84
                if ((x - px) // 3) % 2 == 1:
                    sh *= 0.9
                _sp_put(img, y, x, np.clip(base * sh, 0, 255))
        if emblem == "rocket":  # a small white rocket with red fins, and a lit column on the cloth's left edge
            for yy, row in enumerate(("..W..", ".WWW.", ".WVW.", ".WWW.", "RWWWR", "R...R")):
                for xx, ch in enumerate(row):
                    if ch != ".":
                        _sp_put(img, top + 1 + yy, px + 5 + xx,
                                {"W": (250, 250, 255), "R": (214, 64, 56), "V": (60, 96, 176)}[ch])
            for y in range(top, top + 8):
                _sp_put(img, y, px + 2, np.clip(base * 1.25 + 14, 0, 255))
        else:
            for dy in range(3):
                for dx in range(3):
                    _sp_put(img, top + 2 + dy, px + 5 + dx, (250, 250, 255))
        _sp_put(img, top - 1, px, (255, 232, 140))
    if side < 0:
        img = img[:, ::-1].copy()
    return _sp_up(img, k)


def _d_space_rocks(W, H, color, rng, k=5, n=12, side=1, maxw=8):
    """Scattered pixel rocks / boulders on a k-px texel grid (3 tone steps lit from `side`, shadow texels)."""
    k = max(1, int(k))
    Wt, Ht = max(8, W // k), max(4, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    base = np.array(color, np.float32)
    for _ in range(int(n)):
        w = rng.choice([v for v in (2, 2, 3, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20) if v <= int(maxw)] or [2])
        h = max(2, int(round(w * rng.uniform(0.5, 0.75))))
        x0, y0 = rng.randint(0, max(0, Wt - w - 2)), rng.randint(0, max(0, Ht - h - 1))
        for dy in range(h):
            for dx in range(w):
                ex, ey = (dx + 0.5 - w / 2) / (w / 2), (dy + 0.5 - h / 2) / (h / 2)
                if ex * ex + ey * ey > 1.05:
                    continue
                lit = (ex * side * 0.7 - ey * 0.7)
                m = 1.22 if lit > 0.45 else (1.0 if lit > -0.2 else (0.78 if lit > -0.6 else 0.6))
                _sp_put(img, y0 + dy, x0 + dx, np.clip(base * m, 0, 255))
        for dx in range(w - 1):  # contact shadow, away from the light
            _sp_put(img, y0 + h, x0 + dx - side + 1, (4, 4, 14), 0.45)
    return _sp_up(img, k)


def _d_space_crater(W, H, color, rng, k=5, side=1):
    """A shallow impact crater seen at a low angle (elliptical rim lit from `side`, shadowed inner wall)."""
    k = max(1, int(k))
    Wt, Ht = max(8, W // k), max(4, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    base = np.array(color, np.float32)
    ys, xs = np.mgrid[0:Ht, 0:Wt].astype(np.float32)
    ex, ey = (xs + 0.5 - Wt / 2) / (Wt / 2), (ys + 0.5 - Ht / 2) / (Ht / 2)
    d = ex * ex + ey * ey
    for y in range(Ht):
        for x in range(Wt):
            dd = d[y, x]
            if dd > 1.0:
                continue
            if dd > 0.72:  # rim
                m = 1.28 if (ex[y, x] * side - ey[y, x] * 0.8) > 0.25 else 0.92
            else:  # inner floor: far wall (towards the light) shadowed, near wall lit
                v = ex[y, x] * side * 0.5 - ey[y, x]
                m = 0.45 if v > 0.35 else (0.62 if v > -0.2 else 0.84)
            _sp_put(img, y, x, np.clip(base * m, 0, 255))
    return _sp_up(img, k)


def _d_space_rover(W, H, color, rng, k=5, side=1, lsign=1):
    """Pixel lunar rover (white/gold body, solar roof, camera mast, dish, four wheels) in profile, facing right
    (side = -1 mirrors it). Needs a canvas of about 36 x 26 texels; wheels touch the bottom row."""
    k = max(1, int(k))
    Wt, Ht = max(34, W // k), max(26, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    P = _sp_put
    wy = Ht - 4.0
    for cx in (6.0, 14.0, Wt - 15.0, Wt - 7.0):  # wheels
        for y in range(Ht):
            for x in range(Wt):
                d = math.hypot(x + 0.5 - cx, y + 0.5 - wy)
                if d <= 3.6:
                    lit = (x + 0.5 - cx) * 0.6 * lsign - (y + 0.5 - wy) * 0.6
                    if d > 2.5:
                        P(img, y, x, (88, 92, 108) if lit > 1.2 else (34, 36, 46))
                    elif d > 1.2:
                        P(img, y, x, (176, 182, 200) if lit > 0.2 else (120, 126, 146))
                    else:
                        P(img, y, x, (70, 74, 92))
    y0 = Ht - 13
    x0, x1 = 3, Wt - 3
    rows = [(238, 242, 252), (214, 220, 236), (214, 220, 236), (240, 190, 70), (160, 168, 192), (104, 110, 138), (60, 64, 84)]
    for i, c in enumerate(rows):
        for x in range(x0, x1):
            if (i in (0, len(rows) - 1)) and (x < x0 + 2 or x >= x1 - 2):
                continue
            P(img, y0 + i, x, c)
    for i in range(1, 4):  # cabin window
        for x in range(x1 - 11, x1 - 5):
            P(img, y0 + i, x, (28, 38, 74))
    P(img, y0 + 1, x1 - 10, (140, 206, 255))
    P(img, y0 + 1, x1 - 9, (140, 206, 255))
    for x in range(x0 + 2, x0 + 8):  # hatch panel
        P(img, y0 + 2, x, (150, 158, 184))
    P(img, y0 + 4, x1 - 1, (255, 236, 150))  # headlight
    for x in range(x0 + 3, x0 + 22):  # solar roof
        P(img, y0 - 1, x, (176, 184, 204))
        P(img, y0 - 2, x, (46, 100, 190) if (x - x0) % 4 else (120, 200, 255))
        P(img, y0 - 3, x, (30, 74, 150) if (x - x0) % 4 else (90, 170, 245))
    mx = x1 - 6
    for y in range(y0 - 8, y0):  # camera mast + head
        P(img, y, mx, (190, 196, 214))
        P(img, y, mx + 1, (116, 122, 144))
    for yy in range(3):
        for xx in range(5):
            P(img, y0 - 11 + yy, mx - 2 + xx, (62, 68, 90))
    P(img, y0 - 10, mx + 2, (120, 224, 255))
    dx = x1 - 15  # small dish on a stem
    for i in range(5):
        P(img, y0 - 6 - (1 if i in (0, 4) else 0), dx + i, (176, 182, 200))
    P(img, y0 - 5, dx + 2, (176, 182, 200))
    P(img, y0 - 4, dx + 2, (176, 182, 200))
    if side < 0:
        img = img[:, ::-1].copy()
    return _sp_up(img, k)


def _d_space_trail(W, H, color, rng, k=5, p0=(0.0, 1.0), p1=(0.5, 0.0), p2=(1.0, 0.1), step=4.0, fade=0.6, arrow=False):
    """Dotted flight path on a k-px texel grid: a quadratic Bezier p0 -> p1 -> p2 (box fractions, y down) drawn as
    square texel dots every `step` texels (every 4th dot 2x2, opacity fading by `fade` towards p2)."""
    k = max(1, int(k))
    Wt, Ht = max(8, W // k), max(8, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    pts = []
    for i in range(801):
        t = i / 800.0
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x * (Wt - 1), y * (Ht - 1)))
    acc, nxt, n = 0.0, 0.0, 0
    total = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(800)) or 1.0
    for i in range(800):
        if acc >= nxt:
            x, y = int(round(pts[i][0])), int(round(pts[i][1]))
            a = 1.0 - fade * acc / total
            size = 2 if n % 4 == 0 else 1
            for dy in range(size):
                for dx in range(size):
                    _sp_put(img, y + dy, x + dx, color, a)
            nxt += float(step)
            n += 1
        acc += math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
    if arrow:  # solid arrowhead at p2 pointing along the end tangent (5 texels long)
        ex, ey = pts[800]
        ux, uy = pts[800][0] - pts[760][0], pts[800][1] - pts[760][1]
        ln = math.hypot(ux, uy) or 1.0
        ux, uy = ux / ln, uy / ln
        for yy in range(int(ey) - 8, int(ey) + 9):
            for xx in range(int(ex) - 8, int(ex) + 9):
                rx, ry = xx + 0.5 - ex - 0.5, yy + 0.5 - ey - 0.5
                back = -(rx * ux + ry * uy)  # distance behind the tip
                side = abs(-rx * uy + ry * ux)
                if -0.6 <= back <= 5.0 and side <= back * 0.5 + 0.7:
                    _sp_put(img, yy, xx, color, 1.0)
    return _sp_up(img, k)


_DECOR.update({"space_planet": _d_space_planet, "space_rocket": _d_space_rocket, "space_gantry": _d_space_gantry,
               "space_crop": _d_space_crop, "space_astronaut": _d_space_astronaut, "space_rocks": _d_space_rocks,
               "space_crater": _d_space_crater, "space_rover": _d_space_rover, "space_trail": _d_space_trail})


# ---------------------------------------------------------------- space chapter motifs (round 3: sun, stars, satellite, solar array, ground shadows, tracks)
# Same conventions as the round-2 space motifs above: drawn on a grid of `k` canvas px per texel and NEAREST-upscaled.
_SP_BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) / 16.0 + 1.0 / 32.0


def _d_space_sun(W, H, color, rng, k=5, r=11, corona=None, rays=True, seed=1, ray_len=0.95):
    """Round pixel sun on a k-px texel grid, centred in the box: a hard-edged disc in four warm tones
    (white-hot core to orange limb, a few granulation texels), a corona of 7 dithered alpha steps out to `corona`
    texels (default: half the box) tinted from `color` towards orange, and (rays=true) four 1-texel pixel rays
    with short diagonals (length = ray_len x r). r = disc radius in texels."""
    k = max(1, int(k))
    Wt, Ht = max(12, W // k), max(12, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    cx, cy = Wt / 2.0, Ht / 2.0
    R = float(r)
    Rc = float(corona) if corona else min(Wt, Ht) / 2.0
    ys, xs = np.mgrid[0:Ht, 0:Wt].astype(np.float32)
    d = np.sqrt((xs + 0.5 - cx) ** 2 + (ys + 0.5 - cy) ** 2)
    glow = np.array(color, np.float32) / 255.0
    warm = np.array((255, 164, 70), np.float32) / 255.0
    t = np.clip(1.0 - (d - R) / max(1.0, Rc - R), 0, 1) ** 1.9
    bay = np.tile(_SP_BAYER, (Ht // 4 + 1, Wt // 4 + 1))[:Ht, :Wt]
    v = t * 7.0
    lev = np.floor(v) + ((v - np.floor(v)) > bay)
    a = np.clip(lev / 7.0, 0, 1) * 0.72
    mixm = (np.clip(1.0 - t * 1.5, 0, 1) * 0.6)[..., None]
    rgb = glow * (1 - mixm) + warm * mixm
    outside = d > R
    img[..., :3] = np.where(outside[..., None], rgb, 0)
    img[..., 3] = np.where(outside, a, 0)
    pal = np.array([(255, 253, 234), (255, 241, 180), (255, 219, 112), (255, 181, 76)], np.float32) / 255.0
    tone = np.digitize(d / R, [0.42, 0.7, 0.9])
    g = _sp_h3(xs.astype(np.int64), ys.astype(np.int64), 9, int(seed))
    tone = np.clip(tone + ((g > 0.9) & (tone < 3)).astype(np.int64) - ((g < 0.04) & (tone > 0)).astype(np.int64), 0, 3)
    disc = d <= R
    img[..., :3] = np.where(disc[..., None], pal[tone], img[..., :3])
    img[..., 3] = np.where(disc, 1.0, img[..., 3])
    if rays:
        i0 = int(R * 1.16)
        la, lb = max(1, int(R * ray_len)), max(1, int(R * ray_len * 0.42))
        for sx, sy, ln in ((1, 0, la), (-1, 0, la), (0, 1, la), (0, -1, la), (1, 1, lb), (-1, 1, lb), (1, -1, lb), (-1, -1, lb)):
            diag = sx != 0 and sy != 0
            for i in range(ln):
                step = i0 * (0.78 if diag else 1.0) + i
                px = int(cx + sx * (step / (1.414 if diag else 1.0))) - (1 if sx < 0 else 0)
                py = int(cy + sy * (step / (1.414 if diag else 1.0))) - (1 if sy < 0 else 0)
                al = float(np.clip(1.0 - i / max(1, ln), 0, 1))
                al = (1.0, 0.8, 0.55, 0.35)[min(3, int((1 - al) * 4))]
                _sp_put(img, py, px, (255, 246, 206), al)
    return _sp_up(img, k)


def _d_space_stars(W, H, color, rng, k=5, n=60, sparkle=3):
    """Square pixel stars on a k-px texel grid: n single texels (alpha 0.3-1, white / warm / cool), ~7 % 2x2 texels
    and `sparkle` plus-shaped twinkles. `color` is required but unused. Keep the box off the quest panels."""
    k = max(1, int(k))
    Wt, Ht = max(8, W // k), max(8, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    pal = [(226, 222, 255), (255, 238, 205), (190, 212, 255), (255, 255, 255)]
    for _ in range(int(n)):
        x, y = rng.randrange(Wt), rng.randrange(Ht)
        c, a = rng.choice(pal), rng.choice((0.3, 0.45, 0.6, 0.8, 1.0))
        s = 2 if rng.random() < 0.07 else 1
        for dy in range(s):
            for dx in range(s):
                _sp_put(img, y + dy, x + dx, c, a)
    for _ in range(int(sparkle)):
        x, y = rng.randrange(3, max(4, Wt - 3)), rng.randrange(3, max(4, Ht - 3))
        c, L = rng.choice(pal[:3]), (2 if rng.random() < 0.4 else 1)
        _sp_put(img, y, x, (255, 255, 255), 1.0)
        for i in range(1, L + 1):
            for ddx, ddy in ((i, 0), (-i, 0), (0, i), (0, -i)):
                _sp_put(img, y + ddy, x + ddx, c, 0.7 if i == 1 else 0.4)
    return _sp_up(img, k)


def _d_space_satellite(W, H, color, rng, k=5, side=1):
    """Pixel satellite: gold-foil hub, two navy solar wings on trusses, a small dish and a mast with a red light.
    About 34 x 14 texels (w 7.1, h 3 units at k 5). side = -1 mirrors it. `color` is required but unused."""
    k = max(1, int(k))
    Wt, Ht = max(34, W // k), max(14, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    P = _sp_put
    cx, cy = Wt // 2, Ht // 2 + 2
    foil = [(150, 106, 40), (206, 160, 58), (244, 200, 96), (255, 228, 146)]
    for y in range(cy - 4, cy + 4):
        for x in range(cx - 4, cx + 4):
            lv = 3 if x < cx - 2 else (2 if x < cx + 1 else (1 if x < cx + 3 else 0))
            if y == cy - 4:
                lv = min(3, lv + 1)
            if y == cy + 3:
                lv = max(0, lv - 1)
            if (x * 3 + y * 5) % 7 == 0 and 0 < lv < 3:
                lv -= 1
            P(img, y, x, foil[lv])
    for x in range(cx - 4, cx + 4):
        P(img, cy - 1, x, (96, 72, 36))
    for sgn in (-1, 1):
        for x in range(cx + sgn * 4 if sgn > 0 else cx - 7, cx + 7 if sgn > 0 else cx - 3):  # truss
            P(img, cy - 1, x, (150, 158, 182))
            P(img, cy, x, (92, 98, 122))
        wx0 = cx + 7 if sgn > 0 else cx - 7 - 11
        for y in range(cy - 4, cy + 4):
            for x in range(wx0, wx0 + 11):
                i, j = x - wx0, y - (cy - 4)
                c = (24, 48, 104)
                if i % 3 == 0 or j % 3 == 0:
                    c = (58, 108, 188)
                if (i * 2 + j * 3 + (0 if sgn < 0 else 2)) % 14 in (0, 1):
                    c = (96, 156, 230)
                if j == 0:
                    c = (178, 186, 206)
                elif j == 7:
                    c = (62, 68, 92)
                if i == 0:
                    c = (150, 158, 182)
                elif i == 10:
                    c = (74, 80, 104)
                P(img, y, x, c)
    for i in range(5):  # dish
        P(img, cy - 7 - (1 if i in (0, 4) else 0), cx - 5 + i, (186, 192, 210))
    P(img, cy - 6, cx - 3, (150, 158, 182))
    P(img, cy - 5, cx - 3, (150, 158, 182))
    P(img, cy - 5, cx - 2, (110, 116, 140))
    for y in range(cy - 8, cy - 4):  # mast + red light
        P(img, y, cx + 2, (170, 176, 198))
    P(img, cy - 9, cx + 2, (255, 74, 64))
    if side < 0:
        img = img[:, ::-1].copy()
    return _sp_up(img, k)


def _d_space_solar(W, H, color, rng, k=5, side=1):
    """Solar array on a mast: two navy panels (frame, thin grid, a diagonal sheen) in one plane tilted towards the
    upper left, a mast with diagonal struts and a base plate. Designed 30 x 24 texels (w 6.25, h 5 units at k 5).
    side = -1 mirrors it. `color` is required but unused."""
    k = max(1, int(k))
    Wt, Ht = max(26, W // k), max(20, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    P = _sp_put
    mx = Wt // 2 - 1
    pw, ph = mx - 1, 7
    drop = 3.0

    def top(x):
        return 1 + int(round(x * drop / max(1, Wt - 1)))

    for y in range(Ht - 3, Ht):  # base plate
        for x in range(mx - 5, mx + 7):
            P(img, y, x, (150, 158, 182) if y == Ht - 3 else ((100, 106, 130) if y == Ht - 2 else (62, 66, 86)))
    for y in range(top(mx) + ph + 1, Ht - 3):  # mast
        P(img, y, mx, (176, 182, 202))
        P(img, y, mx + 1, (96, 102, 126))
    for xe, xm in ((3, mx), (Wt - 4, mx + 1)):  # struts from the mast to the panel undersides
        y0, y1 = Ht - 8, top(xe) + ph + 1
        n = max(abs(xe - xm), abs(y1 - y0), 1)
        for i in range(n + 1):
            P(img, int(round(y0 + (y1 - y0) * i / n)), int(round(xm + (xe - xm) * i / n)), (104, 110, 134))
    for x0 in (0, mx + 3):
        for i in range(pw):
            x = x0 + i
            for j in range(ph):
                y = top(x) + j
                c = (22, 40, 88)
                if i % 4 == 2 or j == 3:
                    c = (38, 68, 128)
                if (x - y * 2) % 15 in (0, 1) and 0 < j < ph - 1 and 0 < i < pw - 1:
                    c = (62, 104, 176)
                if j == 0:
                    c = (182, 190, 210)
                elif j == ph - 1:
                    c = (58, 64, 88)
                if i == 0:
                    c = (160, 168, 192)
                elif i == pw - 1:
                    c = (70, 76, 100)
                P(img, y, x, c)
    for x in range(mx - 1, mx + 4):  # bracket joining the panels over the mast
        P(img, top(x) + ph, x, (120, 126, 150))
        P(img, top(x) + ph + 1, x, (84, 90, 114))
    if side < 0:
        img = img[:, ::-1].copy()
    return _sp_up(img, k)


def _d_space_shadow(W, H, color, rng, k=5, skew=0.0):
    """Texel-snapped ground shadow: a flat ellipse in `color` with a hard core and a checkerboard-dithered rim.
    skew = texels the top row is shifted to the right of the bottom row (cast away from a light on the left).
    Use the layer alpha (0.4-0.6) for strength."""
    k = max(1, int(k))
    Wt, Ht = max(4, W // k), max(2, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    ys, xs = np.mgrid[0:Ht, 0:Wt].astype(np.float32)
    ex = (xs + 0.5 - Wt / 2.0 - skew * (0.5 - (ys + 0.5) / Ht)) / (Wt / 2.0)
    ey = (ys + 0.5 - Ht / 2.0) / (Ht / 2.0)
    dd = ex * ex + ey * ey
    chk = ((xs + ys) % 2 == 0)
    core = dd <= 0.62
    rim = (dd > 0.62) & (dd <= 1.0) & chk
    m = core | rim
    img[..., :3] = (np.array(color, np.float32) / 255.0)
    img[..., 3] = m.astype(np.float32)
    return _sp_up(img, k)


def _d_space_tracks(W, H, color, rng, k=5, kind="tread", sep=4, amp=1.0, fade=0.4):
    """Marks on the regolith on a k-px texel grid, running along the box from right to left. kind 'tread' =
    two parallel rows of 3-on / 1-off tyre dashes `sep` texels apart on a gentle wave of amplitude `amp`;
    'prints' = alternating boot prints (2 x 1 texels, a lighter texel above). `color` = dark mark colour;
    opacity fades by `fade` towards the left end. Use the layer alpha for strength."""
    k = max(1, int(k))
    Wt, Ht = max(8, W // k), max(4, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    base = np.array(color, np.float32)
    hi = np.clip(base * 1.5 + 22, 0, 255)
    mid = Ht / 2.0
    ph = rng.uniform(0, 6.28)
    if kind == "prints":
        step, n = 6, 0
        for x in range(Wt - 3, 1, -step):
            fy = int(round(mid + math.sin(x * 0.07 + ph) * amp)) + (1 if n % 2 else -1)
            a = 1.0 - fade * (Wt - x) / float(Wt)
            for dx in range(2):
                _sp_put(img, fy, x + dx, base, a)
                _sp_put(img, fy - 1, x + dx, hi, a * 0.8)
            _sp_put(img, fy, x - 1, base, a * 0.7)
            n += 1
    else:
        for row in (-1, 1):
            for x in range(Wt):
                if x % 4 == 3:
                    continue
                fy = int(round(mid + row * sep / 2.0 + math.sin(x * 0.09 + ph) * amp))
                a = 1.0 - fade * (Wt - 1 - x) / float(Wt)
                _sp_put(img, fy, x, base, a)
                if x % 4 in (0, 1):
                    _sp_put(img, fy - 1, x, hi, a * 0.75)
    return _sp_up(img, k)


def _d_space_mast(W, H, color, rng, k=5, side=1):
    """Radio mast: a 2-texel pole on a small foot, a tilted dish bowl with a feed horn and a red light on top.
    About 9 x 12 texels (w 1.9, h 2.5 units at k 5). `color` is required but unused. side = -1 mirrors it."""
    k = max(1, int(k))
    Wt, Ht = max(9, W // k), max(10, H // k)
    img = np.zeros((Ht, Wt, 4), np.float32)
    P = _sp_put
    cx = Wt // 2
    for y in range(5, Ht):
        P(img, y, cx, (180, 186, 206))
        P(img, y, cx + 1, (96, 102, 126))
    for x in range(cx - 2, cx + 4):
        P(img, Ht - 1, x, (132, 140, 162))
    for x in range(cx - 1, cx + 3):
        P(img, Ht - 2, x, (150, 158, 182))
    for x in range(cx - 3, cx + 5):  # dish bowl, facing up and to the left
        P(img, 3, x, (196, 202, 220))
    for x in range(cx - 2, cx + 4):
        P(img, 4, x, (150, 158, 182))
    for x in range(cx - 1, cx + 3):
        P(img, 5, x, (104, 110, 134))
    P(img, 2, cx - 2, (150, 158, 182))
    P(img, 1, cx - 3, (226, 232, 244))
    P(img, 2, cx + 4, (150, 158, 182))
    P(img, 0, cx + 1, (255, 70, 60))
    P(img, 1, cx + 1, (150, 158, 182))
    if side < 0:
        img = img[:, ::-1].copy()
    return _sp_up(img, k)


_DECOR.update({"space_sun": _d_space_sun, "space_stars": _d_space_stars, "space_satellite": _d_space_satellite,
               "space_solar": _d_space_solar, "space_mast": _d_space_mast, "space_shadow": _d_space_shadow, "space_tracks": _d_space_tracks})


# ---------------------------------------------------------------- create chapter, round 2 (additive): machines
# A tiny texel painter (oblique 3-face boxes like `blocks`) plus the press / mixer station, the steam boiler with a lit
# firebox and a hard-edged smoke plume. Everything lives on a k-px texel grid and is NEAREST-upscaled.
def _cx_arr(name):
    return np.asarray(tex(name).convert("RGBA"), np.float32) / 255


def _cx_fit(src, w, h, tx=False, ty=False):
    """Face source (texture array, flat 0..255 rgb tuple, or fn(i, j) -> rgb 0..1 | None) -> (h, w, 4) float array."""
    out = np.zeros((h, w, 4), np.float32)
    if callable(src):
        for j in range(h):
            for i in range(w):
                c = src(i, j)
                if c is not None:
                    out[j, i, :3], out[j, i, 3] = c, 1.0
        return out
    a = np.asarray(src, np.float32)
    if a.ndim == 1:
        out[..., :3], out[..., 3] = a[:3] / 255, 1.0
        return out
    th, tw = a.shape[:2]
    for j in range(h):
        v = j % th if ty else min(th - 1, int(j * th / h))
        for i in range(w):
            u = i % tw if tx else min(tw - 1, int(i * tw / w))
            px = a[v, u]
            if a.shape[2] < 4 or px[3] > 0.5:
                out[j, i, :3], out[j, i, 3] = px[:3], 1.0
    return out


class _CxPaint:
    """Texel painter: put / rect / blit and `box` = front face + top face sheared right + side face sheared up
    (the same oblique view as the `blocks` layer)."""

    def __init__(self, w, h):
        self.w, self.h = int(w), int(h)
        self.c = np.zeros((self.h, self.w, 4), np.float32)

    def put(self, x, y, rgb, mul=1.0):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.c[y, x, :3] = np.clip(np.asarray(rgb, np.float32)[:3] * mul, 0, 1)
            self.c[y, x, 3] = 1.0

    def rect(self, x0, y0, x1, y1, rgb, mul=1.0):
        for y in range(y0, y1):
            for x in range(x0, x1):
                self.put(x, y, rgb, mul)

    def blit(self, x, y, arr, mul=1.0):
        for j in range(arr.shape[0]):
            for i in range(arr.shape[1]):
                if arr[j, i, 3] > 0.5:
                    self.put(x + i, y + j, arr[j, i, :3], mul)

    def box(self, x, y, w, h, d, front, top=None, side=None, tm=1.16, sm=0.6, tx=False, ty=False, fm=0.96,
            between=None):
        if d > 0:
            s = _cx_fit(front if side is None else side, d, h)
            for i in range(d):
                for j in range(h):
                    if s[j, i, 3] > 0.5:
                        self.put(x + w + i, y + j - i - 1, s[j, i, :3], sm)
            t = _cx_fit(front if top is None else top, w, d, tx=tx)
            for j in range(d):
                for i in range(w):
                    if t[j, i, 3] > 0.5:
                        self.put(x + i + (d - j), y - d + j, t[j, i, :3], tm)
        if between:
            between()
        self.blit(x, y, _cx_fit(front, w, h, tx=tx, ty=ty), fm)

    def image(self, k, W, H):
        im = _img(np.clip(self.c, 0, 1), "RGBA").resize((self.w * k, self.h * k), Image.NEAREST)
        res = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        res.paste(im, (0, 0))
        return res


def _cx_plate(base, w, h, grain=0.4, bevel=True, seed=0):
    """fn(i, j) painting a bevelled iron plate of colour `base` (0..255) with the grain of industrial_iron_block."""
    iron = _cx_arr("create:block/industrial_iron_block")[..., :3].mean(axis=2)
    m = float(iron.mean()) or 1.0
    b = np.array(base, np.float32) / 255

    def f(i, j):
        g = iron[(j + seed) % 16, (i + seed * 3) % 16] / m
        c = b * (1 - grain / 2 + grain * g)
        if bevel:
            if j == 0:
                c = c * 1.28
            elif j == h - 1:
                c = c * 0.62
            elif j == h - 2:
                c = c * 0.84
            if i == 0:
                c = c * 1.12
            elif i == w - 1:
                c = c * 0.7
        return np.clip(c, 0, 1)
    return f


def _cx_shade_rows(n):
    """Brightness per row of a lit horizontal cylinder (bright top, dark belly)."""
    out = []
    for j in range(n):
        t = (j + 0.5) / n
        out.append(1.4 - 0.5 * t if t < 0.25 else 1.18 - 0.62 * (t - 0.25) / 0.75 - (0.28 if j == n - 1 else 0))
    return out


def _d_create_station(W, H, color, rng, kind="press", k=4, d=5, post=5, pole=6, head=9, basin_h=12):
    """Create machine station on a gantry, front view (oblique like `blocks`): a casing block on top (andesite for
    `kind` 'press', brass for 'mixer') on an iron beam between two iron posts that reach the floor (image bottom).
    A brass-banded pole hangs from the casing. 'press': an iron press head `head` texels tall `pole` texels below
    the beam (a belt passes between the posts under it). 'mixer': a silver whisk dips into an andesite basin full
    of molten brass standing between the posts. Width W = (span + d) * k, span >= 24 (26 for a press, 32 for a
    mixer); the power shaft goes behind the casing at its middle height (y = (d + 8) * k from the top)."""
    k, w, h = _cx_grid(W, H, k)
    P = _CxPaint(w, h)
    bw = w - d
    y0 = d
    cx = (bw - 16) // 2
    girder = _cx_plate((88, 92, 92), bw, 5, 0.35)
    beam_y, post_top = y0 + 16, y0 + 21
    gap0, gap1 = post, bw - post
    mx = bw // 2
    pole_img = _cx_arr("create:block/mechanical_press_pole")[:, 0:6]
    if kind == "mixer":
        bwid = gap1 - gap0 - 2
        bx = gap0 + 1
        bt = h - basin_h
        rim = np.array([118, 120, 124], np.float32) / 255

        def b_front(i, j):
            if j == 0:
                return rim * 1.1
            if j == 1:
                return rim * 0.8
            g = 0.9 + 0.1 * ((i * 7 + j * 3) % 5) / 4
            c = np.array([92, 92, 98], np.float32) / 255 * g * (1.0 - 0.34 * (j / basin_h))
            if i == 0:
                c = c * 1.1
            if i == bwid - 1:
                c = c * 0.7
            if j == basin_h - 1:
                c = c * 0.6
            return c

        paste = np.array([206, 160, 74], np.float32) / 255

        def b_top(i, j):          # j = 0 far edge .. d-1 near edge
            if j == d - 1 or i == 0 or i >= bwid - 1:
                return rim * 1.2
            r = (i * 5 + j * 11) % 7
            return paste * (1.14 if r == 0 else (0.82 if r == 3 else 1.0))

        wy = bt - 3                       # whisk centre, dips 3 texels behind the front wall

        def whisk():
            sil = np.array([196, 202, 208], np.float32) / 255
            ry, rx = 5, 6
            for t in range(0, 360, 6):
                a = math.radians(t)
                xx, yy = int(round(mx + rx * math.cos(a))), int(round(wy + ry * math.sin(a)))
                P.put(xx, yy, sil, 1.15 if (math.sin(a) < 0 and math.cos(a) < 0.3) else 0.72)
            for dx in (-2, 2):
                for yy in range(wy - ry + 1, wy + ry):
                    if abs(dx) * 1.0 < rx:
                        P.put(mx + dx, yy, sil, 0.9 if dx < 0 else 0.62)
            for yy in range(y0 + 16, wy - ry + 1):                     # stem
                P.put(mx - 1, yy, sil, 1.05)
                P.put(mx, yy, sil, 0.7)

        P.box(bx, bt, bwid, basin_h, d, b_front, b_top, b_front, tm=1.0, sm=0.72, between=whisk, fm=1.0)
    # posts + beam
    for px in (0, bw - post):
        P.box(px, post_top, post, h - post_top, 2, _cx_plate((86, 90, 90), post, 8, 0.35, seed=px), tm=1.2, sm=0.6, fm=1.0)
    P.box(0, beam_y, bw, 5, d, girder, (150, 154, 152), girder, tm=1.0, sm=0.62, fm=1.0)
    if kind == "mixer":
        cas = "create:block/brass_casing"
        P.box(cx, y0, 16, 16, d, _cx_arr(cas), _cx_arr(cas), _cx_arr(cas), tm=1.1)
    else:
        P.box(cx, y0, 16, 16, d, _cx_arr("create:block/mechanical_press_side"), _cx_arr("create:block/mechanical_press_top"),
              _cx_arr("create:block/andesite_casing"), tm=1.1)
    # pole (banded brass) from the casing down
    if kind == "press":
        head_top = beam_y + 5 + pole
        pole_end = head_top
    else:
        pole_end = beam_y + 5
    P.blit(mx - 3, beam_y, _cx_fit(pole_img, 6, max(1, pole_end - beam_y), ty=True), 1.0)
    if kind == "press":
        hw = gap1 - gap0 - 2
        hx = gap0 + 1
        hf = _cx_plate((90, 92, 98), hw, head, 0.5, seed=3)
        orn = (hw - 6, head - 4)

        def head_front(i, j):
            c = hf(i, j)
            ox, oy = i - 3, j - 2
            if 0 <= ox < orn[0] and 0 <= oy < orn[1]:
                edge = ox in (0, orn[0] - 1) or oy in (0, orn[1] - 1)
                c = c * (1.3 if edge and (ox == 0 or oy == 0) else (0.62 if edge else 0.82))
            if (i in (1, hw - 2)) and j in (1, head - 3):
                c = c * 1.6
            return np.clip(c, 0, 1)
        P.box(hx, head_top, hw, head, 3, head_front, (118, 120, 126), (46, 47, 52), tm=1.0, sm=1.0, fm=1.0)
    return P.image(k, W, H)


def _d_create_boiler(W, H, color, rng, k=4, tank_h=22, plinth_h=15, fire=True, d=4):
    """Copper steam boiler (front view): a horizontal riveted copper tank (`color` = copper, default (186,104,74)) with
    brass bands, a steam dome with a rod, a tall flared chimney near the right end, a brass pressure gauge, on a dark
    iron plinth whose left part is a lit brass-framed firebox (3-tone orange / yellow fire). Canvas is
    (tank width + d) x (chimney .. floor); the chimney reaches the image top; the plinth stands on the image bottom.
    Pair it with scene `lights` and a soft_glow at the firebox."""
    k, w, h = _cx_grid(W, H, k)
    P = _CxPaint(w, h)
    tw_ = w - d
    cop = np.array(color if color else (186, 104, 74), np.float32) / 255
    ty = h - plinth_h - tank_h                       # tank top row
    shade = _cx_shade_rows(tank_h)
    brass = np.array([200, 156, 70], np.float32) / 255
    # chimney (behind the tank): 5 wide + flare cap + base collar
    chx = tw_ - 8
    for j in range(0, ty + 2):
        for i in range(5):
            m = (1.28, 1.12, 0.96, 0.8, 0.6)[i]
            band = 0.78 if (j % 9 == 8) else 1.0
            P.put(chx + i, j, cop, m * band)
    for i in range(-1, 6):
        for j in (0, 1):
            P.put(chx + i, j, cop, (1.35 if j == 0 else 1.05) * (1.0 if i < 4 else 0.7))
        P.put(chx + i, 2, cop, 0.5)
    for i in range(-1, 6):
        P.put(chx + i, ty - 1, cop, 1.2 if i < 3 else 0.8)
        P.put(chx + i, ty - 2, cop, 0.9 if i < 4 else 0.6)
    # steam dome + rod
    dx0, dw = tw_ // 2 - 8, 12
    for j in range(6):
        for i in range(dw):
            if (j == 0 and (i < 2 or i >= dw - 2)) or (j == 1 and (i < 1 or i >= dw - 1)):
                continue
            m = (1.36, 1.2, 1.05, 0.92, 0.78, 0.66)[j] * (1.1 if i < 2 else (0.68 if i >= dw - 2 else 1.0))
            P.put(dx0 + i, ty - 5 + j, cop, m)
    for i in range(dw):
        P.put(dx0 + i, ty - 1, brass, 1.0 if i < dw - 2 else 0.7)
    for j in range(3):
        P.put(dx0 + dw // 2 - 1, ty - 8 + j, brass, 1.1)
        P.put(dx0 + dw // 2, ty - 8 + j, brass, 0.7)
    # plinth: dark iron with a brass trim; firebox opening on the left
    pl = _cx_plate((54, 56, 58), tw_, plinth_h, 0.5, bevel=False, seed=5)
    P.box(0, h - plinth_h, tw_, plinth_h, d, pl, (96, 98, 100), (40, 41, 44), tm=1.0, sm=1.0, fm=1.0)
    for i in range(tw_):
        P.put(i, h - plinth_h, brass, 1.05)
        P.put(i, h - plinth_h + 1, brass, 0.6)
    # small ash-pit door and bolts on the right part of the plinth
    ax0 = tw_ - 18
    for j in range(-1, 6):
        for i in range(-1, 9):
            edge = i in (-1, 8) or j in (-1, 5)
            P.put(ax0 + i, h - plinth_h + 5 + j, brass if edge else np.array([0.12, 0.1, 0.1], np.float32),
                  (1.0 if (i == -1 or j == -1) else 0.6) if edge else 1.0)
    for bx_ in (20, 24, tw_ - 3):
        P.put(bx_, h - plinth_h + 3, brass, 0.9)
        P.put(bx_, h - 3, brass, 0.9)
    # tank: rounded ends, shaded rows, seams + rivets, end bands
    ncol = tw_
    for j in range(tank_h):
        for i in range(ncol):
            r = 4
            cut = 0
            if j < r:
                cut = r - j
            elif j >= tank_h - r:
                cut = r - (tank_h - 1 - j)
            cut = {4: 3, 3: 2, 2: 1, 1: 1, 0: 0}.get(cut, 0) if cut else 0
            if i < cut or i >= ncol - cut:
                continue
            m = shade[j]
            m *= 1.0 + 0.05 * (((i // 3) + j // 5) % 2)
            seam = i in (ncol // 4, ncol // 2, 3 * ncol // 4)
            if seam:
                m *= 0.6
            elif (i - 1 in (ncol // 4, ncol // 2, 3 * ncol // 4)) and j % 6 == 2:
                m *= 1.38
            if i < 2 or i >= ncol - 2:
                m *= 0.78
            P.put(i, ty + j, cop, m)
    for bxp in (4, ncol - 6):                      # brass bands
        for j in range(tank_h):
            if P.c[ty + j, bxp, 3] > 0:
                P.put(bxp, ty + j, brass, shade[j] * 1.02)
                P.put(bxp + 1, ty + j, brass, shade[j] * 0.7)
    # pressure gauge
    gx, gy = ncol // 2 + 4, ty + tank_h // 2 + 1
    for yy in range(-5, 6):
        for xx in range(-5, 6):
            rr = math.hypot(xx, yy)
            if rr <= 4.7:
                if rr > 3.5:
                    P.put(gx + xx, gy + yy, brass, 1.12 if (xx + yy) < 0 else 0.62)
                else:
                    P.put(gx + xx, gy + yy, np.array([0.9, 0.88, 0.8], np.float32), 1.0 if (xx + yy) < 2 else 0.86)
    for t in range(0, 4):
        P.put(gx + t, gy - t, np.array([0.18, 0.1, 0.08], np.float32))
    P.put(gx, gy, np.array([0.18, 0.1, 0.08], np.float32))
    # firebox door with fire
    fx0, fw = 3, 13
    fy0, fh = h - plinth_h + 3, plinth_h - 5
    for j in range(-1, fh + 1):
        for i in range(-1, fw + 1):
            edge = i in (-1, fw) or j in (-1, fh)
            if edge:
                lit = (i == -1 or j == -1)
                P.put(fx0 + i, fy0 + j, brass, 1.15 if lit else 0.6)
    for j in range(fh):
        for i in range(fw):
            if (j == 0 and (i < 1 or i >= fw - 1)):
                continue
            P.put(fx0 + i, fy0 + j, np.array([0.2, 0.07, 0.05], np.float32))
    if fire:
        cols = []
        for i in range(fw):
            cols.append(3 + int(round(rng.random() * 3.0 + 2.0 * math.sin(i * 1.3 + 0.7) ** 2)))
        for i in range(fw):
            for t in range(min(cols[i], fh - 1)):
                j = fh - 1 - t
                rel = t / max(cols[i], 1)
                if t >= cols[i] - 1 and cols[i] > 4:
                    c = (0.86, 0.3, 0.1)
                elif rel > 0.6:
                    c = (0.98, 0.52, 0.12)
                elif rel > 0.28:
                    c = (1.0, 0.7, 0.18)
                else:
                    c = (1.0, 0.92, 0.52)
                P.put(fx0 + i, fy0 + j, np.array(c, np.float32))
        for i in range(0, fw, 2):                                   # grate bars
            P.put(fx0 + i, fy0 + fh - 1, np.array([0.28, 0.1, 0.04], np.float32))
    return P.image(k, W, H)


def _d_create_smoke(W, H, color, rng, k=4, puffs=4, drift=-0.5):
    """A short plume of hard-edged smoke puffs rising from the bottom centre of the box: `puffs` clumps growing
    towards the top, three tones (light upper-left, `color` mid, dark lower-right), no soft alpha; the upper puffs are
    semi-transparent in steps. `drift` leans the plume sideways (-1 left .. 1 right). Use unlit true, shadow 0."""
    k, w, h = _cx_grid(W, H, k)
    base = np.array(color, np.float32) / 255
    out = np.zeros((h, w, 4), np.float32)
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    r0 = max(2.0, min(w, h) * 0.13)
    rs = [r0 * (1.0 + 1.0 * i / max(1, puffs - 1)) for i in range(puffs)]
    span = h - 2 - 2 * rs[-1]
    items = []
    used = 0.0
    for i, r in enumerate(rs):
        t = i / max(1, puffs - 1)
        cy = h - 1 - r - (span * t if puffs > 1 else 0)
        cxp = w * 0.5 + drift * w * 0.22 * t + rng.uniform(-0.15, 0.15) * r
        items.append((cxp, cy, r, 1.0 if i < puffs - 2 else (0.85 if i == puffs - 2 else 0.62)))
    for cxp, cyp, r, al in reversed(items):
        for ox, oy, rr in ((0.0, 0.0, r), (-0.78 * r, 0.3 * r, 0.62 * r), (0.8 * r, 0.34 * r, 0.56 * r)):
            lx, ly = cxp + ox, cyp + oy
            body = np.hypot(x + 0.5 - lx, y + 0.5 - ly) <= rr
            inner = np.hypot(x + 0.5 - (lx - 0.3 * rr), y + 0.5 - (ly - 0.32 * rr)) <= rr * 0.92
            cap = np.hypot(x + 0.5 - (lx - 0.38 * rr), y + 0.5 - (ly - 0.4 * rr)) <= rr * 0.42
            tone = np.where(inner, 0.96, 0.74)
            tone = np.where(cap & (rr > 2.4), 1.14, tone)[..., None] * base
            out[..., :3] = np.where(body[..., None], np.clip(tone, 0, 1), out[..., :3])
            out[..., 3] = np.where(body, al, out[..., 3])
    return _cx_up(out, k, W, H)


def _cx_up(out, k, W, H):
    h, w = out.shape[:2]
    im = _img(out, "RGBA").resize((w * k, h * k), Image.NEAREST)
    res = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    res.paste(im, (0, 0))
    return res


_DECOR.update({"create_station": _d_create_station, "create_boiler": _d_create_boiler, "create_smoke": _d_create_smoke})


DECOR_MOTIFS = set(_DECOR) | {"sprite", "sprite_row", "blocks"}


# ---------------------------------------------------------------- scene (map-space illustration)
SCENE_PX = 24  # pixels per grid unit for the big scene canvas (soft art, upscales fine)
SPRITE_K_MAX = 10  # max texture-pixel scale for sprites: 16 px -> 160 px = 6.7 grid units


def scene_box(content, spec, center=None):
    """Scene canvas in map units: (cx, cy, w, h). Centred on the quests (where FTB centres the view),
    big enough that the dissolving edges fall outside the screen at the usual zoom."""
    x0, y0, x1, y1 = content
    cx, cy = center or ((x0 + x1) / 2, (y0 + y1) / 2)
    mx, my = spec.get("margin", (18, 13))
    w = max(2 * max(cx - x0, x1 - cx) + 2 * mx, spec.get("min_w", 64))
    h = max(2 * max(cy - y0, y1 - cy) + 2 * my, spec.get("min_h", 48))
    return cx, cy, w, h


PIXEL_MOTIFS = {"sprite", "sprite_row", "blocks"}
# soft light / weather / particle motifs: never pixelated or shadowed by scene-wide switches
ATMOSPHERE = {"soft_glow", "sky_band", "nebula_glow", "aurora", "milky_way", "blueprint", "contour_map", "embers",
              "fireflies", "snowfall", "star_cluster", "falling_leaves", "comet", "heartbeat", "lightning", "sun",
              "light_rays"}
# big soft backdrops: the scene-wide 'pixelate' switch leaves them smooth too (a layer may still opt in)
BACKDROP = {"mountain_range", "snowy_range", "strata_band", "tree_line", "wheat_field", "planet_horizon", "planet",
            "moon", "ringed_planet", "power_line", "castle"}
# create chapter: pixel parts take the scene light / contact shadow like sprites and `blocks`
PIXEL_MOTIFS.update({"create_cog", "create_wheel", "create_sails", "create_shaft", "create_belt", "create_water",
                     "create_steam"})
PIXEL_MOTIFS.update({"create_station", "create_boiler", "create_smoke"})


def _motif_opts(fn, ly) -> dict:
    """Optional per-layer parameters a motif function declares as keyword arguments (e.g. lightning width)."""
    params = inspect.signature(fn).parameters
    return {k: ly[k] for k in params if k not in ("W", "H", "color", "rng") and k in ly}


def _sprite_k(fit, ly, sc) -> int:
    """Texel scale (canvas px per texture pixel). Layer 'k' > scene 'texel' > fitted to the box (capped)."""
    if ly.get("k"):
        return max(1, int(ly["k"]))
    if sc.get("texel"):
        return max(1, int(sc["texel"]))
    return max(1, min(int(sc.get("k_max", SPRITE_K_MAX)), int(fit)))


def _square(asset) -> Image.Image:
    t = tex(asset)
    return t.crop((0, 0, t.size[0], min(t.size))) if t.size[1] != t.size[0] else t


def _sprite_row(ly, sc, lw, lh, rng):
    """Several real textures: 'arrange' row (even rail, legacy) | scatter (irregular gaps and heights,
    some mirrored) | pile (a heap, front row widest)."""
    assets = ly["assets"]
    n = len(assets)
    arrange = ly.get("arrange", "row")
    sp = float(ly.get("spacing", 1.35))
    if arrange == "pile":
        rows, left = [], n
        width = max(1, math.ceil((math.sqrt(8 * n + 1) - 1) / 2))
        while left > 0:
            rows.append(min(width, left))
            left -= rows[-1]
            width = max(1, width - 1)
        cols = rows[0]
        k = _sprite_k(min(lw / ((cols * 0.78 + 0.22) * CELL), lh / ((len(rows) * 0.55 + 0.45) * CELL)), ly, sc)
        s = CELL * k
        img = Image.new("RGBA", (int((cols * 0.78 + 0.22) * s) + 1, int((len(rows) * 0.55 + 0.45) * s) + 1))
        it = iter(assets)
        placed = []
        for r, cnt in enumerate(rows):  # r = 0 is the bottom (front) row
            x0 = (cols - cnt) * 0.39 * s
            for c in range(cnt):
                x = x0 + c * 0.78 * s + rng.uniform(-0.06, 0.06) * s
                y = img.size[1] - s - r * 0.55 * s - rng.uniform(0, 0.05) * s
                placed.append((r, x, y, next(it)))
        for r, x, y, a in sorted(placed, key=lambda p: -p[0]):  # back rows first, front row on top
            t = _square(a).resize((s, s), Image.NEAREST)
            if rng.random() < 0.35:
                t = t.transpose(Image.FLIP_LEFT_RIGHT)
            img.alpha_composite(t, (int(max(0, x)), int(max(0, y))))
        return img, k
    k = _sprite_k(min(lw / (n * CELL * sp), lh / CELL), ly, sc)
    s = CELL * k
    if arrange == "scatter":
        gaps = [rng.uniform(0.72, 1.0 + 1.8 * (sp - 1)) for _ in range(n)]  # some overlap, some wide gaps
        lift = [rng.choice((0, 0, 0.1, 0.22, 0.34)) for _ in range(n)]
        img = Image.new("RGBA", (int(sum(gaps) * s) + 1, int(s * 1.25) + 1), (0, 0, 0, 0))
        x = 0.0
        for j, a in enumerate(assets):
            t = _square(a).resize((s, s), Image.NEAREST)
            if rng.random() < 0.4:
                t = t.transpose(Image.FLIP_LEFT_RIGHT)
            img.alpha_composite(t, (int(x + (gaps[j] - 1) * s * 0.5), int(img.size[1] - s - lift[j] * s)))
            x += gaps[j] * s
        return img, k
    img = Image.new("RGBA", (int(n * s * sp), s), (0, 0, 0, 0))
    for j, a in enumerate(assets):
        img.alpha_composite(_square(a).resize((s, s), Image.NEAREST), (int(j * s * sp), 0))
    return img, k


def _emit(img, color, strength=1.0) -> Image.Image:
    """Light given off by a glowing sprite: a broad soft pool of light around it plus a faint close
    bloom. Replaces the old tight outline halo, which made sprites look like cut-out stickers."""
    w, h = img.size
    s = max(w, h)
    pad = int(s * 0.55)
    W, H = w + 2 * pad, h + 2 * pad
    al = np.asarray(img.getchannel("A"), np.float32) / 255
    tot = max(float(al.sum()), 1.0)
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = float((al * xs).sum() / tot) + pad, float((al * ys).sum() / tot) + pad
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / (s * 1.15)
    pool = np.clip(1 - r, 0, 1) ** 1.8 * 0.42 * strength
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = np.array(color, np.float32) / 255
    out[..., 3] = pool
    res = _img(out, "RGBA")
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base.paste(img, (pad, pad))
    res.alpha_composite(_glow_of(base, tuple(color), max(3, s * 0.07), 0.32 * strength))
    res.alpha_composite(base)
    return res


def _light_vec(light) -> tuple[float, float]:
    """Unit vector pointing TOWARDS the light (screen coords, y down). 'dir' = [dx, dy] or degrees."""
    d = light.get("dir", [-1, -1])
    if isinstance(d, (int, float)):
        a = math.radians(d)
        d = [math.cos(a), -math.sin(a)]
    n = math.hypot(d[0], d[1]) or 1.0
    return d[0] / n, d[1] / n


def _shift(a, dx, dy):
    """Shift a 2-D array by whole pixels, zero fill."""
    out = np.zeros_like(a)
    H, W = a.shape
    xs0, xs1 = max(0, dx), min(W, W + dx)
    ys0, ys1 = max(0, dy), min(H, H + dy)
    out[ys0:ys1, xs0:xs1] = a[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx]
    return out


def _relight(img, k, light, tint=None, rim=None, shade=None, haze=0.0, haze_color=None) -> Image.Image:
    """Put a pixel-art (or vector) layer into the scene light: multiply-tint toward the light colour,
    a gradient across the object (lit side brighter), a one-texel rim light on the edges facing the
    light and an optional depth haze. k = canvas px per texel (rim width)."""
    a = np.asarray(img, np.float32) / 255
    rgb, al = a[..., :3], a[..., 3]
    col = np.array(light.get("color", (255, 244, 225)), np.float32) / 255
    tint = light.get("tint", 0.0) if tint is None else tint
    rim = light.get("rim", 0.0) if rim is None else rim
    shade = light.get("shade", 0.0) if shade is None else shade
    lx, ly_ = _light_vec(light)
    if tint:
        rgb = rgb * (1 - tint + tint * col * 1.08)
    if shade:
        H, W = al.shape
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        t = ((x / max(W, 1) - 0.5) * lx + (y / max(H, 1) - 0.5) * ly_)  # +0.5 towards the light
        rgb = rgb * (1 + shade * 0.5 * np.clip(t * 1.6, -1, 1))[..., None]
    if rim:
        k = max(1, int(k))
        m = (al > 0.5).astype(np.float32)
        nb = _shift(m, -int(round(lx * k)), -int(round(ly_ * k)))  # neighbour on the light side
        edge = (m * (1 - nb))[..., None] * rim
        rimc = col * 0.55 + 0.45
        rgb = rgb * (1 - edge) + rimc * edge
    if haze:
        hc = np.array(haze_color or light.get("haze_color", (40, 44, 56)), np.float32) / 255
        rgb = rgb * (1 - haze) + hc * haze
    out = np.concatenate([np.clip(rgb, 0, 1), al[..., None]], axis=2)
    return _img(out, "RGBA")


def _with_shadow(img, contact=0.0, drop=0.0, light=None) -> tuple[Image.Image, int]:
    """Ground the object: a soft contact shadow under its footprint and/or a drop shadow cast away
    from the light (for things hanging on a wall). Returns (image, padding added on each side)."""
    w, h = img.size
    s = max(w, h)
    pad = int(s * 0.18) + 4
    out = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    al = img.getchannel("A")
    bb = al.point(lambda v: 255 if v > 60 else 0).getbbox()
    if not bb:
        out.paste(img, (pad, pad))
        return out, pad
    if drop:
        lx, ly_ = _light_vec(light or {})
        off = max(2, int(s * 0.05))
        sh = Image.new("L", out.size, 0)
        sh.paste(al.point(lambda v, d=drop: int(v * 0.75 * min(1, d))), (pad - int(lx * off), pad - int(ly_ * off)))
        g = Image.new("RGBA", out.size, (0, 0, 0, 0))
        g.putalpha(sh.filter(ImageFilter.GaussianBlur(max(1.5, s * 0.025))))
        out.alpha_composite(g)
    if contact:
        x0, y0, x1, y1 = bb
        # footprint = width of the lowest 15 % of the silhouette (a lantern's base, not its handle)
        foot = np.asarray(al, np.float32)[max(y0, int(y1 - (y1 - y0) * 0.15)):y1] > 60
        cols = np.where(foot.any(0))[0]
        fx0, fx1 = (float(cols.min()), float(cols.max())) if len(cols) else (x0, x1)
        cw = float(max(fx1 - fx0, (x1 - x0) * 0.6) * 1.15)
        cx = (fx0 + fx1) / 2 + pad
        ch = max(3.0, cw * 0.12)
        cy = y1 + pad - ch * 0.15
        g = Image.new("RGBA", out.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).ellipse([cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2],
                                  fill=(0, 0, 0, int(255 * 0.8 * min(1, contact))))
        out.alpha_composite(g.filter(ImageFilter.GaussianBlur(max(1.5, ch * 0.45))))
    out.alpha_composite(img, (pad, pad))
    return out, pad


def _pixelate(img, k, colors=0, outline=0.0) -> Image.Image:
    """Re-render a smooth layer on a k-px texel grid so it shares the pixel-art look of the sprites:
    premultiplied block average, alpha snapped to 4 levels, optional palette reduction and a one-texel
    dark outline, then nearest-upscaled back to size."""
    k = max(2, int(k))
    W, H = img.size
    w, h = max(1, -(-W // k)), max(1, -(-H // k))
    a = np.zeros((h * k, w * k, 4), np.float32)
    a[:H, :W] = np.asarray(img, np.float32) / 255
    a[..., :3] *= a[..., 3:4]
    s = a.reshape(h, k, w, k, 4).mean(axis=(1, 3))
    al = s[..., 3]
    rgb = s[..., :3] / np.maximum(al[..., None], 1e-4)
    # crisp silhouette, smooth fades: an edge texel snaps to its neighbourhood's opacity or to zero,
    # while a slow gradient (dissolving mountain foot, smoke) keeps its continuous alpha
    loc = np.asarray(Image.fromarray((al * 255).astype(np.uint8), "L").filter(ImageFilter.MaxFilter(3)),
                     np.float32) / 255
    al = np.where(al >= 0.5 * loc, loc, 0.0)
    al = np.where(al < 0.04, 0, al)
    if colors:
        q = _img(np.clip(rgb, 0, 1)).quantize(colors=int(colors), method=Image.Quantize.FASTOCTREE,
                                                  dither=Image.Dither.NONE)
        rgb = np.asarray(q.convert("RGB"), np.float32) / 255
    if outline:
        m = (al >= 0.5).astype(np.float32)
        dil = np.asarray(Image.fromarray((m * 255).astype(np.uint8), "L").filter(ImageFilter.MaxFilter(3)),
                         np.float32) / 255
        ring = (dil > 0.5) & (m < 0.5)
        src = np.asarray(_img(np.clip(rgb * m[..., None], 0, 1)).filter(ImageFilter.MaxFilter(3)), np.float32) / 255
        rgb = np.where(ring[..., None], src * 0.35, rgb)
        al = np.where(ring, np.maximum(al, min(1.0, outline)), al)
    out = np.concatenate([np.clip(rgb, 0, 1), np.clip(al, 0, 1)[..., None]], axis=2)
    big = _img(out, "RGBA").resize((w * k, h * k), Image.NEAREST)
    return big.crop((0, 0, W, H))


def _blocks(ly, sc, lw, lh):
    """A small structure built from real block textures in an oblique (front + top + right side) view,
    every texel on one grid: rows = front elevation (top row first), legend = char -> asset or
    {front, top, side}. Hidden faces are skipped, top faces lit, side faces shaded."""
    rows = ly["rows"]
    legend = ly.get("legend", {})
    nr, nc = len(rows), max(len(r) for r in rows)
    d = max(1, int(round(CELL * float(ly.get("depth", 0.45)))))
    Wt, Ht = nc * CELL + d, nr * CELL + d
    k = _sprite_k(min(lw / Wt, lh / Ht), ly, sc)
    can = np.zeros((Ht, Wt, 4), np.float32)

    def cell(r, c):
        return 0 <= r < nr and 0 <= c < len(rows[r]) and rows[r][c] not in " ."

    def face(ch, which):
        v = legend.get(ch)
        if isinstance(v, dict):
            v = v.get(which) or v.get("front") or next(iter(v.values()))
        t = _square(v)
        if t.size != (CELL, CELL):
            t = t.resize((CELL, CELL), Image.NEAREST)
        return np.asarray(t, np.float32) / 255

    def put(y, x, px, mul):
        if 0 <= y < Ht and 0 <= x < Wt and px[3] > 0.01:
            ca, b = px[3], can[y, x]
            oa = ca + b[3] * (1 - ca)
            can[y, x, :3] = (px[:3] * mul * ca + b[:3] * b[3] * (1 - ca)) / max(oa, 1e-4)
            can[y, x, 3] = oa

    for r in range(nr - 1, -1, -1):  # bottom row first: upper blocks cover the top faces below them
        for c in range(nc):
            if not cell(r, c):
                continue
            ch = rows[r][c]
            ox, oy = c * CELL, d + r * CELL
            if not cell(r, c + 1):  # right side face, sheared up
                sd = face(ch, "side")
                for i in range(d):
                    sx = min(CELL - 1, int(i * CELL / d))
                    for j in range(CELL):
                        put(oy + j - i - 1, ox + CELL + i, sd[j, sx], 0.62)
            if not cell(r - 1, c):  # top face, sheared right
                tp = face(ch, "top")
                for j in range(d):  # j = 0 is the far edge
                    sy = min(CELL - 1, int(j * CELL / d))
                    for i in range(CELL):
                        put(oy - d + j, ox + i + (d - j), tp[sy, i], 1.18)
            fr = face(ch, "front")
            for j in range(CELL):
                for i in range(CELL):
                    put(oy + j, ox + i, fr[j, i], 0.94 - 0.1 * (j >= CELL - 2 and cell(r + 1, c)))
    img = _img(np.clip(can, 0, 1), "RGBA")
    return img.resize((Wt * k, Ht * k), Image.NEAREST), k


def _light_pass(can, sc) -> Image.Image:
    """Scene-wide cast light: content near each light is brightened and tinted in its colour, content
    elsewhere optionally dimmed ('ambient' < 1). Only lights what is drawn; it adds no glow of its own."""
    lights = sc.get("lights") or []
    amb = float(sc.get("ambient", 1.0))
    if not lights and amb == 1.0:
        return can
    W, H = can.size
    a = np.asarray(can, np.float32) / 255
    rgb, al = a[..., :3], a[..., 3:4]
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    add = np.zeros((H, W, 3), np.float32)
    for L in lights:
        r = max(1.0, float(L.get("radius", 0.3)) * W)
        d = np.sqrt((x - L["x"] * W) ** 2 + ((y - L["y"] * H)) ** 2) / r
        f = np.clip(1 - d, 0, 1) ** 2 * float(L.get("strength", 0.6))
        add += f[..., None] * (np.array(L.get("color", (255, 170, 90)), np.float32) / 255)
    rgb = rgb * amb + rgb * add * 1.3 + add * 0.06 * (al > 0.02)
    return _img(np.concatenate([np.clip(rgb, 0, 1), al], axis=2), "RGBA")


def _layer_image(ly, i, seed, sc, lw, lh):
    """Render one scene layer at canvas resolution; returns (image, texel scale or None)."""
    m = ly["motif"]
    rng = random.Random(f"{seed}:{i}")
    if m == "sprite_row":
        img, k = _sprite_row(ly, sc, lw, lh, rng)
    elif m == "blocks":
        img, k = _blocks(ly, sc, lw, lh)
    elif m == "sprite":  # a real game texture, pixel-scaled (Minecraft-native focal props)
        t = tex(ly["asset"])
        k = _sprite_k(min(lw / t.size[0], lh / t.size[1]), ly, sc)
        img = t.resize((t.size[0] * k, t.size[1] * k), Image.NEAREST)
        if ly.get("flip"):
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
    else:
        fn = _DECOR[m]
        img = fn(lw, lh, tuple(ly["color"]), rng, **_motif_opts(fn, ly))
        k = None
    # rotate before lighting/shadows (so they stay upright); pixel art rotates with nearest sampling
    if ly.get("rot"):
        img = img.rotate(-ly["rot"], resample=Image.NEAREST if m in PIXEL_MOTIFS else Image.BICUBIC, expand=True)
    if m not in PIXEL_MOTIFS:
        pix = ly.get("pixelate", sc.get("pixelate") if m not in ATMOSPHERE | BACKDROP else None)
        if pix:  # after rotation, so the texel grid stays upright
            k = int(sc.get("texel") or 4) if pix is True else int(pix)
            img = _pixelate(img, k, ly.get("colors", sc.get("colors", 0)), ly.get("outline", sc.get("outline", 0)))
    light = sc.get("light")
    pixel = m in PIXEL_MOTIFS
    if light and (pixel or ly.get("lit")) and not ly.get("unlit"):
        img = _relight(img, k or 4, light, ly.get("tint"), ly.get("rim"), ly.get("shade"), ly.get("haze", 0.0),
                       ly.get("haze_color"))
    elif ly.get("haze"):
        img = _relight(img, k or 4, {}, 0, 0, 0, ly["haze"], ly.get("haze_color") or sc.get("haze_color"))
    contact = ly.get("shadow", sc.get("shadow", 0.0) if pixel else 0.0)
    shadowed, pad_s = (_with_shadow(img, contact, ly.get("drop", 0.0), light) if contact or ly.get("drop")
                       else (img, 0))
    if ly.get("glow"):  # light pool from the bare object, shadow + object on top of it
        res = _emit(img, tuple(ly["glow"]), float(ly.get("glow_strength", 1.0)))
        pad_e = (res.size[0] - img.size[0]) // 2
        if pad_s:
            res.alpha_composite(shadowed, (pad_e - pad_s, pad_e - pad_s))
        return res, k
    return shadowed, k


def scene(path: Path, spec: dict, w_units, h_units, seed: str):
    """Compose the chapter illustration: layers placed by canvas fractions, edges dissolved.
    Optional scene keys (all new, default off): texel, k_max, pixelate, colors, outline, light, shadow,
    lights, ambient, haze_color - see ART_GUIDE.md."""
    W, H = int(w_units * SCENE_PX), int(h_units * SCENE_PX)
    can = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for i, ly in enumerate(spec["layers"]):
        lw_u = ly["w"]
        lh_u = ly.get("h") or lw_u / DECOR_ASPECT.get(ly["motif"], 1.0)
        lw, lh = max(8, int(lw_u * SCENE_PX)), max(8, int(lh_u * SCENE_PX))
        img, _k = _layer_image(ly, i, seed, spec, lw, lh)
        img.putalpha(img.getchannel("A").point(lambda v, a=ly.get("alpha", 1.0): int(v * max(0, min(1, a)))))
        x = int(ly["x"] * W - img.size[0] / 2)
        y = int(ly["y"] * H - img.size[1] / 2)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        layer.paste(img, (x, y))
        can.alpha_composite(layer)
    can = _light_pass(can, spec)
    # dissolve the edges into the tiled background
    fx = np.clip(np.minimum(np.arange(W), W - 1 - np.arange(W)) / (W * 0.12), 0, 1)
    fy = np.clip(np.minimum(np.arange(H), H - 1 - np.arange(H)) / (H * 0.12), 0, 1)
    f = np.outer(fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)).astype(np.float32)
    a = np.asarray(can.getchannel("A"), np.float32) * f
    can.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    can.save(path)


def anchor_center(anchor, bounds, banner_box, w, h):
    """Map-space centre for a decoration of w x h units. bounds = content box incl. panels."""
    x0, y0, x1, y1 = bounds
    if anchor == "behind_banner":
        bx, by, _, _ = banner_box
        return bx, by
    if anchor == "center":
        return (x0 + x1) / 2, (y0 + y1) / 2
    if anchor == "left_edge":
        return x0 - w * 0.2, (y0 + y1) / 2
    if anchor == "right_edge":
        return x1 + w * 0.2, (y0 + y1) / 2
    vx = x0 + w * 0.1 if "left" in anchor else x1 - w * 0.1
    vy = y0 + h * 0.15 if "top" in anchor else y1 - h * 0.1
    return vx, vy


# ---------------------------------------------------------------- spec validation
def validate(style: dict, key: str) -> list[str]:
    errs = []
    sh = style.get("shapes", {})
    for role in ("normal", "milestone", "optional", "gate"):
        if sh.get(role) not in SHAPES:
            errs.append(f"{key}: shape for {role} must be one of {sorted(SHAPES)}")
    bg = style.get("background", {})
    for t in bg.get("tiles", []):
        if not has_tex(t["asset"]):
            errs.append(f"{key}: background texture missing: {t['asset']}")
    if (bg.get("overlay") or {}).get("type", "none") not in BG_OVERLAYS:
        errs.append(f"{key}: unknown background overlay {bg['overlay']}")
    b = style.get("banner", {})
    for a in [b.get("ribbon_asset")] + list(b.get("icons_left", [])) + list(b.get("icons_right", [])):
        if a and not has_tex(a):
            errs.append(f"{key}: banner texture missing: {a}")
    if b.get("motif", "none") not in BANNER_MOTIFS:
        errs.append(f"{key}: unknown banner motif {b.get('motif')}")
    for dc in style.get("decor", []):
        if dc["motif"] not in DECOR_MOTIFS:
            errs.append(f"{key}: unknown decor motif {dc['motif']}")
        if dc["anchor"] not in ANCHORS:
            errs.append(f"{key}: unknown decor anchor {dc['anchor']}")
    for ly in (style.get("scene") or {}).get("layers", []):
        if ly.get("motif") not in DECOR_MOTIFS:
            errs.append(f"{key}: unknown scene motif {ly.get('motif')}")
        if ly.get("motif") == "sprite" and not has_tex(ly.get("asset", "")):
            errs.append(f"{key}: scene sprite texture missing: {ly.get('asset')}")
        for a in ly.get("assets", []) if ly.get("motif") == "sprite_row" else []:
            if not has_tex(a):
                errs.append(f"{key}: scene sprite_row texture missing: {a}")
        if ly.get("motif") == "sprite_row" and ly.get("arrange", "row") not in ("row", "scatter", "pile"):
            errs.append(f"{key}: sprite_row arrange must be row|scatter|pile")
        if ly.get("motif") == "blocks":
            rows, legend = ly.get("rows") or [], ly.get("legend") or {}
            if not rows:
                errs.append(f"{key}: blocks layer needs 'rows'")
            for ch in {c for r in rows for c in r if c not in " ."}:
                v = legend.get(ch)
                for a in (v.values() if isinstance(v, dict) else [v]):
                    if not a or not has_tex(a):
                        errs.append(f"{key}: blocks legend '{ch}' texture missing: {a}")
        if not (0 <= ly.get("x", -1) <= 1 and 0 <= ly.get("y", -1) <= 1):
            errs.append(f"{key}: scene layer {ly.get('motif')} needs x, y in 0..1")
    hx = style.get("palette", {}).get("text_key_hex", "")
    if not (len(hx) == 7 and hx.startswith("#")):
        errs.append(f"{key}: text_key_hex must look like #RRGGBB")
    return errs
