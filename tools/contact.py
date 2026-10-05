"""Contact sheet of all chapters' screen29 previews (for a whole-book coherence check)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

stage = Path(sys.argv[1])
keys = sys.argv[2].split(",")
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 4
tw, th = 438, 315
sheet = Image.new("RGB", (cols * (tw + 8) + 8, ((len(keys) + cols - 1) // cols) * (th + 30) + 8), (12, 12, 14))
def _font():
    for p in ["C:/Windows/Fonts/msyh.ttc", *sorted(str(x) for d in ("/usr/share/fonts", str(Path.home() / ".fonts"))
                                                  for x in Path(d).rglob("NotoSansCJK-Regular.ttc"))]:
        if Path(p).exists():
            return ImageFont.truetype(p, 18)
    return ImageFont.load_default()


f = _font()
d = ImageDraw.Draw(sheet)
for i, k in enumerate(keys):
    p = stage / f"preview_screen29_{k}.png"
    x, y = 8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 30)
    if p.exists():
        sheet.paste(Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y + 24))
    d.text((x, y), k, font=f, fill=(230, 230, 230))
out = stage / "contact_sheet.png"
sheet.save(out)
print(out)
