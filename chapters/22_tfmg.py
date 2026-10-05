from qlib import *

ch = Chapter("tfmg", "钢铁工业（TFMG）", icon="tfmg:steel_casing", group="industry", order=2,
             theme="tfmg", subtitle="焦炭、生铁与石油，铸就真正的重工业")

# ============================================================ A · 焦化与机壳
ch.quest("start", 1.45, 3.1, "钢，是工业的通行证", icon="tfmg:steel_casing", shape="gear", size=1.5,
         deps=["create:finale", "steel_age:finale"],
         subtitle="没有钢制外壳，就没有真正的重机械",
         desc=["&o&7「创造 Mod 教你用铜与黄铜搭机器，TFMG 教你用钢和石油建工厂。」&r",
               "",
               "&6Create: The Factory Must Grow（TFMG）&r是在创造 Mod 机械体系之上，"
               "扩展出的&6重工业&r模组：炼焦、高炉炼铁、抽油、分馏、塑料、内燃机、发电……",
               "",
               "&c本整合包的桥接：&rTFMG 自带的铸铁锭、钢锭、铝锭、镍锭、铅锭等&c已被隐藏&r，"
               "统一改用&6本整合包 TFC 的对应金属&r（&6forge:ingots/steel&r、&6forge:ingots/cast_iron&r"
               "等标签）。也就是说，钢铁时代打出的&6钢&r，直接就能喂给 TFMG 的机器。",
               "",
               "&a前置要求：&r你需要先完成&6创造（Create）&r章节（动力网络、机械台面）"
               "和&6钢铁时代&r（弄到稳定的&6钢锭&r来源），这里才能继续。"],
         tasks=[item("tfmg:steel_casing", title="钢制外壳")],
         rewards=[item("tfc:metal/ingot/steel", 16), xp(200), item("tfc:metal/ingot/copper", 12), item("tfc:powder/flux", 24)])

ch.quest("steel_casing", 3.65, 2.1, "钢制外壳：重型机器的身躯", icon="tfmg:steel_casing", deps=["start"],
         desc=[
               "&6钢制外壳&r是 TFMG 机器的基础结构材料，本包直接使用 TFC 等统一金属。",
               "",
               "&e制作：&r放置&6防腐木块&r，再手持&6钢薄板&r右键应用，得到钢制外壳；详见 JEI 的应用配方。",
               "&a准备：&r保持防腐木和钢板的供应，外壳既用于普通机器，也要继续加工成重型机械外壳。"],
         tasks=[item("tfmg:steel_casing", 4, title="钢制外壳 ×4")],
         rewards=[item("tfc:metal/ingot/steel", 24), xp(225), item("immersiveengineering:treated_wood_horizontal", 32), item("tfc:powder/flux", 24)])

ch.quest("heavy_casing", 3.65, 4.1, "重型机械外壳", icon="tfmg:heavy_machinery_casing", deps=["heavy_plate"],
         desc=[
               "&6重型机械外壳&r用于引擎、抽油机与其他重型设备，先准备钢制外壳和厚钢板。",
               "",
               "&e制作：&r在&6钢制外壳&r上应用&6厚钢板&r，完成外壳升级。详见 JEI。",
               "&a安排：&r先做厚钢板再升级外壳，可以避免在材料还没齐时提前攒大量半成品。"],
         tasks=[item("tfmg:heavy_machinery_casing", 2, title="重型机械外壳 ×2")],
         rewards=[item("tfc:metal/ingot/steel", 24), xp(250), item("immersiveengineering:ingot_lead", 16), item("tfc:powder/flux", 32)])

ch.quest("heavy_plate", 5.85, 3.1, "厚钢板：钢与铅的焊接", icon="tfmg:heavy_plate", deps=["steel_casing"],
         shape="hexagon", size=1.25,
         desc=[
               "&o&7「厚钢板先从砧上的一次焊接开始。」&r",
               "",
               "&e早期路线：&r在最低 &63 级 TFC 砧&r上，将&6钢板与铅板&r按焊接配方加工为厚钢板，准备助熔剂并加热到合适的焊接温度。",
               "&e气动路线：&r后期也可在压力室中用&6钢板、铅板与助熔剂&r加工，需要 &64.5 bar&r。",
               "&c注意：&r本包不是把钢锭连续冲压三次；按 JEI 确认材料、温度与设备。"],
         tasks=[item("tfmg:heavy_plate", 4, title="厚钢板 ×4")],
         rewards=[item("tfc:metal/ingot/steel", 24), xp(275), item("immersiveengineering:ingot_lead", 12), item("tfc:powder/flux", 32)])

ch.quest("steel_mechanism", 8.05, 2.1, "钢铁构件", icon="tfmg:steel_mechanism", deps=["heavy_plate"],
         desc=[
               "&6钢铁构件&r由&6厚钢板&r开始序列组装，是发电机等高级机器的重要零件。",
               "",
               "&e顺序：&r依次部署&6钢齿轮、Create Stuff & Additions 热力引擎、钢弹簧、一把钢螺丝、钢环与螺丝刀&r。",
               "&e检查：&r上面是本包新增的组装路线；其副产物写法存在疑点，先确认它在 JEI 中实际可用。模组自带路线的材料与循环不同，&6按当前 JEI 选择完整配方&r，成品与工具消耗也以该配方为准。",
               "&c常见的坑：&r拿普通钢板或错种金属零件代替厚钢板与钢制零件，会使半成品卡住。"],
         tasks=[item("tfmg:steel_mechanism", 2, title="钢铁构件 ×2")],
         rewards=[item("tfc:metal/ingot/steel", 24), xp(300), item("tfmg:steel_cogwheel", 8), item("tfmg:heavy_plate", 8)])

ch.quest("fireproof_bricks", 8.05, 4.1, "耐火砖块", icon="tfmg:fireproof_bricks", deps=["coke_oven"],
         desc=[
               "&6TFMG 耐火砖块&r由&6四块 TFMG 耐火砖&r合成，用于鼓风炉和耐高温化学设备。",
               "",
               "&e本包路线：&rTFC 未烧制耐火砖先经过&6焦炉加工&r成为&6沉浸地质耐火砖&r，再经过一次焦炉加工成为&6TFMG 耐火砖&r。",
               "&e设备：&r对应配方支持 IE 焦炉或 TFMG 炼焦炉，逐级查看 JEI 的产物名称，确认用的是正确砖种。",
               "&c注意：&r这里并非普通黏土烧制路线，也不是直接把 TFC 陶瓷耐火砖当作 TFMG 耐火砖。"],
         tasks=[item("tfmg:fireproof_bricks", 4, title="耐火砖块 ×4")],
         rewards=[item("minecraft:clay_ball", 48), xp(200), item("tfc:ceramic/unfired_fire_brick", 16)], hide_lines=True)
# ============================================================ B · 炼焦与炼铁
ch.quest("coke_oven", 11.375, 2.225, "炼焦炉：把煤变成焦煤", icon="tfmg:coke_oven", deps=["steel_casing"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=[
               "&o&7「焦煤和木馏油，从这一排小炉子里慢慢积起来。」&r",
               "",
               "&e制作：&r放置&6IE 焦炉砖&r，手持&6铸铁板&r右键应用，得到 TFMG 炼焦炉；也可用机械手自动应用。",
               "&e运转：&r按 JEI 投入支持的煤类原料；焦煤从底部排出，顶部提取二氧化碳，其他位置可提取木馏油。",
               "&a扩建：&r单炉速度较慢，可并排建一组；给焦煤与流体都安排出口，并留出储存缓冲。"],
         tasks=[item("tfmg:coke_oven", title="炼焦炉")],
         rewards=[item("minecraft:coal", 64), xp(300), item("tfc:metal/ingot/cast_iron", 16)])

ch.quest("coal_coke", 13.575, 3.225, "焦煤与杂酚油", icon="immersiveengineering:coal_coke", deps=["coke_oven"],
         desc=[
               "本包 TFMG 炼焦产出的焦煤统一为&6IE 焦煤&r，同时产生&6木馏油与二氧化碳&r。",
               "",
               "&e用途：&r焦煤用于对应的冶炼与化工配方，木馏油可作为支持的流体燃料或化工原料。",
               "&c区分：&r&6鼓风炉消耗空气与流体燃料&r，不能把焦煤塞进去当作它的热风燃料。",
               "&a建议：&r分别收集固体焦煤与流体副产物，用 JEI 确认下一道设备接受的燃料。"],
         tasks=[item("immersiveengineering:coal_coke", 16, title="焦煤 ×16")],
         rewards=[item("minecraft:coal", 48), xp(225), item("tfc:metal/ingot/cast_iron", 16)])

ch.quest("cast_iron_tank", 11.375, 4.225, "铸铁流体罐与管道", icon="tfmg:cast_iron_fluid_tank", deps=["steel_casing"], hide_lines=True,
         desc=[
               "鼓风炉与炼焦线需要&6铸铁流体罐与管道&r来连接输入、输出和缓冲储存。",
               "",
               "&e罐体：&r&64 根铸铁棒、2 块铸铁板与 2 块强化玻璃板&r，具体材料名称与摆法见 JEI。",
               "&e管道：&r铸铁板在最低 &63 级 TFC 砧&r上锻造，按 JEI 的规则加工。",
               "&c金属来源：&rTFC 铸铁来自赤铁矿、磁铁矿、褐铁矿等铁矿石的熔炼；生铁是另一种炼钢中间材料，不能混淆。"],
         tasks=[item("tfmg:cast_iron_fluid_tank", 2, title="铸铁流体罐 ×2"),
                item("tfmg:cast_iron_pipe", 4, title="铸铁流体管道 ×4")],
         rewards=[item("tfc:metal/ingot/cast_iron", 24), xp(225), item("tfc:metal/ingot/copper", 12), item("tfc:powder/flux", 24)])

ch.quest("blast_stove", 15.775, 3.225, "鼓风炉：给高炉吹热风", icon="tfmg:blast_stove", deps=["coal_coke", "cast_iron_tank", "fireproof_bricks"],
         shape="hexagon", size=1.25,
         desc=[
               "&o&7「鼓风炉负责热风，冶炼要由另一座炉子完成。」&r",
               "",
               "&e制作：&r使用铸铁管道、铸铁流体罐与 TFMG 耐火砖块，详见 JEI。",
               "&e搭建：&r按物品提示和思索构建多方块炉体，最低结构为&6三个竖直堆叠的鼓风炉块&r；扩建布局与接口见提示。",
               "&e运转：&r输入&6空气&r和支持的&6流体燃料&r，例如对应的木馏油或炉气，收集&6热空气与二氧化碳&r。",
               "&c注意：&r鼓风炉本身不炼铁；把热风送进接受它的设备，不能拿热空气管道代替分馏塔底部要求的方块热源。"],
         tasks=[item("tfmg:blast_stove", 3, title="鼓风炉 ×3")],
         rewards=[item("tfmg:cast_iron_pipe", 24), xp(350), item("minecraft:coal", 32), item("tfc:powder/flux", 32)], hide_lines=True)

ch.quest("finale_mid", 17.975, 3.225, "热风已备，钢铁管网成型", icon="tfmg:heavy_machinery_casing", deps=["blast_stove", "steel_mechanism", "heavy_casing"],
         any_dep=False, shape="hexagon", size=1.5, hide_lines=True,
         subtitle="从这里开始，向石油和电力分叉",
         desc=[
               "&o&7「有了机壳、零件与管网，工厂才能继续长大。」&r",
               "",
               "你已准备&6钢制外壳、重型机械外壳、厚钢板与钢铁构件&r，建立炼焦与热风设备。",
               "&e继续推进：&r",
               "&7- &6石油线&r：勘测油田 → 抽油机 → 原油储存 → 分馏与化工。",
               "&7- &6动力线&r：液体燃料驱动内燃机，旋转带动发电机，再用转换器连接 FE 设备。",
               "&a建议：&r先给管网和输出做好缓冲，分馏与化工都会同时处理多种材料。"],
         tasks=[checkmark("我已经建好炼焦炉和鼓风炉")],
         rewards=[item("tfc:metal/ingot/steel", 32), item("tfmg:cast_iron_pipe", 24), xp(400), item("immersiveengineering:coal_coke", 32)])
# ============================================================ C · 石油与分馏
ch.quest("oil_hammer", 1.2, 9.325, "石油锤：找到地下油田", icon="tfmg:oil_hammer", deps=["finale_mid"], hide_lines=True,
         desc=[
               "&6石油锤&r用于勘测地下石油矿床，先确认位置再建抽油机。",
               "",
               "&e制作：&r&62 个钢锭、1 块铝板与 2 根钢筋&r，详见 JEI。",
               "&e使用：&r手持石油锤右键地面调查，结合提示继续定位矿床。",
               "&a建议：&r在附近多个位置检测，确定适合铺设工业管道的位置，别按固定深度盲挖。"],
         tasks=[item("tfmg:oil_hammer", title="石油锤")],
         rewards=[item("tfc:metal/ingot/steel", 24), xp(225), item("tfc:metal/ingot/cast_iron", 16), item("firstaid:bandage", 6)])

ch.quest("industrial_pipe", 3.4, 9.325, "工业级管道铺设", icon="tfmg:industrial_pipe", deps=["oil_hammer"],
         desc=["找到&6油田&r后，&e从矿床到地表铺设一整条&6工业级流体管道&r，"
               "这是抽油机能正常工作的前提。",
               "",
               "&c常见的坑：&r管道必须&6连续直通&r到矿床所在深度，中间不能断。"],
         tasks=[item("tfmg:industrial_pipe", 8, title="工业级流体管道 ×8")],
         rewards=[item("tfmg:cast_iron_pipe", 24), xp(225), item("tfc:metal/ingot/steel", 16)])

ch.quest("pumpjack", 5.6, 9.325, "抽油机：地表磕头机", icon="tfmg:pumpjack_base", deps=["industrial_pipe"],
         shape="hexagon", size=1.25,
         desc=[
               "&o&7「游梁装好并连成整体，抽油机才能开始往复。」&r",
               "",
               "&e1.&r 让&6工业管道&r从矿床连续铺到地表，在顶端放抽油机基座。",
               "&e2.&r 在基座后方放锤支架，按思索布置曲柄、连接器、锤头与游梁部件。",
               "&e3.&r 使用&6强力胶&r把运动部件连接成完整结构，不能只把零件挨着摆放。",
               "&e4.&r 按思索安装&6机械输入口&r和上方曲柄，给输入口提供旋转动力，并接好流体输出。",
               "&c常见的坑：&r基座红色标记必须背对锤支架；不出油时检查结构、粘接、管道连续性和动力。"],
         tasks=[item("tfmg:pumpjack_base", title="抽油机基座"),
                item("tfmg:pumpjack_hammer", title="抽油机锤支架")],
         rewards=[item("tfmg:cast_iron_pipe", 32), xp(400), item("tfc:metal/ingot/steel", 32), item("firstaid:bandage", 8)])

ch.quest("crude_oil", 7.8, 9.325, "原油", icon="tfmg:crude_oil_bucket", deps=["pumpjack"],
         desc=[
               "&6原油&r由正确搭建并运转的抽油机从矿床中抽出，接到流体罐中缓冲储存。",
               "",
               "&e下一步：&r原油送入分馏塔，分离&6重油、柴油、煤油、汽油和石脑油&r。",
               "&a准备：&r先确认储罐和输出管道有空位，再继续扩抽油设备，避免原油到达后无处存放。"],
         tasks=[item("tfmg:crude_oil_bucket", 2, title="原油桶 ×2")],
         rewards=[item("tfc:metal/ingot/steel", 24), xp(250), item("tfmg:cast_iron_pipe", 16)])

ch.quest("steel_tank", 10, 9.325, "钢制流体储罐", icon="tfmg:steel_fluid_tank", deps=["crude_oil"],
         desc=[
               "&6钢制流体储罐&r既可储液，也是钢制分馏塔的基础结构。",
               "",
               "&e制作：&r钢棒、钢板与强化玻璃板，具体配方见 JEI。",
               "&a安排：&r普通原油缓冲罐与分馏塔主体分开规划，给控制器、输出口和底部热源留出施工空间。"],
         tasks=[item("tfmg:steel_fluid_tank", 2, title="钢制流体储罐 ×2")],
         rewards=[item("tfc:metal/ingot/steel", 24), xp(275), item("minecraft:glass", 16), item("tfc:powder/flux", 32)])

ch.quest("distillation", 12.2, 9.325, "分馏塔：把原油拆开", icon="tfmg:steel_distillation_controller", deps=["steel_tank", "steel_mechanism"],
         shape="hexagon", size=1.25,
         desc=[
               "&o&7「原油进入塔里，多种馏分从各层分开。」&r",
               "",
               "&e1.&r 按思索搭钢制流体储罐主体，在旁边放&6钢制分馏控制器&r。",
               "&e2.&r 最多安装&6六个分馏输出口&r，按思索用工业管道连接各层，并给每种产物安排储罐。",
               "&e3.&r 在储罐&6下方放置符合要求的热源&r，从控制器输入原油，观察塔体状态。",
               "{@pagebreak}",
               "&e本包原油配方：&r分离出&6重油、柴油、煤油、汽油与石脑油&r。石脑油还有进一步分馏路线，其他油品的加工按 JEI 查看。",
               "&c常见的坑：&r产物未排出会堵塞流程；热空气是一种流体，不能直接当成塔下的方块热源。"],
         tasks=[item("tfmg:steel_distillation_controller", title="钢制分馏控制器")],
         rewards=[item("tfmg:industrial_pipe", 32), xp(450), item("tfmg:cast_iron_pipe", 24), item("tfc:metal/ingot/steel", 32)], hide_lines=True)

ch.quest("fuels", 14.4, 8.325, "汽油、柴油与液化气", icon="tfmg:gasoline_bucket", deps=["distillation"], optional=True,
         shape="diamond",
         desc=[
               "&6汽油、柴油和其他燃料&r用于对应配置的内燃机。先在 JEI 确认油品来源，再按引擎提示选择装配配置。",
               "",
               "&e加工：&r原油分馏得到汽油和柴油，石脑油、重油等还可继续加工。并非每种燃料都由原油一轮直接产出。",
               "&a准备：&r为引擎安排独立油罐与废气出口，先用一台引擎测试燃料供应能否持续。"],
         tasks=[checkmark("我已经分馏出至少一种燃料")],
         rewards=[item("tfmg:industrial_pipe", 16), xp(175), item("tfc:metal/ingot/cast_iron", 16)])

ch.quest("plastic", 14.4, 10.325, "塑料：现代材料的起点", icon="tfmg:plastic_sheet", deps=["distillation"], hide_lines=True,
         desc=[
               "&o&7「化工线把流体做成现代材料。」&r",
               "",
               "&e合成：&r本包化学缸配方使用&6焦煤粉与乙烯或丙烯&r，在符合要求的&6钢制或耐火砖衬里化学缸&r中加热、搅拌，得到&6熔融塑料&r与沥青。",
               "&e浇铸：&r每 &6100 mB 熔融塑料&r铸成 &61 块 TFMG 塑料板&r；本包使用 PneumaticCraft 的熔融塑料流体。",
               "&e用途：&r塑料板用于管道、阀门、泵与电路材料，详见 JEI。",
               "&c注意：&r检查原料流体名称、化学缸材质、附件和加热条件；只把材料放进普通缸不会自动发生反应。"],
         tasks=[item("tfmg:plastic_sheet", 8, title="塑料板 ×8")],
         rewards=[item("tfmg:industrial_pipe", 24), xp(350), item("immersiveengineering:coal_coke", 32), item("tfc:metal/ingot/steel", 24)])
# ============================================================ D · 引擎与发电
ch.quest("rebar", 1.325, 14.425, "钢筋与钢筋混凝土", icon="tfmg:rebar", deps=["finale_mid"], hide_lines=True,
         desc=["&c本整合包特殊配方：&r&6钢筋&r要在&6TFC 砧上用锻铁棒（forge:rods/wrought_iron）锻造&r"
               "（tier 3，详见 JEI 锻造规则）。",
               "",
               "钢筋除了做石油锤，也是&6钢筋混凝土&r系列建材的核心材料——"
               "地基打得结实，厂房才扛得住大型机械的振动。"],
         tasks=[item("tfmg:rebar", 8, title="钢筋 ×8")],
         rewards=[item("tfc:metal/rod/wrought_iron", 24), xp(225), item("tfc:metal/ingot/steel", 16)])

ch.quest("engine", 1.325, 16.425, "常规引擎：液体燃料动力", icon="tfmg:regular_engine", deps=["heavy_casing", "distillation"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=[
               "&6常规引擎&r提供旋转动力，需要装配内部零件并供应对应的液体燃料。",
               "",
               "&e制作：&r&62 个钢锭、1 个重型机械外壳与 3 块厚钢板&r可合成两个引擎块，详见 JEI。",
               "&e装配：&r直线放置 &61–5 个引擎块&r，按提示或原理图选择配置，装入气缸和传动轴，接燃料入口与废气出口。",
               "&e启动：&r按思索接入红石启动，确认燃料和配置匹配，再连接负载。",
               "&c常见的坑：&r常规引擎不能直接烧煤或焦煤；缺气缸、燃料、排气或启动条件时不会正常运行。"],
         tasks=[item("tfmg:regular_engine", title="常规引擎")],
         rewards=[item("tfmg:cast_iron_pipe", 24), xp(350), item("tfc:metal/ingot/steel", 24), item("tfmg:heavy_plate", 8)])

ch.quest("generator", 3.525, 15.425, "发电机：从旋转到电力", icon="tfmg:generator", deps=["engine", "steel_mechanism"], hide_lines=True,
         shape="hexagon", size=1.5,
         desc=[
               "&o&7「转动发电机，电压和功率才有了来源。」&r",
               "",
               "&e制造：&r从 Create 传动杆开始，依次部署&6电容元件、钢板&r，绕入&6铜卷轴&r，再部署&6磁铁、钢铁构件和螺丝刀&r；整组循环 &63 次&r。",
               "&e使用：&r输入旋转动力，发电机输出&6TFMG 自己的电力&r，布线与电压分配按电力思索学习。",
               "&e互通：&r用&6TFMG 转换器&r将 TFMG 能量与 FE 互相转换，再连接 IE 等 FE 设备。转换方向与电压可配置。",
               "&c注意：&r不能把 TFMG 电力当成可直接通用的 FE；先确认转换方向与接口，再接其他模组机器。"],
         tasks=[item("tfmg:generator", title="发电机")],
         rewards=[item("tfmg:steel_mechanism", 8), xp(450), item("tfc:metal/ingot/copper", 32), item("tfc:metal/ingot/steel", 24)])

ch.quest("circuit", 5.725, 14.425, "电路板：迈向精密元件", icon="tfmg:circuit_board", deps=["generator", "plastic"], optional=True, hide_lines=True,
         shape="diamond",
         desc=[
               "&6电路板&r需要塑料、金属涂层、酸液和电子元件，适合化工线稳定后制作。",
               "",
               "&e1.&r &6塑料板 + 绿色染料&r制成空白电路板。",
               "&e2.&r 用机械手应用&6金板&r，得到涂层电路板。",
               "&e3.&r 在符合要求的化学缸中用&6硫酸&r蚀刻，得到蚀刻电路板。",
               "&e4.&r 序列部署&6电容元件、电阻、晶体管、电阻&r，整组循环 &64 次&r，完成电路板。",
               "&c常见的坑：&r电子元件是装配材料，需要事先制作；涂层在蚀刻之前，不能调换。酸液与完整工序详见 JEI。"],
         tasks=[item("tfmg:circuit_board", title="电路板")],
         rewards=[item("tfmg:empty_circuit_board", 8), xp(350), item("tfmg:plastic_sheet", 24), item("tfc:metal/ingot/gold", 8)])

ch.quest("finale", 5.725, 16.425, "重工业时代", icon="tfmg:generator", deps=["generator", "plastic"], any_dep=False, hide_lines=True,
         shape="gear", size=1.75,
         subtitle="从一块钢板，到一整座炼油厂",
         desc=[
               "&o&7「从钢板到炼油厂，车间开始处理更多种材料。」&r",
               "",
               "你已推进到&6旋转发电与塑料化工&r，两条线都完成才算建立起本章的核心工业能力。",
               "&7- &6机壳、厚钢板、钢铁构件&r：重型机器的材料基础。",
               "&7- &6炼焦与鼓风&r：分别供应焦煤、流体副产物和热风。",
               "&7- &6抽油与分馏&r：取得油品，再继续化工加工。",
               "&7- &6内燃机、发电机与转换器&r：连接旋转动力、TFMG 电力和 FE 电网。",
               "",
               "&a下一步：&r继续探索气动与 Mekanism 的加工、物流和能源体系，先在 JEI 核对每一步互通所需的设备。"],
         tasks=[checkmark("我已建立起自己的石油与钢铁重工业")],
         rewards=[item("tfc:metal/ingot/steel", 64), item("tfmg:plastic_sheet", 32), levels(16), item("tfmg:industrial_pipe", 48), item("tfc:metal/ingot/copper", 32)])

ch.section("第一节 · 焦化与机壳", ["start", "steel_casing", "heavy_casing", "heavy_plate", "steel_mechanism", "fireproof_bricks"])
ch.section("第二节 · 炼焦与炼铁", ["coke_oven", "coal_coke", "cast_iron_tank", "blast_stove", "finale_mid"])
ch.section("第三节 · 石油与分馏", ["oil_hammer", "industrial_pipe", "pumpjack", "crude_oil", "steel_tank", "distillation", "fuels", "plastic"])
ch.section("第四节 · 引擎与发电", ["rebar", "engine", "generator", "circuit", "finale"])
