#!/bin/sh
# full staged build + screen29 previews + diff vs baseline
cd "D:/.minecraft/versions/HardRock TerraFirmaCraft 4 - realistic survival/questgen"
PY=C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
QGEN_STAGE=_stage_render $PY build.py --stage 2>&1 | tail -3
STEMS=$(ls chapters/*.py | xargs -n1 basename | sed 's/\.py$//' | tr '\n' ' ')
QGEN_STAGE=_stage_render QPREVIEW_SCREEN=29 $PY preview.py $STEMS > /dev/null 2>&1 || echo PREVIEW FAILED
$PY -c "
from PIL import Image; import numpy as np, glob, os
for f in sorted(glob.glob('_art_review/base/*.png')):
    g='_stage_render/'+os.path.basename(f)
    a=np.asarray(Image.open(f).convert('RGB'),np.float32); b=np.asarray(Image.open(g).convert('RGB'),np.float32)
    dd=float(np.abs(a-b).mean())
    if dd>0: print('changed', os.path.basename(f)[17:-4], round(dd,3))
"
