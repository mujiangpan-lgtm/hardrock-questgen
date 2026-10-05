from qlib import *

ch = Chapter("mekanism", "通用机械", icon="mekanism:steel_casing", group="industry", order=4,
             theme="mekanism", subtitle="能量、化学与自动化的通用框架")

# ============================================================ A · 钢质机壳
ch.quest("start", 1.45, 3.1, "钢质机壳：接续组装的骨架", icon="mekanism:steel_casing", shape="gear", size=1.5,
         deps=["iron_quartz", "pneumatic:finale"],
         subtitle="通用机械的一切，都从一块钢质机壳开始",
         desc=["&o&7「先有加工线，再把这条加工线装进新的机壳。」&r",
               "",
               "&6通用机械（Mekanism）&r在本包里承接 Create、浸没地质学和气动材料链。很多原版材料、机器与配方已被调整，必须查看本包 JEI。",
               "",
               "&e钢质机壳的实际工序：&r",
               "&71.&r 起始件为&6精炼存储的机器外壳（refinedstorage:machine_casing）&r。它也由 Create 接续组装获得，继续查看其 JEI 配方。",
               "&72.&r 注入&625 mB 铁英合金液&r。",
               "&73.&r 用&6机械手&r部署一张钢板。",
               "&74.&r 再注入 25 mB 铁英合金液，再部署一张钢板，完成一轮。",
               "",
               "&c设备区别：&r注液用 Create 注液器，部署用机械手，机械臂不能替代这两种工序。中间件要按 JEI 的顺序逐步处理，别把半成品误送进仓库。"],
         tasks=[item("mekanism:steel_casing", 4, title="钢质机壳 ×4")],
         rewards=[item("tfc:metal/sheet/steel", 12), xp(200), item("minecraft:redstone", 32)])

ch.quest("iron_quartz", 3.65, 2.1, "铁英合金", icon="tfc:metal/ingot/wrought_iron", deps=["create:finale", "steel_age:finale"],
         desc=["&6铁英合金&r是制作机器外壳和钢质机壳的合金液，本包配比为：",
               "&7- &6铸铁 50%～75%&r",
               "&7- &6石英 25%～50%&r",
               "",
               "在&6坩埚&r里按配比熔炼；铁英合金熔点为&6930℃&r。其它材料各自的熔化温度与配比仍要满足，确认坩埚已形成正确合金后再提取。",
               "&a连续生产：&r先查 RS 机器外壳的接续组装工序，再接 Mek 钢质机壳工序。为两段注液器都准备足够的合金液。"],
         tasks=[checkmark("我熔出了一炉铁英合金")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 16), xp(150), item("tfc:powder/flux", 24)])

ch.quest("osmium", 3.65, 4.1, "锇：浸没地质学的矿脉", icon="mekanism:ingot_osmium", deps=["start"],
         shape="hexagon", size=1.25,
         desc=["&6锇&r是本包通用机械的重要金属，优先沿&6浸没地质学（IG）&r矿物链寻找和加工自然锇。",
               "",
               "&e已经确认的冶炼路线：&r将矿物加工成&6锇砂（forge:grits/osmium）&r，用&6IE 电弧炉&r冶炼成锇锭。九份锇砂加两份助熔剂也可冶炼为锇块，详见 JEI。",
               "&c电弧炉要能实际运行：&r先准备电力、石墨电极及完整多方块，不要把砂丢进无法工作的 IE 高炉。",
               "&a控制电路还需要锇线：&r拿到锭后继续查杆与线的加工路线，原版「锇锭 + 红石」的电路做法在本包不适用。"],
         tasks=[tag("forge:ingots/osmium", 4, title="锇锭 ×4")],
         rewards=[item("tfc:powder/flux", 32), xp(250), item("immersiveengineering:graphite_electrode", 2), item("minecraft:redstone", 24)])

ch.quest("control_circuit", 5.85, 3.1, "控制电路", icon="mekanism:basic_control_circuit", deps=["osmium"],
         desc=["&6基础控制电路&r是多数 Mek 设备的核心部件。本包用&6压力室，2 bar&r加工以下材料：",
               "&7- HOP 石墨锭×1",
               "&7- 锇线×1",
               "&7- 塑料片标签内的材料×1",
               "&7- 铀氧化物×1",
               "",
               "&c材料都要查本包链条：&rHOP 石墨、锇线和铀氧化物各有加工门槛；塑料片可用项也应按 JEI 展开标签确认。",
               "&a后续电路：&r高级、精英、终极控制电路同样改为压力室配方。别照原版合成表升级，先准备对应等级的合金、富集材料与染料。"],
         tasks=[item("mekanism:basic_control_circuit", 4, title="基础控制电路 ×4")],
         rewards=[item("minecraft:redstone", 48), xp(300), item("pneumaticcraft:ingot_iron_compressed", 24), item("tfc:metal/ingot/copper", 16)])
# ============================================================ B · 富集与灌注：五机器
ch.quest("enrichment", 9.175, 2.225, "富集仓：纯化与富集材料", icon="mekanism:enrichment_chamber", deps=["control_circuit"],
         shape="hexagon", size=1.25,
         desc=["&6富集仓&r能把&6污浊粉&r处理成对应粉，也能制作富集碳等灌注原料。它不是粉碎机之后直接保证矿石倍增的万能设备。",
               "",
               "&e原版中间产物的顺序：&r化学压射室处理碎晶/适用输入 → 提纯仓处理碎片 → 粉碎机处理碎块 → 富集仓处理污浊粉；最前面还可能需要溶解、清洗和结晶。",
               "&c本包删改了大量原矿入口：&r对一种矿先按 U 查用途，确认实际输入、中间产物和最终冶炼设备；不要用原版二倍、四倍、五倍数值估算收益。",
               "&a初次使用：&r先用石墨制作富集碳，试好供电、侧面输入输出，再扩大产线。"],
         tasks=[item("mekanism:enrichment_chamber", title="富集仓")],
         rewards=[item("mekanism:basic_control_circuit", 8), xp(300), item("mekanism:ingot_osmium", 16), item("tfc:metal/ingot/steel", 16)])

ch.quest("crusher", 9.175, 4.225, "粉碎机", icon="mekanism:crusher", deps=["control_circuit"],
         desc=["&6粉碎机&r处理物品并输出粉末。例如本包仍有&6碎块 → 污浊粉&r的中间加工配方，部分金属锭也能磨成粉。",
               "",
               "&e先查用途：&r把目标矿物或中间产物放到 JEI，按 U 查看它能进哪台设备。TFC 和 IG 的含岩碎块、矿砂不能一概当成原版原矿。",
               "&c常见的坑：&r本包还删除了 Mek 粉碎机的生物燃料输出配方，不能把随便一种作物放进去就认定会产出生物燃料。"],
         tasks=[item("mekanism:crusher", title="粉碎机")],
         rewards=[item("mekanism:dust_osmium", 16), xp(250), item("mekanism:basic_control_circuit", 8)])

ch.quest("metallurgic_infuser", 9.175, 6.225, "冶金灌注机", icon="mekanism:metallurgic_infuser", deps=["control_circuit"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=["&6冶金灌注机&r把灌注物质注入物品。本包仍有&6铁粉 + 碳灌注物质 → 富集铁&r等配方，输入与数量详见 JEI。",
               "",
               "&e两种输入：&r一边放待加工物品，另一边放能转成对应灌注类型的材料。界面会显示内部灌注类型和余量，材料是否接受以 JEI 为准。",
               "&c三种核心合金也改成了压力室配方：&r灌注合金为 2 bar 的红石模块、HOP 石墨锭与塑料片；强化、原子合金以 4.5 bar 处理前级合金和对应富集材料。不要在这里照原版做这三种合金。",
               "&c不要混淆化学品：&r冶金灌注物质与普通气体是不同类型；气罐不能自动当作灌注原料。换配方前先检查内部是否残留了错误类型。"],
         tasks=[item("mekanism:metallurgic_infuser", title="冶金灌注机")],
         rewards=[item("mekanism:basic_control_circuit", 8), xp(300), item("mekanism:ingot_osmium", 16), item("minecraft:redstone", 32)])

ch.quest("combiner", 11.375, 3.225, "融合机与压缩机", icon="mekanism:combiner", deps=["enrichment", "metallurgic_infuser"], hide_lines=True,
         optional=True, shape="diamond",
         desc=["&6融合机&r把两种物品合并；原版常见用途是用矿物材料和岩石重组矿石，但本包保留哪些配方必须以 JEI 为准。",
               "",
               "&6锇压缩机&r接受锇材料作为另一项输入，用于制作&6精炼黑曜石锭、精炼辉石锭&r等。它不是「把锇粉直接压成锇锭」的机器。",
               "&a先查需求：&r这两台设备需要较高等级的电路与合金，等主线供电和基础加工稳定后再补齐。"],
         tasks=[item("mekanism:combiner", title="融合机"), item("mekanism:osmium_compressor", title="锇压缩机")],
         rewards=[item("mekanism:dust_osmium", 24), xp(350), item("mekanism:basic_control_circuit", 12), item("tfc:metal/ingot/steel", 24)])

ch.quest("energized_smelter", 11.375, 5.225, "富集碳与实际冶炼路线", icon="mekanism:enriched_carbon", deps=["enrichment"], hide_lines=True,
         desc=["本包的&6电力熔炼炉&r以及四档&6熔炼工厂&r配方被脚本删除，因此本节改用可实际制作的灌注原料目标。",
               "",
               "&e制作富集碳：&r将&6石墨标签内的材料&r送入富集仓，得到富集碳。后续压力室合金与电路升级会用到它；本包删除了富集碳直接转碳灌注物质的原版配方。",
               "&e矿物的最终冶炼：&r查目标粉末或矿砂的 JEI 用途，使用本包提供的 TFC、IE 电弧炉等路线。单纯做出 Mek 中间粉末不代表已经走通锭的产线。",
               "&a批量设备选择：&r下一节采用富集工厂，不要求制作配方已删除的熔炼工厂。"],
         tasks=[item("mekanism:enriched_carbon", 4, title="富集碳 ×4")],
         rewards=[item("minecraft:charcoal", 48), xp(225), item("mekanism:basic_control_circuit", 8)])
# ============================================================ C · 能量与电路
ch.quest("energy_cube", 14.7, 3.1, "能量立方：储能核心", icon="mekanism:basic_energy_cube", deps=["enrichment", "metallurgic_infuser"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=["&6能量立方&r存储电能，用于缓冲发电与机器耗电，也能给兼容的物品充电。它不能存流体或化学品。",
               "",
               "&e连接：&r把已有 IE、TFMG 或其它兼容电源通过对应线缆接入，检查能量立方侧面的输入输出设置，再给 Mek 设备供电。",
               "&c动力和电力不同：&rCreate 的转速与应力不会直接进入能量立方，必须先由能发电的设备转换。",
               "&a观察缓冲：&r机器运转时储量持续下降，说明发电跟不上负载；先扩充电源，再安装更多速度升级。"],
         tasks=[item("mekanism:basic_energy_cube", title="基础能量立方")],
         rewards=[item("mekanism:basic_control_circuit", 12), xp(350), item("minecraft:redstone", 48), item("tfc:metal/ingot/steel", 24)])

ch.quest("generators", 16.9, 2.1, "热力与生物能发电机", icon="mekanismgenerators:heat_generator", deps=["energy_cube"],
         optional=True, shape="diamond",
         desc=["Mek 提供多种发电设备，本包中所需材料按 JEI 准备。",
               "",
               "&7- &6热力发电机&r：使用熔岩热量或其它可燃资源，也会受相邻岩浆与维度环境影响；运行方式以设备界面为准。",
               "&7- &6生物能发电机&r：消耗生物燃料，但本包删除了 Mek 粉碎机的生物燃料配方，先查替代来源。",
               "&7- &6燃气发电机&r：消耗带可燃属性的气体，先查具体气体能否作为燃料。",
               "",
               "&a先做热力发电机试运行：&r接好通用线缆，观察输出与机器耗电，再决定是否扩建。"],
         tasks=[item("mekanismgenerators:heat_generator", title="热力发电机")],
         rewards=[item("minecraft:lava_bucket", 2), xp(200), item("mekanism:ingot_osmium", 12), item("tfc:metal/ingot/copper", 16)])

ch.quest("universal_cable", 16.9, 4.1, "通用线缆与配置器", icon="mekanism:basic_universal_cable", deps=["energy_cube"],
         desc=["&6通用线缆&r传输兼容的电能；&6配置器&r可设置管线连接、旋转方块或在扳手模式下拆卸设备。",
               "",
               "&e切换工具模式：&r查看「控制」里的&6Mekanism 物品模式开关&r按键，当前配置为 N；潜行时也可用滚轮切换，按工具提示确认模式。",
               "&e配置管线：&r在对应配置模式下潜行右键连接处切换推拉或断开等状态，机器侧面的输入输出还可在 GUI 中设置。",
               "&c常见的坑：&r潜行右键的作用取决于模式，不是通用的「切换模式」操作；拆卸前先确认处于扳手模式。"],
         tasks=[tag("mekanism:configurators", title="任意配置器"),
                item("mekanism:basic_universal_cable", 4, title="基础通用线缆 ×4")],
         rewards=[item("mekanism:basic_control_circuit", 8), xp(250), item("tfc:metal/ingot/steel", 24), item("minecraft:redstone", 32)])

ch.quest("logistical_transporter", 19.1, 3.1, "物流管道", icon="mekanism:basic_logistical_transporter", deps=["universal_cable"],
         optional=True, shape="diamond",
         desc=["&6物流管道&r搬运物品，可配合物流分类机过滤与分拣。机器需配置自动输出，或把管线连接设为拉取，物品才会离开容器。",
               "",
               "&e先试一段：&r用输入箱、目标机器、输出箱搭一个小回路，确认每面接收的是物品而非能量。",
               "&a仓储选择：&r小型产线可用管道；QIO 还需要更高阶材料与频率配置，可以等后期再升级。"],
         tasks=[item("mekanism:basic_logistical_transporter", 4, title="基础物流管道 ×4")],
         rewards=[item("mekanism:basic_control_circuit", 8), xp(250), item("mekanism:ingot_osmium", 16), item("tfc:metal/ingot/steel", 16)])
# ============================================================ D · 工厂与批量生产
ch.quest("factory", 1.325, 11.45, "工厂机：并行加工", icon="mekanism:basic_enriching_factory", deps=["energized_smelter", "metallurgic_infuser"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=["&o&7「加快一份原料的加工，也可以让几份原料一起开工。」&r",
               "",
               "&6工厂&r把对应单体机器升级为并行加工设备。基础、高级、精英、终极档分别有&63、5、7、9 个加工槽位&r。",
               "&e本任务做基础富集工厂：&r按 JEI 准备富集仓、控制电路和其它材料，也可使用适用的工厂安装器原地升级。",
               "&c本包禁用了熔炼工厂配方：&r不要照原版路线先做基础熔炼工厂。富集、粉碎、灌注等种类按各自实际配方选择。",
               "&a供电要够：&r并行槽位多了，满负载时总需求也会增加，先观察储能，再决定同时跑多少槽。"],
         tasks=[item("mekanism:basic_enriching_factory", title="基础富集工厂")],
         rewards=[item("mekanism:basic_control_circuit", 16), xp(500), item("mekanism:ingot_osmium", 24), item("tfc:metal/ingot/steel", 32)])

ch.quest("factory_upgrade", 3.525, 10.45, "工厂升级与速度/能量升级", icon="mekanism:upgrade_speed", deps=["factory"],
         optional=True, shape="diamond",
         desc=["&6工厂安装器&r用于把兼容的机器或工厂原地升到对应档位；手持安装器使用前先看 JEI 与物品提示，确认当前等级能接受该升级。",
               "",
               "&6速度升级&r提高加工速度并增加耗电；&6能量升级&r改善能耗与储能能力。两种升级可以同时安装，&c并不互斥&r；兼容种类和上限以机器升级面板为准。",
               "&a逐步调整：&r先加能量升级保证供电，再逐个增加速度升级，避免机器因缺电停停走走。"],
         tasks=[item("mekanism:upgrade_speed", title="速度升级"), item("mekanism:upgrade_energy", title="能量升级")],
         rewards=[item("mekanism:basic_control_circuit", 12), xp(350), item("mekanism:ingot_osmium", 24), item("minecraft:redstone", 48)])

ch.quest("digital_miner", 3.525, 12.45, "数字型采矿机", icon="mekanism:digital_miner", deps=["factory"],
         shape="hexagon", size=1.25,
         desc=["&6数字型采矿机&r按照设定的半径、高度范围与过滤器采集世界里的方块，并可把产物自动输出到相邻物流。",
               "",
               "&e设置：&r先添加目标过滤器，检查预览数量，设置输出与回填需求，再开启采矿。当前配置的最大半径是&632 格&r。",
               "&c范围不是靠雷达升级扩大：&r这里没有所述的雷达升级。速度与精准采集等设置会改变耗电，精准采集尤其需要更稳定的电源。",
               "&a先小范围试挖：&r确认过滤器只包含需要的矿物，准备好输出空间，再扩大范围；受保护区域仍可能阻止采集。"],
         tasks=[item("mekanism:digital_miner", title="数字型采矿机")],
         rewards=[item("mekanism:basic_control_circuit", 16), levels(8), item("mekanism:alloy_atomic", 12), item("mekanism:ingot_osmium", 32), item("tfc:metal/ingot/steel", 32)])
# ============================================================ E · QIO 与装备
ch.quest("qio_drive", 6.975, 12.45, "QIO 驱动器：云端仓储", icon="mekanism:qio_drive_base", deps=["factory"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=["&6QIO&r是无线物品仓储：&6驱动器阵列&r容纳驱动器，驱动器决定容量与物品种类上限，&6仪表板&r用于取放、搜索与合成。",
               "",
               "&e最简配置：&r放置一个阵列、装入驱动器，再放仪表板。为两者创建或选择&6同一 QIO 频率&r，确认频率的所有者与权限匹配。",
               "&a便携访问：&r便携式 QIO 仪表板也要绑定该频率；需要相关区块保持加载才能使用。高阶配方门槛详见 JEI，先用基础驱动器验证网络。"],
         tasks=[item("mekanism:qio_drive_array", title="QIO 驱动器阵列"),
                item("mekanism:qio_drive_base", title="QIO 驱动器"),
                item("mekanism:qio_dashboard", title="QIO 仪表板")],
         rewards=[item("mekanism:basic_control_circuit", 16), xp(750), item("mekanism:alloy_atomic", 16), item("immersiveengineering:ingot_lead", 32), item("tfc:metal/ingot/steel", 32)])

ch.quest("qio_io", 9.175, 10.45, "QIO 输入输出端口", icon="mekanism:qio_exporter", deps=["qio_drive"], optional=True,
         shape="diamond",
         desc=["&6QIO 输入端口&r把相邻容器里的物品导入已绑定的 QIO 频率；&6输出端口&r按过滤器把仓库物品送入相邻容器或机器。",
               "",
               "&e设置：&r各端口选择与阵列相同的频率，设置过滤器及允许的取放行为，先用少量物品试运行。",
               "&6QIO 红石适配器&r可以根据频率内物品数量输出信号，用于控制补货。",
               "&a产线汇入仓库：&r先确认原料与成品的过滤条件，避免输入输出互相循环搬运。"],
         tasks=[item("mekanism:qio_exporter", title="QIO 输出端口"), item("mekanism:qio_importer", title="QIO 输入端口")],
         rewards=[item("mekanism:basic_control_circuit", 12), xp(400), item("mekanism:alloy_atomic", 8), item("immersiveengineering:ingot_lead", 24)])

ch.quest("jetpack", 9.175, 12.45, "喷气背包", icon="mekanism:jetpack", deps=["qio_drive"], optional=True,
         desc=["&6喷气背包&r消耗&6氢气&r提供推力，穿在胸甲槽。普通模式下按住&6跳跃键&r上升，适合矿井与基地间移动。",
               "",
               "&e准备燃料：&r电解分离器处理水可以制氢，使用兼容的充气设备给背包装入氢气。&c不需要先液化成液氢。&r",
               "&e切换模式：&r查看控制设置中的胸部装备模式开关，选择普通、悬浮或关闭。",
               "&c出门前检查：&r燃料耗尽就无法继续飞行；先在低处试飞，留意 TFC 负重和装备条件。"],
         tasks=[item("mekanism:jetpack", title="喷气背包")],
         rewards=[item("mekanism:basic_control_circuit", 12), xp(350), item("mekanism:ingot_osmium", 24), item("firstaid:bandage", 12)])

ch.quest("hazmat", 9.175, 14.45, "防辐射服", icon="mekanism:hazmat_mask", deps=["qio_drive"], optional=True, shape="diamond",
         desc=["&6防辐射服&r需要&6面具、外衣、护腿、靴子四件完整穿戴&r，才提供完整的 Mek 辐射防护。接触放射性化学品、裂变装置与废料前先检查装备。",
               "",
               "&c防护不能治疗已有的辐射剂量：&r如果已经受到照射，穿上防护服也不会立即清除体内剂量。离开污染区域，并用放射量测定器查看自身剂量。",
               "&a分清仪表：&r盖革计数器用于环境辐射，放射量测定器用于玩家已接受的剂量。避免拆开含放射性物质的设备导致泄漏。"],
         tasks=[item("mekanism:hazmat_mask", title="防辐射面具"), item("mekanism:hazmat_gown", title="防辐射外衣"), item("mekanism:hazmat_pants", title="防辐射护腿"), item("mekanism:hazmat_boots", title="防辐射靴子")],
         rewards=[item("mekanism:dosimeter", 1), xp(350), item("firstaid:bandage", 16), item("immersiveengineering:ingot_lead", 16)])

ch.quest("finale", 11.375, 12.45, "通用机械的骨架", icon="mekanism:qio_dashboard", deps=["digital_miner", "qio_drive"], hide_lines=True,
         shape="gear", size=1.75,
         subtitle="从一块机壳，到一座自动化工厂",
         desc=["&o&7「机械手做出外壳，压缩空气做出电路，新的工厂才能开工。」&r",
               "",
               "你已经建立了&6钢质机壳与控制电路&r、&6富集与灌注加工&r、&6工厂机并行生产&r，并取得&6数字型采矿机与 QIO 仓储&r。",
               "",
               "&6MekaSuit、裂变与聚变、化学工业、反物质&r等内容还有更深的设备与材料门槛，具体路线继续查 JEI。",
               "&c辞典的用途：&r它查询物品、方块和化学品的标签，不是内置图文教程。判断配方接受哪些替代材料时会有帮助。",
               "&a下一步：&r把稳定供电、加工设备与仓储端口接起来，先让一条小产线连续运转，再扩大基地。"],
         tasks=[checkmark("我已经搭起了通用机械产线")],
         rewards=[item("mekanism:basic_control_circuit", 32), item("mekanism:ingot_osmium", 48), levels(20), item("mekanism:alloy_atomic", 24), item("tfc:metal/ingot/steel", 64)])

ch.section("第一节 · 钢质机壳", ["start", "iron_quartz", "osmium", "control_circuit"])
ch.section("第二节 · 富集与灌注", ["enrichment", "crusher", "metallurgic_infuser", "combiner", "energized_smelter"])
ch.section("第三节 · 能量与电路", ["energy_cube", "generators", "universal_cable", "logistical_transporter"])
ch.section("第四节 · 工厂与批量生产", ["factory", "factory_upgrade", "digital_miner"])
ch.section("第五节 · QIO 与装备", ["qio_drive", "qio_io", "jetpack", "hazmat", "finale"])
