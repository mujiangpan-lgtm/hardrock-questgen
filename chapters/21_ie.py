from qlib import *

ch = Chapter("ie", "沉浸工程", icon="immersiveengineering:hammer", group="industry", order=1,
             theme="ie", subtitle="从一把锤子，到遍布全场的电网")

# ============================================================ A · 工程师的第一把锤子
ch.quest("start", 1.45, 4.1, "工程师锤", icon="immersiveengineering:hammer", shape="gear", size=1.5,
         deps=["create:finale"],
         subtitle="沉浸工程的世界，从锻一把锤子开始",
         desc=[
               "&o&7「一把工程师锤，能把散落的结构块组装成机器。」&r",
               "",
               "&6沉浸工程（IE）&r提供发电、架空电线和多方块工业设备。本包把许多零件接入 TFC 锻造与 Create 序列组装。",
               "&e制作：&r锻铁锭在最低 &63 级砧&r上锻成&6工程师锤头&r，再配&61 根木棍与 1 份线&r组装。",
               "&e用途：&r调整支持的方块朝向、配置接口，并在多方块结构的指定位置敲击，完成机器组装。",
               "&a准备：&r制作并随身携带&6工程师手册&r，手册的分层预览与材料清单是搭建大型机器的依据。"],
         tasks=[item("immersiveengineering:hammer", title="工程师锤")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 12), xp(150), item("tfc:metal/ingot/copper", 8), item("tfc:powder/flux", 16)])

ch.quest("wirecutter", 3.65, 2.1, "剪线钳", icon="immersiveengineering:wirecutter", deps=["start"],
         desc=[
               "&6剪线钳&r用于拆除电线与维护电网，回收线路前先停止相关供电。",
               "",
               "&e制作：&r锻铁锭在最低 &63 级砧&r上加工钳头，再配&62 根木棍与 1 份线&r组装。",
               "&e使用：&r按工程师手册的操作拆除连接器之间的线路，整理时留意线缆掉落物。"],
         tasks=[item("immersiveengineering:wirecutter", title="剪线钳")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 8), xp(150), item("tfc:metal/ingot/copper", 8)])

ch.quest("voltmeter", 3.65, 4.1, "工程师多用表", icon="immersiveengineering:voltmeter", deps=["start"],
         optional=True, shape="diamond",
         desc=[
               "&6工程师多用表&r用来检查蓄电池等设备的&6储能&r，或测量线路的&6能量传输&r。",
               "",
               "&e排障：&r先检查发电机是否工作、连接器是否接在正确接口，再用多用表看实际供电。",
               "&c注意：&rIE 的 IF/FE 是电能单位，不能当作 Create 的旋转动力；线缆分档与接口接法见工程师手册。"],
         tasks=[item("immersiveengineering:voltmeter", title="工程师多用表")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 8), xp(150), item("tfc:powder/flux", 16)])

ch.quest("treated_wood", 3.65, 6.1, "防腐木：在杂酚油中浸泡", icon="immersiveengineering:treated_wood_horizontal",
         deps=["coke_oven"], shape="hexagon",
         desc=[
               "&6防腐木&r是工程师工作台、桨叶与许多 IE 结构件的基础材料，先用焦炉取得杂酚油。",
               "",
               "&e木桶路线：&r&6一块木板 + 200 mB 杂酚油&r，密封 &68000 ticks&r，得到防腐木块。",
               "&e另一条路线：&r防腐细木材也可在桶中浸泡后合成防腐木；后期有 TFMG 化学缸配方，详见 JEI。",
               "&c常见的坑：&r本包禁用了 IE 原版的工作台浸油配方，拿木板和一瓶油直接摆合成栏做不出来。"],
         tasks=[tag("forge:treated_wood", 8, title="防腐木板 ×8")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 12), xp(175), item("tfc:metal/ingot/copper", 8)], hide_lines=True)

ch.quest("component_iron", 5.85, 4.1, "铁质部件", icon="immersiveengineering:component_iron", deps=["treated_wood", "aluminum"],
         desc=[
               "&6铁质部件&r是发电机与其他设备的标准件。稳定的早期路线是&6工程师工作台 + 部件蓝图&r。",
               "",
               "&e1.&r 制作工程师工作台，放置时留出它占用的空间；它是直接放置的方块，不需要锤击组装。",
               "&e2.&r 准备部件蓝图并放入工作台。蓝图配方涉及铜、锻铁和铝等材料，详见 JEI。",
               "&e3.&r 每个铁质部件需要&62 块铁板、2 枚铜粒、2 枚金粒与 1 个 TFC 黄铜机件&r。",
               "&a建议：&r先用蓝图做出第一批部件；其他组装路线按 JEI 核对半成品与步骤。"],
         tasks=[item("immersiveengineering:component_iron", 4, title="铁质部件 ×4")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 16), xp(250), item("tfc:metal/ingot/copper", 12), item("immersiveengineering:treated_wood_horizontal", 24)], hide_lines=True)
# ============================================================ B · 焦炉与杂酚油
ch.quest("cokebrick", 9.05, 3.1, "焦炉砖", icon="immersiveengineering:cokebrick", deps=["start"],
         shape="hexagon",
         desc=[
               "&6焦炉砖&r用于 IE 的焦炉结构，先备齐材料再开工。",
               "",
               "&e配方：&r&64 块玄武岩砖、4 份灰浆和 1 个 TFC 耐火砖块&r，按 JEI 摆放。中心用的是砖块，不是单个陶瓷耐火砖。",
               "&e结构用量：&r一座焦炉要 &627 块焦炉砖&r，组成&6实心 3×3×3&r立方体，内部也不能留空。",
               "&a准备：&r耐火砖和灰浆沿用 TFC 材料链，可以边烧砖边制作焦炉外壁。"],
         tasks=[item("immersiveengineering:cokebrick", 8, title="焦炉砖 ×8")],
         rewards=[item("tfc:ceramic/fire_brick", 16), xp(225), item("tfc:powder/flux", 16)], hide_lines=True)

ch.quest("coke_oven", 11.25, 3.1, "焦炉：烘焦与产杂酚油", icon="immersiveengineering:coke_oven",
         deps=["cokebrick"], shape="hexagon", size=1.25,
         desc=[
               "&o&7「煤变成焦煤，杂酚油从炉子里积起来。」&r",
               "",
               "&e搭建：&r用 &627 块焦炉砖&r摆出实心 &63×3×3&r，拿工程师锤点击正面中央，形成焦炉。",
               "&e加工：&r放入 JEI 支持的煤类原料，等待焦煤与杂酚油产出。不同煤的时间与产油量不同。",
               "&e提取：&r用桶或管道与泵把杂酚油送入储罐，再供防腐木生产。",
               "&c常见的坑：&r油槽或成品栏积满会停止加工，留好两个出口，再安排连续投料。"],
         tasks=[checkmark("我搭好并点燃了焦炉")],
         rewards=[item("minecraft:coal", 48), item("tfc:metal/ingot/wrought_iron", 16), xp(300), item("tfc:ceramic/vessel", 4)])

ch.quest("creosote", 13.45, 2.1, "杂酚油与防腐木生产线", icon="immersiveengineering:treated_wood_horizontal",
         deps=["coke_oven"], hide_lines=True,
         desc=[
               "&6杂酚油&r把焦炉和防腐木生产连接起来，桶装储存适合起步，管道与泵适合长期运行。",
               "",
               "&e产线：&r焦炉产油 → 储罐缓冲 → TFC 木桶密封浸泡木料 → 收集防腐木。",
               "&a建议：&r先用少量木料确认配方与油量，再扩成多桶并行生产，机器停炉时也能继续用存油加工。"],
         tasks=[tag("forge:treated_wood", 16, title="防腐木板 ×16")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 16), xp(200), item("tfc:wood/lumber/oak", 32), item("tfc:powder/flux", 16)])

ch.quest("blastbrick", 13.45, 4.1, "高炉砖：工业装饰", icon="immersiveengineering:blastbrick",
         deps=["coke_oven"], optional=True, shape="diamond",
         desc=[
               "&6IE 高炉砖&r由地狱砖、黏液、灰浆、焦炉砖与岩浆膏合成，具体摆法详见 JEI。",
               "",
               "&c本包作者提示：&rIE 高炉&c无法工作，仅供装饰&r，不能把它作为矿石冶炼或炼钢路线。",
               "&e钢铁主线：&r仍使用钢铁时代章节介绍的&6TFC 高炉与精炼&r，制作普通钢不需要先得到蓝钢或红钢。",
               "&a用途：&r喜欢高炉外观可以建作厂房装饰，这个支线不会阻挡后续电网任务。"],
         tasks=[item("immersiveengineering:blastbrick", 4, title="高炉砖 ×4")],
         rewards=[item("minecraft:magma_cream", 8), xp(150), item("tfc:metal/ingot/wrought_iron", 8)])
# ============================================================ C · 发电与电网
ch.quest("watermill", 1.2, 10.2, "水车：河边的免费电力", icon="immersiveengineering:watermill", hide_lines=True,
         deps=["treated_wood"], shape="hexagon",
         desc=[
               "&6IE 水车&r把水流转化为&6IE 的机械转动&r，接上动能发电机后才输出电能。",
               "",
               "&e制作：&r先用防腐木料、胶水等制作水车桨叶，再从&6铁齿轮&r开始序列组装。每轮部署四片桨叶与一个黄铜机件后冲压，&6循环两次&r。",
               "&e安装：&r按手册布置流动水，把水车接在&6IE 动能发电机&r的轴面。",
               "&c注意：&r它不能直接接入 Create 传动杆网络。序列组装的半成品和完整步骤请先在 JEI 核对。",
               "&c配方疑点：&r本包序列有一步使用未找到定义的半成品标签。若 JEI 不显示可用配方，先用&6TFC 水轮&r邻接动能发电机轴面供电，继续主线。"],
         tasks=[item("immersiveengineering:watermill", title="水车")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 16), xp(250), item("immersiveengineering:treated_wood_horizontal", 24), item("tfc:metal/ingot/copper", 8)])

ch.quest("windmill", 1.2, 12.2, "风车：没有河的替代方案", icon="immersiveengineering:windmill", hide_lines=True,
         deps=["treated_wood"], optional=True, shape="diamond",
         desc=[
               "&6IE 风车&r是水车之外的发电驱动源，同样需要接在&6IE 动能发电机&r上。",
               "",
               "&e制作：&r以铁齿轮开始，序列部署风车叶片与黄铜机件，再冲压；整组&6循环两次&r，详见 JEI。",
               "&e选址：&r给叶片留出空旷空间，避免周围方块遮挡；安装方向和叶片扩展见工程师手册。",
               "&a提示：&r先核对本包的组装步骤，再备料，不要照原版工作台配方直接拼风车。",
               "&c配方疑点：&r本包序列有一步使用未找到定义的半成品标签。若该路线不可用，&6TFC 风车&r也能通过本包联动驱动动能发电机。"],
         tasks=[item("immersiveengineering:windmill", title="风车")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 12), xp(200), item("immersiveengineering:treated_wood_horizontal", 16), item("tfc:metal/ingot/copper", 8)])

ch.quest("dynamo", 3.4, 11.2, "动能发电机：把旋转变成电", icon="immersiveengineering:dynamo",
         deps=["component_iron"], any_dep=False, shape="hexagon", size=1.25,
         desc=[
               "&o&7「水车先转动，发电机再把它变成电。」&r",
               "",
               "&6动能发电机&r接受 IE 水车或风车的转动，输出&6IF/FE 电能&r。",
               "&a本包联动：&rTFC-IE Crossover 也让&6TFC 水轮与风车&r向相邻的动能发电机供能，把轮轴方向与发电机轴面对应即可；它们和 Create 动力源是不同体系。",
               "&e制作：&r普通工作台合成，需要&62 个锻铁锭、1 个铁质部件、1 个低压线圈和 2 份红石&r，详见 JEI。",
               "&e安装：&r按手册将水车或风车接到发电机轴面，再在&6橙色电力输出面&r安装合适的接线器，用电线送到机器或蓄电池。",
               "&c注意：&r它不接受 Create 传动杆的旋转。先完成至少一种&6IE 或 TFC 驱动源&r，再检查输出接口。"],
         tasks=[item("immersiveengineering:dynamo", title="动能发电机")],
         rewards=[item("tfc:metal/ingot/copper", 24), xp(300), item("tfc:metal/ingot/wrought_iron", 16), item("immersiveengineering:treated_wood_horizontal", 16)], hide_lines=True)

ch.quest("diesel_generator", 5.6, 10.2, "柴油发电机", icon="immersiveengineering:diesel_generator",
         deps=["dynamo"], optional=True, shape="diamond",
         desc=[
               "&6柴油发电机&r是需要组装的&6多方块结构&r，适合在燃料供给稳定后建设。",
               "",
               "&e建造：&r打开工程师手册查看材料表与分层布局，摆齐结构，再用工程师锤在指定位置组装。",
               "&e运转：&r接入 JEI 支持的燃料，安排电力输出；生物柴油需要榨油、发酵和精炼等配套流程。",
               "&a建议：&r先算清燃料产能再扩大发电规模，备用电厂也需要储油与输电线路。"],
         tasks=[checkmark("我按工程师手册组装并运行了柴油发电机")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 24), xp(350), item("tfc:metal/ingot/copper", 16), item("immersiveengineering:treated_wood_horizontal", 24)])

ch.quest("wire_lv", 5.6, 12.2, "低压电网：铜线圈", icon="immersiveengineering:wirecoil_copper",
         deps=["dynamo"], shape="hexagon",
         desc=[
               "&6IE 铜线圈&r用于低压线路。IF、FE、RF 描述的是电能，不是转速。",
               "",
               "&e本包制作：&r从卷轴开始，按序部署铜线，完整步骤见 JEI 的序列组装页。",
               "&e连接：&r手持线圈依次右键两端&6低压接线器&r；线路太长时增设低压继电器。",
               "&c注意：&r线缆与接线器必须同档匹配，过量传输可能烧毁线路，裸线也可能电击玩家。远离通行路线或使用绝缘线。",
               "&a调试：&r先接一台机器试供电，确认接口与线缆正确，再扩展电网。"],
         tasks=[item("immersiveengineering:wirecoil_copper", 4, title="低压线圈 ×4")],
         rewards=[item("tfc:metal/ingot/copper", 16), xp(200), item("tfc:metal/ingot/wrought_iron", 12), item("immersiveengineering:treated_wood_horizontal", 24)])

ch.quest("connector_lv", 7.8, 11.2, "低压接线器", icon="immersiveengineering:connector_lv",
         deps=["wire_lv", "aluminum"],
         desc=[
               "&6低压接线器&r把线路接到相邻机器的电力接口，输入和输出都要找准面。",
               "",
               "&e制作：&r&6铝棒 + Create Crafts & Additions 铜卷轴 + 棕色陶瓦&r，详见 JEI。",
               "&c区分：&r&6低压继电器&r只连接多段电线，&c不会向相邻机器输入或提取电能&r；接机器要用接线器。",
               "&a布线：&r用继电器做转角与中继，用接线器接发电机、蓄电池和用电机器。"],
         tasks=[item("immersiveengineering:connector_lv", 2, title="低压接线器 ×2")],
         rewards=[item("immersiveengineering:wirecoil_copper", 16), xp(200), item("immersiveengineering:ingot_aluminum", 16)], hide_lines=True)

ch.quest("capacitor_lv", 10, 10.2, "低压蓄电池：电网的水箱", icon="immersiveengineering:capacitor_lv",
         deps=["connector_lv"], optional=True, shape="diamond",
         desc=[
               "&6低压蓄电池&r储存电能，缓冲发电与用电之间的变化。放置后用工程师锤配置输入、输出面。",
               "",
               "&e组装：&r从防腐木块开始，以木桶为半成品，依次部署&6铅板&r、灌注 &6500 mB 红石酸&r、部署&6铁锭&r与防腐木，&6循环两次&r。",
               "&c常见的坑：&r完整序列不是在桶界面中混合材料；灌注和部署要使用对应的 Create 设备。",
               "&a接线：&r确认供电端与负载端连到各自接口，多用表可以检查蓄电池是否实际充电。"],
         tasks=[item("immersiveengineering:capacitor_lv", title="低压蓄电池")],
         rewards=[item("minecraft:redstone", 32), xp(225), item("tfc:metal/ingot/copper", 16), item("immersiveengineering:wirecoil_copper", 8)])

ch.quest("aluminum", 10, 12.2, "铝：接线器与蓝图材料", icon="immersiveengineering:ingot_aluminum",
         deps=["start"], shape="hexagon",
         desc=[
               "&6铝土矿&r按 TFC 矿脉生成方式分布，地表小矿粒可提示地下矿脉。低压接线器和部件蓝图已经会用到铝。",
               "",
               "&e早期路线：&r铝土矿在 &6650℃&r熔化，使用 TFC 小缸熔炼或坩埚加热，再用铸锭模具铸成&6IE 铝锭&r。",
               "&e找矿：&r先收集地表小矿粒，再用勘矿镐定位；不同品位的熔融量按 JEI 查看。",
               "&a准备：&r多留一些铝锭加工铝棒，后续 LV、MV、HV 接线器都要使用。"],
         tasks=[item("immersiveengineering:ingot_aluminum", 8, title="铝锭 ×8")],
         rewards=[item("tfc:powder/flux", 32), xp(250), item("tfc:metal/ingot/copper", 16), item("minecraft:charcoal", 32)], hide_lines=True)

ch.quest("wire_mv", 12.2, 11.2, "中压电网：琥珀金线", icon="immersiveengineering:wirecoil_electrum",
         deps=["connector_lv"], shape="hexagon",
         desc=[
               "&6中压线路&r使用&6琥珀金电线圈&r，适合扩大输电能力，线路与接线器须同档配套。",
               "",
               "&e线圈：&r卷轴经序列部署琥珀金线，详见 JEI。",
               "&e接线器：&r&6铝棒 + 金卷轴 + 棕色陶瓦&r，按本包配方制作。",
               "&c别混淆：&r&6电线圈（wirecoil_electrum）&r用于架线；&6中压线圈块（coil_mv）&r是机器合成材料。",
               "&a升级：&r先确认发电量与线路传输能力，再把机器逐个接入，使用多用表检查供电。"],
         tasks=[item("immersiveengineering:wirecoil_electrum", 4, title="中压线圈 ×4"),
                item("immersiveengineering:connector_mv", 2, title="中压接线器 ×2")],
         rewards=[item("immersiveengineering:ingot_aluminum", 16), xp(250), item("tfc:metal/ingot/copper", 16), item("immersiveengineering:treated_wood_horizontal", 32)])

ch.quest("wire_hv", 14.4, 11.2, "高压电网与变压器", icon="immersiveengineering:connector_hv",
         deps=["wire_mv"], optional=True, shape="diamond",
         desc=[
               "&6高压线路&r适合大功率与长距离输电，用高压电线圈配&6高压接线器或继电器&r。",
               "",
               "&e本包材料：&r高压线圈由卷轴序列部署&6银线、钢线、铝线、钢线&r制成；高压接线器用铝棒、琥珀金卷轴与矿渣玻璃，详见 JEI。",
               "&e变压器：&r用于连接不同档位的线路，普通与高压变压器的接法见工程师手册。",
               "&c注意：&r高压线路要预留安全距离，防止裸线触电与传输超载。给机器供电时核对其 FE 接口和实际能量需求。"],
         tasks=[item("immersiveengineering:connector_hv", title="高压接线器")],
         rewards=[item("immersiveengineering:ingot_aluminum", 24), xp(300), item("immersiveengineering:wirecoil_electrum", 16), item("tfc:metal/ingot/wrought_iron", 16)])
# ============================================================ D · 破碎、冲压与电弧炉
ch.quest("crusher", 1.325, 16.425, "粉碎机：矿物加工", icon="immersiveengineering:crusher", hide_lines=True,
         deps=["wire_mv"], shape="hexagon", size=1.25,
         desc=[
               "&6IE 粉碎机&r是一座用电的&6多方块结构&r，实际材料与组装位置按工程师手册查看。",
               "",
               "&e1.&r 摆齐结构，用工程师锤点击正面中央组装。",
               "&e2.&r 在电力入口安装接线器，保持足够的发电与传输能力。",
               "&e3.&r 从&6顶部&r投入支持的物品，或用传送带送入，再从输出端收集产物。",
               "&c本包变化：&r许多原版矿石配方已调整。只按 JEI 中实际存在的配方安排加工，不能保证所有矿石统一翻倍。"],
         tasks=[checkmark("我按手册组装并运行了 IE 粉碎机")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 32), xp(350), item("immersiveengineering:wirecoil_electrum", 16), item("tfc:metal/ingot/copper", 16)])

ch.quest("metal_press", 1.325, 18.425, "金属冲压机：模具加工", icon="immersiveengineering:metal_press", hide_lines=True,
         deps=["wire_mv"], shape="hexagon",
         desc=[
               "&6金属冲压机&r用模具加工特定物品，是带传送带的&6多方块结构&r。",
               "",
               "&e搭建：&r按工程师手册摆出结构，用工程师锤敲活塞组装，手持模具右键安装。电力接入顶部接口。",
               "&e投料：&r材料通过传送带进入。已确认&6铜粒 + 子弹壳模具&r能加工&6空弹壳&r，每次耗电 &62400 IF&r。",
               "&c本包变化：&r多种原版板、杆、齿轮加工配方已删除，不能用它代替全部 TFC 锻造；先查 JEI 再挑模具。"],
         tasks=[checkmark("我按手册组装并用模具加工了金属冲压机")],
         rewards=[item("tfc:metal/ingot/copper", 24), xp(350), item("tfc:metal/ingot/wrought_iron", 24), item("tfc:powder/flux", 32)])

ch.quest("arc_furnace", 3.525, 16.425, "电弧炉：高耗能冶炼", icon="immersiveengineering:arc_furnace",
         deps=["metal_press", "pneumatic:finale"], shape="hexagon", size=1.25,
         desc=[
               "&6电弧炉&r需要稳定供电和可更换的&6石墨电极&r，适合后期冶炼与特殊材料加工。",
               "",
               "&e搭建：&r按工程师手册完成多方块结构，安装&6三个石墨电极&r，接好背面的电力入口。",
               "&c材料前置：&r本包电极加工涉及气动压力室，先查看 JEI 的石墨锭与电极配方，准备好气动生产线。",
               "&e用途：&r&6玻璃 + 铁粉或干净铁矿粉&r可制作&6绝缘玻璃&r；矿渣加工得到的是&6矿渣玻璃&r，两者不同。",
               "&a维护：&r电极会磨损，产物与矿渣积满会阻止加工，定期检查供电、电极和输出。"],
         tasks=[checkmark("我搭建并通电了一座电弧炉")],
         rewards=[item("immersiveengineering:graphite_electrode", 3), xp(400), item("tfc:metal/ingot/wrought_iron", 32), item("immersiveengineering:wirecoil_electrum", 16)], hide_lines=True)

ch.quest("excavator", 5.725, 17.425, "挖掘机：自动化露天采矿", icon="immersiveengineering:excavator",
         deps=["arc_furnace"], optional=True, shape="diamond",
         desc=[
               "&6IE 挖掘机&r从该区域的&6抽象矿藏&r中持续开采矿物，并非挖掉周围的 TFC 矿脉方块。",
               "",
               "&e勘测：&r使用岩芯钻探与样本等手册工具确认矿藏，再决定设备位置。",
               "&e建造：&r挖掘机主体与斗轮分别按工程师手册组装，接好电力与产物输出。",
               "&a建议：&r先查样本中的矿种和储量，确认资源值得建设；无需寻找所谓矿脉标记块。"],
         tasks=[checkmark("我见过挖掘机的工作方式（JEI / 手册）")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 8), xp(150), item("minecraft:coal", 16)])

ch.quest("conveyor", 3.525, 18.425, "传送带：机器之间搬东西", icon="immersiveengineering:conveyor_basic",
         deps=["metal_press"], optional=True, shape="diamond",
         desc=[
               "&6IE 传送带&r放下就能运送物品，&6不需要电力&r。用工程师锤调整方向，按类型设置坡道与接口。",
               "",
               "&e用途：&r给粉碎机顶部送料、把材料送进金属冲压机，或把成品搬到储存容器。",
               "&a扩展：&r转弯、提取、投放和红石控制有对应变种；先用一小段确认方向，再连接整条产线。"],
         tasks=[item("immersiveengineering:conveyor_basic", 4, title="传送带 ×4")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 16), xp(200), item("tfc:metal/ingot/copper", 8), item("immersiveengineering:treated_wood_horizontal", 16)])
# ============================================================ E · 工坊收尾
ch.quest("toolbox", 8.925, 16.3, "工程师工具箱", icon="immersiveengineering:toolbox", deps=["component_iron"], hide_lines=True,
         optional=True, shape="diamond",
         desc=["&6工具箱&r放地上会生成一个小型多格容器，专门收纳 IE 的各类工具和零件，"
               "基地搭机器的工作台旁边放一个很方便。"],
         tasks=[item("immersiveengineering:toolbox", title="工程师工具箱")],
         rewards=[item("tfc:metal/ingot/copper", 8), xp(150), item("tfc:metal/ingot/wrought_iron", 8), item("tfc:powder/flux", 16)])

ch.quest("fluid_pipe", 8.925, 18.3, "流体管道", icon="immersiveengineering:fluid_pipe", deps=["start"], hide_lines=True,
         optional=True, shape="diamond",
         desc=[
               "&6IE 流体管道&r在最低 &63 级砧&r上由&6锻铁板&r锻造，用于连接油、水和其他工业流体。",
               "",
               "&e输送：&r连接机器的流体输出与储罐，按需要使用&6流体泵&r提取或提高输送能力。",
               "&c区分：&r&6流体出口（fluid_placer）&r负责把流体放到世界中，不是用于驱动管网的阀门。",
               "&a实践：&r先把焦炉杂酚油接到缓冲桶，确认流量与输入面后再延伸到加工设备。"],
         tasks=[item("immersiveengineering:fluid_pipe", 4, title="流体管道 ×4")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 16), xp(175), item("tfc:metal/ingot/copper", 8), item("firstaid:bandage", 4)])

ch.quest("metal_barrel", 8.925, 20.3, "金属桶：工业流体储存", icon="immersiveengineering:metal_barrel", hide_lines=True,
         deps=["component_iron"], optional=True, shape="diamond",
         desc=[
               "&6IE 金属桶&r适合保存工业流体，能够容纳热流体和气体；它与 IE 木桶的容量相同。",
               "",
               "&e制作：&r按本包的 TFC 焊接配方，使用&6两块锻铁双层薄板&r加工，详见 JEI。",
               "&a用途：&r作为管网缓冲储罐，检查接入面与剩余空间，避免上游机器因满槽停机。"],
         tasks=[item("immersiveengineering:metal_barrel", title="金属桶")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 16), xp(200), item("tfc:powder/flux", 24)])

ch.quest("finale", 11.125, 18.3, "沉浸工程：电气化基地", icon="immersiveengineering:dynamo", deps=["crusher", "metal_press", "wire_mv", "coke_oven"], hide_lines=True,
         shape="gear", size=1.75,
         subtitle="从一把锤子到一座电网",
         desc=[
               "&o&7「电线延伸到车间，工坊多了一套新的力量。」&r",
               "",
               "你已掌握&6工程师工具、焦炉与防腐木、发电机和 LV/MV 电网&r，并组装了粉碎机与金属冲压机。",
               "&e检查基地：&r至少一种电源持续工作，线路和接口匹配，产物能被收集，材料与能量不会因堵塞而停住。",
               "&a下一步：&r气动生产线会帮助准备电弧炉材料；TFMG 等工业体系可通过各自的转换设备接入 FE 电网。"],
         tasks=[checkmark("我已经建成了可运转的 IE 电气化工坊")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 64), item("tfc:metal/ingot/copper", 32), levels(14), item("immersiveengineering:wirecoil_electrum", 24), item("immersiveengineering:treated_wood_horizontal", 48)])

ch.section("第一节 · 工程师的第一把锤子", ["start", "wirecutter", "voltmeter", "treated_wood", "component_iron"])
ch.section("第二节 · 焦炉与杂酚油", ["cokebrick", "coke_oven", "creosote", "blastbrick"])
ch.section("第三节 · 发电与电网", ["watermill", "windmill", "dynamo", "diesel_generator", "wire_lv",
                                   "connector_lv", "capacitor_lv", "aluminum", "wire_mv", "wire_hv"])
ch.section("第四节 · 破碎、冲压与电弧炉", ["crusher", "metal_press", "arc_furnace", "excavator", "conveyor"])
ch.section("第五节 · 工坊收尾", ["toolbox", "fluid_pipe", "metal_barrel", "finale"])
