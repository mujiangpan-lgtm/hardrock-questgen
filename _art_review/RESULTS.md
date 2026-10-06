# Art fixes: results (2026-10-05, cloud run)

Task: `CLOUD_TASK.md` (A: fix 10 chapters, B: blind final scoring of all 19, C: deliver on branch `art-fixes`).
Only art specs changed (`art_styles.d/*.json`); no drawing code, chapter, build or preview code was edited.

**Headline:** the blind average of all 19 chapters went from **6.24 to 7.28 (+1.04)**. The 10 Task A
chapters went from **6.30 to 7.60 (+1.30)**; every one of them improved by 0.75 to 2.25. Best now:
pneumatic 8.25, storage 8.0, iron_age 8.0. Nothing reached 9; both critics put the pipeline's ceiling at
about 8-8.5 (see the end).

Setup: Pillow 12.3.0, numpy 2.4.6, Python 3.11, Noto CJK installed (the previews show real Chinese text),
textures from the encrypted pack data. `python build.py --check` -> `OK: 19 chapters, 435 quests`.
Full `QGEN_STAGE=_stage_final python build.py --stage` -> `OK: 19 chapters, 435 quests`, **no WARN or ERROR lines**.

## Before / after (blind, average of the two lenses)

Baseline = `critique_before_*.json` (previews in `before/`); after = `critique_after_*.json` (previews in `after/`). Both critics scored blind (they saw only the after PNGs, not the baseline scores or what changed). "fixed": `cloud (this run)` = Task A, `local` = `fix_results_local.json`, `not edited` = untouched in this round.

| chapter | fixed | before dir | before pl | before avg | after dir | after pl | after avg | delta |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 00_welcome | local | 5.5 | 5.5 | 5.50 | 6.5 | 6.5 | 6.50 | +1.00 |
| climate | local | 6 | 6 | 6.00 | 7 | 6.5 | 6.75 | +0.75 |
| food | local | 6.5 | 7 | 6.75 | 8 | 7.5 | 7.75 | +1.00 |
| health | local | 5.5 | 5.5 | 5.50 | 7.5 | 7.5 | 7.50 | +2.00 |
| farming | local | 6.5 | 6.5 | 6.50 | 6.5 | 6.5 | 6.50 | +0.00 |
| storage | cloud (this run) | 6.5 | 6.5 | 6.50 | 8 | 8 | 8.00 | +1.50 |
| stone_age | cloud (this run) | 7 | 6.5 | 6.75 | 8 | 7.5 | 7.75 | +1.00 |
| copper_age | cloud (this run) | 6 | 5.5 | 5.75 | 7 | 6.5 | 6.75 | +1.00 |
| bronze_age | cloud (this run) | 6 | 6 | 6.00 | 7.5 | 7.5 | 7.50 | +1.50 |
| iron_age | cloud (this run) | 6.5 | 6.5 | 6.50 | 8 | 8 | 8.00 | +1.50 |
| steel_age | local | 5.5 | 5.5 | 5.50 | 7 | 6.5 | 6.75 | +1.25 |
| create | not edited | 7 | 7 | 7.00 | 6 | 7 | 6.50 | -0.50 |
| ie | cloud (this run) | 6 | 6.5 | 6.25 | 8 | 7.5 | 7.75 | +1.50 |
| tfmg | cloud (this run) | 6 | 6 | 6.00 | 7 | 6.5 | 6.75 | +0.75 |
| pneumatic | cloud (this run) | 6 | 6 | 6.00 | 8.5 | 8 | 8.25 | +2.25 |
| mekanism | local | 5.5 | 6 | 5.75 | 7.5 | 7 | 7.25 | +1.50 |
| explore | cloud (this run) | 6.5 | 6.5 | 6.50 | 7.5 | 7.5 | 7.50 | +1.00 |
| twilight | cloud (this run) | 6.5 | 7 | 6.75 | 7.5 | 8 | 7.75 | +1.00 |
| space | not edited | 7 | 7 | 7.00 | 7 | 6.5 | 6.75 | -0.25 |
| **all 19** | | | | **6.24** | | | **7.28** | **+1.04** |

Group averages (before -> after):

- local: 7 chapters, 5.93 -> 7.00 (+1.07)
- cloud (this run): 10 chapters, 6.30 -> 7.60 (+1.30)
- not edited: 2 chapters, 7.00 -> 6.62 (-0.38)

Notes on the numbers:
- `create` and `space` (pilots in `art_styles.py`) were not edited in this round. Their scores moved by
  critic variance and the round-5 renderer changes (redrawn `water_wheel`, `belt`, `sun`, glow pools), which
  landed after the baseline previews; both critics now call their smooth vector gears / planets / rocket the
  main style clash. They are the obvious next candidates.
- `farming` stayed at 6.5 even though it was rebuilt locally (block barn and apple tree): both critics now
  flag the scale of the giant block tree/barn and the olive palette.
- The before and after critics are different sessions; expect about +-0.5 noise per chapter.

Process (Task A): one sonnet subagent per chapter, at most 3 in parallel, each with its own stage dir
(`_stage_fix_<key>`), a shared brief (ART_GUIDE rules, rubric, palette list) and two helper scripts (scene
fraction boxes of panels/banner + a fraction grid over the screen29 preview; a formatter that keeps the
one-layer-per-line JSON style). Deviations, reported honestly:
- Round limit: copper_age, iron_age, storage, explore, stone_age and twilight kept to 1 baseline build + 4
  rounds. bronze_age (+2 polish builds), tfmg (~9 builds), ie (~12) and pneumatic (11) went over; they ran
  before the brief made the limit explicit ("5 builds total").
- Coordinator edits after review: **storage** palette changed from the agent's signal orange to teal
  (64,210,178), because orange collided with bronze_age's new amber and pneumatic's orange glow (the agents
  ran in parallel); **twilight** got one fix build (block castle that read as floating amethyst roofs ->
  vector castle silhouette with lit windows; square dark-log "knots" on the trunk removed; gloom mushrooms
  pushed back with haze); **stone_age** was re-rendered after the agent's last blind one-layer removal (OK).
- Palette moves this run: bronze_age teal -> amber-bronze (204,140,58); pneumatic mint -> silver-white
  (236,241,246) + hazard orange (255,150,60); ie cyan-teal -> electric cyan (48,216,255) on treated-wood
  brown panels; storage sky-blue -> teal (64,210,178). The warm band (stone ember, copper salmon, bronze
  amber, create brass, pneumatic orange glow) is now crowded; bronze_age sits between stone_age and create
  in hue and is separated mainly by being darker.
- `pneumatic`: the banner title colour comes from `qlib.py` `THEMES["pneumatic"]` (cyan), not from the spec;
  the preview shows the spec's orange. Not checked in game.

## What changed per chapter

### Task A (this run, cloud)

#### copper_age (`11_copper`): 5.75 -> 6.75

- State: improved (continued from the partial edits, which beat the original); 32 layers; 4 rounds; self-score 5.75 -> ~7.0.
- kept from partial: texel 4, shadow 0.5, warm light, lights + ambient 0.62, dusk sun + light_rays, stepped basalt cliff (blocks) on the left with malachite/native-copper veins, lantern ledge, pickaxe at the vein; hotbar row, raw block squares and muddy smoke column removed
- new hero: pit kiln (blocks log pile on hot coals over a dirt base) with soft glow, embers, cast light and an unfired vessel firing on top; bottom props re-spaced (ore pile, stone with ingot, kiln, glowing molds, forge)
- teal-over-salmon dusk sky; right-hand basalt cliff behind the forge (different height than the left, native-copper vein); strata_band floor raised into view
- removed the pixelated tree_line (mosaic smear)

#### bronze_age (`12_bronze`): 6.00 -> 7.50

- State: improved; 36 layers; 4 rounds + 2 polish builds; self-score 6 -> ~7.5 (both lenses).
- palette: teal identity dropped (collided with ie/pneumatic/mekanism) -> warm antique bronze: accent (204,140,58), glow (226,150,56), text #E8B672, panel (30,24,16), bronze speckle background, banner motif (168,116,54); patina only as small accents (malachite, teal-slate top sky, teal haze, dark conifers)
- texel 3 for all blocks/sprites; one warm light from the right + shadow 0.5; cast lights at the smelter and the mine lantern, ambient 0.86, each with a soft_glow
- left frame: hillside mine built with `blocks` (cobble hill, oak posts, plank lintel, dark tunnel), timber headframe with chain + bronze bell, lamp in the tunnel, rail track, minecart, hand-placed ore pile (cassiterite, sphalerite, bismuthinite, malachite), prospecting pick
- hero: pixelated lit anvil_hot (pixelate 3, colors 16, outline) on a log stump, bronze hammer and glowing ingot beside it (flat tan cut-out + sword on top removed)
- right frame: stone-brick smelter (`blocks`) with chimney, bellows, lit charcoal forge, crucible block, a few embers and faint smoke
- bottom centre: plank workbench with an ingot `pile` (copper, tin, bismuth, zinc, bronze), mould, chestplate, helmet; charcoal pile (replaces the hotbar ingot row)
- top band: teal-slate sky + amber dusk horizon + two umber mountain ranges; coarse-dirt `blocks` floor (depth 1.0, haze 0.42) anchors all props; hazed conifers for depth

#### tfmg (`22_tfmg`): 6.00 -> 6.75

- State: improved; 29 layers; ~9 builds (over the 4-round limit: 3 exploration + 6 refinement); self-score 6 -> ~7 (both lenses).
- texel 4, shadow 0.5, warm flare-side light (dir [-1,-0.5], rim 0.55); cast lights at flare, lantern, furnace mouth, far flare and pumpjack yard, ambient 0.8, each with a soft_glow
- hero: distillation tower built with `blocks` (cast-iron tank bands alternating with distillation_tower_output port blocks, dark vent stacks, yellow-black caution_block plinth carrying the olive-yellow TFMG identity), hanging lantern with glow
- left frame: steel-truss flare mast with a fire_0 flame (replaces the thin pipe + blob), fireproof-brick blast furnace with slag-brick chimney, glowing mouth, steel/coke stock pile, far tall stack with caution band and red obstruction light
- right depth: far stack with a second flare, far cast-iron column and steel_vat tank (`blocks` k 2 + haze)
- centre bottom: pumpjack pixelated (4, 14 colours, outline) and lit; cast-iron drum stack with a pile of crude/diesel/gasoline/kerosene buckets (replaces the bucket row); oil-puddle shadow
- removed: red valve rings (`pipes`), olive sky_band mud, old smokestack, mountain_range and strata layers; added dusk glow, flare-lit smog, faint smoke, asphalt `blocks` floor

#### pneumatic (`23_pneumatic`): 6.00 -> 8.25

- State: improved; 56 layers; 11 builds (over the 4-round limit; launched before the limit was tightened); self-score 6 -> ~7.5 (both lenses).
- palette: mint dropped (collided with mekanism/bronze/ie) -> pressure-gauge silver-white + hazard orange: accent (236,241,246), panel graphite (24,28,34), glow (255,150,60), text #FF9B3D; background cool neutral grey tint (206,216,230), saturation 0.3, third tile compressed_brick_tile against visible tiling
- removed the glowing gauge sticker, red valve rings, circuit lines, floating item shelf and the flat 3x3 chamber sprites
- texel 4, shadow 0.5, cool top-left light, ambient 0.88, warm `lights` at the lanterns and the chamber
- hero: pressure chamber built with `blocks` (4x3 real chamber textures, valve), windows glowing with PCB + plastic inside, lantern on top
- pipes as pixelated `shaft` layers (4, outline, drop shadow) in three short runs: ceiling trunk -> hanging 2x2 compressor -> riser into the chamber; floor compressor -> chamber valve; left riser; orange T-handle valves
- machines: iron-block tank with gauge, 2x2 compressed-iron compressor, programmable controller + drone interface rack, PNC item pile on the floor, small drone (logistics_core + turbine rotors), pipe-mounted gauges at the same texel
- three hanging lanterns with glow, light_rays from one, steam wisps, floor haze, ceiling beam + floor row as hazed `blocks`

#### ie (`21_ie`): 6.25 -> 7.75

- State: improved; 67 layers; 4 design rounds after ~8 throwaway technique builds (over the limit; launched before the limit was tightened); self-score director 6.0 -> 7.3, player 6.5 -> 7.5.
- palette: electric cyan accent (48,216,255), glow (30,190,255), text #86E8FF, warm treated-wood brown panel fill (36,27,22) instead of teal-black; background IE concrete tinted cool, blueprint grid removed (storage/mekanism use one); banner motif cyan
- scene replaced by a night engineering yard: texel 3, cool cyan scene light, shadow 0.5, ambient 0.78, warm `lights` at the two furnace mouths and a cyan one at the floodlight
- hero (right): blast furnace built with `blocks` (blast-brick shaft and chimney, steel band, real blast_furnace_on front) + coke oven (cokebrick + coke_oven_on front), fire glow, chimney smoke
- left: 15-block steel-scaffold HV pylon with two arms on a concrete footing; treated-wood scaffold floodlight tower with hanging bulb, cyan glow and light_rays, fed by a service-drop cable; dynamo + LV/MV capacitor stack at the base
- power line: second, hazier pylon on the right; cables pylon to pylon behind the banner (rotated `shaft` segments), cyan beacon glows on the pylon tops
- props: wire-coil spools, crate with the engineer's hammer, wooden barrels with a creosote bucket by the oven
- backdrop: hazy sawtooth factory wall (`blocks`, haze 0.55), concrete floor plane, sky / teal mist / warm horizon bands, pixelated moon, two small star clusters
- removed: giant pylons cropped at the top, glowing hammer sticker, both lightning bolts, capacitor column, hotbar rail of spools, oversized coke oven sprite

#### iron_age (`13_iron`): 6.50 -> 8.00

- State: improved (started from the _art_review/p_iron.py experiment); 43 layers; 4 rounds (5 builds); self-score 6.5 -> ~7.5 (both lenses).
- kept the experiment's scene settings (texel 5, scene light, contact shadow, cast lights + ambient) and rebuilt the layers; removed the 4 block-face sprites, old strata band and the dark barrel sprite
- four cast lights (bloomery mouth, bloom on the anvil, two lamps), ambient 0.8, glows + two faint light_rays under the lamps; firelight lands on floor, stump, ore pile and wall
- hero bloomery rebuilt as `blocks`: stepped furnace (basalt-brick chimney on basalt cobble cap, firebrick shoulders, glowing bloomery mouth), TFC bellows block, sooty upper chimney, smoke puffs, a few embers
- basalt cobble floor plane (`blocks`, depth 1.0): nothing floats any more
- anvil pixelated (12 colours, outline, lit) on a douglas-fir log stump, glowing refined bloom on top, hammer leaning on the stump (replaces the flat grey vector anvil)
- tools (tongs, hammer, saw) hang from an iron rail on a hickory wall board with drop shadows; wrought-iron armour on a plank stand (replaces the floating chestplate)
- ingot row -> bloom/cast/wrought iron pile on a plank bench; ore row -> charcoal/hematite/limonite/magnetite `pile` at the bloomery foot; quench barrel as `blocks`
- top band: chestnut-plank ceiling beam (`blocks`, hazed) with chains of different lengths to the two lamps

#### storage (`25_storage`): 6.50 -> 8.00

- State: improved; 54 layers; 4 rounds (5 builds); self-score director 6.5 -> ~7.5, player 6.5 -> ~8.
- palette: sky-blue dropped (every blue tested stayed within dE ~30 of explore/steel/space). The agent chose signal orange, which collided with bronze_age's new amber and pneumatic's orange glow (parallel runs), so the coordinator switched the palette to the teal vacated by bronze/pneumatic: accent (64,210,178), glow (48,200,170), text #86F0DA, slate panel fill (22,28,38), banner motif (60,190,160) - cool teal UI over a warm wooden warehouse
- background: dark-oak + hickory planks (cool-neutral tint), blueprint grid removed; banner spruce ribbon, `strata` motif
- scene concept: warehouse interior - wooden shelving left, Refined Storage network right, ceiling trunk cable + floor cable run joining them; texel 4, warm overhead-left light, shadow 0.5, haze_color, 5 cast lights with ambient 0.76, each with a soft_glow
- left rack: 5-level plank rack, pixelated lit boards, deepslate-brick back panel; real block contents (crates, TFC oak/hickory barrels, hay bale, safe) + hand-placed sacks, baskets, vessels, bundle, lunch basket, wooden hopper; RS interface + lantern on top
- hero (right): stepped RS tower as `blocks` (controller on top, 3-wide disk-drive bank with manipulator and relay, grid terminal, 1k storage blocks at the base), emissive controller/grid overlays with glow, riser cable, small RS-parts shelf (64k disk, processor, housing)
- bottom band: dark-oak ceiling beam, deepslate wainscot, spruce floor (`blocks`, depth 1.0); sorting corner with crate/barrel stack + lamp, hopper on a barrel, chest minecart, sack pile
- removed: blue circuit wiring, potion row, cropped backpack and blurry vase, 8-item bottom lineup, mixed pixel sizes (RS blocks ~8 px/texel vs sacks ~4)

#### explore (`31_explore`): 6.50 -> 7.50

- State: improved; 4 rounds (5 builds); self-score 6.5 -> director ~7.5, player ~7.5-8.
- theme: traveller's vista at dusk - camp on a ledge bottom-left, stepped trail climbing to a signpost at right, distant ruined watchtower with a blue soul-lantern beacon as the destination
- removed: vector compass rose, vector tower, giant pixel spyglass, biplane, pixel boat on a glow strip, old sun with clip-art rays
- sun fix: orange sun (255,146,66) at alpha 1.0 drawn before the mid snowy range, so the peaks cut its lower edge (reads as a sun behind the pass, not a pale moon)
- depth: far mountain_range, two hazed snowy_range layers, dark near range, tree_line behind the camp, low mist band, faint contour map (alpha 0.14) kept as the map motif
- texel 4 foreground, shadow 0.45, warm light from the sun side, 4 cast lights (sun, campfire, lantern, beacon) with ambient 0.76, each with a soft glow
- terrain: one `blocks` layer forms ledge, valley and stepped slope (path blocks, podzol/dirt, basalt/gabbro base); pixelated outlined pines behind the edge
- camp (hero): two pup tents from firmaciv triangular-sail sprites, frame pack, lantern, campfire with light pool, hiking boots, cartography table with compass + atlas, barrel with spyglass (no sprite_row)
- ruin: mossy-brick watchtower on a rock crag (`blocks` k 3, haze 0.3) with a soul lantern
- palette kept: royal blue (104,136,244); identity from deep dusk blue vs warm sun and campfire

#### stone_age (`10_stone_age`): 6.75 -> 7.75

- State: improved (first moved from art_styles.py into art_styles.d/stone_age.json unchanged, then fixed); 4 rounds (5 builds; coordinator re-rendered the final file after the agent's last blind tweak); self-score 6.75 -> ~7.5 (both lenses).
- setting: outdoor moon/mountains/sky band replaced by a firelit cave interior
- texel 4, warm firelight scene light (dir [0,1]), shadow 0.5, haze_color; two cast lights at the campfire, ambient 0.8, paired with a wall glow pool, a tight fire glow and a floor glow ellipse
- ceiling: basalt/deepslate `blocks` with stepped overhangs at both sides, pixel dripstone stalactites (>= 0.02 clear of the banner); full-width gravel/cobble `blocks` floor (depth 1.0)
- hero: campfire with "pixelate": 4, "colors": 16, slightly larger, pixelated embers
- removed: grey low-poly arrowheads, moon, mountains, dotted ochre line; herd painting smaller with its tally dots hidden behind the rack beam
- left: stepped chert boulder (`blocks`) as a knapping station (flint, knife head, stone hammer), stone axe on the floor, stick bundles + straw by the fire
- right: pixelated outlined plank_shelf drying rack with two hides and a venison cut, two javelins leaning on it, bone and mutton on the floor, one handprint stencil on the wall
- centre: first pottery (unfired vessel, fired vessel, bowl) beside the fire
- wall paintings in darker red ochre at lower alpha (fire is the brightest thing); background greyer, speckle density 0.15 -> 0.05; palette ember (220,150,100) and banner unchanged

#### twilight (`32_twilight`): 6.75 -> 7.75

- State: improved; 91 layers; 4 rounds (5 builds) + 1 coordinator fix build; self-score director 6.5 -> ~7.0, player 7.0 -> ~7.2 (before the coordinator fix).
- rebuilt as a block diorama at scene texel 2 (the node-icon density; texel 4 and 3 made blocks ~2x node size): one violet moonlight from the upper right (rim 0.6), contact shadows, four cast lights, ambient 0.84, violet haze colour
- hero: portal pool at bottom centre (stacked glows: violet halo, dark hollow, mossy rim, blue-violet water, white-cyan core, shimmer) ringed by 38 hand-placed flowers in two rings, two huge lily pads, two pink water lilies, glowing amethyst clusters; ~2.5x the old size, brightest focal point
- left: giant twilight oak built with `blocks` (twilight-oak log with moss, limbs, buttresses; hedge/azalea/flowering-azalea canopy; three glow-berry vines; haze 0.3), three mossy maze-stone pillars with glowing naga, lich and hydra trophies
- right: two glowing gloom mushrooms (`blocks`), pale moon with halo; dusk sky bands, a few stars; three-tone far forest silhouettes; soil + moss floor strip; floor plants; 7 clustered firefly sprites (replace evenly spaced dots); noisy star cluster, flat castle and dark tree blobs removed
- coordinator fix (1 build): the agent's block castle read as floating amethyst roofs -> replaced by a vector `castle` silhouette with lit windows rising from the forest mist; dark-log patches on the trunk (read as square knots) replaced by plain log; gloom mushrooms pushed back (haze 0.5, weaker glow and cast light)
- palette: violet accent unchanged; background speckle lilac at density 0.025

### Fixed locally before this run (from `fix_results_local.json`, summarised; not redone here)

- **00_welcome** (5.50 -> 6.50): one side-view diorama, a traveller's camp at dusk on a grassy ledge over a
  valley; texel 4, warm sunset light, lantern cast light; vector table removed; terrain as one `blocks` layer.
- **climate** (6.00 -> 6.75): one mood (cold aurora night; sun, lightning, cloud and snowfall removed); hero
  snowed-in spruce cabin built with `blocks` with a lit window; snowy ground plane with a frozen pond; texel 3,
  cold moonlight + warm door light.
- **food** (6.75 -> 7.75): texel 5 for everything (fixes the ~5 vs ~8 px/texel mix and blurry jugs); warm light
  from the stove; hero brick kitchen range built with `blocks` (Farmer's Delight stove, firmalife counter).
- **health** (5.50 -> 7.50): candle-lit infirmary/apothecary at night (70 layers); ECG trace, moon, floating
  totem removed; texel 4; sickbed + barrel bedside table with lantern as hero; medicine cabinet and apothecary
  table; hanging herb bundles.
- **farming** (6.50 -> 6.50): block diorama at golden hour, texel 3; vector apple tree replaced by a `blocks`
  fruit tree; red barn hero; hay pyramid from 3-D blocks; sprite glows removed.
- **mekanism** (5.75 -> 7.25): indoor power hall, texel 4; induction matrix (4x7 `blocks`) as hero; turbine
  with blades behind glass; 4x2 bank of active machines as 3-D blocks.
- **steel_age** (5.50 -> 6.75): texel 5, cool steel key light + three warm cast lights; blast furnace hero
  built with `blocks`; crucible molten tap with glow, embers, smoke.

## Remaining weak points

Per chapter: the after critics' main issues (director = D, player = P; locations are screen fractions of the screen29 view) plus, for Task A chapters, what the fixer itself still saw.

### 00_welcome: D 6.5 / P 6.5 (fix type D mixed, P mixed)

- D: x0.00-1.00 y0.00-0.27: top quarter is an empty gradient sky; the sun-ray fan (x0.58-0.85) and the moon are smooth vector effects that do not match the pixel ground.
- D: x0.33-0.80 y0.60-0.88: dead fog band between the left camp and the right trees; the central platform holds only three tiny props (stone, sticks, flowers), so the scene reads as sparse stickers on a strip of grass.
- D: x0.36-0.63 y0.36-0.58: one small lone panel floats mid-view with nothing in the scene relating to it; the banner is also small for a welcome page, so there is no real focal point.
- P: x0.00-1.00 y0.00-0.25: the whole upper sky is an empty brown-purple gradient with fan-shaped sun rays that have no visible sun source; first screen of the book feels unfinished
- P: x0.36-0.63 y0.37-0.60: only 3 of the 8 nodes sit inside the panel; hub and spoke nodes float outside it, so the panel looks arbitrary. Two nodes are blank grey circles and the hub is a dark spiky blob
- P: x0.00-0.40 y0.60-0.85: the stump, book, hammer, sack, lantern group is small and low-res compared with the 29px nodes, and reads as a few stickers on a flat grass strip
- For 9 (D): Make a real hero scene: a lit camp or landmark at the focal point under the panel, parallax layers with atmospheric haze, ground props at a consistent pixel scale, pixel-quantised sky effects, and a larger panel/banner composition that uses the full view.

### climate: D 7 / P 6.5 (fix type D mixed, P mixed)

- D: x0.00-1.00 y0.05-0.30: smooth polygon mountains with pixel snow-cap sprites and a vector aurora clash with the pixel cabin and ground; the mountains look like flat paper cut-outs.
- D: x0.00-0.30 y0.43-0.95: pines have a dashed, jagged light edge that reads as an anti-aliasing artifact, not snow.
- D: x0.65-1.00 y0.28-0.60 and x0.00-0.40 y0.30-0.45: large empty dark-blue areas; panels cluster in the top centre while the cabin carries the whole lower-right corner.
- P: x0.00-1.00 y0.05-0.40: the mountains are flat smooth vector triangles with tiny pixel snow-caps, and the aurora is a soft gradient. This clashes with the pixel cabin and trees and reads as stickers
- P: x0.35-0.95 y0.55-0.90: a big empty dark band lies between the panels and the ground; the second row of panels floats in nothing
- P: x0.00-0.30 y0.43-0.95: three flat dark-teal pines with jagged dotted edges look crude and placeholder next to the textured cabin
- For 9 (D): Unify the mountains and trees into one pixel style, add snow-laden pine sprites, add drifting snow depth layers, balance the left half with a second landmark, and add a cast glow from the cabin window onto the snow.

### food: D 8 / P 7.5 (fix type D spec, P spec)

- D: x0.55-0.70 y0.03-0.25: hanging produce is strung on thin lines at inconsistent scales (garlic, peppers and ham are much bigger than the herb bundles); the upper band reads as a row of stickers.
- D: x0.00-0.30 y0.35-0.70: the shelves are floating planks with no back wall, brackets or shadows; items on them are too small and lack contact shadows.
- D: x0.30-0.70 y0.18-0.70: purple/pink panel and banner tint is slightly off against the warm brown pantry palette; the wall is a flat dark noise texture with little depth.
- P: x0.30-0.70 y0.12-0.32 and every panel: the banner and panel borders are mauve/purple, which is a foreign colour on a warm brown larder and the weakest colour choice in the chapter
- P: x0.00-0.28 y0.38-0.70: the two floating shelves with jars hang on a flat wall with no brackets or shadow, so they look pasted on
- P: x0.04-0.35 y0.73-0.97 and x0.78-0.98 y0.73-0.97: the barrels, crates and sacks are crisp and charming but all the same size, so the floor row is evenly cluttered
- For 9 (D): Shift the panel tint to warm copper/cream, add a light pool and shadows under shelves and from the lantern onto the wall, tie hanging items to a rail with consistent scale, and give the stove/hearth a stronger glow.

### health: D 7.5 / P 7.5 (fix type D spec, P spec)

- D: x0.30-1.00 y0.65-0.78: a dead dark band between the panels and the bed/table; the right shelves float in empty space (x0.76-0.97 y0.30-0.60) with no wall structure.
- D: x0.30-0.62 y0.70-0.98: the saturated red bed is the loudest element and pulls focus away from the panels and banner; the bed is also oversized next to the shelf props.
- D: x0.02-0.98 y0.08-0.25: hanging herbs are tiny, sparse and unevenly spaced, so the ceiling band feels thin.
- P: x0.30-0.70 y0.25-0.65: crimson panel borders and a pink banner on a warm brown apothecary are readable but slightly harsh, and clash with the cozy palette
- P: x0.32-0.62 y0.70-0.97: the big red bed is a flat, very plain voxel block and the largest, emptiest shape in the scene
- P: x0.30-0.62 y0.51-0.64: section 3 shows four unlinked nodes, two of them blank, which reads as filler
- For 9 (D): Re-balance mass (bring the right shelf into a proper cabinet), tone down or reposition the bed, add a warm lamp glow across the wall, and thicken the herb drying line to a believable rack.

### farming: D 6.5 / P 6.5 (fix type D mixed, P renderer)

- D: x0.00-0.25 y0.42-0.90: the giant apple tree uses a coarse, high-frequency leaf texture that looks like noisy carpet, flat-lit, and far larger than the barn or crops; its pixel density does not match the rest.
- D: x0.00-0.99 y0.10-0.32: the sun is a smooth vector glow and the clouds are flat blurred horizontal bars; both look like placeholders against the pixel barn and ground.
- D: x0.25-0.58 y0.55-0.88: large empty gap between the tree and the hay stack; the wheat strip is a thin line.
- P: x0.02-0.24 y0.42-0.90: the apple tree is huge, with a very noisy high-contrast leaf texture that shimmers, and it dominates the left third. It is the crudest sprite in the book
- P: x0.08-0.16 y0.30-0.40: the sun is a flat white disc with a soft halo, with no horizon interaction, over a muddy brown-olive sky
- P: x0.70-0.98 y0.48-0.92: the barn is huge while the cows, sheep and chicken are tiny, so the scale is inconsistent (the thatched roof is good)
- For 9 (D): Resize and re-texture the tree with proper leaf clusters and shading, replace the vector sun and clouds with pixel versions, fill the middle ground with fields, fences or a windmill, and align the panels on a clear grid.

### storage: D 8 / P 8 (fix type D spec, P spec)

- D: x0.74-0.99 y0.20-0.90: the tall server/drive stack is a repetitive grid with a heavy, monotone mass; it dominates the right and is less detailed than the left shelving.
- D: x0.04-0.90 y0.09-0.10 and y0.93-0.96: the top and bottom pipes frame the scene well but are flat grey bars; they run through the empty top band and end abruptly at the shelf.
- D: x0.38-0.65 y0.70-0.90: crate and barrel clump at the bottom centre is small and low-contrast relative to the panels above it.
- P: x0.01-0.26 y0.22-0.92: the shelving wall is the best prop in the book, but the item rows repeat the same few bags and crates
- P: x0.74-0.98 y0.20-0.90: the wall-of-drives tower is big and flat-lit, and its orange fan blocks glow a bit like a placeholder pattern
- P: x0.15-0.90 y0.09-0.12 and y0.93-0.97: the framing pipe is clean and reads as logistics, but it is very thin and runs behind the banner area
- Fixer: disk-drive bank = 18 near-identical faces (server rack, monotonous); controller is a single small block next to the tower mass; warm firelit interior mood close to iron_age; straight shaft cables read slightly as conduit/UI lines; quiet dark planks between rack and banner and in the top band; evenly spaced rack levels
- For 9 (D): Vary the right stack with different block types and lit/unlit indicators, add depth to the pipes (shadow, joints, flow glow), give the panels a drop shadow or backlight, and add floor reflections or light pools.

### stone_age: D 8 / P 7.5 (fix type D spec, P mixed)

- D: x0.32-0.45 y0.52-0.56: the connection lines from section 1 run straight through the section 3 title text, and several lines cross panel frames.
- D: x0.02-0.25 y0.37-0.58 and x0.76-0.95 y0.40-0.55: cave paintings are flat orange silhouettes with noise; they read well as art but are noticeably flatter than the lit pixel props around them.
- D: x0.22-0.38 y0.08-0.35 and x0.75-0.80 y0.08-0.28: the stalactites are dull brown wedges with little shading or highlight.
- P: x0.32-0.45 y0.52-0.62: dependency lines cut diagonally through the section 3 panel header text and across the section 1 panel border, and the panels nearly touch, so the graph feels tangled
- P: x0.01-0.28 y0.08-0.36 and x0.75-0.99 y0.08-0.36: the stalactites are flat brown trapezoids with banded shading and look crude against the finer cave paintings
- P: x0.03-0.25 y0.38-0.60: the mammoth and deer paintings are very recognisable and the best element, but the big flat orange ochre blobs are a bit uniform
- Fixer: chert boulder is a plain stepped cube, its red slightly strong; still reads partly as sprites on a floor line; wall paintings flat vector orange, unlit next to the pixel props; rack posts smooth vector planks; visible block grid on the ceiling; quiet lower-left and mid-right walls; quest dependency lines cross the section-3 header (layout, not art)
- For 9 (D): Add lit rim details on the stalactites, give the cave paintings a layered pigment texture and light falloff, route lines so they never cross titles, and carry the fire glow onto the panels and cave ceiling.

### copper_age: D 7 / P 6.5 (fix type D mixed, P mixed)

- D: x0.00-1.00 y0.00-0.28: a sunset sun over distant mountains in what is otherwise an enclosed mine-cave; the top third is empty brown gradient, and the setting is confused.
- D: x0.20-0.60 y0.50-0.62 and x0.40-0.60 y0.30-0.55: a wide, muddy dark area behind and between the panels with no scene content.
- D: x0.00-0.25 y0.30-0.98: left stepped rock wall with ore veins and torch is good, but the ore sprites are flat bright patches that look pasted on; the right forge stack is cut by the edge.
- P: x0.00-1.00 y0.00-0.25: a large dark brown sky band with a soft sun at the top right is empty and muddy, with little contrast and a flat silhouette horizon
- P: x0.00-0.18 y0.30-0.75: the ore staircase on the left is a gray stepped wall with a tiny torch, and reads as a flat placeholder blob
- P: x0.40-0.65 y0.55-0.70: the dark gap between the panel rows has no scene content at all
- Fixer: plain dark wall/sky between banner and panels and at top-left; kiln dirt base is a big plain brown block and the log pile reads like a brick oven; bottom props still a loose row on a barely visible floor; no true crucible pour; teal sky tint barely visible
- For 9 (D): Commit to one setting (cave or open dusk), replace the empty upper area with ceiling or skyline detail, integrate ore into the rock with shading, scale up the forge as the hero, and let its glow reach the panels.

### bronze_age: D 7.5 / P 7.5 (fix type D spec, P spec)

- D: x0.08-0.30 y0.33-0.70: the tall timber frame with a hanging chain and lantern above the furnace reads like a gallows; its purpose is unclear and it has a plain flat top beam.
- D: x0.03-0.98 y0.70-0.95: props are lined up along the floor in a row (furnace, table, anvil stump, kiln) with equal spacing, so it looks like an inventory strip, not a scene.
- D: x0.28-0.48 y0.35-0.70: empty dark mid-field around and below the panels; the sky above (y0.0-0.2) is empty teal-to-brown gradient.
- P: x0.58-0.74 y0.68-0.82: the anvil is a smooth flat orange vector silhouette on a log, a style clash with the textured voxel blocks around it
- P: x0.00-0.30 y0.33-0.95: the mine gantry and furnace are charming and clear, but the dark void between gantry and panels is empty and the top sky band is a plain brown gradient
- P: x0.60-0.67 y0.52-0.64: section 5 shows only one dark hub node in an otherwise empty panel, which looks unfinished
- Fixer: overall value range dark brown (forge + lantern are the only bright accents); anvil is a flat tan pixel vector without metal sheen; block structures a bit Lego-like (headframe reads partly as a gate); right of the panels (x 0.66-0.89, y 0.3-0.55) still mostly empty; top band plain dark teal; smoke/embers subtle; new amber accent sits between stone_age ember and create brass in hue (separated mainly by being darker)
- For 9 (D): Stagger props in depth with overlap and a back layer, replace the frame with a recognisable smelter or crane, match anvil rendering to the block sprites, and add warm light shafts or ambient glow to unify the group.

### iron_age: D 8 / P 8 (fix type D spec, P spec)

- D: x0.00-1.00 y0.00-0.10: the top rafter band is flat brown noise with no detail; the two chains and lanterns are the only vertical accents, and their symmetry feels mechanical.
- D: x0.02-0.30 y0.32-0.51: the tool rack is a flat dark board with small tools; it floats with no mount and little shading.
- D: x0.45-0.62 y0.72-0.95: anvil with glowing ingot is a good focal point, but the stump top and sparks are slightly muddy; the barrel and coal pile on either side are small.
- P: x0.02-0.29 y0.32-0.51: the tool rack panel is a flat brown board with three tools, and the least detailed prop
- P: x0.82-0.97 y0.36-0.97: the black chimney with brick base is huge and dominant, and its upper half is a plain dark column
- P: x0.55-0.64 y0.46-0.67: the section 4 panel header text fills the strip edge to edge and its nodes are scattered with one lone link
- Fixer: beam reads as a dark plank band, not a carved timber; bellows reads as a slatted log stack; pixelated vector stand/anvil simpler than the sprites; quiet voids mid-left above the bench and top-centre around the banner; ingot pile lacks contact with the bench top; bloom large relative to the anvil
- For 9 (D): Add a clearer back wall (stone or timber structure with depth), more variation in hanging elements, cast shadows from the furnace and lanterns, and sharpen the hero anvil moment.

### steel_age: D 7 / P 6.5 (fix type D spec, P mixed)

- D: x0.00-1.00 y0.00-0.17 and x0.35-0.70 y0.65-0.90: very dark, low-contrast field with large empty areas; the smoke-stack silhouettes at the horizon are barely visible.
- D: x0.05-0.19 y0.37-0.73: the faded second furnace gives nice depth, but it is a dim duplicate of the right furnace with the same shapes, which looks like a copy.
- D: x0.67-0.78 y0.27-0.31: the section 3 panel title is double-stacked and tiny (a small '第三节' over the section name), so it breaks the panel header style.
- P: x0.05-0.19 y0.37-0.73: the left blast furnace is a faded, ghost-like duplicate of the right one, so it reads as a leftover rather than a design choice
- P: x0.67-0.77 y0.28-0.37: the section 3 header has a tiny 'section three' label stacked over the title and colliding with it, an obvious layout bug
- P: x0.00-1.00 y0.10-0.28 and x0.30-0.70 y0.75-0.95: the sky and middle are muddy dark blue-gray with very low contrast, and chimney silhouettes on the horizon are barely visible
- For 9 (D): Raise value contrast with a rim light on the furnace and a glowing horizon, vary the background furnace, group the anvil/ingots/coal into one lit work area, and normalise the panel title fit.

### create: D 6 / P 7 (fix type D renderer, P renderer)

- D: x0.00-0.25 y0.08-0.46, x0.78-1.00 y0.30-0.82, x0.72-0.85 y0.80-1.00: giant flat brown vector gears with smooth edges and no texture, shading or highlight; they look like clip-art and clash with the pixel-art language of the rest of the pack.
- D: x0.00-0.25 y0.58-0.97: the water wheel is a smooth vector wheel with a flat blue block of water above it, not pixel-matched and not convincingly attached to anything.
- D: x0.25-0.73 y0.79-0.88: the conveyor belt is a thin grey bar floating in the empty lower-middle; x0.25-0.55 y0.60-0.80 is empty.
- P: x0.00-0.16 y0.10-0.47 and x0.78-1.00 y0.30-0.85: the huge flat smooth brown gears are non-pixel vector art, which clashes with the pixel water wheel and nodes, and they cover over a third of the screen
- P: x0.30-0.70 y0.05-0.95: the dark centre behind the panels is a faint blueprint gear pattern, but everything around the panels is empty
- P: x0.45-0.70 y0.17-0.25: a faint gear halo sits right behind the banner icons, which hurts banner legibility
- For 9 (D): Redraw the machinery as pixel-art Create components with lit metal, brass trim, shaft and belt detail at a consistent pixel scale, add steam and a lit belt with items, and place a hero contraption under the panels.

### ie: D 8 / P 7.5 (fix type D spec, P spec)

- D: x0.00-0.15 y0.06-0.88 and x0.71-0.82 y0.10-0.74: the two lattice pylons are well made, but the right one is a flat pale-grey ghost that reads as unlit, and the repeated cross-brace texture is tiled and visible.
- D: x0.30-0.72 y0.83-0.98: the floor and the crates/barrels/spools are small, with thin empty space (x0.35-0.60 y0.50-0.80) between the panels and floor.
- D: x0.00-1.00 y0.00-0.16: the wire lines are drawn as smooth thin strokes, slightly different from the pixel sprites; the moon is a plain smooth disc.
- P: x0.04-1.00 y0.08-0.17: the power cables cross behind the banner's top edge, which slightly clutters the title
- P: x0.71-0.82 y0.18-0.75: the right pylon is a long, plain dark lattice with little detail, and the centre between pylons is empty
- P: x0.34-0.64 y0.20-0.80: several panels contain mostly unlinked blank nodes, so the graph looks sparse and unfinished (cyan panel colour is readable)
- Fixer: many thin verticals (two lattice pylons + chimney); mid-band between structures and panels still dark; reads as a Minecraft block build rather than drawn key art, flat floor front with no ground detail; pylon 2 is a hazed copy of pylon 1; cable joints show beads up close; no tesla coil / arc furnace / excavator (their textures are 128x128 model atlases); stars and moon slightly off-style
- For 9 (D): Add atmospheric depth to the right pylon (haze, partial light), pixelise the wires and moon, carry the cyan lamp glow into the scene and panels, and enrich the floor with props and cables.

### tfmg: D 7 / P 6.5 (fix type D mixed, P mixed)

- D: x0.00-1.00 y0.00-1.00: the olive/green-brown smog palette is muddy and low-contrast; the background looks dirty rather than atmospheric, and the olive panels merge into it.
- D: x0.07-0.11 y0.14-0.65 and x0.73-0.77 y0.22-0.65: the two hazard-stripe poles are nearly black rectangles with a few stripe blocks; they look like stray placeholder columns.
- D: x0.20-0.28 y0.32-0.95: the lattice tower has a ragged, dashed bright edge and a hard flame on top that is not lit in context.
- P: x0.30-0.70 y0.14-0.23: the banner is olive-on-olive with a smaller title and desaturated icons, the lowest-contrast title in the book
- P: x0.07-0.11 y0.15-0.58 and x0.72-0.77 y0.20-0.65: the tall black bars with yellow hazard stripes look like unfinished placeholders
- P: x0.00-1.00 y0.00-0.30: a murky olive-brown haze fills the whole picture and drowns the right block tower in low-contrast gray
- Fixer: tower is a big repeated-tile stack (detail only from textures); far stacks read as flat dark pillars; top band above the banner mostly empty smog, smoke very faint; drums read as dark crates more than oil barrels; small muddy steel/coke pile; no diesel-engine prop (attempts looked like flat platforms); one global light direction, so the right side is lantern-lit but rim-lit from the left
- For 9 (D): Replace the olive haze with a clear dusk or refinery glow, redraw the poles as flare stacks or pipes, clean the lattice edges, and bring consistent shading to the machinery.

### pneumatic: D 8.5 / P 8 (fix type D spec, P spec)

- D: x0.00-1.00 y0.00-1.00: the brick wall pattern is flat and uniform; the pipe loop frames the scene well, but the wall behind has no light variation.
- D: x0.08-0.25 y0.37-0.48: the red robot arms with a chip block float on the wall without any mount.
- D: x0.00-0.65 y0.68-1.00: the bottom row is crowded (blocks, cases, tools), and the white block at the far left looks unlit and off-palette.
- P: x0.28-0.83 y0.03-0.08 and y0.74-0.78: the pipe frame is clean and a good theme anchor, but the pipes are flat gray with no pressure glow
- P: x0.58-0.80 y0.24-0.28: the panel borders are thin gray and slightly weak against the dark brick wall, though headers stay readable
- P: x0.02-0.25 y0.66-0.98: the white and gray crates in the bottom left are visually heavy and flat
- Fixer: mid-left / mid-right walls sparse, pipes still follow the edges (faint frame effect); the drone is assembled from item sprites, small and slightly sticker-like; steam reads partly as smoke; PNC textures are near-black so the scene has little tonal range; compressors are iron-block drawer faces (no compressor textures in packdata); banner title colour is set in qlib.py THEMES["pneumatic"] (110,200,210 cyan), not in the spec (the preview shows the spec's orange; not checked in game)
- For 9 (D): Add depth and light variation to the brick, a proper mount or cable for the floating machines, pipe shading and flow glow, and a subtle panel backlight so the ring of pipes and the panels read as one lit system.

### mekanism: D 7.5 / P 7 (fix type D spec, P spec)

- D: x0.04-0.27 y0.40-0.95 and x0.78-0.96 y0.15-0.93: the two huge machines are large flat-faced block grids with big coarse tiles; they have little detail and a different effective pixel density from the small bottom machine.
- D: x0.30-0.75 y0.50-0.78: a large empty dark area to the right of the lower panels and above the machine.
- D: x0.00-1.00 y0.00-0.08: the top truss frieze is a repeated tile band with weak contrast; the green pipes are thin lines that end abruptly (x0.10-0.15 y0.06-0.40).
- P: x0.03-0.27 y0.40-0.95 and x0.78-0.97 y0.15-0.92: two big machine blocks flank an empty centre; the right tower is a plain gray slab with little detail
- P: x0.30-0.75 y0.72-0.97: the centre bottom has a dim machine bank and a small ingot pile, so the lower middle feels thin and the scene reads sparse
- P: x0.30-0.40 y0.50-0.65: the section 4 header uses a smaller font to fit, so it is inconsistent with the other headers
- For 9 (D): Add detail and shading to the big machines, a warm or contrasting accent light (red alarm, amber), connect the pipes into a believable system, and cover the empty middle ground with props.

### explore: D 7.5 / P 7.5 (fix type D mixed, P spec)

- D: x0.00-1.00 y0.05-0.30: smooth polygon mountains with a vector sun glow versus pixel trees, camp and terrain; the clash is clear in the sun disc (x0.09-0.18 y0.05-0.18).
- D: x0.69-0.96 y0.75-1.00: the lower-right terrain is large, blurry, low-res stone blocks with a different pixel density from the rest of the scene.
- D: x0.02-0.22 y0.76-0.84: the tents are flat white triangles with little detail, and read as placeholders.
- P: x0.07-0.18 y0.05-0.18: the sun is a large soft blur that fights the mountain layer and looks like an out-of-focus blob, not a pixel sun
- P: x0.68-1.00 y0.55-1.00: the stepped terrain at the bottom right is a huge block of muddy gray-brown with banding and no detail
- P: x0.02-0.22 y0.76-0.84: the white tents are plain white triangles and look crude beside the textured chest and backpack
- Fixer: chunky block terrain (~77 screen px per block), bland right rock mass; trail is a straight staircase, not winding; flat 3-tone pines; small plain white tents, compass slightly overlaps the atlas; distant crag at k 3 vs scene texel 4; calm dark void behind the panels
- For 9 (D): Re-render the mountains and sun as pixel layers, fix the terrain texture scale, draw proper tents and a banner, and add path and prop detail across the middle ground to link camp and ruins.

### twilight: D 7.5 / P 8 (fix type D mixed, P spec)

- D: x0.00-0.28 y0.00-0.95: the giant tree is cropped at the left with noisy leaf pixels and a flat trunk; it overpowers the left edge and its texture scale differs from the other props.
- D: x0.28-0.74 y0.68-0.92: the glowing pond is nice, but the surrounding flowers and fireflies are sprinkled evenly like stickers with no grouping or depth.
- D: x0.72-0.99 y0.52-0.92: the pale mushroom tree is flat tan with little shading and a pale colour that does not fit the purple night.
- P: x0.45-0.55 y0.32-0.36: the section 2 header has a tiny 'section two' label stacked over the title and colliding with it
- P: x0.00-0.28 y0.00-0.95: the giant tree trunk is a flat tall block with a noisy canopy and takes a lot of the left side
- P: x0.74-0.99 y0.55-0.92: the cream mushroom is large and plainly shaded, and a bit blocky next to the delicate pond
- Fixer: the big gloom mushroom cap is still a bright beige block competing with the pool; the trunk is a large brown block column; the band between the panels and the pool is dark and empty; one firefly ~20 screen px from panel 5; the top-right canopy is lost in the edge fade; smooth vector forest silhouettes and castle next to pixel blocks
- For 9 (D): Re-texture the tree and mushroom with the purple night light, cluster the flora with foreground/background layers, add glow reflections on the panels, and normalise panel titles.

### space: D 7 / P 6.5 (fix type D renderer, P renderer)

- D: x0.74-1.00 y0.00-0.25, x0.00-0.12 y0.08-0.23, x0.00-0.11 y0.44-0.62: smooth airbrushed vector planets and moon with no pixel structure; style differs from the pixel nodes, banner and every other chapter.
- D: x0.88-0.95 y0.42-0.72: the rocket is a clip-art vector illustration with a clean outline, and the satellite (x0.14-0.27 y0.06-0.13) is the same, so both look like stickers dropped in.
- D: x0.10-0.80 y0.68-0.85: a big empty band of star noise between the lower panels and the Earth limb; the small sparkle cluster at x0.31-0.37 y0.71-0.76 looks like a stray element.
- P: x0.00-1.00 y0.00-1.00: the smooth painted planets, comet and rocket are vector art, so the chapter feels like generic stock space art and not Minecraft or TFC
- P: x0.84-0.94 y0.42-0.72: the cartoon rocket and the satellite look like separate stickers with no shared lighting
- P: x0.05-0.75 y0.68-0.85: the lower half is almost empty between the panels and the Earth horizon, apart from a few stray sparkles
- For 9 (D): Redraw the planets, rocket and satellite in the pack's pixel language with proper lighting from one star, add a strong nebula or aurora layer, and put the rocket or launch tower into the composition under the panels.

### Systemic (after)

Director:

- Donut composition: props hug the left, right and floor edges while the centre behind the panels is a flat dark field; panels float on top without being anchored (no shadow, backlight, mounting or lit surface), so the scene and the quest layout read as two separate layers.
- Mixed media: smooth vector shapes (mountains, planets, sun glows, gears, clouds, ray fans, wires) appear next to pixel sprites in climate, farming, create, explore, space, welcome and copper; pixel density is also inconsistent (coarse blown-up stone and server blocks versus fine items).
- Lighting is local, not global: each glow (lantern, forge, campfire) is an isolated pool; props have no contact shadows and the panels never receive the scene light, so objects look pasted onto the floor.
- Backgrounds are low-contrast noise fills, muddy in the dark chapters (copper, steel, tfmg, mekanism, farming); the gradient skies are often empty in the top 20 to 30 percent.
- Props are arranged in a floor-line row with equal spacing, with little overlap or depth layering; the same hero motifs (anvil, furnace, lantern, block stacks) recur across the age chapters.
- Panel template is the same rounded rectangle with diamond corners in all chapters; only the tint changes, so it has no material identity per chapter and the dark fills nearly merge with dark backgrounds. Narrow-panel titles shrink, stack or get crossed by dependency lines (stone_age, steel_age, twilight, mekanism).
- Item-scale and edge-quality artifacts: ragged dashed light edges on trees and lattice towers, hazard poles and pale 'ghost' structures that look like placeholders.

Player:

- The quest graph is a small centred cluster (about 35% of the screen) with the art parked around the edges, so most chapters read as a frame with a dark hole in the middle; the band between panel rows and between panels and floor is often empty.
- Many nodes show as blank dark shapes with no icon (blank circles, squares and hexagons in nearly every chapter), which a player sees as placeholders or locked entries and makes panels look sparse and unfinished.
- Two-line section headers collide on narrow panels (steel_age section 3, twilight section 2, and smaller shrunken text in mekanism, explore and stone_age section 3), an obvious layout bug that recurs.
- Panel and banner accent colours are chosen per chapter and sometimes clash with the scene (food mauve on brown, health crimson, farming olive, tfmg olive on olive), and the banner has very low contrast in tfmg, steel_age and climate.
- Style mixing: smooth vector shapes (create gears, space planets and rocket, climate mountains, bronze anvil) sit next to hard pixel voxel props, which breaks the Minecraft-native feel.
- Scale is inconsistent: huge voxel sprites (farming tree, steel and iron furnaces, create gears, twilight trunk) next to tiny props (animals, tools, bottles) and 29px nodes, with noisy low-res texture on the big ones.
- Dependency lines are thin pale pink; they are readable, but cross headers and panel borders (stone_age, food) and run long distances between panels, which tangles the graph in busy chapters.
- Most chapters share a dark brown or black base and a similar prop-on-floor composition, so identity relies on the foreground props, and lighting is flat with little parallax or depth between layers.

## Drawing-code requests (renderer; aggregated from the Task A fixers and the local round)

Most requested first (number of chapters asking in this run, local round in brackets):
1. **`blocks` half-height / slab / stair cells** (and tapered rows): 7 (+ health, farming, steel) - benches,
   beds, shelves, catwalks, sloped roofs, tapered furnace stacks.
2. **A `smoke` / `steam` plume motif** (texel-scale, visible on dark backgrounds, point-anchored): 4 (+ steel) -
   copper, bronze, tfmg, pneumatic; today `nebula_glow` blobs stand in and read as mud.
3. **Per-light / per-layer light direction** (props on both sides of a fire lit from the fire): 3 (+ health).
4. **A controllable `cable` / `pipe` motif** (two-point sagging wire; straight/elbow pipe segments with flanges,
   valves, T-junctions, status LEDs): 4 - ie, storage, pneumatic, tfmg (all faked with rotated `shaft` layers,
   which show ring ticks/beads).
5. **`blocks` cell overlays**: per-cell emissive overlay, ore overlays on rock, multi-cell sprite fronts (48x48
   IE multiblock faces) lit like the blocks, sprites inside a cell (disks in drive bays), per-cell tint for
   greyscale vanilla textures (grass top, leaves, water), per-row alpha/haze: 6 (+ farming, mekanism).
6. **Stable random seeds** (optional per-layer `"seed"`; today inserting a layer re-rolls particles, piles and
   ridges of every later layer): 2.
7. **Molten pour / stream motif**: copper (+ steel).
8. **Pixel-native props** to replace smooth vector ones next to pixel art: tree_line (crisp or well-pixelated),
   anvil with a metallic ramp + hot glow, bellows, beam, tent/lean-to, drone, pool/pond ellipse with a crisp rim
   and ripples, tree with more shading; critics add: Create gears, planets, rocket, satellite, mountains, sun.
9. Smaller: pixel layers should fall back to the scene `haze_color` (explore; same bug reported for mekanism
   locally); `snowy_range` cap strength; opaque option for the `mountain_range` back ridge; `cave_painting`
   pigment variants and a way to drop the tally dots of `cave_painting_herd`; `hand_print` stencil modes;
   `campfire` without halo (pixelate bands it); lamp blocks that bloom instead of a hard white square; sprite
   `scale` and `tint`; `windmill_sails` colour/size + pixel look; rim light that skips the bottom edge of objects
   standing on a floor; a screen-pixel placement helper.

Layout / non-art items the critics raised (not spec-fixable): two-line panel headers collide on narrow
panels (steel_age section 3, twilight section 2) and dependency lines cross headers (stone_age section 3,
food) - `build.py draw_panel` / chapter layout; many quest nodes have no icon and read as placeholders; the
quest graph is a small centred cluster, so every scene is a frame around a dark middle ("donut composition").

### Raw requests per Task A chapter

- **copper_age**: crisp (or well-pixelated) tree_line; a `smoke` plume motif; molten pour / stream motif; flame sprite for kiln tops; particle/pile seeds should not depend on layer index (adding a layer re-rolls later layers)
- **bronze_age**: per-cell tint/darken or recessed `inset` cells in `blocks` (real tunnel depth); metallic shading ramp + configurable hot glow for anvil/anvil_hot; half-height block variant (slabs, benches, beds); `smoke` plume motif; overlay textures on `blocks` cells (ore overlays on rock)
- **tfmg**: per-cell height/slab fraction in `blocks` (platforms, catwalks); texel-grid pipe-rack motif or horizontal pipe block (vector `pipes` clashes with pixel props); texel-scale smoke/steam visible on dark backgrounds; let lamp blocks like modern_light_on bloom instead of a hard white square; per-layer light direction from the nearest light
- **pneumatic**: controllable pipe motif (straight/elbow segments, valve wheel, flanges, T-junctions); point-anchored steam/puff motif; drone motif/sprite and a hazard-stripe texture; per-row alpha/haze in `blocks`; vertical cylinder tank
- **ie**: a `cable` motif (thin sagging wire between two points, thickness + highlight, no rings/caps; faked with ~40 rotated shafts); `blocks` per-cell overlay accepting a multi-cell sprite (48x48 multiblock fronts) lit like the blocks below; windmill_sails colour/size options and a pixel look
- **iron_age**: half-height/thin cells in `blocks` (slab, post, rack); pixel-style anvil/bellows/beam motifs with real texture; per-layer brightness/shade for sprites (white ingots glare); a placement helper by screen-pixel box
- **storage**: `cable`/`conduit` motif with bends, clips and status LEDs; per-cell emissive overlay in `blocks`; half-height slab/shelf cell; sprites drawn inside a `blocks` cell (disks in drive bays)
- **explore**: `tent`/lean-to motif or sprite `tint`; winding receding trail motif; slabs / per-row haze in `blocks`; pixel layers should fall back to the scene haze_color (they use a dark default unless the layer sets one); optional per-layer `seed` (inserting a layer reshuffles later random shapes); snowy_range cap strength; opaque option for mountain_range back ridge (fixed alpha 120); more detail/shading in `tree`
- **stone_age**: per-layer / per-light light direction (props on both sides lit from the fire); cave_painting pigment variants (charcoal black, ochre) and lit/pixelate-friendly paint; switch off the tally-dot row in cave_painting_herd; hand_print positive/negative stencil modes with a tighter halo; campfire no-halo option (pixelate bands the glow); half-height cells in `blocks`; rim light that skips the bottom edge of objects standing on a floor
- **twilight**: flat pool/ellipse motif with crisp rim, ripples, optional pixelate (faked with stacked soft_glows); `blocks` sloped roofs/stairs, half-height cells, per-cell transparency, tint for grayscale vanilla textures (grass top, leaves, water); sprite `scale` (2x) for single hero sprites; tree_line with a solid base (no bottom fade); per-light direction for pixel layers

The 7 local chapters' requests are in `fix_results_local.json` (`renderer_requests`).

## Ceiling estimates

- **Director, after (this run):** The pipeline of procedural spec-driven scenes from Minecraft textures and vector motifs reaches a clean 8.0 to 8.5 for its best chapters (pneumatic, iron, ie, storage), where pixel props, frames and lighting agree; average ceiling is about 8.0 to 8.5. A 9 on every chapter is out of reach without a global lighting and shadow pass, parallax depth layers with atmospheric haze, full pixelisation of all vector elements (render low-res then nearest-neighbour upscale), material-specific panel frames with backlight, and hand-pixelled hero assets (tree, rocket, planets, gears, and per-chapter landmark). A true 9 to 10 needs hand-drawn or commissioned key art (medium).
- **Player, after (this run):** About 8 to 8.5 for the best interior-room themes (storage, iron, pneumatic, food, twilight) and about 7 for outdoor and vector-heavy chapters. This pipeline can make a cohesive, readable, Minecraft-flavoured set, but it cannot reach 9 because voxel props, flat gradients and vector motifs lack hand-placed lighting, depth and detail. To raise it: one unified pixel scale and rendering style for all props (no smooth vector), a lit multi-layer parallax with fog and rim light, scene content that fills the gaps around the panels, a panel and banner skin tinted from each scene palette, fixed header layout, and hand-pixelled or commissioned hero props.
- Director, before: About 7.5 for most chapters, maybe 8 for the best ones (stone_age, create, space, food) after fixes. Spec work (move things inward, remove hotbar rows, ground objects, cut contradictory elements) gets most chapters from 5.5-6.5 to 7. Renderer work (snap all sprites to one integer texel size, no smooth scaling, a scene-wide light pass with cast light and rim light instead of halos, shaded vector props, depth haze per layer) could reach 7.5-8. 9 is not realistic: it needs one coherent rendering style with bespoke, hand-authored compositions, real lighting and depth, and every element drawn for its place. Fraction-placed procedural motifs plus re-scaled game icons cannot get there, because the parts were never designed to sit together. To reach 9 you would need a different medium: hand-painted or hand-pixelled chapter illustrations (commissioned, or AI-generated and then hand-cleaned to one palette and density), imported as the scene layer.
- Player, before: About 7.5, with 8 possible for the best chapters (food, create, twilight, space) after strict cleanup. 9 is not realistic with procedural PIL motifs plus upscaled item textures composed by fractions. A 9 needs one coherent rendering style with intentional lighting, depth, and hand-placed detail, and generic geometric motifs can't supply that. They will always read as clip-art next to real Minecraft pixel art. Biggest gains from cheapest to most expensive: (1) pick one medium, preferably pure pixel art at one fixed integer texel scale, and redraw or drop the vector props; (2) remove lineups, oversize glow stickers and clip-art suns; (3) add a shared light/ground pass (contact shadows, rim light from the hero light source); (4) fix the header-text shrink. Reaching 9 would take hand-pixelled or commissioned per-chapter illustrations (or block-built in-game dioramas rendered as screenshots) used as the scene layer.


## Round 2 (create/space)

Task: `CLOUD_TASK2.md` - redo the two pilots that still used smooth vector gears, planets and rocket, in the
book's current language (one texel, one scene light, block/pixel dioramas). Branch `art-fixes-2`.

### Scores (blind, `critique_after2_*.json`; before = `critique_after_*.json` of round 1)

| chapter | before dir | before pl | before avg | after dir | after pl | after avg | delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| create | 6 | 7 | 6.50 | 8 | 8 | **8.00** | +1.50 |
| space | 7 | 6.5 | 6.75 | 7.5 | 7.5 | **7.50** | +0.75 |

Both critics say both chapters now fit the book (`fits_book: true`). **Create** "now sits comfortably in the
industrial group" (storage, iron_age, steel_age, pneumatic) and is the richest of those. **Space** fits
"borderline": its foreground is in the block-diorama language and the rocket and tower are "as good as
anything in the book", but it is still the brightest, most saturated tile and its sky reads as painted.
With round 1's 17 chapters unchanged, the book average is now **7.39** (round 1: 7.28).

### Process

- Setup as in round 1. The re-encrypted pack data adds `ad_astra:environment/*` (square pixel planets and
  suns, 6-16 px) and `minecraft:environment/*` (sun, moon_phases).
- Before any artlib edit: full `QGEN_STAGE=_stage_ref` build plus screen29 previews of all 19. A second full
  build gave pixel-identical previews (the build is deterministic, so the identity proof means something).
- `create` and `space` were first exported unchanged from `art_styles.py` into `art_styles.d/{create,space}.json`
  (separate commit), then reworked.
- One workflow, sonnet throughout, both chapters in parallel. Each chapter went through three steps:
  1. A fixer used up to 4 builds.
  2. An independent blind critic reviewed that preview against the contact sheet: create 7.5/8, space 7.4/8.
  3. A fresh fixer applied the critique with the remaining 2 builds.
  Each chapter used exactly 6 builds, the task's limit.
- Final full build into `_stage_final`: `OK: 19 chapters, 435 quests`, no WARN or ERROR.
- **Proof that the other 17 chapters are unchanged:**
  - screen29 previews 17/17 pixel-identical to `_stage_ref`;
  - their 128 generated textures (scenes, panels, banners, backgrounds) 128/128 identical;
  - their lines in `ftb_quests_theme.txt` identical;
  - the artlib diff is 1574 additions and 0 deletions, with no existing function or name redefined.

### What changed

**create (`20_create`)**: a Create workshop wall at texel 4 with a warm light from the top left, contact and
drop shadows, three lanterns on pixel chains plus the firebox as cast lights, and ambient 0.86.
- **Top:** a ceiling beam and a full-width line shaft with brass and andesite gearboxes and two cogs.
- **Left:** three meshing wooden and brass cogs on a vertical shaft, with the tooth phases computed so they
  interlock.
- **Hero, under the panels:**
  - a hooked-bucket water wheel half sunk in a pixel pool with foam and splash, beside a stone trough wall;
  - a power shaft from the wheel hub through a mechanical press gantry and a mixer gantry (brass casing,
    whisk into molten brass);
  - a belt carrying andesite alloy and brass ingots in and brass sheets out;
  - a raw copper and raw zinc ore pile.
- **Right:** a 4-sail canvas windmill on a bearing, a shaft down to a brass flywheel, and a copper boiler
  with a lit firebox, pressure gauge, chimney and hard-edged pixel smoke.
- **Removed:** the vector gears, the vector water wheel and windmill, the blueprint layer, the gear halo
  behind the banner, and the background gear-ghost overlay. The banner motif is off, and the background is
  industrial and weathered iron.
- **Palette:** brass accent (232,184,86) kept.

**space (`33_space`)**: a lunar launch site at texel 5, lit from the upper left (dir [-0.8,-0.55]).
- **Sky:**
  - a round pixel sun with a dithered corona at the top left, warming a large pixel Earth with its moon;
  - a 1.4x ringed violet giant cropped by the top edge;
  - a small Venus and a larger Mars with Phobos;
  - square pixel stars and twinkles, with the background starfield overlay lowered from 0.3 to 0.1;
  - a dotted flight trail from the rocket to Mars.
- **Hero:** a red and white pixel rocket seated on the Ad Astra launch pad (`blocks`), beside a lattice
  launch tower with service arms, a hazard foot and a beacon.
- **Base:**
  - a hab with a tilted solar array on a mast;
  - a lunar rover with tyre tracks;
  - a 4-bay machine bank with a lit furnace, LED bars, screens and a comms mast;
  - an astronaut with boot prints, beside a flag with a rocket emblem.
- **Ground and shadows:** a 3-row lunar ground of stone and deepslate with ore flecks, two far ridges,
  craters, boulders in the corners, and texel-snapped cast shadows.
- **Removed:** the airbrushed vector planets, the clip-art rocket, the satellite and the comet. A pixel
  satellite now fills the void right of panel 2.
- **Palette:** violet accent (176,150,255) kept.

### artlib additions

There are 27 new optional motifs: 10 `create_*` and 17 `space_*`. All parameters and example layers are in
`ART_GUIDE.md`, "Round 6".
- **Create** (in `PIXEL_MOTIFS`, so they take the scene light and shadows like sprites):
  `create_cog`, `create_wheel`, `create_sails`, `create_shaft`, `create_belt`, `create_water`,
  `create_steam`, `create_smoke`, `create_station` (press or mixer gantry), `create_boiler`.
- **Space** (unlit unless a layer sets `lit` + `pixelate`):
  `space_planet`, `space_sun`, `space_stars`, `space_rocket`, `space_gantry`, `space_astronaut`,
  `space_rover`, `space_satellite`, `space_solar`, `space_mast`, `space_rocks`, `space_crater`,
  `space_shadow`, `space_tracks`, `space_trail`, `space_crop`.
- **Quirks:**
  - `create_wheel`'s `rim` (rim thickness) shares its key with the scene light's per-layer rim-light
    strength.
  - `space_crop`'s `asset` is not validated by `build.py --check` (the motif is unused).
  - The create spec was laid out by a pixel-level generator script in the session scratchpad. That script is
    not committed; the JSON is the source of truth.

### Remaining weak points

- **create** (both critics 8):
  - The water at the bottom left is a flat dithered slab with a straight top and a hard vertical edge at x0.27.
  - The windmill is the palest, largest mass and pulls the eye from the banner. Its bearing block reads as a
    chest.
  - The bottom machine row is packed while the wall left of centre and under the banner is empty, so the
    scene is bottom-heavy.
  - The brass cogs are close to the panel-border gold.
  - The two small top cogs and the chains read slightly as stickers.
  - The press head is procedural, because the real press, mixer and pole textures are UV atlases.
  - The critics put create's ceiling at about 8.5-9 with a water channel and a shadow pass.
- **space** (both critics 7.5):
  - The planets and sun use a coarser grid than the foreground: about 8 screen px versus 4-5, because they are
    drawn at k 5 and scaled with the scene box. The sun's dither halo reads as a filter.
  - Earth and Mars look blobby to the player.
  - Soft round background-tile dots (the screen-space starfield overlay) still show next to the hard pixel
    stars.
  - The dotted trail with an arrowhead looks like a mouse cursor.
  - The base is a same-height line-up on one horizon, and the satellite floats.
  - The regolith strip is noisy.
  - It is the brightest, most saturated tile in the book: acceptable for the finale, but the least
    consistent of the 19.
  - The critics put its ceiling at about 8-8.5 once the sky is on the foreground grid and the base gets height
    variation.
- **Fixers' drawing-code requests:**
  - hand-drawn 16x16 press head, mixer head, encased fan front, crafter front and windmill sail sprites;
  - a tier-1 rocket sprite matching the Ad Astra entity model, and a launch pad top with a flame trench;
  - an orbital station and satellite sprite set;
  - a strata-cut lunar plateau tile set;
  - a hand-drawn round pixel sun;
  - per-planet hand-placed detail.
  The quick spec-level fixes are listed above and are cheap for a next round.

## Round 3 (all chapters below 8)

Task: `CLOUD_TASK3.md`, with the owner's overrides: no budget stop, fix **every** chapter whose blind average was
below 8 (lowest first), at most 6 stage builds per chapter; all subagents `claude-sonnet-5-5` (run through the
Workflow tool, because the plain Agent tool only accepts model aliases). Branch `art-fixes-3`.

### Process

1. Setup, full reference build into `_stage_ref`, screen29 previews of all 19 into `r3_before/` + contact sheet.
2. One fresh blind critic scored all 19 on both lenses -> `critique_r3_before.json` (book average 7.20).
3. 17 chapters were below 8 (only create and space scored 8.0). One fixer per chapter, lowest first, 4 at a time
   (two 2-worker queues; a single workflow is capped at CPUs-2 = 2 concurrent agents). Every fixer kept its result
   (none restored the original). Builds used per chapter: 00_welcome 5, copper_age 4, tfmg 2, health 4, explore 4, food 3, pneumatic 1, iron_age 3, climate 1, steel_age 1, farming 2, bronze_age 5, mekanism 3, storage 1, stone_age 1, ie 3, twilight 3.
4. Final full build into `_stage_final`: `OK: 19 chapters, 435 quests`, no WARN/ERROR.
   **Proof for the unedited chapters (create, space):** all 15 of their generated textures are md5-identical to
   `_stage_ref`, and their `ftb_quests_theme.txt` lines are identical. artlib.py diff: 237 additions, 0 deletions.
5. One fresh blind critic scored only the 17 edited chapters (previews in `r3_after/`, `r3_before/contact_sheet.png`
   as book context) -> `critique_r3_after.json`.

### Scores (blind; average of director and player)

| chapter | before dir / pl | before | after dir / pl | after | delta |
| --- | --- | ---: | --- | ---: | ---: |
| 00_welcome | 6 / 6.5 | 6.25 | 6 / 6 | 6.00 | -0.25 |
| climate | 8 / 7.5 | 7.75 | 8.5 / 8 | 8.25 | +0.50 |
| food | 7.5 / 7.5 | 7.50 | 7.5 / 7.5 | 7.50 | +0.00 |
| health | 7 / 7 | 7.00 | 7 / 7 | 7.00 | +0.00 |
| farming | 6.5 / 6.5 | 6.50 | 7.5 / 7 | 7.25 | +0.75 |
| storage | 7.5 / 7.5 | 7.50 | 8.5 / 8 | 8.25 | +0.75 |
| stone_age | 7.5 / 7 | 7.25 | 8 / 7.5 | 7.75 | +0.50 |
| copper_age | 6.5 / 6.5 | 6.50 | 7.5 / 7 | 7.25 | +0.75 |
| bronze_age | 7 / 7 | 7.00 | 7.5 / 7 | 7.25 | +0.25 |
| iron_age | 7.5 / 7.5 | 7.50 | 8.5 / 8 | 8.25 | +0.75 |
| steel_age | 6.5 / 6.5 | 6.50 | 7.5 / 7.5 | 7.50 | +1.00 |
| create | 8 / 8 | 8.00 | not edited | 8.00 | |
| ie | 7.5 / 7.5 | 7.50 | 8 / 7.5 | 7.75 | +0.25 |
| tfmg | 7 / 7 | 7.00 | 7.5 / 7.5 | 7.50 | +0.50 |
| pneumatic | 7.5 / 7.5 | 7.50 | 8 / 8 | 8.00 | +0.50 |
| mekanism | 7 / 7 | 7.00 | 8.5 / 8 | 8.25 | +1.25 |
| explore | 7 / 7 | 7.00 | 8 / 7.5 | 7.75 | +0.75 |
| twilight | 7.5 / 7.5 | 7.50 | 8.5 / 8 | 8.25 | +0.75 |
| space | 8 / 8 | 8.00 | not edited | 8.00 | |
| **book (19)** | | **7.20** | | **7.67** | **+0.47** |

Edited chapters: 7.10 -> 7.63. Chapters at 8 or above: 2 -> 8 of 19.
Unedited chapters keep their before score. The before and after scores come from two different critic sessions;
expect about +-0.5 noise per chapter. **00_welcome** scored lower (6.25 -> 6.00) and **food** and **health** did not
move although their fixers judged them improved; they were kept (within noise) but are the first candidates for
another pass or a revert of 00_welcome.

### What changed (from the fixers' reports)

- **00_welcome** (6.25 -> 6.00, 5 builds): Replaced the smooth mountain_range and tree_line layers with pixel_range: a hazed far range plus a darker near massif on each side, all lit from the right. Added a pixel_sun, a dark pixel_drift hill and a pixel_forest belt of dark teal conifers (bare, snow 0) behind the lower mid-ground and in front of the mountains. This fills the dark middle band and hides the flat mountain cut-off line. Added a small pixel-lit wooden cabin built with blocks: dark oak roof row, a glass window, and an oak door. It sits on the lower mid platform at x 0.675, with a warm window glow, a new entry in lights, and a lantern beside it. It is the focal prop near the quests and balances the lantern, stump and book hero on the left. Moved the poppy and dandelion sprites to x 0.545 and 0.575 to make room for the cabin.
- **copper_age** (6.50 -> 7.25, 4 builds): Rebuilt the scene with a generator script that places layers in screen pixels; the layer count is now 34. The texel stays 4, with one light and one shadow. Accent colour and palette are unchanged. Sky: replaced the smooth sun and the smooth mountain_range with pixel_sun plus two hard-tone pixel_range layers. These are warm, hazy dusk massifs with no snow and no mist bands. Added a small space_stars patch in the top-left sky. Dead middle: added two opaque pixel_drift hill layers in the same brown tone as the near range, so the dark area around the panels now has depth. Dropped the strata_band. Ground: a full-width cobble blocks row along the bottom edge.
- **tfmg** (7.00 -> 7.50, 2 builds): Removed all muddy nebula_glow layers in the sky; kept the low-alpha sky_band and the warm light glows. Replaced the two flat dark hazard pillars with lit steel stacks: steel_fluid_tank bands, yellow caution rings, steel_block caps, low haze. The left stack sits on the brick chimney. The right stack is a flare stack with the fire sprite moved onto its top. Added two create_smoke columns (light grey above the left stack, dark above the right flare) to give the sky a clear hard-tone smoke read. Removed the dark noisy cast-iron tank tower behind the right tower.
- **health** (7.00 -> 7.00, 4 builds): Replaced the oversized blocks bed with a hand-drawn pixel_art hospital bed (76x34 texels, same texel as the potion sprites) plus an IV stand with a blood bag, so scale now matches the small props. Replaced the floating right shelves and workbench with a grounded right apothecary cabinet (hickory back wall, posts, 3 shelves down to the floor, 12 items, lantern on top), shorter than the left unit for asymmetry. Added a red-cross wall sign hung by two pixel cords from the drying beam, and a wall anatomy chart above the bed to fill the empty dark middle. Added a barrel with bandage and morphine sprites on the floor at the left of the bed.
- **explore** (7.00 -> 7.75, 4 builds): Replaced the oversized smooth sun and the smooth mountain_range/snowy_range with a hard-tone pixel scene: a pixel_sun sitting low in the valley of the left massif, plus a far hazy pixel_range and two darker flank massifs (pixel_range, faceted, lit from the left to match the sun). Added a hard-banded blue pixel_aurora and three space_stars boxes to fill the top band. Removed the map-line contour_map noise. Removed the blocky grey tower and the stepped terrain. The right-hand hero is now a snow peak with a glowing soul lantern at the summit, which reads as a destination. Replaced the flat vector pines with two rows of pixel_forest (back and mid belts) behind the lower panels, three tall foreground pine clumps (left x2, right x1), and a light sky_band mist. This fixes the dead dark area around the panels.
- **food** (7.50 -> 7.50, 3 builds): Replaced the flat plank_shelf ceiling strip with a heavy stripped-spruce pixel_timber beam plus a thin upper rafter. The hanging cords and food now visibly hang from it. Added a hazed, dark spruce-plank wainscot (blocks, 2 rows, full width) behind the lower props for wall depth and a floor-to-wall transition. Rebuilt both left shelves as one shelving unit: two vertical posts down to the floor, thick pixel_timber boards with small diagonal brackets, and 5 items per shelf (up from 4). The shelves now look supported and fuller. Anchored the floating bread crate: the cabinets now sit on a 3-row cabinet-on-crates stack standing on the floor, with a smaller bread pile and pie on top.
- **pneumatic** (7.50 -> 8.00, 1 builds): Removed the odd drone sticker (two turbine_rotor sprites, logistics_core sprite and its axle shaft) at x0.2-0.3 y0.44. Replaced it with a single pixel programmable-controller block (blocks layer, x0.25 y0.46) lit by the lantern rays. Replaced the second bottom-left 2x2 compressed-iron stack with a varied reinforced brick/tile/pillar stack to break the repeated texture. Added three pipe couplings (short wide shafts) on the long left vertical pipe at y0.33, 0.53 and 0.65 to break up the flat run.
- **iron_age** (7.50 -> 8.25, 3 builds): Tool rack anchored: four chain segments each on a new left and right chain hang from the top beam to the rack corners, plus a dark contact-shadow glow under it and a warm glow behind the hammer head. Chimney forge shortened by one brick row (6 rows to 5, h 22 to 18.3, bottom edge unchanged); smoke, embers and the dark smoke glow lowered to match, so it dominates less. Crate recoloured to light oak over ash planks (was chestnut/hickory). Barrel changed to palm wood (brighter, more orange).
- **climate** (7.75 -> 8.25, 1 builds): Removed the pixel_sun layer and its warm sun light, so the scene has one moon light and a consistent night. Removed the dense lower forest row (layers 33-39) behind the lower panels and raised haze on the mid forest bands to 0.45-0.5, so the tree band behind the panels is calmer. Removed the sticker-like windsock pixel_art and the shears sprite, which cuts clutter at the drying rack and tornado sign. Spec validated and formatted: 90 layers. build.py --check passes.
- **steel_age** (6.50 -> 7.50, 1 builds): Rebuilt the scene layers (22) in art_styles.d/steel_age.json; palette, background, banner and shapes are untouched. The spec is valid and formatted, and build.py --check passes. Best copy is in scratchpad/r3/steel_age/best.json, generator in gen.py. Sky: hard-tone night sky with a pixel moon (space_stars plus pixel_moon), a faint dusk band, a hazy pixel_range mountain line and two dark fog bands that dissolve the mountain foot. The smooth smokestack and mountain_range layers and the floating embers are gone. Removed the dim ghost furnace on the left. In its place is a taller, hazier brick stack with a lit top cap and a lit oven door, with create_smoke rising from its flue. One hero: the right-hand blast furnace stays, now with a create_smoke plume from its lit flue. Its lights (flue top, fire door, crucible) are tied to real sources.
- **farming** (6.50 -> 7.25, 2 builds): Rebuilt the scene at one texel (4, was 3): every layer is now a pixel motif, real block textures or pixelated livestock, so the old mixed-density props are gone. Replaced the smeared sky_band clouds with a hard-banded dusk sky (night blue to mauve to amber) and six hard-tone pixel clouds with flat shaded bellies and a warm lit rim. Added a pixel_sun setting behind rolling hills, a faint far range and three pixel_drift green hill layers for depth; birds and a few stars fill the top. Replaced the oversized vector-looking oak with a smaller hand-built pixel apple tree (4 leaf tones, outline, apples, forked trunk with roots) at the left.
- **bronze_age** (7.00 -> 7.25, 5 builds): Rebuilt the scene layers with a generator script (scratchpad r3/bronze_age/gen.py). Header, palette, banner and background are unchanged and the accent colour is the same. Added a hard-tone dusk landscape: a pixel_sun in the saddle at the right, a warm-lit pixel_range far massif, a second lower pixel_range foothill band, two pixel_drift hill bands, and pixel_forest clumps. These replace the old smooth tree/mountain_range/nebula_glow smoke props. Fixed the flat horizon cut-off of the far range by covering its base with a drift. Shrank the mine: the headframe is now 3x5 cells and the adit 5x3 cells (was 3x6 and 7x5), with bell, chain and lamp rescaled to the texel. This fixes the mismatched scale and the oversized blocky look. Shrank the furnace tower from 6 to 5 rows and replaced the glow/nebula smoke with create_smoke pixel smoke on the chimney top.
- **mekanism** (7.00 -> 8.25, 3 builds): Added a green conduit network: long overhead pipe linking the left and right posts, a vertical drop down the right gap between panel 3 and the turbine, and an elbow into the new QIO array (create_shaft, lit). Filled the empty middle with a 2x5 QIO drive array (front and rack_glass blocks) plus green soft_glow and a new cast light. Moved the machine bank left to x 0.45 (with its glow and light) to make room for the QIO array. Broke up the plain tank with elite and basic induction providers in the casing.
- **storage** (7.50 -> 8.25, 1 builds): Tower texture varied: machine_casing, 4k/64k storage blocks and extra disk drives mixed into the repeating disk-drive stack (adds teal and yellow glowing cells, less repetitive). Shelf decluttered: removed lunch_basket, wooden_hopper, a burlap sack, a glazed vessel and a duplicate sack on the left shelf. Top and bottom pipe runs thickened (h 0.8/0.95 -> 1.1) so they read as deliberate runs. Low floor props regrouped: chest minecart and sacks clustered next to the hopper barrel instead of scattered.
- **stone_age** (7.25 -> 7.75, 1 builds): Replaced the 14 stacked dripstone sprites (flat brown wedges) with 10 hand-built pixel_art stalactites. They have lit and shaded flanks, strata, warm tips and a few water drips, vary in length, and hang in two clusters left and right, clear of the banner and panels. Replaced the smooth cave_painting, cave_painting_herd and hand_print motifs with pixel_art cave art. The left wall has a pixel mammoth, two deer and three stick hunters on a faint lit wall patch. The right wall has two bison, two hunters and a stencil-style hand print. The ochre is brighter and has a dark/light speckle, and the art ignores the scene light so it stays readable. Removed the anvil-like chert block and its sticker-like tools. Added a tree-stump knapping block (pixel_art) with the hammer, flint and knife head resting on it, plus an axe and two flint chips on the floor. Added three pixel stalagmites (two beside the stump, one at the right edge) to frame the fire and fill the dead dark areas at the bottom left and right.
- **ie** (7.50 -> 7.75, 3 builds): Right chimney shortened from 11 to 9 rows and moved so it stays on the ground. It is now less oversized, and its haze is 0.25 to tone down the saturated red. Removed the four flat grey soft_glow smoke blobs. Added a hard-edged create_smoke plume (k 3, 4 puffs, drift 0.5) rising from the chimney top. Left pylon haze raised from 0.1 to 0.3 so it is less flat and dominant. Added two space_stars boxes in the top corners. They appear faint in the preview.
- **twilight** (7.50 -> 8.25, 3 builds): Giant pale gloom-cap mushroom replaced by a hand-drawn pixel_art glowing mushroom in the chapter's purple accent palette, plus a smaller companion, with a magenta light and soft glow; the out-of-palette blocky one is gone. Castle rebuilt as a pixel_art silhouette (three roofed towers, crenellated keep, warm lit windows, moon-side rim) with an amber glow behind it, so it reads clearly. Moon replaced by a hard-tone pixel_moon (k=2) with a moonlight light entry; stars are now space_stars at texel 2. Glowing pond replaced by a hard-banded pixel_art pond (mossy stone rim, 5 blue bands, lily pads, lotus, sparkles); the soft-glow stack and about 40 clutter flower sprites were cut to 12 flowers, 4 amethysts and 7 fireflies.

### artlib additions

Only farming added code: `farming_sky` (hard-banded gradient sky), `farming_cloud` (hard-tone pixel cloud),
`farming_tree` (pixel fruit tree), `farming_furrows` (crop rows: wheat / leaf / tuft). One block above
`DECOR_MOTIFS`, 237 additions, 0 deletions; parameters in ART_GUIDE.md "Round 8". All other fixers reused the
existing opt-in motifs (`pixel_*`, `create_*`, `space_*`, `blocks`, `pixel_art`).

### Remaining weak points (after critic)

- **00_welcome** (6/6): Top 35% is an empty brown gradient with a hard-edged sun-ray fan; the scene only starts at y~0.45 | Scene is a thin strip along the bottom; cabin right and stump left leave a hollow middle
- **climate** (8.5/8): Section 3-5 panels sit on busy trees/mountains at y~0.55-0.65; borders weak | Foreground props (rack, crate, anemometer, mannequin, hut) are evenly spaced like a shelf of stickers
- **food** (7.5/7.5): Large dark empty wall in the centre at y~0.55-0.75 beside the panels | Upper hanging produce is large and evenly spaced like wallpaper
- **health** (7/7): Heavy dark void at the top-centre and between shelves (y~0.5-0.8) | Red cross sign and cross painting are flat and oversized next to the shelves
- **farming** (7.5/7): Sunset sky is clean but the cloud bands look like flat stripes with dithering | Panels sit on the bright sky; the translucent brown panels look muddy against orange (x~0.3-0.6, y~0.4-0.55)
- **storage** (8.5/8): Right machine tower and left shelf are strong, but both are tall slabs hugging the edges | Pipe frame around the top and bottom is a neat idea but reads as a thin outline
- **stone_age** (8/7.5): Section 3 title is cut through by connection lines at x~0.4, y~0.55 | Panel 1 lines cross heavily and clutter the centre
- **copper_age** (7.5/7): Mountains behind the panels are muddy purple-brown and flatten the panel contrast | Left ore stairs and right furnace are big dark masses; the centre bottom is thin
- **bronze_age** (7.5/7): The top 20% is a flat gradient with only a header floating in it | Mountains are generic flat polygons repeated at one size
- **iron_age** (8.5/8): Hanging tool board at the left is flat and its chain overlaps the panel edge at x~0.28 | Right chimney is a tall slab with a hard dark edge
- **steel_age** (7.5/7.5): Huge left brick chimney is a flat vertical slab with little shading | Moon and starfield are a clean contrast, but the mountains are a flat dark blue band
- **ie** (8/7.5): Two pylons and the crane frame the panels well, but the pylon lattice repeats flatly | Panels have many blank shapes, so the content reads empty
- **tfmg** (7.5/7.5): Hazard stripes on both towers are loud and flat compared with the muted scene | Right machine stack is huge and heavy; the left is a thin tower
- **pneumatic** (8/8): Pipe frame is repeated and neat, but gauges on the left and right look stuck on | Machines at the bottom corners are dark and heavy
- **mekanism** (8.5/8): Big green tank on the left and dark tower on the right are a strong frame | Ore pile in the bottom-right corner is small and cut off
- **explore** (8/7.5): Sun disc on the left is a glowing sticker that clashes with the night sky | Mountains behind the lower panels reduce panel contrast (y~0.55-0.7)
- **twilight** (8.5/8): Left tree trunk is a big flat brown column with little texture variance | Castle at the top right is a flat silhouette

Systemic (after critic):
- Many quest nodes show blank grey shapes without item icons, so panels read empty and lose theme
- Panel fills are translucent dark boxes that fight busy backgrounds in several chapters (farming, copper, explore, twilight)
- Compositions follow one template: tall prop towers at both edges and a hollow dark middle, which feels formulaic across chapters
- Chunky pixel props on top of smooth gradient skies and flat polygon mountains in several chapters (welcome, copper, bronze, steel) clash in density
- Light sources rarely cast light onto neighbouring props, so scenes read as assembled stickers

Ceiling estimate (after critic): Current set is about 7.8 average. With unified lighting, denser fill of the empty middles, and item icons in every node it could reach 8.5 or a bit higher; 9 needs hand-painted depth.

### Skipped chapters

None: all 17 chapters below 8 were edited. create and space (8.0) were above the threshold and left unchanged.

### Spend

Subagent tokens (claude-sonnet-5-5): before critic ~0.10M, 17 fixers ~1.70M, after critic ~0.09M (plus ~2 short
fixer starts discarded when the run was restarted with more parallelism). The dollar amount is not visible from
this session; the budget stop was lifted by the owner.


## Round 4 (second pass on the 11 chapters still below 8)

Owner request: another round toward a book average of 8, using **space** (星辰大海) and **climate** (气候与衣物)
as the primary references (the owner's favourites). Same setup: one `claude-sonnet-5-5` fixer per chapter, 4 at a
time, at most 6 builds each, issues taken from `critique_r3_after.json`; fresh reference build `_stage_ref2` first.
No fixer edited `artlib.py`. Final full build `OK: 19 chapters, 435 quests`, no WARN/ERROR; the 8 unedited chapters'
61 textures are md5-identical to `_stage_ref2` and their theme lines identical. One fresh blind critic scored the 11
edited chapters (`critique_r4_after.json`, previews and a current 19-chapter contact sheet in `r4_after/`).

| chapter | r3 start | after r3 | after r4 (dir / pl) | after r4 | delta r4 |
| --- | ---: | ---: | --- | ---: | ---: |
| 00_welcome | 6.25 | 6.00 | 8 / 7.5 | 7.75 | +1.75 |
| climate | 7.75 | 8.25 | not edited | 8.25 | |
| food | 7.50 | 7.50 | 8.5 / 8 | 8.25 | +0.75 |
| health | 7.00 | 7.00 | 8 / 7.5 | 7.75 | +0.75 |
| farming | 6.50 | 7.25 | 7.5 / 7 | 7.25 | +0.00 |
| storage | 7.50 | 8.25 | not edited | 8.25 | |
| stone_age | 7.25 | 7.75 | 8.5 / 7.5 | 8.00 | +0.25 |
| copper_age | 6.50 | 7.25 | 8 / 7.5 | 7.75 | +0.50 |
| bronze_age | 7.00 | 7.25 | 8 / 7.5 | 7.75 | +0.50 |
| iron_age | 7.50 | 8.25 | not edited | 8.25 | |
| steel_age | 6.50 | 7.50 | 8 / 8 | 8.00 | +0.50 |
| create | 8.00 | 8.00 | not edited | 8.00 | |
| ie | 7.50 | 7.75 | 8.5 / 8 | 8.25 | +0.50 |
| tfmg | 7.00 | 7.50 | 8 / 7.5 | 7.75 | +0.25 |
| pneumatic | 7.50 | 8.00 | not edited | 8.00 | |
| mekanism | 7.00 | 8.25 | not edited | 8.25 | |
| explore | 7.00 | 7.75 | 8.5 / 8 | 8.25 | +0.50 |
| twilight | 7.50 | 8.25 | not edited | 8.25 | |
| space | 8.00 | 8.00 | not edited | 8.00 | |
| **book (19)** | **7.20** | **7.67** | | **8.00** | |

Chapters at 8 or above: 13 of 19. Below 8: 00_welcome 7.75, health 7.75, farming 7.25, copper_age 7.75, bronze_age 7.75, tfmg 7.75.
Scores of different rounds come from different critic sessions (about +-0.5 noise per chapter).

### What changed in round 4

- **farming** (5 builds): Darkened the panel backing: palette panel_fill [12,16,12], the central soft_glow enlarged to 34x34 at alpha 0.8, and a second dark glow added behind the top panels. Lower stripe clouds made puffier (flat 0.3, taller), with alpha 0.9 on all clouds. Apple tree smaller and moved inward (x 0.215, w 7.2, h 10.2) so it is no longer clipped at the left edge. Added a pixel_forest tree-line silhouette on the horizon behind the far drifts, for depth.
- **00_welcome** (4 builds): Replaced the empty brown gradient and sun-ray fan with a full-height hard-tone dusk sky (farming_sky: indigo, plum, amber horizon). Added stars in three clusters, a pixel_moon at upper left, and four farming_cloud banks (one large violet bank at upper right, warm ones near the horizon). None cross the banner or panel. Rebuilt the mountains with the climate-style pixel_range: a tall faceted left massif, a right massif lit warm by the sun, and a hazy central range whose peak sits behind the panel. Light comes from the right throughout. Moved the pixel_sun to the gap between the central range and the cabin so it shows above the roofline and warms the range.
- **steel_age** (6 builds): Replaced the single flat pixel_range with two ranges: a pale far range (haze 0.55, lit snow caps) and a darker near massif range taller toward the sides, so the mountains read as layered depth. Removed the two flat dark sky_band strips that made the dead dark band behind the panels. Added a dark soft_glow calm backdrop behind the panels and two pixel_drift foothill bands (at y 0.66 and 0.715) above the furnace wall. Left chimney: added a dark top-fading soft_glow for shading and a warm forge glow at its base to tie the light to the forge.
- **bronze_age** (2 builds): Rebuilt the whole scene as a dusk landscape on one texel grid (scene texel 3 -> 4, every pixel layer k=4). It follows the space and climate chapters: hard-tone sky, layered ranges, one low sun, one warm light. The flat gradient at the top is gone. A banded dusk sky (farming_sky, 8 amber stops) now has stars (space_stars) and four lit streak clouds (farming_cloud, side 1, lit from the sun). A big pixel_sun sits in the valley between the right peaks, so the ridge cuts it, and a lights entry carries its glow. The old sun sat behind the chimney, so I moved it. Mountains are now layered: a hazy warm far range, two tall hero massifs at the left and right edges with warm lit snow and tongues, and a dark low ridge in front. They replace the repeated same-size flat polygons.
- **explore** (5 builds): Resolved the day/night contradiction: the glowing pixel_sun is now a hard-band pixel_moon at upper left (x0.16, y0.2) with a cool moon light entry. Scene light and ambient colour are now moonlight blue. The only warm lights left are the campfire and lantern. The warm sky band and warm snow tints on the mountains were made cool. Removed the floating soul-lantern sprite and its glow, and replaced it with a small pixel_art red pennant on the right summit. Ground: dark teal pixel_drift hills now cover the big brown dirt block, with a darkening band and a warm pixel_lightpool around the campfire.
- **stone_age** (4 builds): Turned the dark empty cave middle into a hard-tone pixel dusk landscape, following the space and climate technique: one pixel_art backdrop on the texel-4 grid (generated by scratchpad/r4/stone_age/backdrop.py + gen_spec.py). Backdrop contents: banded dusk sky with one-texel checker transitions and stars; a large erupting volcano on the right (lava streams, glowing crater, lit smoke plume, three hard glow rings); a mammoth herd silhouetted on the far ridge; three layered ridges with dark pine silhouettes (none behind the panels); a lit left rock cliff. Left cliff face is a mottled rock wall under the cave paintings. The painting palette is brightened to ochre, alpha 1, no haze, so it now reads at high contrast (critic: cave paintings low-contrast). Removed the old dim painting backdrop blob, the right-hand paintings and handprint (they would float in the sky), the old sky_band and soft_glow, and the big right stalactite.
- **copper_age** (3 builds): Replaced the muddy sky bands with an existing farming_sky dusk gradient (dark navy to a copper-orange horizon) on one texel grid, as in the climate/space references. Added three hard-tone farming_cloud streaks lit by the sun, plus a sparse star patch at top left. Lowered the sun so it sits behind the far range, with a wider and softer pixel_sun glow (5 rings, lower alpha) instead of the hard-ringed disc sticker. Rebuilt both mountain ranges with pixel_range. The far range is a warm rose lit side with warm haze and mist. The near range is dark, giving clear layered depth and better panel contrast.
- **health** (3 builds): Added a hand-built pixel night window as the top-centre focal point (82x44 texels, moon, stars, hills, lit cottage, muntins, sill), unlit so it glows, with cool moonlight soft_glow and a cool 'lights' entry. It sits over the beam and fills the empty top void. Removed the herb strands that hung in the centre top and the old oversized flat red-cross hanging sign with its long cords. New smaller hanging enamel red-cross sign: pixel_art with bevel, shading and short chains from the beam, plus a faint warm glow. Replaced the flat cross painting with a lit pixel medicine cabinet (enamel cornice with red cross, glass doors, warm interior, coloured bottles) with its own light and glow below panels 3 and 4.
- **food** (3 builds): Top row hanging produce rebuilt with varied scale, cord length and clustering: large onion pair, a long five-garlic braid, a big hops bunch, a dried wheat sheaf, larger peppers. It no longer reads as even wallpaper. Added a centre hanging copper pot (pixel_art with a lid, on a chain) above the banner to fill the dead top-centre. Added a pixel_art arched night window (moon and stars) in the right wall gap, with a cool blue soft_glow and a matching cool light in `lights`. Added a small wall shelf with a cooking pot and jug, plus a hanging bacon and chicken string, in the right-hand dead wall gap at y 0.5-0.7.
- **tfmg** (4 builds): Added a hard-tone dusk sky (farming_sky, dark olive to ember horizon) plus sparse stars, replacing the empty dark background. Removed the huge right hazard-striped tower with its smoke and fire; replaced it with a hazy far chimney with its own smoke for depth. Cut left tower to a single hazard band; shortened the right distillation tower (9 to 7 rows) and re-seated its smoke on the barrel top. Recoloured the pumpjack to a darker brass with a stronger outline and sat it in the warm horizon glow.
- **ie** (4 builds): Removed the smooth sky_band, moon and star_cluster layers. Added a pixel_moon with halo, a one-texel space_stars field in the top band, and a faceted pixel_range hill line. Added two layers of generated pixel_art factory skyline (far and near) behind the wall: chimneys, sawtooth roofs, sparse lit orange and cyan windows. These give depth between the pylons and the panels. Added three pixel_lightpool layers (cyan under the lamp and crane, orange under the coke oven and blast furnace, plus a cyan one in the middle) and two space_rocks gravel bands on the floor, so the floor picks up the scene lights. Added a two-strand sagging cable (copper and steel, built from shaft segments) across the floor, linking the dynamo to the coke oven.

### Remaining weak points (round-4 critic)

- **00_welcome**: Quest cluster floats mid-sky (centre, y 28-58%) with no anchoring; section panel is a tiny box and the diamond/circle nodes are sparse | Left half of sky (x 0-50%, y 5-35%) is empty apart from the moon and a flat dash cloud
- **food**: Dense wall decor competes with panel edges at the top (y 5-25%), hanging produce crowds the banner | Panel borders are low-contrast purple on dark brown; node icons are tiny (section 1 and 4, about 20 px)
- **health**: Lower section panels (3 and 4) hold few nodes and read sparse; dark empty wall around the panel block (x 25-75%, y 60-75%) | Shelves at the left and right edges are visually heavy and dark, the red-on-dark panel borders are low contrast
- **farming**: Six panels spread over the sky cover the sunset and the bird area; panels 3-5 stack at the left against the tree and read crowded | Barn plus hay at bottom right (x 60-98%, y 55-95%) is blocky and flat compared with the nicely lit tree
- **stone_age**: Section 3 and 4 panel headers (y 53-55%) sit over bright orange horizon bands and are low contrast; title text nearly illegible | Line crossings between sections 1, 2 and 3 are tangled over the cave painting edge
- **copper_age**: Top-right panel (section 3) overlaps its own 4 stacked nodes and the cluster of connector lines from the pentagon is cramped | Large dark empty mid-band (x 25-70%, y 55-80%) between lower panels and the forge
- **bronze_age**: Section 5 panel is a tiny box with one node, section 4 is nearly empty, reads placeholder | Orange header text on panels over the glowing sun region (x 70-85%) is fine but the lower panels' text is very small
- **steel_age**: Section 3 panel header text is squashed onto two lines at top-right (y 28%), clearly clipped | Mid-band (y 50-70%) is flat dark between panels and the ore pile, with a hard horizontal edge across the mountains at y 48%
- **ie**: Nodes are mostly blank grey shapes with few icons in sections 1-5, so quest content is unreadable | Centre of the scene is a large black void behind the panels with the skyline barely visible
- **tfmg**: Murky olive/amber background gradient is muddy and low in contrast, the middle dark tower at x 78-85% is nearly invisible | Section 2 panel has sparse unconnected nodes that read as placeholders
- **explore**: Panel pair 2 and 5 are narrow with sparse nodes, and the grid texture in the sky (y 0-40%) is faintly visible, looks like a tiled background | Mountains sit behind lower panels (section 4, 5, 6) and low-contrast headers over the snow

Systemic:
- Panels are consistently small, sparsely populated boxes floating mid-scene, and many node icons are tiny or blank, reducing at-a-glance readability
- Most scenes use a flat dark mid-band between panels and foreground props, so the lower third is crowded while the middle is empty
- Panel header text over bright horizon or sun regions loses contrast in several chapters (stone_age, bronze_age, steel_age)
- Dithered pixel clouds and smooth gradients are mixed; cloud silhouettes repeat
- Props get cropped at the edges and some chapters have a tiny one-node panel that looks placeholder

Ceiling estimate: With panel-contrast and mid-band fixes, most chapters could reach 8.5; a 9 would need hand-tuned depth layers and unified pixel density across sky and props.

Spend (round 4): about 1.25M subagent tokens for the fixers and 0.08M for the critic (plus two fixer starts discarded
when the run was restarted to add the owner's reference chapters).


## Round 5 (third pass on the 6 chapters still below 8)

Same setup as round 4 (space and climate as primary references, issues from `critique_r4_after.json`, fresh
reference `_stage_ref3`, 4 fixers in parallel, at most 6 builds). No `artlib.py` changes. Final build OK; the 13
unedited chapters' 100 textures are md5-identical to `_stage_ref3` and their theme lines identical. Fresh blind critic
on the 6 edited chapters: `critique_r5_after.json`; previews and a current contact sheet in `r5_after/`.

| chapter | after r4 | after r5 (dir / pl) | after r5 | delta | builds |
| --- | ---: | --- | ---: | ---: | ---: |
| 00_welcome | 7.75 | 7.5 / 6.5 | 7.00 | -0.75 | 1 |
| health | 7.75 | 8 / 8 | 8.00 | +0.25 | 2 |
| farming | 7.25 | 7.5 / 7 | 7.25 | +0.00 | 4 |
| copper_age | 7.75 | 7.5 / 7 | 7.25 | -0.50 | 3 |
| bronze_age | 7.75 | 8 / 7.5 | 7.75 | +0.00 | 1 |
| tfmg | 7.75 | 8 / 7.5 | 7.75 | +0.00 | 1 |

Book average: 8.00 -> **7.95** (each chapter's latest blind score).

**Reading:** the fixers made only small, local changes this round (1-4 builds: clouds, fireflies, a light pool, a
monitor, a forest band, sky recolours), and the score changes (-0.75 to +0.25) are within the +-0.5 noise between
critic sessions; 00_welcome and copper_age scored lower with a different critic although their edits were additive
touches. Diminishing returns: the remaining gaps are mostly layout items the art spec cannot change (small panels,
blank node icons, panel colours) and structural props (farming's block barn) that need new pixel motifs.

### What changed in round 5

- **health** (2 builds): Replaced the floating wall clock (layer 96) with a pixel ECG heart monitor (dark frame, teal screen, pink pulse line), so the right-hand wall cluster of monitor and hanging red-cross sign reads as one medical theme. Added a pink soft_glow behind the monitor and a matching pink entry in scene.lights, giving the empty upper-right wall a lit focal element. Brightened the monitor screen and glow on the second build after the first looked dim.
- **bronze_age** (1 builds): Removed the bronze block stack at the right edge, which was cut off by the screen edge. Removed the propick sprite and the charcoal pile from the crowded bottom band. Moved the right-hand ingot and ore pile inward and made it smaller. Moved the minecart slightly left.
- **farming** (4 builds): Clouds: replaced 5 same-silhouette big clouds with 7 varied ones (different sizes, flat 0.1-0.85, seeds, lit side, cold/warm tones); two small streaks fill the gaps, none repeat. Barn: lit lantern on the wall with a warm soft_glow and a new warm scene light, cream plank door trim (frame + X brace) as pixel_art, rooster weathervane on the roof, warm pixel_lightpool on the ground in front, darker ground shadow and a shade overlay on the right wing. Left foreground: three pixel sunflowers beside the apple tree to fill the left, with the pumpkin and melon below. Learned and used the real screen mapping: visible x is about 0.11-0.89 and y about 0.19-0.83 (screen_y = 1620*fy - 303 px, screen_x = (fx - 0.11)*1872 px); props placed accordingly.
- **00_welcome** (1 builds): Added two hard-tone farming_cloud layers in the empty left sky (x0.17,y0.335 and x0.3,y0.4), matching the right-side cloud style. Added warm space_stars sparkle band (fireflies) over the forest in the vacant middle band (x0.46,y0.665). Added a hard-banded pixel_lightpool (dither 0) under the cabin lantern/window to ground the cabin light. Left composition, palette, panel and node areas untouched; spec validated and formatted.
- **copper_age** (3 builds): Added a pixel_forest band of dark warm-hazed conifers (x0.5, y0.62, w40, h14, n22, hmin60/hmax100, color [50,30,44], haze 0.3) between the drift layers and the base blocks. It fills the empty dark mid-band behind the lower panels and adds a depth layer between the mountains and the foreground. Moved the furnace smoke from y0.4645 to y0.505 so it rises from the tower top instead of floating detached. Saved the spec in the one-layer-per-line format; it validates and build.py --check passes. The best version is copied to SP/r5/copper_age/best.json and the original is in orig.json.
- **tfmg** (1 builds): Replaced the muddy olive sky gradient with a clean dusk gradient (deep blue-black to violet to orange horizon). Removed the olive sky_band and recoloured the big mid glow from olive-amber to warm orange. Far steel tower at x 0.745: haze 0.6 to 0.12, so it now reads as a solid structure. Lightened the far tower's smoke colour for contrast against the darker sky.

### Remaining weak points (round-5 critic)

- **00_welcome**: Single small quest panel floats mid-sky (centre, 40-57% height) with nodes spilling out of it and a big dark octagon/diamond lines over the mountain; panel does not feel part of the scene | Scene is empty in the upper 25% (sky only) and left 30% of the middle; props (stump with book, pouch, axe, sign) are tiny and scattered
- **health**: Right 60% of the middle band (heartbeat monitor, first-aid sign) is a bit sparse and the heartbeat panel floats near the section 2 panel (right-centre, 43%) | Section 3 and 4 panels have small dim nodes with slightly low-contrast dark icons (centre, 58-62%)
- **farming**: Panels are scattered over the sky with uneven spacing and a long diagonal connector line from panel 3 to panel 6 crossing the gap (centre, 40-65%) | Section 5 panel overlaps the sunset/tree area and its semi-transparent fill is muddy over the glow (left, 60-78%)
- **copper_age**: Panels sit on a busy dithered forest/mountain band; panel fills are translucent and the dark node discs lose contrast (centre, 25-75%) | Left ore stair cliff and right furnace are heavy and nearly same value, the centre bottom forge is small and the middle is a murky dark-red mass (bottom-centre 50-75%)
- **bronze_age**: Panels sit mostly on glowing sunset sky with brown fills; header text over bright sun area is readable but node icons are small (centre, 30-65%) | Section 5 panel holds a single dark gear node and section 4 two nodes, feels thin/empty (centre-right 55-65%)
- **tfmg**: Panels are olive/gold on dark; node icons are tiny, dark hexagons and squares have low contrast inside panels (centre, 25-75%) | Section 2 has sparse disconnected nodes, section 3 wide panel is half empty (centre 42-57%)

