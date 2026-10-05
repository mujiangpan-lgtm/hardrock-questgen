"""Scratch harness for renderer experiments (not used by the build).

    QGEN_STAGE=_stage_try python _art_review/_try.py TAG 13_iron,01_climate [patches.py]

Renders the screen29 preview of the given chapter stems into _art_review/try/TAG_<key>.png,
optionally after applying in-memory spec patches (patches.py defines PATCH = {key: fn(spec)}).
Never writes outside the stage directory (forces --stage).
"""
import ast
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
os.environ.setdefault("QGEN_STAGE", "_stage_try")
tag, stems = sys.argv[1], sys.argv[2]
patch_file = sys.argv[3] if len(sys.argv) > 3 else None
sys.argv = ["build.py", "--stage", "--only", stems]
sys.path.insert(0, str(HERE))
import build  # noqa: E402

assert build.STAGE and "_stage" in str(build.TEX_DIR)
build.load_chapters()
if patch_file:
    ns = {}
    exec(Path(patch_file).read_text("utf-8"), ns)
    for k, fn in ns["PATCH"].items():
        if k in build.STYLES:
            fn(build.STYLES[k])
build.TEX_DIR.mkdir(parents=True, exist_ok=True)
build.write_backgrounds_and_theme(True)

src = (HERE / "preview.py").read_text("utf-8")
tree = ast.parse(src)
defs = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
pns = {"build": build, "TEX": build.TEX_DIR, "math": __import__("math")}
exec("from PIL import Image, ImageDraw\n", pns)
exec(compile(ast.Module(body=defs, type_ignores=[]), "preview_defs", "exec"), pns)
out = HERE / "_art_review" / "try"
out.mkdir(parents=True, exist_ok=True)
for ch in build.CHAPTERS.values():
    imgs = build.chapter_images(ch, write=True)
    p = out / f"{tag}_{ch.key}.png"
    pns["render_screen"](ch, imgs, 29).convert("RGB").save(p)
    print(p)
