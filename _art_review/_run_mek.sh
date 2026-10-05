#!/bin/sh
cd "D:/.minecraft/versions/HardRock TerraFirmaCraft 4 - realistic survival/questgen" || exit 1
PY=C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
$PY _art_review/_gen_mek.py || exit 1
QGEN_STAGE=_stage_fix_mekanism $PY build.py --stage --only 00_welcome,24_mekanism 2>&1 | tail -2
QGEN_STAGE=_stage_fix_mekanism QPREVIEW_SCREEN=29,55 $PY preview.py 24_mekanism 2>&1 | tail -2
