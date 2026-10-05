# 开局屠宰与兽皮教学修正

2026-10-04。用户要求记录未来航空学整合计划，补充早期尸体处理教学，并指出牛皮和彩色兽皮的 JEI 刮制配方缺少操作说明。

## 任务书改动

- `02_food.py`：重写原 `food:butcher`，新增 `butcher_process` 与可选 `butcher_hook`。第一节直接说明未腐烂尸体 + TFC 石刀可在背包无序合成，大型尸体不必等挂钩。补充副产物、腐烂检查与后续兽皮加工入口。
- `10_stone_age.py`：新增 `hide_scraping`，讲解兽皮铺原木顶面、刀右键 4×4 共 16 格、打掉薄皮取产物；原狩猎任务补充尸体与模组兽皮转换说明。牛皮和有对应配方的彩色兽皮转换成 TFC 生兽皮，尚不是成品皮革。
- `11_copper.py`：修正原木侧面、淡水预制、原木制鞣酸等错误；补充本包盐水预制、树皮粉制鞣酸、上油批量、种子油水陶锅路线、再次刮制和 SewingKit 缝纫台裁剪。首次裁剪可用燧石剪刀，避免先做需要皮革绳的金属剪刀。
- `FUTURE_IDEAS.md`：记录机械动力：航空学及附属的后期整合方向、版本核对与测试顺序；本轮未安装模组。

本轮新增 3 个任务，原任务 key、任务/检测/奖励 ID 均保留。原有奖励和完成检测保留，屠夫任务改为开局常规教学节点。玩法配方和掉落未修改。

## 配方与机制依据

- `kubejs/data/butchersdelight/recipes/dead_*.json`：未腐烂尸体与 `#forge:tools/knives` 的背包分割配方；`tags.js:900` 纳入 `#tfc:knives`，石刀可用。牛尸体输出 16 份牛肉，鸡尸体输出 2 份鸡肉；兔背包配方明确只写棕色尸体，不泛化所有颜色。
- `kubejs/data/butchersdelight/recipes/hook_recipe.json`：tier 1 砧配方，铜棒等可用。TFC 铜为 Tier I，铜棒锻造同为 tier 1，所以铜砧即可；原模组铁粒合成被本包覆盖。
- TFC 3.2.22 当前代码：`InteractionManager` 要求原木顶面、上方空气；`ScrapingBlockEntity` 检查 16 个位置完成后转化。刀检验 `#tfc:knives`。旧中英文图鉴的“侧面”不符合当前代码。
- `kubejs/data/tfc/recipes/scraping/cow_to_hide.json` 与同目录彩色兽皮配方：实际输出 `tfc:large_raw_hide`，白色输出纹理不代表它已是 scraped。
- `kubejs/data/hardrock/recipes/tfc_tools_crafting/sheep_hide.json`：绵羊皮与刀背包合成羊毛，副产物是大型生兽皮。
- `kubejs/data/tfc/recipes/barrel/*_prepared_hide.json`、`*_leather.json`、`tannin.json`：盐水预制、自定义鞣制皮、树皮粉制鞣酸。
- `kubejs/data/hardrock/recipes/firmalife_mixing/hide_oiled_*.json`、`tfc_scraping/leather_*.json`、`sewing_table/leather_from_*.json`：上油、再刮、裁剪；小/中/大上油批量为 3/2/1 张，每批 1000 mB。
- `kubejs/data/hardrock/recipes/tfc_pot/seed_oil_water.json` 与 `tfc_quern/seed_tree_paste.json`：早期树种糊与种子油水路线。
- `mods/htm-1.20.1-forge-1.0.8.jar` 内剪刀配方与 `data/forge/tags/items/shears.json`：燧石剪刀可用于首次裁剪。

静态机制核对不等于游戏内操作实测。正式部署与验证记录保存在 `backups/ftbquests-before-butcher-guide-20261004/validation.txt`。重启游戏后加载新任务。
