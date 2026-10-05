# 气动工艺与通用机械事实审校

本次只编辑 `23_pneumatic.py`、`24_mekanism.py`；所有 quest key 与章节任务数保留（22 / 21）。未设置 hidden。新增跨区依赖的长线和交叉线使用 hide_lines 隐藏，任务仍显示。根代理负责最终全量部署与清理。

## 气动工艺

- 起步压缩铁输入改为锻铁双锭，爆炸损耗 33%；压力室为 2 bar、一个双锭产一个压缩铁锭。
- 强化石/砖改为石头/石砖加压缩铁网的 Create 物品应用；网可用钢级砧焊接两根压缩铁线产四张，避免先有压力室才能做外壳的循环。
- 墙壁为强化砖加压缩铁板，玻璃为玻璃加压缩铁板；阀门为机械手部署管道到墙壁，接口为漏斗加墙壁。最小压力室外壳改为 26 格。
- 压力管道改为钢级砧加工压缩铁板，或接续组装滚压两次、冲压三次产三根；普通管道 5 bar。阀门任务显式依赖管道。
- 手摇机修为一个压缩铁锭，空气压缩机为六块强化石砖类材料；空气罐红石数改为二，充气改为充能站。
- 塑料补充本包热气动工厂与 TFMG 两条路线，说明气动炼油厂已删除，区分气动塑料与 TFMG 塑料片。
- 空白电路板保留经 jar 核实的 1.5 bar、红石火把×2、布线标签×3、塑料×1、产三片；灯箱材料改动与电子元件标签替换明确写出。10 分钟曝光、150/30 秒蚀刻来自本版本手册，不是推测。
- 成品电路板说明原版电容/晶体管配方删除、应查本包电子元件标签；RS 处理器后续改为未组装板起始、部署原处理器/铜线/红石/铜线后冲压。
- 扳手旋转和潜行拆卸顺序修正；装备升级改在充能站；无人机用编程器写程序，不需安装可编程控制器。
- finale 同时依赖成品板、原处理器和空气压缩机，不再只走粘合物支线即可声称完整毕业。

主要来源：`kubejs/data/pneumaticcraft/recipes/**`、`hardrock/recipes/tfc_welding/compressed_mesh.json`、`hardrock/recipes/tfc_anvil/compressed_sheet.json`、`refinedstorage/recipes/{processor_binding,raw_basic_processor,basic_processor}.json`；`unify_others.js`；`pneumaticcraft-repressurized-6.0.22+mc1.20.1.jar` 的实际配方与 Patchouli 手册；`config/pneumaticcraft-common.toml`。

## 通用机械

- 钢质机壳输入改为 RS 机器外壳，每轮 25 mB 铁英合金注液、部署钢板，再重复一组；更正机械手与机械臂区别。
- 铁英合金 50–75% 铸铁、25–50% 石英、熔点 930℃；该学习任务改为钢壳前置，消除先有成品壳才能学习其原料的问题。start 引用气动 finale。
- 锇改为 IG 锇砂经 IE 电弧炉；任务用 forge:ingots/osmium 接受不同模组的锇锭，奖励替换为助熔剂。基础控制电路改为 2 bar 的 HOP 石墨锭、锇线、塑料片、铀氧化物，奖励替换为红石。
- 原矿入口大量删除，不再保证原版倍矿；中间机器顺序更正，灌注与气体输入区别更正，锇压缩机不再教粉压成锇锭。灌注/强化/原子三种核心合金实际均在压力室做（2/4.5/4.5 bar），富集碳转碳灌注物质的原版配方删除；正文已明写。
- 脚本明确删除电力熔炼炉和四档熔炼工厂配方：保留 energized_smelter 任务 key，目标改为富集仓制作富集碳；factory 任务改为实际可制作的基础富集工厂。
- 工厂并行槽位 3/5/7/9，以 jar FactoryTier 的初始化字节码核实；速度/能量升级不互斥。
- 生物燃料粉碎配方已删除；不再宣称发电配方未修改或 IE 蒸汽/Create 直接供电。配置器模式按控制设置，当前物品模式键 N。
- 数字采矿最大半径 32，删除不存在的雷达升级；QIO 补充同频率配置；喷气背包燃料为氢气、跳跃上升；防辐射任务补四件全套。
- 辞典是标签查看器，不是图文教程。删去五机矿链已完成的无根据毕业声明。

主要来源：`kubejs/data/mekanism/recipes/**`、`refinedstorage/recipes/machine_casing.json`、`tfc/recipes/alloy/iron_quartz_alloy.json`、`tfc/tfc/metals/iron_quartz.json`、`immersivegeology/recipes/arc_smelting/arc_grit_osmium_to_osmiumingot.json`、`hardrock/recipes/ie_arcfurnace/block/osmium.json`；`unify_others.js`；Mekanism / MekanismGenerators 10.4.16.80 jar 的配方、中文语言与 FactoryTier 字节码；`config/Mekanism/general.toml`、`options.txt`。

## 验证与保留的不确定项

- 两章个人 stage build 分别 `OK: 3 chapters, 58 quests` 和 `OK: 3 chapters, 57 quests`，已实际查看预览，面板无重叠、长交叉线已收敛。
- 全量 `--check` 为 `OK: 20 chapters, 440 quests`（在锇任务改为标签之后亦通过）。
- 不替玩家推定所有 IG 矿脉分布、完整五倍矿物链、生物燃料替代来源、QIO/MekaSuit 核材料门槛的完整建设方案；相关地方写明按本包 JEI 查具体配方。没有运行游戏，机器实际交互由本版本手册与代码静态核实。
