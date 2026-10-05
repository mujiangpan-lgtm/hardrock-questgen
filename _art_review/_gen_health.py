"""Scratch generator for art_styles.d/health.json (infirmary / apothecary interior).
Places blocks and sprites in canvas pixels on one texel grid (k=4) and writes fractions.
Usage: python _art_review/_gen_health.py  (writes art_styles.d/health.json)"""
import json, sys
sys.path.insert(0, ".")
import artlib

K = 4            # canvas px per texel (scene texel)
W, H = 64 * 24, 48 * 24
CELL = 16
U = 24           # canvas px per map unit
L = []           # layers


def fx(px): return round(px / W, 4)
def fy(py): return round(py / H, 4)


def bbox(asset):
    t = artlib.tex(asset).convert("RGBA")
    return t.size, t.getchannel("A").getbbox()  # (w,h), (x0,y0,x1,y1)


def blocks(rows, legend, depth, left, bottom, **kw):
    """left = x of front-face left edge, bottom = y of front-face bottom (canvas px). Returns geometry."""
    d = max(1, int(round(CELL * depth)))
    nr, nc = len(rows), max(len(r) for r in rows)
    Wt, Ht = nc * CELL + d, nr * CELL + d
    cx, cy = left + Wt * K / 2, bottom - Ht * K / 2
    ly = {"motif": "blocks", "x": fx(cx), "y": fy(cy), "w": round(Wt * K / U + 0.5, 1),
          "h": round(Ht * K / U + 0.5, 1), "rows": rows, "legend": legend, "depth": depth}
    ly.update(kw)
    L.append(ly)
    top = bottom - Ht * K
    # helpers: front-edge y of the top face of row r, and x range of the top surface
    return {"top": top, "d": d, "left": left,
            "row_front_top": lambda r: top + (d + r * CELL) * K}


def sprite(asset, cx, bottom, rot=0, **kw):
    """Place a sprite so that its visible pixels are centred on cx and its lowest visible pixel sits at
    'bottom' (canvas px). rot=180 hangs it upside down: then 'bottom' is the TOP of the visible pixels."""
    (tw, th), (x0, y0, x1, y1) = bbox(asset)
    vcx = (x0 + x1) / 2
    if rot == 180:
        # after a 180 turn the visible box is mirrored
        vcx = tw - vcx
        vtop = th - y1
        cy = bottom - vtop * K + th * K / 2
    else:
        cy = bottom - y1 * K + th * K / 2
    ccx = cx - vcx * K + tw * K / 2
    ly = {"motif": "sprite", "asset": asset, "x": fx(ccx), "y": fy(cy), "w": round(tw * K / U, 2), "alpha": 1.0}
    if rot:
        ly["rot"] = rot
    ly.update(kw)
    L.append(ly)


def layer(**kw):
    L.append(kw)


ROSE = "tfc:block/wood/planks/sequoia"
DARK = "tfc:block/wood/planks/hickory"
FLOORW = "minecraft:block/dark_oak_planks"
WOODC = [104, 58, 52]      # vector boards, close to sequoia
FLOOR_Y = 990        # front-top edge of the floor (canvas px)
STAND = FLOOR_Y - 14  # furniture front bottom (stands a little behind the floor edge)

# ---------------------------------------------------------------- atmosphere
layer(motif="sky_band", x=0.5, y=0.14, w=72, h=12, color=[22, 8, 14], alpha=0.45)
layer(motif="soft_glow", x=0.6, y=0.75, w=36, h=26, color=[255, 156, 96], alpha=0.34)
layer(motif="soft_glow", x=0.245, y=0.42, w=20, h=16, color=[255, 168, 104], alpha=0.22)

# ---------------------------------------------------------------- floor and ceiling beam
blocks(["P" * 25], {"P": FLOORW}, 1.0, -30, FLOOR_Y + 64, shadow=0, haze=0.3)
blocks(["B" * 25], {"B": DARK}, 0.3, -30, 226, shadow=0, haze=0.35)

# ---------------------------------------------------------------- left: medicine cabinet (dark back,
# thin lit boards, small jars at the scene texel)
CL, CR, CT = 200, 468, 498
blocks(["BBBB"] * 7, {"B": DARK}, 0.06, CL + 8, STAND - 6, shadow=0, haze=0.5)
for y in (CT, 640, 785, 930):
    layer(motif="plank_shelf", x=fx((CL + CR) / 2), y=fy(y), w=round((CR - CL + 26) / U, 2), h=1.3,
          color=WOODC, alpha=1.0, lit=True, pixelate=4)
for x in (CL - 2, CR + 2):
    layer(motif="plank_shelf", x=fx(x), y=fy((CT + STAND) / 2), w=round((STAND - CT) / U, 2), h=1.3,
          color=[90, 50, 46], alpha=1.0, rot=90, lit=True, pixelate=4)
# items grouped by hand (no evenly spaced rails): (asset, x offset from CL)
shelves = {640: [("firmalife:item/jar/red_grapes", 58), ("firmalife:item/jar/fig", 94),
                 ("minecraft:item/dragon_breath", 168), ("minecraft:item/glass_bottle", 226)],
           785: [("firstaid:item/bandage", 70), ("firstaid:item/morphine", 150), ("tfc:item/wool_cloth", 212)],
           930: [("tfc:item/ceramic/vessel", 62), ("firmalife:item/jar/honey", 132),
                 ("immersiveengineering:item/fluid_containers_bottle_ethanol", 166), ("firmalife:item/beeswax", 228)]}
for y, items in shelves.items():
    for a_, dx in items:
        sprite(a_, CL + dx, y - 11)
# lantern on the cabinet top
sprite("minecraft:item/lantern", CL + 196, CT - 11, glow=[255, 176, 100], glow_strength=1.1)
sprite("supplementaries:item/tattered_book", CL + 70, CT - 11)
sprite("minecraft:item/book", CL + 120, CT - 11)

# ---------------------------------------------------------------- centre: the sickbed (hero), raised on legs
BL = 548
bed = blocks(["H....", "HPBBB", "H...L"],
             {"H": ROSE, "L": ROSE, "P": "minecraft:block/white_wool", "B": "minecraft:block/red_wool"},
             0.45, BL, STAND, haze=0.32)
sprite("comforts:item/sleeping_bag_white", BL + 150, STAND - 6)

# bedside barrel with the lantern (main light)
SL = BL + 5 * 64 + 40
stool = blocks(["S"], {"S": {"front": "minecraft:block/barrel_side", "top": "minecraft:block/barrel_top",
                             "side": "minecraft:block/barrel_side"}}, 0.45, SL, STAND, haze=0.3)
sprite("minecraft:item/lantern", SL + 44, stool["row_front_top"](0) - 10, glow=[255, 176, 100], glow_strength=1.3)

# ---------------------------------------------------------------- right: apothecary work table
TL = 1092
tab = blocks(["TTT", "L.L"], {"T": ROSE, "L": ROSE}, 0.45, TL, STAND, haze=0.15)
ttop = tab["row_front_top"](0) - 8
sprite("minecraft:item/brewing_stand", TL + 44, ttop)
sprite("tfc:item/ceramic/bowl", TL + 100, ttop)
sprite("tfc:item/wool_cloth", TL + 150, ttop)
sprite("sewingkit:item/bone_sewing_needle", TL + 196, ttop)
sprite("tfc:item/ceramic/vessel", TL + 98, STAND - 4)

# wall shelves above the table
for y, items in ((470, [("minecraft:item/writable_book", 1124), ("firmalife:item/jar/white_grapes", 1196),
                        ("minecraft:item/glass_bottle", 1232), ("supplementaries:item/lumisene_bottle", 1300)]),
                 (640, [("minecraft:item/totem_of_undying", 1134), ("minecraft:item/glass_bottle", 1216),
                        ("firmalife:item/jar/fig", 1252), ("minecraft:item/honey_bottle", 1292)])):
    layer(motif="plank_shelf", x=fx(1210), y=fy(y), w=10.5, h=1.3, color=WOODC, alpha=1.0, lit=True, pixelate=4)
    for a_, x in items:
        sprite(a_, x, y - 11)

# ---------------------------------------------------------------- drying herbs hanging from the beam
BEAM_B = 226
for x, a, cord in ((212, "firmalife:item/spice/rosemary", 1.6), (300, "firmalife:item/spice/thyme", 3.0),
                   (392, "supplementaries:item/flax", 1.2), (470, "firmalife:item/spice/bay_leaves", 0.8),
                   (600, "firmalife:item/spice/oregano", 0.6), (700, "sanitydim:item/garland", 1.0),
                   (860, "firmalife:item/spice/basil_leaves", 0.7), (960, "firmalife:item/spice/rosemary", 0.6),
                   (1060, "firmalife:item/spice/thyme", 1.0), (1150, "supplementaries:item/flax", 2.2),
                   (1240, "firmalife:item/spice/bay_leaves", 1.2), (1322, "firmalife:item/spice/oregano", 2.6)):
    clen = cord * U
    layer(motif="hanging_cord", x=fx(x), y=fy(BEAM_B + clen / 2), w=0.6, h=round(cord + 0.2, 2),
          color=[150, 120, 90], alpha=1.0)
    sprite(a, x, BEAM_B + clen - 4, rot=180 if "garland" not in a else 0, shadow=0, drop=0.35)

spec = json.load(open("art_styles.d/health.json", encoding="utf-8"))
spec["scene"] = {
    "texel": K, "shadow": 0.5,
    "light": {"dir": [1, -0.45], "color": [255, 176, 120], "tint": 0.1, "rim": 0.5, "shade": 0.3},
    "lights": [{"x": 0.61, "y": 0.75, "radius": 0.34, "strength": 0.85, "color": [255, 160, 96]},
               {"x": 0.25, "y": 0.40, "radius": 0.22, "strength": 0.6, "color": [255, 170, 104]}],
    "ambient": 0.66,
    "haze_color": [30, 12, 18],
    "layers": L,
}
with open("art_styles.d/health.json", "w", encoding="utf-8") as f:
    f.write("{\n")
    keys = list(spec.keys())
    for i, k in enumerate(keys):
        if k == "scene":
            sc = spec[k]
            f.write(' "scene": {')
            f.write(", ".join(f'"{kk}": {json.dumps(vv, ensure_ascii=False)}' for kk, vv in sc.items() if kk != "layers"))
            f.write(', "layers": [\n')
            f.write(",\n".join("  " + json.dumps(ly, ensure_ascii=False) for ly in sc["layers"]))
            f.write("\n ]}")
        else:
            f.write(f' "{k}": {json.dumps(spec[k], ensure_ascii=False)}')
        f.write(",\n" if i < len(keys) - 1 else "\n")
    f.write("}\n")
print(len(L), "layers")
