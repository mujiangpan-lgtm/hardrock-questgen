"""Scratch generator for art_styles.d/mekanism.json (Mekanism power hall: induction matrix with glowing
energy behind structural glass, industrial turbine with blades behind glass, machine bank, cables, truss).
Places everything in canvas pixels on one texel grid (k=4) and writes fractions.
Canvas for this chapter: 64 x 50.95 units -> 1536 x 1222 px (24 px/unit).
Usage: python _art_review/_gen_mek.py   (writes art_styles.d/mekanism.json)"""
import json
import sys

sys.path.insert(0, ".")
import artlib  # noqa: E402

K = 4
W, H = 1536, 1222
CELL = 16
U = 24
L = []


def fx(px): return round(px / W, 5)
def fy(py): return round(py / H, 5)


def layer(**kw):
    L.append(kw)
    return kw


def blocks(rows, legend, left, bottom, depth=0.45, **kw):
    """left = x of the front-face left edge, bottom = y of the front-face bottom (canvas px)."""
    d = max(1, int(round(CELL * depth)))
    nr, nc = len(rows), max(len(r) for r in rows)
    Wt, Ht = nc * CELL + d, nr * CELL + d
    cx, cy = left + Wt * K / 2, bottom - Ht * K / 2
    ly = {"motif": "blocks", "x": fx(cx), "y": fy(cy), "w": round(Wt * K / U + 0.5, 1),
          "h": round(Ht * K / U + 0.5, 1), "rows": rows, "legend": legend, "depth": depth}
    ly.update(kw)
    L.append(ly)
    top = bottom - Ht * K
    return {"top": top, "d": d, "left": left, "right": left + Wt * K,
            "cell": lambda r, c: (left + (c * CELL + CELL / 2) * K, top + (d + r * CELL + CELL / 2) * K)}


def sprite(asset, cx, cy, **kw):
    t = artlib.tex(asset)
    ly = {"motif": "sprite", "asset": asset, "x": fx(cx), "y": fy(cy), "w": round(t.size[0] * K / U, 2),
          "alpha": 1.0}
    ly.update(kw)
    L.append(ly)


def cable(x0, y0, x1, y1, color, h=1.1, **kw):
    """Straight cable (shaft) between two canvas points (horizontal or vertical)."""
    if abs(y1 - y0) > abs(x1 - x0):
        layer(motif="shaft", x=fx(x0), y=fy((y0 + y1) / 2), w=round(abs(y1 - y0) / U, 2), h=h, color=color,
              alpha=1.0, rot=90, pixelate=4, lit=True, **kw)
    else:
        layer(motif="shaft", x=fx((x0 + x1) / 2), y=fy(y0), w=round(abs(x1 - x0) / U, 2), h=h, color=color,
              alpha=1.0, pixelate=4, lit=True, **kw)


MEK = "mekanism:block/"
GEN = "mekanismgenerators:block/"
DARK = "minecraft:block/black_concrete"
FLOOR = 1000
CABLE = [64, 156, 98]
HAZE = [16, 30, 24]

# ------------------------------------------------------------------ atmosphere
layer(motif="soft_glow", x=0.5, y=0.6, w=62, h=40, color=[60, 190, 110], alpha=0.12)

# ------------------------------------------------------------------ geometry first (needed by the cables)
ML, MB = 205, FLOOR                      # induction matrix: 4 x 7
TL, TB = 1110, FLOOR - 22                # industrial turbine: 3 x 10, stands further back
BL, BB = 626, FLOOR                      # machine bank 4 x 2
TRUSS_B = 250

m_rows = ["CCCC", "CGGC", "PGGC", "CGGC", "CGGP", "CGGC", "CCCC"]
t_rows = ["TTT", "TVT", "TVT", "TTT", "TGT", "TGT", "TGT", "TGT", "TTT", "TLT"]
m_top = MB - (len(m_rows) * CELL + 7) * K
t_top = TB - (len(t_rows) * CELL + 7) * K

# ------------------------------------------------------------------ ceiling truss + cables
blocks(["S" * 26], {"S": MEK + "steel_casing"}, -70, TRUSS_B, depth=0.3, shadow=0, drop=0.5, haze=0.62)
layer(motif="light_rays", x=fx(470), y=fy(640), w=28, h=32, color=[190, 255, 215], alpha=0.38, src=[0.2, 0.0],
      angle=72, spread=24, count=5)
mcx = ML + 2 * CELL * K + 14             # centre of the matrix top face
tcx = TL + 1.5 * CELL * K + 14
cable(mcx, TRUSS_B - 20, mcx, m_top + 16, CABLE)
cable(mcx - 60, TRUSS_B - 20, mcx - 60, m_top + 20, [70, 84, 80], h=0.8)
cable(tcx, TRUSS_B - 20, tcx, t_top + 16, CABLE)
# steel floor plate (top face = the floor the machines stand on)
blocks(["F" * 26], {"F": "tfc:block/metal/smooth/steel"}, -70, FLOOR + 12 + 64, depth=1.0, shadow=0, haze=0.5)
cable(ML + 250, FLOOR - 30, TL + 60, FLOOR - 30, CABLE)

# ------------------------------------------------------------------ right: industrial turbine (behind)
tz = dict(haze=0.3)
blocks(t_rows, {c: DARK for c in "TVGL"}, TL, TB, shadow=0, rim=0, **tz)
t = {"cell": lambda r, c: (TL + (c * CELL + CELL / 2) * K, t_top + (7 + r * CELL + CELL / 2) * K)}
x_rot = t["cell"](4, 1)[0]
y0, y1 = t_top + (7 + 4 * CELL) * K, t_top + (7 + 8 * CELL) * K
cable(x_rot, y0, x_rot, y1, [150, 160, 162], h=0.9, **tz)
for r in (4, 5, 6, 7):
    cx, cy = t["cell"](r, 1)
    sprite("mekanismgenerators:item/turbine_blade", cx, cy, shadow=0, rim=0, **tz)
blocks(t_rows, {"T": GEN + "turbine_casing", "V": GEN + "turbine_vent", "G": MEK + "structural_glass",
                "L": GEN + "turbine_valve"}, TL, TB, **tz)

# ------------------------------------------------------------------ left: induction matrix (hero)
blocks(m_rows, {c: DARK for c in "CGP"}, ML, MB, shadow=0, rim=0)
blocks(["....", "....", "EEEE", "EEEE", "EEEE", "EEEE", "EEEE"], {"E": "mekanism:liquid/energy"}, ML, MB,
       shadow=0, rim=0)
PORT = {"front": MEK + "induction_port", "top": MEK + "induction_casing", "side": MEK + "induction_casing"}
blocks(m_rows, {"C": MEK + "induction_casing", "G": MEK + "structural_glass", "P": PORT}, ML, MB, haze=0.3)
win_x, win_y = ML + 2 * CELL * K, m_top + (7 + 3 * CELL + CELL / 2) * K
layer(motif="soft_glow", x=fx(win_x), y=fy(win_y), w=13, h=18, color=[90, 255, 140], alpha=0.3)
layer(motif="soft_glow", x=fx(win_x + 20), y=fy(MB + 6), w=18, h=4, color=[90, 255, 140], alpha=0.22)

# ------------------------------------------------------------------ centre: machine bank
mach = ["enrichment_chamber", "crusher", "osmium_compressor", "combiner",
        "energized_smelter", "purification_chamber", "chemical_injection_chamber", "precision_sawmill"]
tops = {"enrichment_chamber": "top", "crusher": "top", "osmium_compressor": "top_active", "combiner": "top"}
sides = {"combiner": "right", "precision_sawmill": "right_active"}
leg = {}
for ch, m in zip("abcdefgh", mach):
    e = {"front": MEK + m + "/front_active"}
    if m in tops:
        e["top"] = MEK + m + "/" + tops[m]
    if m in sides:
        e["side"] = MEK + m + "/" + sides[m]
    leg[ch] = e
blocks(["abcd", "efgh"], leg, BL, BB)
layer(motif="soft_glow", x=fx(BL + 142), y=fy(BB - 4), w=18, h=4, color=[120, 255, 170], alpha=0.2)
# stock pile in front of the turbine base (overlaps it: depth)
layer(motif="sprite_row", assets=["mekanism:item/ingot_osmium", "mekanism:item/alloy_infused", "mekanism:item/ingot_osmium",
      "mekanism:item/ingot_steel", "mekanism:item/alloy_reinforced", "mekanism:item/ingot_osmium"],
      x=fx(1085), y=fy(FLOOR - 67 + 4), w=7, h=6, arrange="pile", alpha=1.0)

# ------------------------------------------------------------------ write
spec = json.load(open("_art_review/orig_mekanism.json", encoding="utf-8"))
spec["background"]["overlay"] = {"type": "blueprint_grid", "density": 0.0, "color": [50, 110, 70]}
spec["scene"] = {
    "texel": K, "shadow": 0.55,
    "light": {"dir": [-0.5, -1], "color": [205, 255, 220], "tint": 0.08, "rim": 0.4, "shade": 0.3,
              "haze_color": HAZE},
    "lights": [{"x": fx(win_x), "y": fy(win_y), "radius": 0.15, "strength": 0.7, "color": [110, 255, 150]},
               {"x": fx(BL + 142), "y": fy(BB - 70), "radius": 0.14, "strength": 0.45, "color": [140, 255, 180]}],
    "ambient": 0.68,
    "haze_color": HAZE,
    "layers": L,
}
with open("art_styles.d/mekanism.json", "w", encoding="utf-8") as f:
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
