# Quest book art guide (chapter themes)

How the per-chapter art works and the rules learned from in-game checks and three critique rounds
(2026-10-05). Code: `artlib.py` (drawing), `build.py` (wiring), `preview.py` (previews).
Specs: `art_styles.py` (pilots: stone_age, create, space) and `art_styles.d/<chapter key>.json`
(one file per chapter, same structure, overrides art_styles.py). Chapters without a spec keep the
classic look.

## What the player sees

- **Screen-space background**: the chapter's tiled texture (FTB theme file, written by build.py to
  `kubejs/assets/ftbquests/ftb_quests_theme.txt`). It does not scroll or zoom, fills the whole quest
  window, and is also behind the quest-detail popup and the chapter list. The player uses GUI scale 4,
  so `tile_size: 12` (GUI px per block) = 48 screen px per block. Keep it dark and calm.
- **Map-space images** (scroll/zoom with the map, always below lines and quest nodes):
  scene (order -30) < decor (-20) < section panels (-10) < banner (-5).
- At the player's usual zoom (~29 screen px per quest unit) the 1460x1050 quest view shows ~50x36 units.
  The scene canvas is >= 64x48 units centred on the quests, so **visible scene fractions are about
  x 0.11-0.89, y 0.12-0.88**. The outer 12 % of the canvas dissolves into the background.
- Quest titles are NOT drawn on the map (hover only). So empty space around the panels is very visible:
  the scene must fill the view.

## Composition rules (from the critiques)

1. One **hero prop** per chapter that tells its story at a glance (stone age: campfire; Create: water
   wheel + windmill; space: rocket over a planet horizon).
2. **Frame left and right** with large themed masses at different heights; avoid mirror symmetry.
   Side bands: x 0.12-0.32 and 0.68-0.88 (check the panels' fractions; keep >= 0.02 clear of panels).
3. **Top band** (y 0.13-0.24, behind/around the banner): sky / ceiling element (sky_band, mountain_range,
   snowy_range, aurora, tree_line, overhead shaft ...).
4. **Bottom band** (y 0.70-0.87): ground / horizon element (strata_band, planet_horizon, wheat_field,
   belt, pipes, tree_line ...). Without it the lower third looks empty.
5. **Solid objects are opaque and shaded** (alpha 0.75-1.0); translucent solids look like ghosts.
   **Atmosphere** (soft_glow, nebula_glow, sky_band, blueprint, contour_map) stays low (alpha 0.15-0.45).
6. **No particle noise near panels**: embers / fireflies / snowfall / star_cluster / falling_leaves only in
   small boxes away from the panels, low density. Dots between nodes read as dirt.
7. Keep important objects inside 0.12-0.88 so the edge dissolve does not ghost them.
8. Typically 10-16 layers; layer order is draw order (back to front): glows/sky first, then far
   silhouettes, then props, then small accents.
9. Nothing may cross a panel's header text; big shapes under panels only if very faint.
   (Long titles on narrow panels no longer shrink to unreadable text: the renderer drops the diamonds and,
   if needed, sets "第N节" small above the name.)
10. One pixel density, one light: prefer scene `"texel"` + `"light"` + `"shadow"` (see below) over
   per-sprite glows; build block structures with `blocks`, not stacked block-face sprites; no evenly spaced
   sprite rows (use `pile`/`scatter` or place items where they belong).

## Spec structure (JSON or dict)

```
{
  "palette":    {"panel_fill": [r,g,b] (dark), "accent": [r,g,b] (bright), "glow": [r,g,b],
                 "text_key_hex": "#RRGGBB" (key terms in descriptions; luminance high)},
  "background": {"tiles": [{"asset": "ns:block/...", "weight": n}, ...], "target_brightness": 0.09-0.11,
                 "saturation": 0.5-0.7, "tint": [r,g,b] (multiplied), "contrast_sd": 0.008-0.022,
                 "overlay": {"type": none|speckle|starfield|strata|gear_ghosts|blueprint_grid|nebula,
                             "density": 0-1, "color": [r,g,b]}, "tile_size": 12},
  "banner":     {"ribbon_asset": "ns:block/..." (calm, no frames/grid), "icons_left": [3 item textures],
                 "icons_right": [3 item textures], "motif": mountains|strata|cogs|planet_rings|starfield|
                 nebula|flames|none, "motif_color": [r,g,b]},
  "decor":      [],
  "shapes":     {"normal": circle|rsquare|square, "milestone": pentagon|hexagon|octagon|heart,
                 "optional": "diamond", "gate": "gear"},
  "scene":      {"layers": [ {"motif": ..., "x": 0-1, "y": 0-1, "w": units, "h": units (optional),
                              "color": [r,g,b], "alpha": 0-1, "rot": degrees (optional)}, ... ]}
}
```

Textures are `namespace:path` under `assets/<ns>/textures/` of a jar in `mods/` or the version jar
(e.g. `tfc:block/rock/raw/granite`, `create:item/brass_ingot`). Tiles must be 16x16 and not animated;
avoid framed/casing textures as tiles (they look like quest nodes). Item textures for banner icons and
sprites must exist (`build.py --check` validates everything).

Book-wide conventions: gate = gear, optional = diamond. Palettes must differ clearly between chapters
(pilots: stone_age ember (220,150,100), create brass (232,184,86), space violet (176,150,255)).

## Scene motifs

Atmosphere: `soft_glow` (radial light), `sky_band` (horizontal band of light/haze), `nebula_glow`,
`aurora` (light curtains), `milky_way` (rotate it), `blueprint` (technical grid + gear outlines),
`contour_map` (topographic lines).
Landscape: `mountain_range` (3:1, bottom dissolves), `snowy_range` (snow-capped peaks), `strata_band` (4:1
rock layers), `tree_line` (forest silhouettes, give w and h), `wheat_field` (crop rows), `planet_horizon`
(curved planet limb with atmosphere, wide), `sun`, `moon`, `planet`, `ringed_planet` (w > h, e.g. 20x13).
Props: `campfire`, `water_wheel`, `windmill_sails`, `cog`, `gear_cluster`, `shaft` (wide, h ~1; rot 90 for
vertical), `belt` (wide conveyor, h ~3), `pipes`, `power_line` (pylons + cables, wide), `smokestack`,
`circuit`, `lightning` (tall), `rocket` (tall, plume down), `satellite` (wide), `castle`, `compass_rose`,
`arrowhead`, `hand_print`, `cave_painting`, `cave_painting_herd`, `heartbeat` (wide ECG trace),
`orbit_ring`.
More props (round 4): `anvil` / `anvil_hot` (side view ~2:1, hot = glowing workpiece and sparks),
`tree` (one complete tree; conifer if h > 1.6 w, else broadleaf), `tower` (tall, lit windows),
`pumpjack` (~1.5:1), `plank_shelf` (wide, h ~1), `hanging_cord` (tall, thin), `livestock` (cows, sheep,
chicken on a ground line, ~2.6:1), `mine_entrance` (timber portal, ~1:1).
Particles (sparingly): `embers`, `fireflies`, `snowfall`, `falling_leaves`, `star_cluster`.
Real game art: `{"motif": "sprite", "asset": "ns:item/...", "w": units, "glow": [r,g,b] optional}` and
`{"motif": "sprite_row", "assets": [...], "w": units, "h": units}` - pixel-scaled textures; great for
iconic props (anvil, furnace, crops, barrels) and the most Minecraft-native look.

Round 5 (renderer, 2026-10-05; details and examples in `_art_review/renderer_changes.md`):
- Redrawn with volume (same boxes as before): `anvil`, `tower` (masonry, arched lit windows, slate roof),
  `pumpjack` (horse head, bridle, crank, counterweight), `mine_entrance` (tunnel depth, rails, lantern),
  `livestock` (shaded cows with patches, woolly sheep, chicken, grass), `water_wheel` (Create paddle wheel,
  splash, channel), `belt` (solid rubber band, frame, legs), `pipes` (gate valves with handwheels instead
  of red rings), `sun` (bloom + corona, no clip-art rays; `"rays": true` = old look).
- `lightning`: forked, white-hot core, glow. Params `"width"` (1 bold, 0.5 thin, 1.6 heavy),
  `"branches"` (0-1.5), `"flash"` (0-1, lit cloud base at the top). Keep the box >= 4 x 10 units.
- `heartbeat`: `"width"` (0.4 = faint ambient trace).
- New `light_rays`: soft shafts from a light source. `{"motif": "light_rays", "x": .35, "y": .4, "w": 40,
  "h": 30, "color": [230,220,170], "alpha": 0.35, "src": [0.05, 0.02], "angle": 50, "spread": 30,
  "count": 6}` (src = source inside the box as fractions, angle 0 = right / 90 = down). Atmosphere: alpha <= 0.4.
- New `blocks`: a structure of real block textures in an oblique front/top/side view on one texel grid -
  use it instead of stacks of flat block-face sprites (bloomery, blast furnace, coke oven, casing walls,
  machine banks): `{"motif": "blocks", "x": .8, "y": .6, "w": 6, "h": 22, "k": 5, "rows": ["G","G","B"],
  "legend": {"G": "tfc:block/rock/bricks/gabbro", "B": {"front": "tfc:block/devices/bloomery/on",
  "top": "...", "side": "..."}}, "depth": 0.45}`. Rows = front elevation, top row first, " " or "." = empty.
- `sprite_row` `"arrange"`: `row` (default, an even rail = reads as a hotbar), `scatter` (irregular gaps,
  heights, mirrored items), `pile` (a heap). Prefer pile/scatter or single sprites in context.
- Sprite `"glow"` is now a soft pool of emitted light (no outline halo); `"glow_strength"` 0.5-1.5.
- Sprite `"flip": true` mirrors it.

### Scene-wide light and pixel density (optional scene keys, next to "layers")

- `"texel": 5` - every sprite / sprite_row / blocks layer at exactly 5 canvas px per texture pixel (one
  pixel density, ~6 screen px per texel; 4-6 recommended). The layer's `w` no longer sets the size; a
  layer `"k"` overrides. Without `texel`, `"k_max"` caps the fitted scale (default 10).
- `"light": {"dir": [dx, dy] (towards the light, y down) or degrees, "color": [r,g,b], "tint": 0.1,
  "rim": 0.6, "shade": 0.3}` - pixel layers (and vector layers with `"lit": true`) take the scene light:
  tint toward its colour, brighter on the lit side, one-texel rim light on edges facing it. Layer
  `"tint"/"rim"/"shade"` override; `"unlit": true` opts out.
- `"shadow": 0.5` - contact shadow under every sprite / sprite_row / blocks layer (layer `"shadow": 0`
  for hanging things); layer `"drop": 0.5` = drop shadow on the wall behind, cast away from the light.
- `"lights": [{"x": .8, "y": .72, "radius": .3, "strength": .8, "color": [255,140,70]}]` + `"ambient": 0.85`
  - cast light: props near a fire/lamp get brighter and warmer, the rest dims. Pair each light with a
  soft_glow layer for the visible glow.
- `"pixelate": 4` (or per layer) - vector props redrawn on a 4-px texel grid to match the sprites;
  backdrops (mountains, tree_line, strata, planets) and atmosphere stay smooth unless the layer itself
  sets `"pixelate"`. `"colors": 12` palette reduction, `"outline": 0.8` dark one-texel outline.
- Layer `"haze": 0.3` (+ scene or layer `"haze_color"`) pushes a layer back into the distance.

## Verify (always look at the screen previews)

```
PY=C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
QGEN_STAGE=_stage_mine QPREVIEW_SCREEN=29,55 $PY questgen/build.py --stage --only 00_welcome,<stem>
QGEN_STAGE=_stage_mine QPREVIEW_SCREEN=29,55 $PY questgen/preview.py <stem>
# -> questgen/_stage_mine/preview_screen29_<key>.png (player's zoom) and preview_screen55_<key>.png
```

`preview_screen29` simulates the real view (GUI scale 4, background tile at true size, item icons in
nodes, no titles). Judge the design there, not in the tight `preview_<key>.png`.
