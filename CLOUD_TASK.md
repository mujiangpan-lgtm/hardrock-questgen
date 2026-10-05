# Cloud task: finish the quest-book art fixes (2026-10-05)

This repo is `questgen`, the generator of the FTB Quests book of a Minecraft 1.20.1 modpack
(HardRock TerraFirmaCraft 4). Each chapter has generated art: a tiled screen-space background, a
map-space scene illustration, a banner, section panels and node shapes. **Your job is only the art
specs.** The owner builds and deploys locally after pulling your branch.

## Setup (do this first)

```bash
pip install "pillow>=12" "numpy>=2"          # local versions: Pillow 12.3.0, numpy 2.3.5, Python 3.12
sudo apt-get install -y fonts-noto-cjk || true  # Chinese text in panels and banners
# Block and item textures from the pack's jars (encrypted; the key is in your task message,
# never write it to a file in the repo or commit it):
printf %s '<key from the task message>' > /tmp/packkey
openssl enc -d -aes-256-cbc -pbkdf2 -pass file:/tmp/packkey -in packdata.tar.gz.enc | tar xz
python build.py --check                           # must print: OK: 19 chapters, 435 quests
```

Without the jars, `artlib.py` reads `_packdata/textures/<ns>/<path>.png` (pixel-identical, checked).
Without Windows fonts, `build.py` uses Noto CJK. If no CJK font can be installed, say so in the
results: the art is still valid, but the previews will show boxes instead of Chinese text.

## Read before working

- `ART_GUIDE.md`: how the art works, spec format, all motifs, the composition rules. Read it fully,
  including the Round 5 section.
- `_art_review/renderer_changes.md`: renderer features added this round (`texel`, `light`, `shadow`,
  `lights`, `ambient`, `blocks`, sprite_row `pile`/`scatter`, `pixelate`, `light_rays`, ...).
- **Do not read `artlib.py` in full** (2600+ lines). Grep it for one motif if you really need to.
- `_art_review/critique_before_director.json` and `_art_review/critique_before_player.json`: two
  critics' scores and issues per chapter (baseline before the fixes).
- `_art_review/before/preview_screen29_<key>.png`: the baseline previews.
- `_art_review/fix_results_local.json`: 7 chapters already fixed locally, with what was changed and
  what is still weak (00_welcome, climate, food, health, farming, mekanism, steel_age). Do not redo them.

## Task A: fix these 10 chapters

| key | file stem | topic | baseline |
| --- | --- | --- | --- |
| copper_age | 11_copper | copper age | 5.75 (interrupted mid-fix, see below) |
| bronze_age | 12_bronze | bronze age | 6 |
| tfmg | 22_tfmg | TFMG: oil, refining, heavy industry | 6 |
| pneumatic | 23_pneumatic | PneumaticCraft | 6 |
| ie | 21_ie | Immersive Engineering | 6.25 |
| iron_age | 13_iron | iron age, bloomery | 6.5 |
| storage | 25_storage | storage and logistics, Refined Storage | 6.5 |
| explore | 31_explore | exploration and travel | 6.5 |
| stone_age | 10_stone_age | stone age | 6.75 |
| twilight | 32_twilight | Twilight Forest | 6.75 |

- Spec file: `art_styles.d/<key>.json`.
- `stone_age` is a pilot. Its spec is in `art_styles.py` `STYLES["stone_age"]`. Do NOT edit
  `art_styles.py`. Create `art_styles.d/stone_age.json` from that dict (json.dumps; tuples become
  lists). The JSON overrides the .py entry.
- `copper_age`: a fixer was killed mid-run. `art_styles.d/copper_age.json` has its partial edits;
  `_art_review/orig_copper_age.json` is the original. Preview both and continue from the better one.
- `iron_age`: `_art_review/p_iron.py` holds a promising experiment (texel 5, scene light, bloomery
  built with `blocks`, ingot pile). Start from it.

**Per chapter, use one subagent on model sonnet**, at most 3 in parallel. Each subagent:

1. Copies its spec to `_art_review/orig_<key>.json`. Skip this if that file already exists.
2. Fixes the critics' issues first, then raises the chapter as high on the rubric as it honestly can.
3. Loops at most 4 rounds:
   - edit the spec
   - `QGEN_STAGE=_stage_fix_<key> python build.py --stage --only 00_welcome,<stem>`
   - `QGEN_STAGE=_stage_fix_<key> QPREVIEW_SCREEN=29,55 python preview.py <stem>`
   - look at `_stage_fix_<key>/preview_screen29_<key>.png` (the player's real view) and compare
     with the baseline preview.
4. Saves the spec after every round that is an improvement. The file must always be valid JSON.
   If the result is not clearly better than the baseline, restore the original.
5. Edits only its own spec file. Puts any wishes for drawing code into its report; it does not
   change `artlib.py`.
6. Keeps its palette clearly distinct from the other chapters, and follows the ART_GUIDE rules:
   - visible fractions x 0.11-0.89 / y 0.12-0.88;
   - keep clear of panels and their header text;
   - solids opaque, atmosphere low;
   - no particle noise near panels;
   - one hero prop.
7. Uses the new tools where they fit:
   - one `texel` per scene;
   - `light`/`shadow`;
   - `blocks` instead of stacks of flat block faces;
   - `pile`/`scatter` instead of hotbar-like rows;
   - `pixelate` for vector props next to pixel sprites.
8. Reports what it changed, what still holds the chapter back, any drawing-code requests, and an
   honest self-score.

## Task B: blind final scoring of all 19 chapters

1. `QGEN_STAGE=_stage_final python build.py --stage` (all chapters; report WARN/ERROR lines).
2. `QGEN_STAGE=_stage_final QPREVIEW_SCREEN=29 python preview.py 00_welcome 01_climate 02_food 03_health 04_farming 25_storage 10_stone_age 11_copper 12_bronze 13_iron 14_steel 20_create 21_ie 22_tfmg 23_pneumatic 24_mekanism 31_explore 32_twilight 33_space`
3. Copy `_stage_final/preview_screen29_*.png` into `_art_review/after/`.
4. `python tools/contact.py _art_review/after 00_welcome,climate,food,health,farming,storage,stone_age,copper_age,bronze_age,iron_age,steel_age,create,ie,tfmg,pneumatic,mekanism,explore,twilight,space 4`
5. Two fresh subagents (model sonnet), each scoring every `_art_review/after/preview_screen29_<key>.png`
   with the rubric below, one per lens. They must not see the baseline scores. Each writes
   `_art_review/critique_after_<lens>.json` with: per chapter score, up to 4 issues,
   fix_type (spec|renderer|medium|mixed) and what_for_9; plus systemic issues and a ceiling estimate.
6. Write `_art_review/RESULTS.md`:
   - a before/after table (average of the two lenses per chapter; baseline from the before files);
   - what changed per chapter (yours plus `fix_results_local.json`);
   - remaining weak points;
   - drawing-code requests;
   - the critics' ceiling estimates.

The previews simulate the player's real view: 1460x1050 quest window at GUI scale 4, about 29 screen
px per quest unit, quest titles hidden, item icons inside the nodes.

**Lens director:** a senior game art director. Judges composition (balance, framing, focal point,
use of the whole view), cohesion and style consistency (pixel sprites vs smooth vector shapes,
consistent pixel density), lighting and depth, colour harmony, and whether elements look intentional
rather than clip-art.

**Lens player:** an experienced Minecraft modpack player and pack designer. Judges whether nodes,
lines and panel headers are easy to read over the art, whether the theme is recognisable at a glance,
whether it feels Minecraft/TFC-native, anything distracting, crude, oversized or empty, and whether
they would enjoy opening the chapter.

**Rubric** (absolute; use the full scale honestly, half points allowed, no curve, no inflation):

| score | meaning |
| --- | --- |
| 10 | professional hand-crafted game key art |
| 9 | as polished as the best custom quest-book or menu art in top commercial modpacks or indie games: one coherent style and light, real depth, every element intentional, nothing looks like a placeholder; a player would screenshot it |
| 8 | clearly good and cohesive; only minor nitpicks |
| 7 | good theme and composition, but some clumsy or placeholder-looking elements or style clashes |
| 6 | theme readable, but feels assembled from stickers; noticeable empty or cluttered areas |
| 5 | style clash, mostly empty or muddy |
| <=4 | harms readability or looks broken |

## Task C: deliver

- Commit the spec changes, `_art_review/after/`, the critique JSONs, `RESULTS.md` and any new
  `orig_*.json` to a new branch `art-fixes`, push it, and do not merge into main.
- Never commit `_packdata/`, the key, `/tmp/packkey` or the `_stage*` dirs (they are in .gitignore).

## Rules

- Never run `build.py` without `--stage` or `--check`.
- Do not edit `chapters/*.py`, `qlib.py`, `registry.json`, `build.py`, `preview.py` or `artlib.py`.
- Budget: this runs on prepaid cloud credits. Use sonnet for every subagent. Stop a chapter after
  4 rounds even if it is not perfect, and report.
