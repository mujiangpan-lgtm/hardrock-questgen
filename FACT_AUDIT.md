# FTB 任务书事实核对记录

核对日期：2026-10-04。目标为 `HANDOFF.md` 指定的八章，另修正食物章中一处死亡营养说明。所有原章节 key 和任务 key 保留，未增加隐藏任务。

## 已修正内容

| 章节 | 主要修正 |
| --- | --- |
| 03 伤病与医疗 | First Aid 为八部位；基础血量随最大生命缩放；绷带恢复 4 点、夹板恢复 2 点；医疗布是 HTM 植物布料；修正愈伤膏、缝纫、吗啡配方、倒地救援及死亡惩罚。坠落主要伤及腿脚，删去没有证据的流血与骨折机制说明。 |
| 20 机械动力 | 安山合金用锡、锌或铸铁；修正传动杆、齿轮、水车和工具配方；先制作黄铜机件与动力合成器，再制作粉碎轮；补充 Picky Wheels 对动力源的影响。 |
| 21 浸没工程 | 更正发电机和序列组装材料、循环次数；区分旋转动力与 FE 电力；多方块机器改为搭建确认，避免要求取得无法正常放进背包的整机方块。 |
| 22 重工业 | 厚钢板为钢板与铅板焊接；机壳依赖按实际制作顺序调整；修正耐火砖、炼焦、鼓风、抽油、分馏、塑料、引擎与发电路线；塑料板使用 100 mB 气动熔融塑料。 |
| 23 气动工艺 | 初始压缩铁由锻铁双锭爆炸取得；修正压力室外壳、网、板、管道和阀门配方及前置；修正充气、塑料、电路板、装配系统和无人机说明。 |
| 24 通用机械 | 钢壳先依赖铁英合金与气动材料；控制电路和核心合金使用本包压力室配方；删除原版倍矿保证；配方已删除的熔炼机任务改为富集碳，熔炼工厂改为富集工厂；更正配置器、QIO、喷气背包和完整防辐射装备。 |
| 32 暮色森林 | 传送门需要星球原矿制成的魔法暮色水晶；首领依游戏进度分成沼泽、黑暗森林、雪原三路，再汇合到高地、巨人镐和余烬之灯；使用进度检测核实区域解锁。 |
| 33 星辰大海 | 补齐钛与哈氏合金、汽油和凝固汽油、反物质催化剂、NASA 机械合成、MekaSuit 航天服、星球金属净化和高温防护等本包实际门槛；修正发射台、返程与目的地说明。 |
| 02 食物与烹饪 | 本包 `keepNutritionAfterDeath=true`，死亡后保留 TFC 营养。 |

多处首次获取任务的奖励改为其它实用物资，避免奖励本任务正在教学的物品。

## 核对依据

- `mods/*.jar` 的配方、物品标签、Patchouli 手册、语言文件；涉及机器动力、工厂槽数等机制时检查相应类的字节码。
- `kubejs/data/**/recipes` 与标签、`kubejs/server_scripts/unify_others.js` 等移除及替换脚本、`kubejs/client_scripts/info.js`。
- `defaultconfigs/firstaid-server.toml`、`defaultconfigs/tfc-server.toml`、现有存档 serverconfig；`config/hardcorerevival-common.toml`、`config/tfc_punishment_for_death-common.toml`、PneumaticCraft 与 Mekanism 配置。
- 没有把普通模组原版配方当成本包配方，也没有把 `replaceInput` 当作删除。

## 验证与部署

- 八章修改均已独立 stage 构建并检查预览；最后全量 `--check` 与正式生成均为 **OK: 20 chapters, 440 quests**。
- 与 `backups/ftbquests-before-fact-audit-20261004/quests/` 逐章对比，**440 个原任务 ID 全部保留**，没有增加隐藏任务标志。
- 已写入 `config/ftbquests/quests/` 和 `kubejs/assets/kubejs/textures/quests/`；正式 SNBT 和 108 张贴图与验证 stage 逐文件一致。
- 本轮修改了八个待核章节与食物章一处说明；生成后的九个章节文件发生变化，其余十一章与本轮备份一致。
- `_stage*`、`_ref/`、旧提取脚本与旧研究笔记已保存到本轮备份的 `questgen-temporary-files.zip`，完整性检验通过后清理。用户已确认保留排版工具 `_layout.py` 与交接文件 `HANDOFF.md`。
- **需要完全退出并重启游戏**。未进行游戏内的完整制造、搭建和首领通关测试。

## 实机确认范围

本轮验证基于包内文件、配置、手册与代码，未进入游戏逐台搭建和试运行。复杂机械合成图案、IG 完整矿脉与化学链、可替代材料仍以重启后的 JEI 和设备界面确认。整合包自身还有以下问题，本轮未修改玩法配方：

1. **暮色水晶配方仍用 Beyond Earth 物品 ID。** `kubejs/data/pneumaticcraft/recipes/pressure_chamber/magic_crystal.json` 引用了未安装模组的四种原料；已在任务正文标明，不能保证现有水晶配方可以制作。对应的已安装物品为 Ad Astra 的粗戴斯、粗紫金、粗耐热金属和寒冰碎片。
2. **IE 序列的半成品标签疑似缺失。** 水车、风车与部分部件配方把 `create:gantry_shaft` 写成 tag，扫描静态资源和 KubeJS 后没有找到定义。铁质部件可走蓝图路线；本包 TFC-IE Crossover 已证实允许 TFC 水轮/风车向相邻动能发电机供能，正文已提供替代。`tfc:brass_mechanisms` 标签实际有定义，不是这个问题。
3. **新增 TFMG 钢铁构件配方有错误副产物 ID。** `tfc:metal/rods/steel` 应为 `tfc:metal/rod/steel`。同一物品还有 jar 自带的另一条序列；正文要求选择当前 JEI 实际可用路线，循环次数不混用。
4. **本包 TFMG 抽油机输入口中文提示有误导。** 实际类继承 Create `KineticBlockEntity`，正文按旋转动力描述。
5. **暮色 `twilight_dinner` 进度加载异常已见于现有日志。** 本章用的是 jar 原生 `progress_*` 进度，没有要求完成出错的聚餐进度。

分章来源与更多说明见 `fact_audit_create_ie_tfmg.md`、`fact_audit_pneumatic_mekanism.md` 及暮色/航天分章核对记录。
