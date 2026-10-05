import sys
sys.path.insert(0, '.')
import artlib
from PIL import Image, ImageDraw
names = """mekanism:block/induction_casing mekanism:block/induction_port mekanism:block/structural_glass mekanism:block/dynamic_tank mekanism:block/dynamic_valve mekanism:block/steel_casing mekanism:block/sps_casing mekanism:block/sps_port mekanism:block/thermal_evaporation_block mekanism:block/boiler_casing mekanism:block/superheating_element_on mekanism:block/basic_induction_cell mekanism:block/elite_induction_cell mekanism:block/ultimate_induction_cell mekanism:block/ultimate_induction_provider mekanism:block/induction_cell_glow mekanism:block/block_osmium mekanism:block/block_steel mekanism:block/qio_drive_array/front mekanism:block/qio_drive_array/side mekanism:block/teleporter_frame mekanism:block/teleporter_portal mekanism:block/glass mekanism:block/thermal_evaporation_controller mekanismgenerators:block/reactor_frame mekanismgenerators:block/reactor_glass mekanismgenerators:block/reactor_controller_on mekanismgenerators:block/reactor_port mekanismgenerators:block/turbine_casing mekanismgenerators:block/turbine_vent mekanismgenerators:block/turbine_valve mekanismgenerators:block/turbine_rotor mekanismgenerators:block/electromagnetic_coil mekanismgenerators:block/fission_reactor_casing mekanismgenerators:block/laser_focus_matrix mekanismgenerators:block/rotational_complex_side mekanismgenerators:block/saturating_condenser mekanism:block/factory/smelting/smelting_factory_front_active mekanism:block/factory/infusing/infusing_factory_front_active mekanism:block/purification_chamber/front_active mekanism:block/enrichment_chamber/front_active mekanism:block/precision_sawmill/front_active mekanism:block/factory/factory_front_back mekanism:block/crusher/side_active mekanism:block/osmium_compressor/left_active mekanism:block/chemical_injection_chamber/left_active mekanism:block/energized_smelter/side mekanism:block/combiner/left""".split()
S=96
cols=8
rows=(len(names)+cols-1)//cols
img=Image.new('RGB',(cols*(S+10),rows*(S+24)),(30,30,30))
d=ImageDraw.Draw(img)
for i,n in enumerate(names):
    try:
        t=artlib.tex(n)
    except Exception as e:
        print(n,e); continue
    if t is None: print('none',n); continue
    t=t.convert('RGBA').resize((S,S),Image.NEAREST)
    x=(i%cols)*(S+10); y=(i//cols)*(S+24)
    img.paste(t,(x,y),t)
    d.text((x,y+S+2),n.split('/')[-1][:16],fill=(220,220,220))
img.save('_art_review/try/mek_sheet.png')
