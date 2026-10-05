# Quest book art guide (chapter themes)

How the per-chapter art works and the rules learned from in-game checks and three critique rounds
(2026-10-05). Code: `artlib.py` (drawing), `build.py` (wiring), `preview.py` (previews).
Specs: `art_styles.py` (pilots: stone_age, create, space) and `art_styles.d/<chapter key>.json`
(one file per chapter, same structure, overrides art_styles.py). Chapters without a spec keep the
classic look. Since round 6 all 19 chapters have a JSON spec (the three pilots too), so the art_styles.py
entries are only fallbacks.

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

### Round 6: pixel motifs for create and space (2026-10-05, additive only)

New motifs in `artlib.py` (two blocks directly above `DECOR_MOTIFS`, plus one `PIXEL_MOTIFS.update` after
`BACKDROP`). No existing code, default or motif output changed: the other 17 chapters render pixel-identical.
All draw on a texel grid: give each layer `"k"` = the scene `texel`, and use square boxes that are multiples
of k where noted. Prefer them over the old smooth `cog`, `gear_cluster`, `water_wheel`, `windmill_sails`,
`belt`, `planet`, `ringed_planet`, `moon`, `rocket`, `satellite` next to pixel art.

**Create parts** (`create_*`; in `PIXEL_MOTIFS`, so they take scene `light`, contact `shadow`, `drop`, `haze`
like sprites; wall-mounted parts: `"shadow": 0, "drop": 0.45-0.6`). Face-on round parts: `w == h`, multiple of
k; centre at `((w/k - depth)/2)*k` px from the top-left; `depth` = dark extruded side in texels (default 2).
- `create_cog`: Create cogwheel (spruce-plank teeth ring, andesite hub, axle). `teeth` 12, `phase` 0 (0..1 of
  a tooth pitch; mesh neighbours with phase1 = (0.25 - a*n1/2pi) % 1, phase2 = (0.75 - (a+pi)*n2/2pi) % 1 for the
  angle a between centres), `hub` (118,122,118), `holes` 0 (window holes), `hole_w` 0.28, `metal` false
  (true = flat metal `color` with grain; brass cogs), `depth` 2. `color` = wood tint (default (112,82,46)).
  `teeth: 0, phase: 0.25` = a plain disc (axle cap plate).
- `create_wheel`: water wheel with boarded rim, spokes, hub and hooked paddles; `blades` 12, `spokes` 8,
  `phase`, `hub` (92,94,92), `ring` false, `paddles` true (false = flywheel), `lip` true, `metal` false,
  `rim` 0.1 (rim thickness / radius - NOTE: the scene light also reads layer `rim` as rim-light strength),
  `spoke_w` 0.058. Flywheel: `"paddles": false, "metal": true, "rim": 0.17, "spoke_w": 0.1, "spokes": 6`.
- `create_sails`: windmill arms (stripped spruce) with canvas sails (`color` = cloth, e.g. (206,186,146)),
  battens and rails; `arms` 4, `ang` 20 (rotation in degrees - not `rot`, which would rotate the image
  again), `hub_r` 0.2 (centre left clear for a `blocks` windmill bearing on top).
- `create_shaft`: horizontal shaft (`"rot": 90` = vertical, exact); `thick` 5 texels, collar every `joints`
  16 texels, `depth` 1; `color` andesite (118,124,120) or copper (186,104,74). h ~ (thick+3)*k.
- `create_belt`: mechanical belt from the side (rubber loop with tread ticks, andesite plate, pulleys,
  `legs` 3); `thick` 10 (12 suits 16 px item sprites at texel 4), `scroll` 0. Put items on top as sprites.
- `create_water`: pixel pool (`pool` fraction of the box, rippled surface, foam, depth) and optional waterfall
  (`fall` x fraction, `fall_w` 7); `foam` 1|2, `splash` [x fractions] (needs `pool` < 1). Draw an opaque pool
  behind a wheel and the same box at alpha ~0.4 in front to tint the submerged part.
- `create_steam`: soft translucent steam puffs (`puffs` 8, `drift` 0.3). Superseded by `create_smoke`.
- `create_smoke`: hard-edged 3-tone pixel smoke puffs rising from the box bottom (`puffs` 4, `drift`
  -0.5..1); put the box bottom on the chimney top; `"shadow": 0, "unlit": true`.
- `create_station`: Create machine on an iron gantry in the `blocks` oblique view. `kind` "press" (andesite
  casing, brass-banded pole, iron head over a belt passing between the posts) or "mixer" (brass casing,
  whisk into an andesite basin of molten brass); `d` 5, `post` 5, `pole` 6, `head` 9, `basin_h` 12.
  W = (span + d)*k with span ~26 (press) / 28-32 (mixer); posts reach the image bottom.
- `create_boiler`: copper steam boiler (riveted tank, brass bands, dome with rod, flared chimney, gauge,
  plinth with a lit firebox); `tank_h` 22, `plinth_h` 15, `fire` true, `d` 4; `color` = copper. Pair the
  firebox with a `lights` entry + soft_glow.

**Space** (`space_*`; NOT in `PIXEL_MOTIFS`: planets, stars, sun, rocks, craters, shadows, tracks, trail are
deliberately unlit; props take the scene light only with `"lit": true, "pixelate": k` (+ `"outline"`) and an
explicit `"shadow"`). `color` is required on every layer even where unused. Light convention in the chapter:
light from the upper left (`dir` [-0.8,-0.55]) -> `side: -1`, `sun: [-1, ..]`, `lsign: -1` (`blocks` always
draws right faces dark).
- `space_planet`: pixel sky body, hard 5-step light + dithered terminator. `kind` earth|moon|mercury|mars|
  venus|glacio|gas (`color` = hue for gas), `sun` (0.7,-0.6) direction to the light, `r` (radius in texels,
  default fills the box), `ring` false (tilted ring with gap; wide box), `tilt` -16, `seed` 1.
- `space_sun`: round pixel sun (4-tone disc, Bayer-dithered corona, short rays); `r` 11, `corona`, `rays` true,
  `ray_len` 0.95, `seed`. Draw after nearby planets; pair with a `lights` entry.
- `space_stars`: square pixel stars + plus-shaped twinkles; `n` 60, `sparkle` 3. Keep the boxes off panels.
- `space_rocket`: upright rocket (ogive nose and fins in `color`, white body, band, porthole, engine bell);
  `side` 1, `window` true; designed 22 x 74 texels.
- `space_gantry`: launch-tower lattice with service arms, hazard foot, beacon; `arm_len` 8, `arms`
  (0.3, 0.62), `side`, `beacon` true; use `"outline": 0`.
- `space_astronaut`: 12x25-texel astronaut, optional planted flag in `color`; `flag` true, `side`, `emblem`
  "square"|"rocket".
- `space_rover`: lunar rover in profile; `side` (-1 mirrors), `lsign` (wheel highlight side).
- `space_satellite`: gold-foil hub, two solar wings, dish, mast; `side`.
- `space_solar`: two tilted solar panels on a mast with struts and base plate; `side`.
- `space_mast`: radio mast with dish and red light; `side`.
- `space_rocks`: scattered 3-tone rocks; `n` 12, `side`, `maxw` 8 (up to 20 for corner boulders).
- `space_crater`: low-angle crater (lit rim, shadowed wall), box ~5:1; `side`; `color` = neutral ground.
- `space_shadow`: texel-snapped ground shadow (hard core, dithered rim); `skew` texels; alpha 0.4-0.5,
  drawn before the prop.
- `space_tracks`: regolith marks; `kind` "tread" (two dashed rows, `sep` 4, `amp` 1.0) | "prints" (boot
  prints); `fade` 0.4; `color` dark.
- `space_trail`: dotted Bezier flight path `p0` -> `p1` (control) -> `p2` (box fractions), `step` 4, `fade` 0.6,
  `arrow` false (true = arrowhead at p2).
- `space_crop`: a sub-rectangle `box` [x0,y0,x1,y1] of any texture/atlas `asset`, nearest-scaled by k, `flip`.
  Its `asset` is NOT validated by `build.py --check`. (Unused now.)

### Round 7: pixel winter landscape for climate (2026-10-05, additive only)

New motifs in `artlib.py` (one block directly above `DECOR_MOTIFS`, header "round 7"). No existing code, default or
motif output changed (`tools/check_unchanged.py` prints OK). All draw on a `k`-px texel grid (give each layer
`"k"` = the scene `texel`, 4 in climate) with hard tones and Bayer dither - no smooth gradients - so they sit with the
sprites and `blocks`. They are NOT in `PIXEL_MOTIFS`: they shade themselves, so the scene light does not tint them and
there is no automatic contact shadow (set `"shadow": 0.4-0.5` on props, `"haze"` + `"haze_color"` to push a layer back).
Pick box sizes that are multiples of `k` canvas px (`w` units x 24 / k); every layer takes an optional `"seed"` that pins
its random shapes (otherwise they depend on the layer index).
- `pixel_peaks`: mountain range of straight-sloped peaks. `peaks` [[x, height, half-width] as box fractions] (or `n`
  random), `side` -1 light from the left, `snow` share of EACH peak that is snow, `base` foothill share, `taper`
  [left, right] (no cliff at the box edge), `fade` (bottom dissolves in dither; 0 = solid, let the next layer cover
  it), `mottle`, `dust` (snow lodged in gullies), `snow_lit` / `snow_shade`, `rough`. Lit/shaded flank split by a
  diagonal arete, radial gullies, snow tongues, dithered darker base. Far range lighter + `haze`, near range darker.
- `pixel_pine` / `pixel_forest`: snow-laden conifers. `pixel_pine` = one tree filling the box (box width ~0.78 x
  height); `pixel_forest` = `n` trees, heights `hmin`..`hmax` texels, `flat` (trunk jitter), `span`, `tier` (texels per
  tier), `fat` (width / height), `snow` (0 bare .. 0.6), `vary`; `color` = mid needle tone (dark teal). Trunks end at
  the box bottom: put a `pixel_drift` in front of them.
- `pixel_drift`: opaque rolling snow hill (top `amp` share of the box is the surface; `waves`, `deep` colour at the
  bottom, `ripple`, `sparkle`). Stack 3-4 (far = darker blue, near = pale) for depth.
- `pixel_aurora`: dithered curtains with rays. `curtains`, `color` (base) -> `color2` (top), `reach`, `sway`, `rays`,
  `levels` (8 = fine steps). Draw before the mountains, layer alpha 0.8-1.
- `pixel_moon`: round moon, 4 tones, maria, craters, dithered halo (`r` texels, `halo` x r). Add a `lights` entry.
- `pixel_cloud` (storm / snow cloud: `puffs`, `belly`, `streaks` = falling snow; box ~1.4:1 or taller so the belly
  has room) + `pixel_bolt` (white-hot zig-zag, `width`, `segs`, `branches`, `wander`) - a storm front on one side.
- `pixel_timber`: timber frame from `beams` [[x0, y0, x1, y1, thickness(, asset)]] in texel coords of the box, real log
  / plank texels along the grain, lit + shaded edge, snow on every upward-facing edge (`snow` 0 = none), dark extruded
  side (`depth`). Racks, posts, sign boards, porch posts; hang `sprite` items from it.
- `pixel_icicles`, `pixel_flakes` (sparse snow, keep boxes off the panels), `pixel_lightpool` (warm cast light on
  snow: dithered ellipse, `skew`, `peak`), `pixel_pond` (frozen pond tiled with a real ice texture, snow shore,
  aurora reflections; `asset`, `reflect`, `cracks`).
Recipe (climate, one texel 4): sky_band + stars + aurora + moon + storm cloud, far peaks (hazy), two dark side peaks,
calm dark `soft_glow` behind the quest panels, far forest, three drifts with pines between them, `blocks` cabin (thatch
roof, snow tops) + timber porch + icicles, hide-drying rack with a campfire, sewing table, sign, pond, lit window
spill with `pixel_lightpool` + `lights`, flakes, framing pines. The spec is generated by `_art_review/gen_climate.py`
from screen-pixel coordinates (helpers `pix`, `blk`, `spr`, `peaks_for`); cycle 2 redid it in `_art_review/gen_climate2.py` (see round 7b).

### Round 7b: height-field mountains and hand-drawn props (climate cycle 2, 2026-10-06, additive only)

Added in `artlib.py` (block "round 7b" above `DECOR_MOTIFS`); every other chapter still renders pixel-identical
(`tools/check_unchanged.py` OK). Same rules as round 7: one texel (`"k"` = scene texel), hard tones.
- `pixel_alps`: mountains rendered from a real height field (voxel-space, near to far), so ridges, aretes, gullies,
  shoulders and shadowed faces are geometry, not texture - this replaced the flat-faced `pixel_peaks` in climate.
  `peaks` [[x, height, half-width]] as box fractions (the tallest summit reaches its height), `side` -1 light from the left,
  `light` (x, y up, z towards viewer), `steps` 5 rock tones from `color` (the mid tone), snow above `snow` (share of the
  tallest peak) on slopes gentler than `steep`, `strata` contour ledges, `mottle` stepped patches, `contrast`, `fill`
  (ambient in the shade), `relief` (ridged-noise carving, 0 = smooth cones), `sharp` (0.6 blunt .. 1 needle spires),
  `foot` (rolling foothills so no flat horizon line shows), `depth` / `tilt` (camera), `taper` [left, right],
  `mist` + `mist_amt` (3 hard haze bands towards far ground), `seed`. No dither, no gradient, specks cleaned. Recipe: far
  range (pale, `mist`, layer `haze`), two hero massifs at the sides (taper towards the panels), dark low foothills, a dark
  conifer belt (`pixel_forest` clumps) at their foot, then forest + drifts. Always give the box the room it needs: summits
  sit at `box bottom - height x box height`.
- `pixel_art`: a hand-drawn prop from ASCII `rows` + palette `pal` {char: [r,g,b(,a)]} (space / '.' = clear), `ox`/`oy`,
  `flip`. It is a pixel motif (scene light, contact `shadow`, `drop` apply). Size the box as columns x k by rows x k canvas
  px. Climate uses it for the thermometer board, the season wheel and the wind vane (rows are generated in
  `_art_review/gen_climate2.py`).
- New optional keys, defaults unchanged: `pixel_drift` and `pixel_lightpool` `"dither": 0` (hard bands instead of the
  Bayer screen-door fall-off), `pixel_pond` `"bright"` < 1 (darker, bluer ice that stands out from pale snow).
- `preview.py`: `ICON_OVERRIDE` maps item ids whose icon is not at `item/<id>` (nested thermometer, plant armour, soulspring
  lamp, weather2 blocks, block-model items like the sewing table drawn as an inventory cube) so the nodes of the preview
  never show blank discs. Preview only; the game resolves the real item models.
- Climate (cycle 2) layout: sky = moon + aurora only (no storm cloud); one hook prop under each lower panel (weather mast
  with vane and tornado plaque under section 3, thermometer board under 4, season wheel under 5), tanning rack with fire,
  sewing table, frozen pond, brick-chimney cabin with a fur coat on its wall. Generator: `_art_review/gen_climate2.py`
  (screen-pixel coordinates, `python _art_review/gen_climate2.py out.json`), dev loop `_art_review/_c2_run.sh`.

### Round 7c: calm planes, hard-tone sky, snow gable roof (climate cycle 3, 2026-10-06, additive only)

Added in `artlib.py` (block "round 7c" above `DECOR_MOTIFS`, plus optional keys on existing round-7 motifs whose defaults are
unchanged: `tools/check_unchanged.py` OK for the other 18 chapters). Lesson from the critique: the height-field `pixel_alps`
paints each screen column from the nearest depth sample, so steep faces turn into vertical streaks whatever the settings;
climate now uses geometry made of a few big flat planes instead. One rendering language for the whole scene: hard tones, no
Bayer screen-door anywhere (sky, mountains, props), single-texel checker only where two planes meet.
- `pixel_range`: calm faceted mountains. `peaks` [[x, height, half-width]] box fractions (taller peaks draw in front), `side`
  -1 lit from the left / 1 from the right (mirror the sun / moon), `snow` snow-cap share of the peak (0.35-0.5), `steps` 4
  rock tones from `color`, `rays` 3-5 crease lines per flank fanning out of the summit region (the facets), `jag` 0.2-0.3
  shoulders on the silhouette, `tongues` snow running down gullies, `crags` short darker rock strokes with a lit edge,
  `edge_dither` 1 = one-texel checker on plane edges and the snow line, `snow_lit` / `snow_shade` (tint them warm for a range
  facing a sun), `mist` + `mist_amt` + `mist_from` three hard haze bands towards the foot (cover the foot with forest / drift),
  `flat` widens the flanks, `seed`. Far range: pale-dark `color`, `haze`, few tones; near range darker. Keep massifs a little
  darker than the snow tones of the hero props so the cabin carries the contrast.
- `pixel_roof`: snow-covered gable roof in the oblique `blocks` view (box = front width + `d` texels wide, `pad` + `d` + `t` +
  rise tall). Thick thatch fascia (`t`) with a lit snow lip and dark underside, overhang `ov`, planked gable wall under it,
  receding slopes as soft-ridged snow (lit left slope, half-shaded right slope, thatch peeks at the left eave), dark right end
  face, and an optional brick chimney `chim` [x, w, top, z, depth] with snow cap and dark flue (smoke box bottom = flue centre at
  screen texel x + w/2 + z + depth/2, top - z - depth/2). Pitch must stay under 45 degrees. Walls: a `blocks` layer with
  `depth` = d / 16 whose left edge sits `ov` texels inside the roof box, roof box bottom on the top row of the front wall. A
  `pixel_art` season wheel fits the gable; a thermometer board fits a wall cell.
- `pixel_sun`: round three-tone sun in hard glow bands (`r`, `rings`, `reach`, `glow` -> `glow2`, `glow_alpha` - NOT `alpha`,
  that is the layer alpha). Draw it before a range so the ridge cuts it; add a warm `lights` entry and tint that range's `snow_lit`.
- New optional keys: `pixel_alps` `oct` / `facet` / `profile` / `snow_steps`; `pixel_aurora` and `pixel_moon` `"dither": 0` (hard
  bands; the aurora keeps its brightness); `pixel_drift` `"taper"` (each end sinks to the box bottom: a short box is a mound
  that hides a post base, used as footing for the mast, the stand and the rack).
- Gotcha: a motif parameter must never be called like a layer key the scene already reads (`alpha`, `x`, `y`, `w`, `h`, `rot`,
  `shadow`, `haze`, ...): `_motif_opts` would feed the layer value into the motif.
- Climate background: calm `powder_snow` / `white_concrete_powder` tiles, no overlay (the old packed-ice tile had diagonal scratch
  lines and a speckle overlay whose light dots read as stray stars in the sky).
- Climate (cycle 3) layout, left to right: moon + one aurora ribbon (hard bands), tall faceted massif, dense dark pine band
  behind the three lower panels (they sit on a calm dark backdrop like panels 1-2 on the night sky), tanning rack + campfire +
  tfc barrel + sewing table as one workstation, weather mast with a red-white windsock and tornado plaque on a snow mound, a clothing stand
  wearing the goat-fur set, a frozen pond, the cabin with gable roof, brick chimney and smoke, thermometer board on the wall,
  season wheel in the gable, lantern, fur coat, footprints to the door, and a low sun rising behind the right massif (warm half
  of the sky, warm rim on the range). Generator: `_art_review/gen_climate3.py` (screen-pixel coordinates, `python
  _art_review/gen_climate3.py out.json`; env `C3_ONLY=sky,mountains` renders layer groups only), quick look without a build:
  `python _art_review/_c3_view.py spec.json out.png [x0 y0 x1 y1 zoom]`.

## Verify (always look at the screen previews)

```
PY=C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe
QGEN_STAGE=_stage_mine QPREVIEW_SCREEN=29,55 $PY questgen/build.py --stage --only 00_welcome,<stem>
QGEN_STAGE=_stage_mine QPREVIEW_SCREEN=29,55 $PY questgen/preview.py <stem>
# -> questgen/_stage_mine/preview_screen29_<key>.png (player's zoom) and preview_screen55_<key>.png
```

`preview_screen29` simulates the real view (GUI scale 4, background tile at true size, item icons in
nodes, no titles). Judge the design there, not in the tight `preview_<key>.png`.
