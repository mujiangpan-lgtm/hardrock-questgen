# Create / IE / TFMG 事实核对

2026-10-04。只修改章节文案、任务与前置；没有修改整合包配方或脚本。所有章节及任务 key 保留。大型 IE 机器原先的库存物品任务改为建造/运转确认，物品任务数量未修改。

## 已纠正

- `20_create.py`：安山合金的铸铁/生铁区别、88–92% 安山石比例、小缸/坑窑/坩埚路线、支撑梁应用制轴、齿轮材料与变速、扳手操作、Picky Wheels 水车/风车条件、传送带操作、搅拌器与冲压设备用途、机械手供料、粉碎轮每次产 1 个、石磨配方差异、黄铜机件砧上早期路线、机械合成出口和依赖循环。
- `21_ie.py`：防腐木的桶浸泡、焦炉 27 块实心结构、IE 高炉仅装饰、IE 与 TFC 水轮/风车驱动发电机、普通合成的发电机配方、铝提前供应、接线器/继电器区别、电网单位、蓄电池循环材料、粉碎机与冲压机多方块及实际用途、电弧炉电极的气动材料前置、两种玻璃、抽象矿藏、免电传送带和流体设备。
- `22_tfmg.py`：机壳应用、厚钢板钢板+铅板焊接/4.5 bar、重型外壳前置、钢铁构件新增序列、耐火砖两段炼焦、铸铁来源、鼓风炉流体燃料、抽油机强力胶与旋转动力、分馏产物、100 mB 塑料浇铸、液体燃料引擎、发电机循环及 FE 转换、电路板涂层/蚀刻顺序。章末同时要求发电与塑料。

## 关键来源（可在 _ref 删除后复查）

- `kubejs/data/tfc/recipes/alloy/andesite_alloy_*.json`、`kubejs/data/create/recipes/crafting/kinetics/shaft.json`、`kubejs/data/tfc/recipes/anvil/brass_mechanisms.json`、`kubejs/data/hardrock/recipes/cr_sequence/brass_mechanisms.json`、`kubejs/data/create/recipes/mechanical_crafting/crushing_wheel.json`。
- `mods/create-1.20.1-6.0.8.jar` 内动力部件配方和 Ponder 文本；`config/createpickywheels-common.toml`。
- `mods/TFC-IE-Crossover-1.20.1-1.3.1.jar` 内 `data/immersiveengineering/recipes/crafting/dynamo.json`：锻铁锭 **2**、铁质部件、低压线圈、红石 **2**；铝土矿熔炼/铸造；被 `forge:false` 覆盖的防腐木工作台配方。
- `kubejs/data/hardrock/recipes/tfc_barrel/treated_planks.json`：木板 1 + IE 杂酚油 200 mB，密封 8000 ticks。`kubejs/client_scripts/info.js` 的 IE 高炉装饰提示；`kubejs/server_scripts/unify_others.js` 的冶炼与金属冲压配方删除。
- `mods/ImmersiveEngineering-1.20.1-10.2.0-183.jar` 内中文工程师手册的发电、布线、机械结构与流体章节。
- `kubejs/data/tfmg/recipes/heavy_plate.json`、`heavy_plate_perssure_chamber.json`、`steel_mechanism.json`、`distillation/crude_oil.json`、`vat_machine_recipe/plastic_from_*.json`、`casting/plastic_sheet.json`、`vat_machine_recipe/etched_circuit_board.json`、`sequenced_assembly/unfinished_circuit_board.json`。
- `mods/tfmg-1.0.2f.jar` 内 `data/tfmg/recipes/sequenced_assembly/generator.json`（loops 3）、`crafting/kinetics/regular_engine.json`（钢锭 2 + 厚钢板 3 + 重型外壳，产 2）与中文 Ponder/tooltip。

## 仍须 JEI / 实机核对（未改变配方）

1. **IE 组装步骤引用的 `create:gantry_shaft` 物品标签未找到定义。** 已扫描全部 mods jar 的静态标签、KubeJS 数据和脚本。`kubejs/data/immersiveengineering/recipes/crafting/watermill.json`、`windmill.json` 的最后冲压步骤将真实物品写为 tag；`component_iron.json` 的第一部署步骤也如此。蓝图路线可绕过铁质部件序列的问题，但 IE 水车/风车的实际可制作性仍待确认。章节已明确此疑点，并提供 TFC 水轮/风车供电替代；它们无需作为主线任务前置。
2. **风车使用的 `tfc:brass_mechanisms` 标签有定义，不能当成缺失。** 已在 `mods/TFCAstikorCarts-1.20.1-1.1.9.jar` 内 `data/tfc/tags/items/brass_mechanisms.json` 验证，值为真实黄铜机件。`forge:ingots/irons` 也由 `kubejs/server_scripts/tags.js` 定义。
3. **新增钢铁构件配方的副产物 id 拼错。** `kubejs/data/tfmg/recipes/steel_mechanism.json` 写了 `tfc:metal/rods/steel`，真实物品是 `tfc:metal/rod/steel`。须确认此错误是否让整条配方加载失败。jar 内原生 `tfmg:sequenced_assembly/steel_mechanism` 是另一个配方 id、loops 2；新增配方 id 并不直接覆盖它。哪些路线经 KubeJS 材料统一后仍出现在 JEI，需要实机确认。
4. **抽油机输入口的中文覆盖有误导。** `kubejs/assets/tfmg/lang/zh_cn.json` 称其“电力输入”；对实际 jar 执行 `javap` 后，`MachineInputBlockEntity` 继承 Create 的 `KineticBlockEntity`，没有电力能力实现。原生 goggles 文本也为“未提供旋转动力”。章节按代码写旋转动力，仍建议按思索实际接轴验证。
5. **电路蚀刻的硫酸前置** 使用 Mekanism 硫酸。它是选做支线，当前没有强加整个 Mekanism 章末依赖，文案已明确原料。

## 根代理交叉复核补充

`TFC-IE-Crossover-1.20.1-1.3.1.jar` 的 `WaterWheelBlockEntityMixin` 与 `WindmillBlockEntityMixin` 都向相邻的 IE `IRotationAcceptor` 调用 `inputRotation`。因此 TFC 原生水轮、风车也能驱动动能发电机，原先写成只接受 IE 两种动力源不完整；已补进章节。Create 传动杆不属于这条联动。

新增钢铁构件配方与 jar 自带配方的材料和循环不同，且新增配方含上述错误副产物。正文不再把新增路线写成唯一确定可运行的路线，要求选择 JEI 当前显示的完整配方。

## 验证

- 独立 `QGEN_STAGE=_stage_verify_a`，基础两章 + 三工业章：`OK: 5 chapters, 110 quests`。
- `preview_create.png`、`preview_ie.png`、`preview_tfmg.png` 已目视检查，面板无重叠；跨节长线用 `hide_lines` 隐去，任务均可见。
- 全量 `build.py --check`：`OK: 20 chapters, 440 quests`。
- 没有写入实机；由根代理统一安装。静态生成器验证不保证上述可疑配方能运行。
