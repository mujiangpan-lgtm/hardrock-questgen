import sys
sys.path.insert(0, '.')
import artlib
import numpy as np
from PIL import Image, ImageDraw
names = """mekanism:liquid/energy mekanism:liquid/liquid mekanism:liquid/heat mekanism:liquid/steam mekanism:block/teleporter_portal mekanism:block/teleporter mekanism:block/structural_glass mekanism:block/glass mekanismgenerators:item/turbine_blade mekanism:item/ingot_osmium mekanism:item/alloy_infused mekanism:item/alloy_reinforced mekanism:item/alloy_atomic mekanism:item/basic_control_circuit mekanism:item/elite_control_circuit mekanism:item/ultimate_control_circuit mekanism:item/energy_tablet mekanism:item/teleportation_core mekanism:item/pellet_antimatter mekanism:item/qio_drive_supermassive mekanism:item/mekasuit_helmet mekanism:item/portable_teleporter mekanism:item/crystal_osmium mekanism:item/upgrade_speed mekanism:item/raw_osmium mekanism:item/hdpe_sheet mekanism:item/enriched_redstone mekanism:item/configurator mekanism:item/atomic_disassembler mekanism:item/jetpack mekanism:block/block_refined_glowstone mekanism:block/induction_provider_glow""".split()
S=96
cols=8
rows=(len(names)+cols-1)//cols
img=Image.new('RGB',(cols*(S+10),rows*(S+24)),(60,60,60))
d=ImageDraw.Draw(img)
for i,n in enumerate(names):
    try:
        t=artlib.tex(n)
    except Exception as e:
        print(n,e); continue
    a=np.asarray(t)[...,3]
    print(n, t.size, 'alpha min/max/mean', a.min(), a.max(), int(a.mean()))
    t=t.convert('RGBA').resize((S,S),Image.NEAREST)
    x=(i%cols)*(S+10); y=(i//cols)*(S+24)
    img.paste(t,(x,y),t)
    d.text((x,y+S+2),n.split('/')[-1][:16],fill=(220,220,220))
img.save('_art_review/try/mek_sheet2.png')
