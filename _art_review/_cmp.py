"""Side-by-side before|after at half scale: python _cmp.py key [afterdir] [scale] [crop x0,y0,x1,y1]"""
import sys
from PIL import Image
key = sys.argv[1]
after = sys.argv[2] if len(sys.argv) > 2 else "_stage_render"
sc = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
crop = [int(v) for v in sys.argv[4].split(",")] if len(sys.argv) > 4 else None
a = Image.open(f"_art_review/base/preview_screen29_{key}.png")
bp = f"{after}/preview_screen29_{key}.png" if not after.endswith(".png") else after
b = Image.open(bp)
if crop:
    a, b = a.crop(crop), b.crop(crop)
w, h = int(a.size[0] * sc), int(a.size[1] * sc)
c = Image.new("RGB", (w * 2 + 6, h), (255, 0, 255))
c.paste(a.resize((w, h), Image.LANCZOS), (0, 0))
c.paste(b.resize((w, h), Image.LANCZOS), (w + 6, 0))
c.save(f"_art_review/try/cmp_{key}.png")
