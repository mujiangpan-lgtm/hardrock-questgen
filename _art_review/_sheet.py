"""Render motifs standalone onto a dark sheet: python _sheet.py out.png"""
import sys, random
sys.path.insert(0, '.')
import artlib
from PIL import Image
items = [("anvil", 7.4, 3.4, (80, 76, 78), {}), ("anvil", 8, 3.6, (170, 130, 80), {}),
         ("tower", 5, 11, (104, 98, 114), {}), ("pumpjack", 18, 12, (84, 86, 78), {}),
         ("mine_entrance", 8, 8, (120, 86, 52), {}), ("livestock", 16, 6.8, (182, 152, 116), {}),
         ("tree", 3.6, 8.5, (50, 64, 62), {}), ("tree", 8, 9, (70, 120, 60), {})]
P = artlib.SCENE_PX
W = int(sum(w for _, w, _, _, _ in items) * P + 20 * len(items))
H = int(max(h for _, _, h, _, _ in items) * P + 20)
sheet = Image.new("RGBA", (W, H), (34, 30, 30, 255))
x = 10
for m, w, h, c, kw in items:
    im = artlib._DECOR[m](int(w * P), int(h * P), c, random.Random(m + "x"), **kw)
    sheet.alpha_composite(im, (x, H - 10 - im.size[1]))
    x += im.size[0] + 20
sheet.save(sys.argv[1])
