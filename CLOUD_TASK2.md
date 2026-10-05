# Cloud task 2: redo the create and space chapter art (2026-10-05)

Round 1 (`CLOUD_TASK.md`, results in `_art_review/RESULTS.md`) moved 17 chapters to one look:
- pixel art at one texel size;
- scene light;
- block dioramas built from real textures.

The owner checked it in game and likes it. Two pilot chapters were never redone: **create** (`20_create`)
and **space** (`33_space`). They still use the old smooth vector gears, planets and rocket. In game they
now look ugly next to the rest, and the blind critics agree (create 6.5, space 6.75; issues are in
`_art_review/critique_after_director.json` and `_art_review/critique_after_player.json`).
**Redo both in the book's current language.**

## Setup

Same as `CLOUD_TASK.md`: pip, fonts-noto-cjk, decrypt `packdata.tar.gz.enc` with the key from your task
message (it was re-encrypted with the same key, and now also contains `<ns>:environment/...` sky
textures), then run `python build.py --check`.

## Read first

1. `ART_GUIDE.md`, including the Round 5 section.
2. `_art_review/renderer_changes.md`.
3. The two after-critiques for create/space.
4. Look at `_art_review/after/contact_sheet.png`. It is the target look: the strongest chapters are
   pneumatic, storage, iron_age, ie, stone_age, twilight and food. Read a couple of their specs in
   `art_styles.d/` to see how they use `texel`, `light`, `shadow`, `lights`, `ambient`, `blocks`,
   `pile`/`scatter` and `pixelate`.

Do not read `artlib.py` in full; grep it.

## Material that exists (in `_packdata/textures`, also in the local jars)

- **Create**:
  - `create:block/` cogwheel, large_cogwheel, cogwheel_axis, axis, axis_top, gearbox, gearbox_top,
    brass_gearbox, andesite_casing, brass_casing, copper_casing, andesite_encased_cogwheel_side,
    brass_encased_cogwheel_side, waterwheel_metal, flywheel, belt, belt_offset, conveyor_casing,
    millstone, mechanical_press_side/head/pole/top, mixer_base_side, mixer_head, fan_casing,
    fan_blades, mechanical_arm, crushing_wheel_plates, `sail/...`, `belt/...`.
  - `create:item/` (brass_ingot, precision_mechanism, andesite_alloy, ...).
  - Several of these are model-face textures. Preview them before relying on one: a flat face may
    not read as a gear.
- **Space**:
  - `ad_astra:environment/` sun, blue_sun, red_sun, earth, mars, moon, mercury, deimos, phobos,
    glacio and more. These are the game's own pixel planets and suns.
  - `minecraft:environment/sun` and `moon_phases` (an atlas: crop one phase with a small artlib helper
    if needed).
  - `ad_astra:block/` launch_pad, steel_block, steel_plating, steel_panel, steel_pillar(_top),
    glowing_steel_pillar, iron_panel, desh/ostrum/calorite_panel, solar_panel, oxygen_distributor,
    oxygen_loader_front(_on), steel_factory_block.
  - `ad_astra:item/` rocket_nose_cone, rocket_fin, space_suit, jet_suit.

## What to do

- Both chapters are pilots: their specs are in `art_styles.py` `STYLES["create"]` / `STYLES["space"]`.
  Do NOT edit `art_styles.py`. Create `art_styles.d/create.json` and `art_styles.d/space.json` from
  those dicts (json.dumps; tuples become lists) and edit those.
- Keep each chapter's identity colours: create brass (232,184,86) / space violet (176,150,255).
  Adjust them slightly if needed.
- Replace the smooth vector props with pixel-art ones at one texel size, lit by one scene light.
- Ideas, not requirements:
  - **create:** a working contraption diorama built with `blocks`: a water wheel or windmill driving
    shafts and gearboxes, a belt carrying items into a press over a basin, brass/andesite casing
    walls. A hero contraption under or beside the panels, steam, warm workshop light.
  - **space:** a launch pad with a pixel rocket (blocks/steel + nose cone/fins) and a gantry.
    The game's own pixel planets and sun in the sky; optionally a lunar/martian surface strip at the
    bottom, starfield background kept.
- **Drawing code may be extended this time**, if a pixel prop cannot be made from textures. Allowed:
  new motifs or new optional keys in `artlib.py` only, with no change to any existing default.
  Proof required:
  1. Before your first artlib edit, run `QGEN_STAGE=_stage_ref python build.py --stage` and
     `QGEN_STAGE=_stage_ref QPREVIEW_SCREEN=29 python preview.py <all stems>`.
  2. At the end, repeat both into `_stage_final`.
  3. The 17 other chapters' screen29 previews must be pixel-identical to `_stage_ref`.
  Document new motifs/keys in ART_GUIDE.md.
- Loop per chapter with screen previews (see `CLOUD_TASK.md`), at most 6 builds per chapter. Save the
  spec after every improvement. Use sonnet subagents, one per chapter, both in parallel; or do it
  yourself.

## Scoring and delivery

1. Final full stage build plus screen29 previews of all 19 chapters into `_stage_final`.
2. Copy the create/space previews into `_art_review/after2/`, and remake the contact sheet of all 19
   into `_art_review/after2/contact_sheet.png`:
   ```
   python tools/contact.py _stage_final <keys> 4
   ```
   then copy the result.
3. Two fresh sonnet critics (director and player lenses, same rubric as `CLOUD_TASK.md`), blind to the
   earlier scores, score **create and space**. They also judge whether the two now fit the contact
   sheet. Each writes `_art_review/critique_after2_<lens>.json`.
4. Append a "Round 2 (create/space)" section to `_art_review/RESULTS.md` covering:
   - scores before → after;
   - what changed;
   - artlib additions;
   - remaining weak points.
5. Commit to a new branch `art-fixes-2` (from main) and push. Do not merge.

Budget: prepaid cloud credits, about $63 left. Aim to spend under $20.

Rules, as before:
- Never run `build.py` without `--stage` or `--check`.
- Do not edit `chapters/*.py`, `qlib.py`, `registry.json`, `build.py` or `preview.py`.
- Never commit `_packdata/` or the key.
