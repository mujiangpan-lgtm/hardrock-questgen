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
