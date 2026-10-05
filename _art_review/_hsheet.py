import sys; sys.path.insert(0, ".")
import sys, artlib
from PIL import Image, ImageDraw
names = sys.argv[2:]
S = 8; cols = 8
rows = (len(names)+cols-1)//cols
W = cols*(16*S+20); H = rows*(16*S+40)
sheet = Image.new("RGB", (W, H), (40, 24, 30))
d = ImageDraw.Draw(sheet)
for i, n in enumerate(names):
    x = (i%cols)*(16*S+20)+10; y = (i//cols)*(16*S+40)+5
    try:
        t = artlib.tex(n).convert("RGBA")
        t = t.crop((0,0,t.width,min(t.height,t.width)))
        t = t.resize((16*S, 16*S*t.height//t.width), Image.NEAREST)
        sheet.paste(t, (x, y), t)
    except Exception as e:
        d.text((x, y+40), "ERR", fill=(255,0,0))
    d.text((x, y+16*S+4), n.split(":")[1][-22:], fill=(230,230,230))
sheet.save(sys.argv[1])
