# Renderer changes (artlib.py / build.py draw_panel) - 2026-10-05

Baseline: `_art_review/base/preview_screen29_<key>.png` (identical to `_art_review/before`).
Verification: full `build.py --stage` into `_stage_render` + screen29 previews of all 19 chapters,
compared side by side with the baseline. Experiments with in-memory spec patches:
`_art_review/_try.py TAG <stems> <patch.py>` (stage only; patches in `_art_review/p_*.py`).

All new spec keys are optional; specs without them keep working (validated by `build.py --check`).

## Default-behaviour changes (kept: better in every affected chapter)

1. **Glow = light pool, not an outline halo** (`"glow"` on sprite layers; 16 chapters use it).
   Old: tight Gaussian of the sprite silhouette at 0.9 strength -> "pasted sticker" outline.
   New `_emit()`: broad radial pool of light around the sprite (radius ~1.15 x sprite size) plus a faint
   close bloom. Optional `"glow_strength": 0.5-1.5` (default 1).
2. **Sun without clip-art rays**: bloom + corona + white-hot disc with coloured limb.
   Legacy look: `{"motif": "sun", ..., "rays": true}`. (welcome, climate, farming, explore)
3. **Lightning rebuilt** (known weak point, climate + ie): sharp-kinked main channel (random walk +
   midpoint jaggies) kept inside the box, 2-3 forks that may fork again, white-hot tapering core, coloured
   inner glow, wide soft outer glow; glow fades at the box edges and the bolt emerges from the top.
   New params: `"width"` (1 = bold default, 0.5 thin, 1.6 heavy), `"branches"` (0..1.5, default 1),
   `"flash"` (0..1 cloud flash at the top, default 0).
   `{"motif": "lightning", "x": 0.81, "y": 0.53, "w": 7, "h": 15, "color": [220,236,255], "alpha": 0.95, "width": 1.3, "flash": 0.5}`
4. **Pipe valves**: the bright red ring ("debug marker") is now a gate valve: bonnet, stem and an
   iron handwheel seen edge-on with an oxide-red highlight. (tfmg, pneumatic)
5. **Prop motifs redrawn with volume (top-left light, gradients, contact shadows)**:
   `anvil`/`anvil_hot` (tapered horn, lit face edge, shadowed overhang, hardy/pritchel holes, arched feet),
   `tower` (staggered stone courses, round-tower shading, corbelled parapet, slate cone roof, arched lit
   windows that spill light, door), `pumpjack` (A-frame samson post with braces, I-beam walking beam, curved
   horse head on an arc around the pivot, bridle + polished rod + wellhead, gearbox, crank, counterweight),
   `mine_entrance` (tunnel depth gradient, receding inner frames, rails and sleepers to a vanishing point,
   lantern glow deep inside, log ends, knee braces), `livestock` (shaded cows with patches, udder, horns,
   eyes; two-tone woolly sheep; white chicken with comb; grass tufts; contact shadows).
   Same boxes/aspect as before, so existing placements still fit.
6. **Panel headers stay readable** (build.py `draw_panel`, drawing code only): titles that fit keep the
   old look; titles that used to shrink first drop the diamond ornaments and use the full width; if they
   would still fall below ~19 px (11.5 screen px), "第N节" goes small on a first line and the name large on
   a second line. Worst cases went from 6.6 to ~12.7 screen px (steel s3, bronze s5, twilight s2...).
7. Rotation is now applied before lighting/shadows (tiny rounding differences in create/space/stone_age,
   mean pixel diff < 0.1, max 20/255 on ~300 px: invisible).
8. **Create props**: `water_wheel` is now a paddle wheel (two plank rims boxing 16 boards, planked spokes,
   andesite hub, water pouring onto the top-left buckets with a splash, a rippling channel that dissolves
   at both ends) - it used to read as a ship's wheel; `belt` is a solid rubber band with tread plates,
   andesite frame, pulleys and legs instead of an empty outline loop.
9. Lightning default thickness raised once more after the in-context check (core ~9 screen px at w=7,
   stronger inner/outer glow, wider wander, longer forks) - the climate bolt is now clearly bold.

Also new (opt-in): `light_rays` motif (soft shafts from a light source: `src`, `angle`, `spread`,
`count`) and `heartbeat` `"width"` (0.4 = faint ambient trace instead of a thick UI-like line).

## Experiments run (in-memory spec patches, `_art_review/p_*.py`, previews in `_art_review/try/`)

- iron_age (`p1`): texel 5 + light + shadow + lights/ambient + ingot `pile` + ore `scatter` + pixelated
  anvil + bloomery as `blocks` -> coherent forge, one pixel density, furnace lights the floor props. Works.
- mekanism (`p2`): casing grid and machine wall as `blocks` (k 6) -> reads as a 3-D multiblock /
  machine bank instead of a wall of texture squares. Works; strongest single new tool.
- welcome (`p2/p3`): scene-wide `pixelate` 4 + texel 6 + lights. First version quantised alpha and
  produced hard box edges on dissolving mountains -> fixed (edge texels snap, slow fades stay smooth) and
  backdrops are now excluded from the scene-wide switch. Pixelated small trees lose their inner detail:
  recommend pixelate only for props next to sprites, not for distant scenery.
- climate (`p4`): lightning width 1.3-1.4 + flash. The first flash was an ellipse that read as a flat bar
  -> replaced by a soft radial blob.
- bronze (`p4`): light_rays + haze on trees + lit anvil/mine + ingot pile -> visible single light direction.
- steel (`p4`): `scatter` was too regular -> widened gaps/lifts (still reads partly as a row: prefer `pile`).
- stone_age / farming (`p5`): pixelated campfire (colors 16) looks like real pixel art and matches the cave
  wall; pixelated apple tree (+ outline) now matches the pixel apples; pixelated arrowheads turn mushy
  (keep them vector or drop them).

## Reverted / not adopted

- Alpha quantisation to 4 levels in `pixelate` (hard rectangular edges on fading layers) - replaced.
- Box-shaped lightning flash - replaced by a radial blob.
- Lowering SPRITE_K_MAX by default (10 -> 8): would shrink hero sprites in food/storage/explore whose
  layout depends on them; left opt-in (`"k_max"` / `"texel"`) so chapter agents decide per chapter.
- Scene-wide pixelate of backdrops (mountains/tree_line): looked like a mosaic filter, excluded by default.

## Remaining weaknesses (renderer side)

- `sun` is better than the ray icon but still reads as a pale moon when a semi-transparent mountain layer
  is drawn over it (welcome, explore) - spec order/alpha issue.
- `pixelate` cannot invent pixel-art detail: small vector props become simple blocky shapes.
- Not redrawn this round: `campfire` (smooth gradients; use `"pixelate": 4, "colors": 16`), `arrowhead`,
  `rocket`, `satellite`, `windmill_sails`, `tree` (use `pixelate` + `outline` next to pixel sprites).
- The preview resizes the scene bilinearly; in game FTB draws it nearest, so pixel edges are a bit crisper
  in game than in the previews.

## Is 9+ realistic?

Both critics put the ceiling of this pipeline at ~7.5-8 (director: "9 is not realistic" with procedural
motifs + rescaled icons). After this round the renderer removes most of the *systemic* reasons for the
6-7 scores (halo stickers, hotbar rails, mixed texel sizes, flat props, unreadable headers, debug-red
rings, thin lightning) - if the chapter agents adopt texel/light/shadow/blocks/pile, 7.5-8 is realistic for
most chapters and 8+ for the best (stone_age, create, space, food, iron_age). A consistent 9 needs every
element designed for its place with one hand-controlled style and lighting - i.e. hand-pixelled or
commissioned (or AI-generated then hand-cleaned) chapter illustrations used as the scene layer, or
`blocks`-based dioramas composed by a human eye. The renderer now supports that path (one texel grid,
scene light, block structures), but procedural placement by fractions alone will not reliably score 9.

## New opt-in features (scene-level keys, all optional)

| key | meaning |
| --- | --- |
| `"texel": k` | every sprite / sprite_row / blocks layer at exactly k canvas px per texture pixel (one pixel density; ~1.2*k screen px). Layer `"k"` overrides. 4-6 recommended. |
| `"k_max": n` | lower cap for fitted sprites (default 10) when not using `texel`. |
| `"light": {"dir": [dx,dy] or degrees, "color": [r,g,b], "tint": 0-0.3, "rim": 0-1, "shade": 0-0.5}` | puts pixel layers (and vector layers with `"lit": true`) into one scene light: multiply-tint toward the light colour, gradient across the object, one-texel rim light on edges facing the light. Layer `"tint"/"rim"/"shade"` override, `"unlit": true` opts out. |
| `"shadow": 0-1` | contact shadow under every sprite / sprite_row / blocks layer (layer `"shadow"` overrides, 0 = none). |
| `"lights": [{"x","y","radius","strength","color"}]` | cast light: content near each light is brightened and tinted (adds no glow of its own); `radius` is a fraction of the canvas width. |
| `"ambient": 0.7-1` | dims everything away from the `lights` (chiaroscuro). |
| `"pixelate": k or true` | re-renders vector PROP layers on a k-px texel grid (crisp silhouette, smooth fades) so they share the sprites' pixel look. Atmosphere and big backdrops (mountains, tree_line, strata, planets ...) are skipped unless the layer itself sets `"pixelate"`. `"colors": n` palette reduction, `"outline": 0-1` one-texel dark outline. |
| `"haze_color": [r,g,b]` | colour for layer `"haze"`. |

Layer-level additions: `"k"`, `"flip": true` (mirror a sprite), `"shadow"`, `"drop": 0-1` (drop shadow cast
away from the light - for things hanging on a wall), `"haze": 0-0.6` (depth: mix toward haze colour),
`"lit"`, `"unlit"`, `"tint"`, `"rim"`, `"shade"`, `"pixelate"`, `"colors"`, `"outline"`, `"glow_strength"`.

`sprite_row` gained `"arrange": "row" (default, legacy rail) | "scatter" | "pile"` and `"spacing"` (1.35).

New motif **`blocks`**: a small structure built from real block textures in an oblique view (front +
lit top + shaded right side, hidden faces skipped, every texel on one grid):
```json
{"motif": "blocks", "x": 0.8, "y": 0.6, "w": 6, "h": 22, "k": 5,
 "rows": ["G", "G", "G", "B"],
 "legend": {"G": "tfc:block/rock/bricks/gabbro",
            "B": {"front": "tfc:block/devices/bloomery/on", "top": "tfc:block/rock/bricks/gabbro",
                  "side": "tfc:block/rock/bricks/gabbro"}},
 "depth": 0.45, "alpha": 1.0}
```
Use it instead of stacks of flat block-face sprites (bloomery, blast furnace, coke oven, casing walls,
machine banks).

Example scene header for a forge:
```json
"scene": {"texel": 5, "shadow": 0.5,
          "light": {"dir": [1, -0.2], "color": [255, 160, 90], "tint": 0.12, "rim": 0.6, "shade": 0.3},
          "lights": [{"x": 0.8, "y": 0.72, "radius": 0.3, "strength": 0.8, "color": [255, 140, 70]}],
          "ambient": 0.85,
          "layers": [ ... ]}
```
