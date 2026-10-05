# FTB 任务书交接 · 已完成事实核对

2026-10-04 更新。HardRock TFC 4（MC 1.20.1 Forge），用户使用中文。

## 当前状态

- 原交接指定的八章事实核对已完成：`03_health`、`20_create`、`21_ie`、`22_tfmg`、`23_pneumatic`、`24_mekanism`、`32_twilight`、`33_space`。
- 另修正 `02_food` 一处死亡后保留 TFC 营养的说明。
- 已全量写入 `config/ftbquests/quests/` 和 `kubejs/assets/kubejs/textures/quests/`：**20 章、443 个任务、108 张装饰贴图**。新增 3 项开局屠宰与刮制教学，详见文末本轮记录。
- 所有 440 个原任务 ID 均保留；任务 key 和章数保留，未添加隐藏任务。若任务类型或内容改变，已经完成的原任务仍沿用其 ID。
- 修改章节均完成独立构建和预览检查；全量 `--check` 与正式生成均通过。实机文件与全量验证 stage 一致。
- **用户需要完全退出并重启游戏**。本轮没有进入游戏逐台搭建、制造或测试设备。

详细修正与已知包内异常见 `FACT_AUDIT.md`，分章来源见 `fact_audit_*.md`。

## 备份

- `backups/ftbquests-before-rewrite/` 是原任务书备份，未修改。
- `backups/ftbquests-before-fact-audit-20261004/quests/` 和 `textures/` 是本轮事实核对前的正式任务书与贴图。
- 同目录 `questgen-temporary-files.zip` 保存收尾时清理的所有 stage、`_ref/`、`_extract_old.py` 与旧 `research_recipes.md`。其中旧研究笔记仍不应作为事实依据。
- `validation.txt` 记录最终生成、原任务 ID 对比及文件一致性验证。

## 已知后续事项

本轮任务书核对已完成。以下属于整合包原配方或提示问题，未修改玩法文件：

1. ~~魔法暮色水晶配方引用未安装的 `beyond_earth:*`~~ 已修复（2026-10-04）：`kubejs/data/pneumaticcraft/recipes/pressure_chamber/magic_crystal.json` 改为 `ad_astra:raw_ostrum/raw_desh/raw_calorite/ice_shard`，原文件备份在 `backups/magic_crystal_fix/`，任务正文的异常提示已删除。需进游戏 JEI 确认配方已加载。
2. 部分 IE 序列将 `create:gantry_shaft` 物品写成未找到定义的 tag。铁质部件可走蓝图；TFC 原生水轮/风车可通过 TFC-IE Crossover 驱动 IE 动能发电机，正文已给替代路线。
3. 新增 TFMG 钢铁构件序列含错误副产物 `tfc:metal/rods/steel`；jar 内还有另一条原生路线，需以重启后的 JEI 实际加载结果确认。
4. TFMG 抽油机输入口中文提示写电力，实际是 Create 旋转动力；章节按代码描述。
5. 现有日志有 `twilight_dinner` 进度加载异常，本章使用的原生 `progress_*` 未引用它。

如果继续修整合包配方，应单独处理这些文件并做游戏内加载及制造验证，不能把静态任务书生成通过当成所有机器已实测。

用户已确认未来考虑加入「机械动力：航空学及附属」，实施方向与版本、测试要求已记录在 `FUTURE_IDEAS.md`。本轮只记录计划，尚未安装；后续应先在复制实例中核对 1.20.1 Forge + Create 6.0.8 的实际兼容发行版。

## 工具链（Windows PowerShell）

必读写作与布局规则：`questgen/agent_guide.txt`。生成工具、注册表与全部章节源文件保留。
系统 `python` / `py` 在本环境不可用；本轮使用桌面依赖运行时：

```powershell
$questPython = 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $questPython questgen/build.py --check

$env:QGEN_STAGE = '_stage_example'
& $questPython questgen/build.py --stage --only 00_welcome,10_stone_age,03_health
& $questPython questgen/preview.py 03_health

# 全量正式生成；不能带 --only
& $questPython questgen/build.py
```

物品/标签查询：`find.py <正则>` / `find.py --tag <正则>`。
后续不能改任务 key 或删除任务，否则会失去对应进度；文字、坐标、任务内容改动可保留 quest ID。
核对包内实际 jar、KubeJS 覆盖、移除/替换脚本和配置；`forge:false` 为禁用，`replaceInput` 是替换输入。

## 清理状态

`questgen/_stage*`、`_extract_old.py`、`research_recipes.md`、`_ref/` 已归档后清理。
用户已于 2026-10-04 确认保留 `_layout.py` 和本交接文件，供后续维护使用。

## 后期奖励调整（2026-10-04）

用户反馈前期奖励合适、后期不足，已完成并正式部署 9 章、175 个任务的奖励加强：钢铁时代后段 9、机械动力后段 12、IE 28、TFMG 24、气动 22、Mekanism 21、RS 仓储后段 13、暮色 20、航天 26。前期奖励保留。

大型建设与航天节点增加成批扩建材料、备用耗材及远征补给，阅读任务奖励较克制。所有 440 个任务 ID 保留；检测、文字、前置与布局未改。原奖励槽位类型与顺序保留，额外物品追加在后；未重置玩家进度或已领取奖励。

全量生成通过 `OK: 20 chapters, 440 quests`；正式 22 个 SNBT 与 108 张贴图均与最终 stage 字节一致。未进行游戏内领取测试，需完全退出并重启游戏。

详细方案见 `REWARD_REBALANCE.md`。备份在 `backups/ftbquests-before-reward-rebalance-20261004/`，含修改前源码、正式文件、`baseline.json`、`reward-changes.json` 和 `validation.txt`；本轮临时脚本、报告、stage 与预览归档至该目录的 `questgen-temporary-files.zip` 后清理。`_layout.py` 与本交接文件继续保留。

## 启动加载计时脚本修复（2026-10-04）

已修复 `kubejs/startup_scripts/load_time.js#6` 的 `redeclaration of var $TitleScreen` 启动错误。根因是安装版本 Rhino 对脚本顶层 `if` 内 `const` 的兼容问题；实际引擎已复现。计时代码改为立即执行函数中的局部 `let` 变量，保留主菜单启动时长显示。

原脚本与错误日志在 `backups/kubejs-load-time-fix-20261004/`，验证说明见同目录 `README.md`。真实 Rhino 解释器配轻量桩的完整脚本、延迟计时、连续渲染、服务端及缺少 ModernFix 分支通过。未进行完整游戏重启验证，用户需要完全退出并重新启动游戏。

## 主菜单计时绘制崩溃修复（2026-10-04，17:41 报告）

用户重启后的日志确认 6/6 启动脚本通过且无错误；随后 `load_time.js` 的 `drawString` 在主菜单绘制时发生 Java 重载歧义并崩溃。此前轻量 GUI 桩未覆盖真实 Java 重载解析，此项验证不足已补齐。

计时显示现已精确选择 Forge 的 `drawString(Font,String,float,float,int,boolean)`，并加入一次性禁用显示的异常保护。仅转 String/Component 和选择已映射的原生 int 重载均已在实际 Rhino 环境验证为不可行，后续不要改回普通重载调用。

本轮备份与说明在 `backups/kubejs-load-time-render-fix-20261004/`。其中 `overload-verify/` 包含安装版本 Rhino、同签名 Java 方法、相关类型转换与方法重映射的复现及验证；最终完整脚本的连续中文绘制、异常保护与环境分支均通过。未进行完整游戏启动测试，用户需重新启动游戏。

## 气候章开局门槛修正（2026-10-04）

用户反馈首任务要求温度计导致开局被金属加工门槛阻断。已将 `climate:start` 改为认识体温指示的勾选确认，正文说明温度计需要金片与红石粉、留作冶金后的可选精确读数工具；使用位置纠正为快捷栏、副手或 Curios。`winter_ready` 同时取消必须带温度计的表述。

任务 key、任务/检测 ID、奖励、依赖和布局保留。已正式部署并验证 20 章 / 440 任务，只有 `climate.snbt` 变化，贴图未变；未重置玩家进度或进行游戏内交互测试。备份、配方与机制依据、验证结果及最终 stage 归档见 `backups/ftbquests-before-climate-entry-fix-20261004/`。用户需重新启动游戏加载新检测。

## 开局屠宰与兽皮教学（2026-10-04）

用户反馈整只尸体处理和牛皮、彩色兽皮的刮制操作缺少教学。已重写 `food:butcher`，新增 `food:butcher_process`、可选 `food:butcher_hook` 和 `stone_age:hide_scraping`，并补全铜器章现有三个制革任务。

关键事实与后续维护注意：

- **未腐烂尸体 + TFC 石刀可在背包 2×2 无序合成**，本包现有配方允许早期处理牛等大型动物，不需要改玩法或等挂钩。不同尸体以各自 JEI 用途为准；棕色兔背包配方不能泛化成所有颜色。
- **屠夫乐事挂钩已经改为 tier 1 砧配方，铜砧 + 铜棒即可**，原模组铁粒配方不适用于本包。
- **刮制在真正原木顶面操作，上方留空气，TFC 刀逐格右键 4×4 共 16 格，完成后打掉薄皮取物**。当前代码要求顶面，旧图鉴的“侧面”误导。牛皮和有对应配方的彩色兽皮刮制后是 TFC 生兽皮，不能当成普通皮革。
- 本包完整制革是：石灰水浸泡 → 原木刮制 → **盐水预制** → **树皮粉制得的鞣酸**鞣制 → 油水上油 → 再刮 → **SewingKit 缝纫台 + 剪刀**裁剪。首次裁剪可用燧石剪刀；小/中/大上油按 3/2/1 张一批，每批 1000 mB 油水。

全量正式生成和最终 stage 均通过 **20 章 / 443 任务**。原 440 个任务及 1758 个原检测/奖励槽位 ID 保留；只有 `food.snbt`、`stone_age.snbt`、`copper_age.snbt` 与两张对应面板变化，22 个 SNBT 和 108 张贴图与最终 stage 一致。三章预览已查看；未进行游戏内刮制、制造或掉落实测，需完全退出并重启游戏。

详细修改与来源见 `BUTCHER_LEATHER_GUIDE.md`。本轮备份、`baseline.json`、`validate.py`、`validation.txt` 与最终 stage/核实报告归档保存在 `backups/ftbquests-before-butcher-guide-20261004/`。`_layout.py` 和本交接文件继续保留。

## 烟熏任务物品为问号（2026-10-04）

用户反馈 `food:smoking` 的「羊毛线」任务图标是问号、JEI 也搜不到。原因：`firmalife:wool_string` 在 Firmalife 2.1.27 中用 `registerNoItem` 注册，**只有方块、没有物品**（战利品表掉落 `tfc:wool_yarn`）。构建校验的注册表按语言键建立，方块也有 `block.*` 键，所以校验放过了它。**以后用 `firmalife:` / `tfc:` 等 id 做物品任务前，注意它可能是纯方块。** 已扫描 Firmalife 与 TFC 的 `registerNoItem` 列表对照全部章节：只有这一处有问题（`tfc:torch`、`firmalife:sprinkler` 另有对应物品，正常）；其他模组未扫描。

已改为：任务1 `tfc:wool_yarn ×8` + 任务2 进度 `firmalife:story/smoker`（放置羊毛线时触发）。原任务 key 和原任务 ID 保留，仅新增一个任务槽位。正文同时纠正：

- 放置：手持羊毛纱右键，在两面相对的实心墙之间水平拉线，羊毛纱数量不能少于跨度（`StringBlock` 代码）。
- 篝火距离是**本包配置 6 格**（`defaultconfigs/firmalife-server.toml` 的 `smokingFirepitRange = 6`），旧图鉴写的 4 格已过时；熏制 8000 tick = 8 小时。
- 熏肉配方只认 `tfc:brined`（卤水浸泡）。**普通盐腌 `tfc:salted` 不满足**，原文「先盐腌或盐水浸泡」是错的。卤水 = 9 海水 + 1 醋，每件 125 mB 浸泡 4000 tick。奶酪不需要卤制。
- 羊毛纱 = `#forge:spindle` + `#forge:wool` → 8 根。`tfc:spindle` 被 `hide.js` 隐藏；最早可用**陶瓷纺锤**（黏土塑形十字图案 → 烧成纺锤头 → 纺锤头 + 木棍 2×2 合成）。羊毛可由 `butchersdelight:sheephide` + 刀合成 4 份。

Firmalife 的 zh_cn 语言文件本身是乱码，进度中文名无法引用，正文未写进度名。

只有 `food.snbt` 变化；全量生成 20 章 / 443 任务；与备份对比原 ID 无丢失。静态核对（含对 `StringBlock` 的反汇编），**未进游戏实测放线、挂肉与进度触发**。备份在 `backups/ftbquests-before-smoking-fix-20261004/`（含修改前 `02_food.py` 与整套 quests）。需完全退出并重启游戏。

## 仓储章前移与 RS 段核对（2026-10-04）

用户反馈仓储章排在侧栏最后、RS 引导太靠后。已做：

- `25_storage.py`：`group` 由 `industry` 改为 `survival`，`order` 5 → 4（在「农耕」之后、「金属时代」之前）。章节 key、全部任务 key 和 ID 不变。
- `rs_start` 前置由 `pneumatic:finale` 改为 `create:press` + `create:deployer`：RS 入口在 Create 压力机和机械手就位后开启。`silicon` 依赖 `rs_start`；`processor_chain` 依赖 `silicon` + `pneumatic:uv_etch` + `pneumatic:raw_processor`。`start` 正文补一句入口说明。
- 原因：气动章 `raw_processor` 需要**硅**，而硅的来源只在仓储章 RS 段教，该段又锁在 `pneumatic:finale`（要求先完成 `raw_processor`），形成教学死循环。`23_pneumatic.py` 的 `raw_processor` 已补指向「硅与富石英铁」。

RS 段此前**从未核对过**，本轮按真实配方改了这些事实错误（静态核对，来源 `kubejs/data/refinedstorage/recipes/*` 与 RS jar 默认配方）：

- **`tinyredstone:silicon` 在本包无法获得**：唯一配方（熔炼硅化合物）被 `unify_others.js` 按输出整体移除，原任务教的「微型红石的硅进焦炉」是死路（`refinedstorage:silicon` 的焦炉配方还在，输入却造不出来）。真实硅来源：Create 动力筛子 + 黄铜筛网筛 `tfc:rock/gravel/quartzite`（2%，`kubejs/data/createsifter/recipes/sifting/sand_andesite_mesh.json`）；IE 电弧炉（石英粉 + 焦炭粉，`hardrock/ie_arcfurnace/silicon.json`）；TFMG 熔石英为 `tfmg:liquid_silicon`，TFC 浇铸出 4 个硅。`#forge:silicon` 含 `refinedstorage:silicon`，所以微型红石粉可由红石 + RS 硅合成。
- 富石英铁：Create 接续组装，石英粉 TFC 加热 930°C 得 25 mB `kubejs:quartz`。机器外壳：列车机壳 + 熔融富石英铁 + 铁板。
- 三档处理器：未处理品在气压机（基础/进阶 2 bar，粉分别铁/金；高级 **4 bar**，钻石粉），成品在以 `pneumaticcraft:unassembled_pcb` 为起点的 Create 接续组装（线材铜/金/电金）。**控制器、磁盘驱动器、合成终端要高级处理器；终端、总线、装配室要进阶处理器**，原文「基础处理器就够、高级留到以后」是错的。
- 成型核心 ← 基础处理器、破坏核心 ← 进阶处理器（PNC 装配，`program: laser`）。终端要两种核心，输入总线要破坏核心，输出总线要成型核心，装配室两种都要，因此 `quartz_grow` 已改成**必做**（原为可选菱形），标题改为「成型核心与破坏核心」并加第二个任务。
- 线缆有两条路线：气压机 4.5 bar，或 `cable_seq.json`（以硅为起点的 Create 接续组装，含激光切割与充能，一次 5 根）。
- 存储盘 1k/4k/… 的数字是**物品总件数**，原文写成「种类数上限」。装配室不是「对应 3×3 一格」，模板放进装配室；合成管理器只是统一查看。
- 新增任务槽位（均为已有任务追加）：`silicon` +富石英铁，`processor_chain` +进阶/高级处理器，`quartz_grow` +破坏核心，`disk_drive` +1k 存储磁盘。

未核对：控制器容量/中继、`extra_storage`、`create_logistics`、早期储物（工具皮带等）这些原文。样板终端配方未读到，正文写「配方见 JEI」。只有 `storage.snbt` 与 `pneumatic.snbt`（一行正文）变化；全量生成 20 章 / 443 任务；原 2231 个 ID 无丢失。未进游戏实测，需完全退出并重启。备份：`backups/ftbquests-before-storage-reorder-20261004/quests/`（改动前整套正式任务书；由于先改源码后备份，改动前的 25_storage.py 源码没有单独备份，以该备份的 SNBT 为准）。

## 拆散「交通与远行」章（2026-10-04）

用户指出该章第一节（负重）应归仓储、第二节（驯养驮运）应归畜牧，且这些都是前期内容，不该放在最后；去掉两节后整章没有存在意义。**用户没有正式存档，因此直接搬任务、改 key、删章节，未保留旧任务 ID。**

结果：删除 `30_transport.py` 与章节 `transport`（19 章 / 435 任务，原 21 个任务 → 13 个搬走、1 个并入、7 个重复删除）。原文件保存在 `backups/ftbquests-before-transport-merge-20261004/source/`，同目录 `quests/` 是改动前整套任务书。

- **并入仓储（`25_storage.py` 第一节，改名「体积、重量与背负」）**：`sacks`（草篮与麻袋）、`frame_pack`（大背包）、`ore_sack`（矿石袋，可选）。第三、四节整体下移 2 格以腾出位置。删除重复项：`start`（行囊有多重，与仓储 `start` 重复）、`toolbelt`、`large_vessel`（与 `vessels` 重复）。
- **并入农耕（`04_farming.py` 新增第六节「骑乘与畜力」，在驯养下方）**：`saddle`（依赖 `taming` + 铜器时代皮革）、`donkey_cargo`、`cart_mats`、`supply_cart`、`animal_cart`（可选）。马/驴/骡说明并入 `saddle`。删除重复项：`tame_animal`（与 `taming` 重复）、`mob_net2`（石器时代已有捕捉网）。
- **并入探索（`31_explore.py`）**：原 `boat`（只检测船用箱子，含糊）改写为独木舟任务，检测 `firmaciv:kayak`，`shipwreck` / `seven_seas` 的依赖保持不变；新增第六节「舟楫与天空」：`rowboat`、`sailboat`（可选）、`navigation`、`glider`、`aircraft_pointer`（可选）。`atlas` 文字补充指向「导航三件套」。删除重复项：交通章的 `kayak`、`atlas`、`finale`。
- 其余章节没有引用 `transport:*`；群组 `frontier` 现在只剩探索 / 暮色 / 航天。

注意：探索章仍在「远方与星辰」组，独木舟虽可早做（需蜂蜡）、滑翔伞需要 Create。如果用户希望探索章整体前移，改 `31_explore.py` 的 `group`/`order` 即可。静态生成与预览已检查；未进游戏实测。需完全退出并重启。

## 启动提速试验（2026-10-04）

用户反馈每次启动约 2 分钟，想降到 90 秒内。最近一次日志里 ModernFix 记录 `Game took 123.332 seconds to start`（到主菜单）：约 11 s 启动器与扫描、43 s 模组构造、54 s 资源重载（模型烘焙为主）、12 s 图集拼接；KubeJS 启动脚本仅 0.5 s，JEI 在进世界后才启动，不在这 123 s 内。机器 i5-12600KF / 32 GB / NVMe，磁盘不是瓶颈。堆参数为 PCL 自动分配：`-Xmx13414m -Xmn2012m`，G1GC，未设 `-Xms`。

已改（备份与撤销方法见 `backups/startup-speed-20261004/README.md`）：

- `config/modernfix-mixins.properties` 加 `mixin.perf.dynamic_resources=true`（默认关）。**可能引发个别模型缺失/闪烁**，若出现，删掉这一行。
- `config/smoothboot.json`：加载线程优先级 1 → 5（Smooth Boot 原设置为让加载"更流畅"，把加载线程压到最低优先级）。

**尚未实测**，改完的启动时间要用户启动一次后看 `logs/latest.log` 里的 `Game took`。若仍高于 90 s，下一步候选：PCL 里加 `-Xms8g`、Windows Defender 对 `D:\.minecraft` 与 `javaw.exe` 加排除项（需用户自己操作）、卸载 Smooth Boot (Reloaded)、评估是否可裁剪的 mod。

**结果（23:15 实测）：`dynamic_resources=true` 让游戏卡死在资源重载，已撤销。** 日志里 ModernFix 对 1404 个模型报 `ModelMissingException`（additionalplacements 840、tinygates 324、moretinygates 216 …），之后没有图集创建与主菜单。（**2026-10-05 更正**：真正原因是 DragonLib，不是 Additional Placements / Tiny Gates，见下一节；动态资源现已可用。）`smoothboot.json` 线程优先级 1 → 5 保留，效果待测。

## 移除 Steam 'n' Rails 与 Macaw's 系列（2026-10-04）

线程优先级调整实测 122.1 s（改前 123.3 s），无效。按方块状态变体统计：Steam 'n' Rails 约占 27%，Macaw's 六个模组合计约 30%，是资源重载（约 54 s）的主要负担。用户确认**不需要这些内容**（不是养老包，以后可能用航空学而不是火车），已把 8 个 jar 移到 `backups/removed-mods-20261004/mods/`（328 → 320 个模组），并同步清理 KubeJS 里引用它们的配方覆盖与脚本行，细节和恢复方法见该目录 `README.md`。任务书没有引用这些模组。

唯一改了玩法的点：`create_power_loader:empty_brass_chunk_loader` 的配方原用 `railways:remote_lens`，已换成 `create:precision_mechanism`。

静态检查：脚本 `node --check` 通过，改动全是删除行，任务书校验仍 19 章 / 435 任务。**未实测启动与时间**；需用户启动后看 `logs/latest.log` 的 `Game took`，并留意是否有新的 KubeJS 报错（`logs/kubejs/*.log`）。

## 启动提速成功：83.2 s（2026-10-05）

飞行记录（JFR）显示：资源重载阶段（约 42 s）只有 1 个 `Worker-ResourceReload` 线程在跑原版单线程的 `ModelBakery` 烘焙（含 FerriteCore 去重），其余 15 个线程空等；加载线程 CPU 利用率很低，改线程优先级 / 换启动器（PCL 与脚本启动同为 ~119 s）/ 删 57 % 方块变体都只有个位数秒的收益。GC 仅 3.85 s。

再次开启 ModernFix `mixin.perf.dynamic_resources=true` 并抓线程转储，发现之前"卡死"不是死锁：**DragonLib 的 `ClientEvents.onModifyBakingResult` 遍历整张模型表并逐个 `getValue`**，使按需烘焙退化成近似平方级的全量烘焙（单线程累计 CPU > 150 s 仍未结束）。DragonLib 只被 Create Railways Navigator 依赖，二者移到 `backups/removed-mods-20261004/mods/`（模组数 318）后再测：

- `Game took 83.211 seconds`（之前 115~123 s）；资源重载 42 s → 14.4 s；无崩溃、无 FATAL，只剩 4 条本来就存在的缺失模型（`tfmg:block/casting_basin/*` 模具、`refinedstorage:cover` 系列）。
- 当前 `config/modernfix-mixins.properties` 保留 `mixin.perf.dynamic_resources=true`；`smoothboot.json` 优先级 5 保留（无副作用）。
- **未做**：游戏内逐项目检视动态资源是否引起个别模型缺失 / 闪烁（需用户目测：JEI 图标、各模组方块与物品、Create 机器与传送带、Mekanism 机器、TFC 工具与金属、手持物品）。出现问题就删掉 `dynamic_resources=true` 这一行（启动会回到约 115 s 的水平，不影响存档）。
- 以后新增模组时，如果启动又卡在资源重载，先看 `logs/latest.log` 里 `Mod '...' is calling replaceAll` / 大量 `Exception baking ... ModelMissingException`，那个模组就是在遍历模型表。
- 另外观察到：你的网络走代理（`api.minecraftservices.com` 解析到 198.18.x.x 的虚拟 IP），启动期有几处同步联网（主线程等 Mojang 接口约 2 s，exposure / natamus collective 的更新检查在后台线程），不是大头。

## 章节美术主题（2026-10-05，样板 3 章）

用户希望任务书更有艺术感、每章有自己的主题。用户选择"方块贴图平铺为底 + 程序绘制光效/剪影"的混合风格，先做 **石器时代、Create、太空** 三个样板章，并顺带做 **每章专属任务形状** 与 **关键词主题色**（未选：重画分节面板版式、按章换依赖连线颜色）。

实现（生成器扩展，未改任务内容）：

- `questgen/artlib.py`（新）：从 `mods/*.jar` 与原版 jar 读贴图（`namespace:路径`）；生成 **无缝章节底图**（8×8 方块、逐贴图亮度归一、去饱和、乘主题色、压对比度，叠加 speckle/starfield/gear_ghosts 等纹样）、**新横幅**（本章方块贴图条带 + 程序纹样 + 左右各 3 个物品像素图标 + 标题光晕）、**地图装饰**（齿轮、行星、环带行星、月球、星云、山脊、箭头、岩画手印、光晕……）。另有 `validate()`：引用的贴图必须存在、取值必须在词表内。
- `questgen/art_styles.py`（新）：每章一份规格（palette / background / banner / decor / shapes）。由 3 个美术指导代理各设计一章、1 个审稿代理统一（配色拉开、起终点一律 gear、可选一律 diamond、里程碑按时代 pentagon→hexagon→octagon，实测白字对比度 ≥ 11.8:1、关键词 ≥ 6.7:1）。tile_size 采用 32（原版菜单底图比例），未用审稿建议的 48。
- `build.py`：有规格的章节使用新横幅（14×2.8 格，原 10×2）、调色板面板、装饰层（order -20 起，位于面板之下）、按角色映射形状（`default_quest_shape` = normal 形状）、描述里 `&6` 替换为 `&#RRGGBB`；并写出 **`kubejs/assets/ftbquests/ftb_quests_theme.txt`**（`[章节ID] background: …_bg.png; tile_size=256`）。没有规格的章节输出逐字节不变。
- `preview.py`：预览会平铺底图（按约 24 界面像素/格估算）并画出新形状。

部署：只有 stone_age / create / space 三个 SNBT 变化；新增 17 张 PNG（3 底图 + 14 装饰），共 122 张；备份在 `backups/ftbquests-before-art-pilot-20261005/`。

**未验证（需用户进游戏确认）**：① 主题文件按章节 ID 切换底图是否生效（只有字节码依据）；② `&#RRGGBB` 十六进制关键词颜色是否正常显示（不应出现原样字符）；③ 任务详情弹窗在新底图上的可读性。若 ① 不生效，需改用"超大低层章节图片"作底图的方案。确认后再按同一流程铺开其余 16 章（每章一份 art_styles 规格即可）。

### 第 2、3 轮（同日，用户反馈"并不好看，非常空"之后）

用户截图证实主题文件的按章底图**生效**；问题是内容在屏幕上只占约三分之一（用户界面缩放 4、约 29 屏幕像素/格），其余全是放大后很抢眼的底图。改进：

- `preview.py` 新增 **屏幕模式**（`QPREVIEW_SCREEN=29,55`）：按 1460×1050 视口、GUI 缩放 4、真实底图尺寸、节点内物品图标、无任务名还原玩家画面。以后一律按它判断效果。
- 每章新增地图层 **场景插画**（`scene`，order -30）：≥64×48 格、以任务中心对齐、边缘 12% 淡入底图；底图改为 12 界面像素/方块、亮度 0.10。
- `artlib.py` 元素库扩到 45 种（篝火、水车、风车、火箭、行星地平线、空间站、岩画、管道、输电塔、烟囱、电路、罗盘、等高线、城堡、森林、极光、雪山……）及 `sprite`/`sprite_row`（直接放大游戏贴图）。实体物件加了明暗与描边。
- 三位视觉评审（构图 / 主题 / 原版质感）各自打分并给出参数修改，已据此重排三章构图；确认十六进制关键词颜色在 FTB Library 解析器中受支持（`&#` + 6 位，交给原版 `TextColor.parseColor`）。
- 样板三章已正式部署（只有这三个 SNBT 变化，其余贴图不变，贴图目录 3.5 MB）。
- 规则与元素目录整理在 **`questgen/ART_GUIDE.md`**；其余章节的规格改为 `questgen/art_styles.d/<章节key>.json`（每章一个，便于并行）。

### 第 4 轮：铺开到全部 19 章（2026-10-05）

用户睡前授权"你觉得效果不错就继续做"。流程：4 个美术指导代理各设计 4 章（规格写在 `art_styles.d/<key>.json`，按屏幕预览最多迭代 2 轮）→ 1 个评审给 16 章打 5.5–7 分、列出 64 条具体修改（配色撞车、巨型像素物品成色块、窄山脉/森林硬切边、主角位置模板化、互相借用招牌元素）→ 渲染器统一修复（山脉/森林/雪山两端淡出；像素精灵最大 10 倍；旋转精灵用最近邻）→ 4 个修正代理按评审意见修改并复核（自评 7–7.5）。另按美术指导要求新增元素：anvil、anvil_hot、tree、tower、pumpjack、plank_shelf、hanging_cord、livestock、mine_entrance（共 54 种）。

各章主角：欢迎页（桌上的日志与油灯、瞭望塔）、气候（雪山极光 + 皮袄 vs 闪电与温度计）、饮食（房梁挂货、罐头架、灶台）、健康（药柜、心电图、不死图腾）、农耕（苹果树、麦田、牲畜、干草垛）、仓储（货架、RS 控制器）、铜器（矿镐、熔炉）、青铜（矿井口、铁砧）、铁器（工具墙、块炼炉）、钢铁（高炉、钢剑）、IE（输电塔、锤与电弧、焦炉）、TFMG（抽油机、烟囱）、气动（管网、压力室）、通用机械（风力机、感应矩阵、机器墙）、探索（罗盘、瞭望塔、帆船）、暮色（城堡、月亮、萤火虫）。

部署：16 个 SNBT 更新（样板 3 章不变），主题文件 19 节，贴图 143 张 / 12 MB（章节打开时才加载，不影响启动）；1691 处 `&#RRGGBB` 关键词颜色全部格式正确。备份 `backups/ftbquests-before-art-rollout-20261005/`（含改前正式文件、贴图、主题文件与源码/规格）。全书屏幕预览与总览图在 `questgen/_stage_all/`（`contact_sheet.png`）。

**未验证**：游戏内实际观感（只按屏幕预览判断）；各章细节仍有提升空间，评审建议见交接历史。若某章不满意，只改对应的 `art_styles.d/<key>.json` 或 `art_styles.py` 后重新 `build.py` 即可。

### 第 5 轮：弱点修复 + 渲染器升级 + 云端会话（2026-10-05）

- **渲染器**（见 `_art_review/renderer_changes.md`、ART_GUIDE.md "Round 5"）：场景级 `texel`/`light`/`shadow`/`lights`/`ambient`/`pixelate`，`blocks`（真实方块贴图拼的立体建筑）、`sprite_row` 的 `pile`/`scatter`、`light_rays`、闪电/太阳/铁砧/塔/抽油机/矿井口/牲畜重画、发光改为光池、窄面板标题改为两行（steel 第三节的小标签被评审认为是缺陷）。
- **逐章修复**：7 章本地（欢迎/气候/饮食/健康/农耕/通用机械/钢铁），10 章在 GitHub 云端会话（公开仓库 `mujiangpan-lgtm/hardrock-questgen`，任务书 `CLOUD_TASK.md`，分支 `art-fixes`，用 Sonnet 子代理，贴图包加密为 `packdata.tar.gz.enc`，钥匙不入库）。云端结果 `_art_review/RESULTS.md`。
- **盲评**（两位独立评审，平均）：19 章 6.24 → 7.28；云端 10 章 6.30 → 7.60。最高：pneumatic 8.25、storage/iron_age 8.0。没有任何章到 9，评审估计本做法上限约 8–8.5：9 分需要手绘/手工像素或"用方块搭景再截图"的插图。
- **未编辑的 create / space** 仍是旧矢量风格，现在和其他章风格冲突（评审分降到 6.5/6.75），是下一批最明显的候选（用 `blocks`/`pixelate`/`texel` 重做）。
- **部署**：`build.py` 正式构建通过（19 章 / 435 任务），贴图 143 张 15 MB，引用无缺失；备份 `backups/ftbquests-before-art-round5-20261005/`（线上 quests、贴图、主题文件、源码）。**未在游戏内验证**，只看过屏幕预览。
- 注意：pneumatic 的横幅标题颜色取自 `qlib.py THEMES`（青色），预览里是规格的橙色，游戏内可能不同。云端环境没有 Windows 字体，`build.py` 会退到 Noto CJK。

### 第 6 轮：机械动力 / 太空重做 + 气候章前置修复（2026-10-05）

- 气候章「四季轮回」不再依赖「避难所与天气预报」（天气预报 = 天气物品×4(铁/金/红石) + 指南针，警报器 = 铸铁棒 + 工业警报器，均为铁器时代以后）；第三节说明注明不挡主线。缝纫台（剪刀 + 原木）不用动：包里有燧石剪刀。
- create / space 在云端（`CLOUD_TASK2.md`，分支 `art-fixes-2`，花费 29 美元）改成像素方块风：盲评 create 6.5 → 8.0、space 6.75 → 7.5，全书平均 7.39。artlib 新增 27 个可选 motif（`create_*`、`space_*`，见 ART_GUIDE "Round 6"），对其他 17 章零影响（本地复核：除 create/space 外所有生成贴图与线上逐字节一致）。
- 云端额度：100 美元，已用 66，剩约 34（之后会动用用户自己的配额）。
- 部署备份：`backups/ftbquests-before-art-round6-20261005/`。未在游戏内验证。
