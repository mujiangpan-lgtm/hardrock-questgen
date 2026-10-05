# Claude 接手包：HardRock TerraFirmaCraft 4

生成时间：2026-10-04（Asia/Shanghai）
项目目录：`D:\.minecraft\versions\HardRock TerraFirmaCraft 4 - realistic survival`

## 给 Claude 的接手指令

请先阅读以下文件，再继续工作：

1. `questgen/HANDOFF.md`（总交接）
2. `questgen/agent_guide.txt`（任务书生成规则，必须遵守）
3. `questgen/BUTCHER_LEATHER_GUIDE.md`（本轮屠宰、兽皮、制革修改说明）
4. `questgen/FUTURE_IDEAS.md`（机械动力：航空学及附属的后续计划）
5. `questgen/chapters/02_food.py`
6. `questgen/chapters/10_stone_age.py`
7. `questgen/chapters/11_copper.py`

继续修改前先核对真实 JAR、KubeJS 覆盖、隐藏物品和配方。不要只依据旧研究笔记或任务书文字推断机制。

## 用户偏好

- 用户使用中文，希望直接完成工作，不要反复询问已经明确的事项。
- 用户希望保留 `questgen/_layout.py` 和 `questgen/HANDOFF.md`。
- 修改任务书时，原则上保留原有任务 key、检测 ID、奖励 ID；但**用户目前没有正式存档**，重构章节、搬任务、删重复任务都可以直接做，不用再提醒“会丢进度”。
- 真实配方、KubeJS 覆盖和 JAR 代码优先于旧图鉴文字。
- 生成任务后必须运行全量 build、预览并检查布局；不能把静态生成通过说成游戏内实测。

## 当前完成状态

- **最新状态（2026-10-05）**：19 章、435 个任务、143 张装饰贴图（全部 19 章已做章节美术主题：底图、场景插画、横幅、形状、关键词色，见 `questgen/ART_GUIDE.md` 与 `HANDOFF.md` 末尾）。「交通与远行」章已拆散并入仓储/农耕/探索，仓储章已移到「生存之道」组；详见 `HANDOFF.md` 末尾两节。用户**没有正式存档**，任务 key / ID 可以随意移动、改名、删除，不必为保进度而绕路（见下方偏好）。
- 以下为上一轮（20 章 / 443 任务）的状态：原有 440 个任务当时全部保留；当时新增：
  - `food:butcher_process`
  - `food:butcher_hook`
  - `stone_age:hide_scraping`
- 本轮正式变更的章节：`food.snbt`、`stone_age.snbt`、`copper_age.snbt`，以及对应面板贴图。
- 全量 build 和 stage 验证通过；原 440 个任务及 1758 个原检测/奖励槽位 ID 保留。
- 尚未完全重启游戏，也没有进行实际放置、刮制、制造或掉落实测。
- 本轮备份：`backups/ftbquests-before-butcher-guide-20261004/`

## 已核实的屠宰事实

- 本包已有 `butchersdelight` 尸体背包分割配方：未腐烂尸体 + `#forge:tools/knives`，2×2 背包无序合成即可。
- `tags.js` 将 `#tfc:knives` 加入 `#forge:tools/knives`，因此 TFC 石刀可用。
- 尸体必须未腐烂；配方输入使用 `tfc:not_rotten`。
- 牛尸体示例：得到 16 份生牛肉，并有骨头、膀胱、凝乳酶、油脂、牛皮等副产物。
- 鸡尸体示例：得到 2 份生鸡肉，并有骨头和羽毛。
- 兔子的背包配方明确使用棕色兔尸体，不能泛化所有颜色。
- 挂钩覆盖配方是 `kubejs/data/butchersdelight/recipes/hook_recipe.json`：tier 1 砧配方，铜棒等材料可用；铜砧即可，不需要炼铁。
- 挂钩不是开局取肉前置；开局路线是尸体 + 石刀。
- `onlyknifedrops` 配置只影响死亡时尸体替换逻辑，不影响尸体分割配方。

## 已核实的牛皮和彩色兽皮刮制事实

用户指出 JEI 里只看到“刮制配方”，不知道实际怎么操作。正确操作不是合成：

1. 放置真正的原木方块（`#minecraft:logs`），上方保持空气。
2. 手持牛皮或有对应配方的彩色兽皮，对原木顶面右键。
3. 用 TFC 石刀或金属刀对铺开的皮逐格右键，4×4 共 16 格。
4. 16 格全部刮完后，打掉铺着的薄皮层并拾取产物；原木不用打掉。
5. 刀每次操作消耗 1 点耐久。

TFC 代码要求点击方向为 `UP`；旧中英文图鉴写“原木侧面”是错误的。

牛皮和彩色兽皮刮制后的真实输出通常是 TFC 生兽皮，例如 `tfc:large_raw_hide`，不是成品皮革。输出贴图变白不代表已经完成制革。

## 本包实际制革路线

`TFC 生兽皮 → 石灰水浸泡 → 原木顶面再次刮制 → 盐水预制 → 树皮粉制鞣酸 → 油水上油 → 原木顶面再次刮制 → SewingKit 缝纫台 + 剪刀裁剪为普通皮革`

关键覆盖：

- 预制使用 `tfc:salt_water`，不是淡水。
- 鞣酸使用树皮粉 + 水的桶配方，不是直接把原木泡桶。
- 鞣制输出为 `kubejs:hide_tanned_s/m/l`，还不是 `minecraft:leather`。
- 上油使用 `kubejs:seed_oil_water` 或 `tfc:olive_oil_water`；每批小/中/大皮分别 3/2/1 张，每批 1000 mB。
- 上油后还要再次在原木顶面刮制，得到 `kubejs:hide_finish_s/m/l`。
- SewingKit 缝纫配方用 `#forge:shears` 裁剪，普通皮革产量按尺寸为小/中/大 1/2/3 张。
- 首次裁剪可用 `htm:flint_shears`，配方为 2 个燧石碎片 + 2 个植物线；不要假设必须先做金属剪刀。

## 航空学后续想法

用户希望以后考虑加入“机械动力：航空学及附属”。目前只记录计划，没有安装模组。

当前环境核对：Minecraft 1.20.1、Forge 47.4.13、Create 6.0.8，320 个模组 JAR（已移除 Steam 'n' Rails 与 Macaw's 系列）。未安装 Aeronautics、Valkyrien Skies、Eureka、Clockwork、Create Interactive。已有 Immersive Aircraft、Create Jetpack、Gliders、船和汽车。`createair-1.0.5.jar` 是 Create Air + Thin Air，不是航空学。

后续必须在复制实例中逐个测试：版本兼容、TFC 材料/燃料适配、移动机器和容器、食物腐烂、加热、温度/缺氧、区块加载、存档、多人同步，以及 Physics Mod / Embeddium / Oculus / Flywheel / 光影表现。

## 验证命令

PowerShell 中使用桌面 Python：

```powershell
$questPython = 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $questPython questgen/build.py --check
& $questPython questgen/build.py
```

本轮验证报告：`backups/ftbquests-before-butcher-guide-20261004/validation.txt`

## 交接注意

- 旧规则「不要删除或改名原有任务 key」只为保护玩家进度；用户目前没有正式存档（2026-10-04），可以不遵守。若用户开始正式存档，恢复此规则。
- 不要给玩家直接奖励正在教学的首次关键产物，以免跳过路线。
- 不要修改生成器、`qlib.py` 或注册表来绕过问题。
- 修改后必须检查物品是否真实存在、是否被 `hide.js` 隐藏、是否被 KubeJS 覆盖。
- 如果没有游戏内证据，明确标记为“静态核对，未实机验证”。
