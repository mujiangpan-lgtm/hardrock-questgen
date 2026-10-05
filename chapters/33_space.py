from qlib import *

ch = Chapter("space", "星辰大海", icon="ad_astra:nasa_workbench", group="frontier", order=3,
             theme="space", subtitle="最后一关：带着一整个工业体系冲出大气层")

# ============================================================ A · 起点与新金属
ch.quest("start", 1.45, 3.225, "跨入航天时代", icon="immersiveengineering:arc_furnace", shape="gear", size=1.5,
         deps=["ie:finale"],
         subtitle="电弧炉烧出来的，不只是钛和哈氏合金",
         desc=["&o&7「离开这颗星球，需要把已有的工厂接成一张网。」&r",
               "",
               "&6航天工业&r把前面的产线汇到一起：钛与哈氏合金冶炼、Create 机械合成和序列组装、TFMG 石油加工、气动装配、Mekanism 与 Refined Storage 的后期部件。",
               "&6一阶火箭之前就有后期门槛：&r火箭燃料的催化剂要用反物质制作；基础航天服以整套 MekaSuit 为序列组装的输入；NASA 工作台还需要核聚变反应堆框架。",
               "&e起步检查：&r确认电弧炉、机械合成与稳定供电可用，再逐项按 R 查看航天服、燃料组分、NASA 工作台和火箭部件。",
               "",
               "&a提示：&r本章按材料、燃料、装配与探索组织路线。遇到尚未建立的设备时，回对应工业章节补齐，并继续用 JEI 查后期配方。"],
         tasks=[checkmark("我已经有一座能用的浸没工程电弧炉")],
         rewards=[item("tfc:metal/ingot/steel", 32), xp(200), item("tfc:metal/ingot/copper", 24), item("tfc:powder/flux", 32)])

ch.quest("titanium", 3.65, 2.225, "钛：轻而强", icon="immersivegeology:ingot_titanium", deps=["start"],
         shape="hexagon", size=1.25,
         desc=["&6钛&r是本包火箭机体与部件的重要材料，使用浸没地质学的加工路线。",
               "&e1.&r 钛铁矿的粉渣可经重力分离得到氧化钛副产物；也可在 JEI 中查看锐钛矿粉等其他来源。",
               "&e2.&r 氧化钛用盐酸在 IG 化学反应器中浸出钛溶液；再用水与钠砂或镁砂处理，得到&6钛砂&r。",
               "&e3.&r 钛砂可在&6浸没工程电弧炉&r炼成钛锭。这个锭配方没有助熔剂；直接制作钛储物块的另一配方则需要钛砂与助熔剂。",
               "",
               "&a查配方的方法：&r从钛锭按 R 向上追溯钛砂、溶液和原矿，确认机器类型及流体标签，再规划各段管路。"],
         tasks=[tag("forge:ingots/titanium", 4, title="钛锭 ×4")],
         rewards=[item("immersiveengineering:graphite_electrode", 3), xp(450), item("tfc:metal/ingot/steel", 32), item("tfc:powder/flux", 48)])

ch.quest("hastelloy", 3.65, 4.225, "哈氏合金：耐高温耐腐蚀", icon="immersivegeology:ingot_hastelloy",
         deps=["start"], shape="hexagon", size=1.25,
         desc=["&6哈氏合金&r是多种金属配成的合金，也是各阶火箭机体和工程部件的重要材料。",
               "&e电弧炉合金配方：&r镍粉 ×8、铬砂 ×4、氧化钼 ×2、铁粉 ×1、钨粉 ×1，产出&6哈氏合金锭 ×12&r。具体标签与替代原料按 R 查看。",
               "",
               "&e储物块：&r本包有哈氏合金锭 ×9 配合助熔剂 ×2 的电弧炉配方。不要把储物块当成金属冲压机的板材产物。",
               "&a备料：&r每阶火箭机体都要哈氏合金储物块 ×2，储罐等部件还会消耗哈氏合金工程块，先核对完整用途再扩大合金产线。"],
         tasks=[tag("forge:storage_blocks/hastelloy", 2, title="哈氏合金储物块 ×2")],
         rewards=[item("immersiveengineering:graphite_electrode", 3), xp(550), item("tfc:metal/ingot/nickel", 32), item("tfc:metal/ingot/steel", 32)])

ch.quest("steel_check", 5.85, 3.225, "钢材清点", icon="tfc:metal/ingot/steel", deps=["titanium", "hastelloy"],
         optional=True, shape="diamond",
         desc=["&6普通钢&r仍会用在基础设备与许多上游零件中。本任务清点 TFC 普通钢锭，帮助检查钢铁产线是否能持续供应。",
               "",
               "&c材料不能只看名字：&r红钢、蓝钢和普通钢是不同材料，不能默认互换。配方接受哪些钢锭或板材，要看当前 JEI 显示的标签。",
               "&a清点后：&r继续准备钛、不锈钢、哈氏合金和各模组机器部件，火箭零件远不止普通钢。"],
         tasks=[item("tfc:metal/ingot/steel", 20, title="钢锭 ×20")],
         rewards=[item("firstaid:bandage", 16), xp(225), item("immersiveengineering:graphite_electrode", 2), item("tfc:metal/ingot/copper", 24)])
# ============================================================ B · 石油与燃料
ch.quest("oil_find", 9.05, 2.225, "找石油", icon="tfmg:crude_oil_bucket", deps=["start"], hide_lines=True,
         desc=["本包有多条原油开采路线，产出的流体可以接入同一套分馏与燃料加工线：",
               "&7- &6TFMG 抽油机&r：用石油锤定位矿床，铺工业管道并搭建抽油结构，详细步骤见 TFMG 章节。",
               "&7- &6TFC Ore Excavation&r：使用对应钻井设备和下界合金钻头，从原油矿脉抽取。",
               "&7- &6浸没石油&r：勘探地下油藏，再用对应抽油设备开采。",
               "",
               "&a准备：&r先确认已找到匹配设备的矿床或油藏，再接好原油缓冲罐和输出管路。"],
         tasks=[checkmark("我已经找到并开始开采原油")],
         rewards=[item("tfmg:industrial_pipe", 24), xp(225), item("tfmg:cast_iron_pipe", 16), item("tfc:metal/ingot/steel", 16)])

ch.quest("distill", 11.25, 2.225, "蒸馏原油", icon="tfmg:steel_distillation_controller", deps=["oil_find"],
         shape="hexagon", size=1.25,
         desc=["把&6原油&r送进&6TFMG 分馏塔&r。本包每 &6100 mB&r 原油配方产出：",
               "&7- 重油 20 mB、柴油 20 mB、煤油 20 mB、汽油 30 mB、石脑油 10 mB。",
               "",
               "&6汽油&r是火箭燃料链的重要原料，其余馏分也要接入各自储罐，避免副产物堵住加工。",
               "&a检查：&r按 R 查看分馏配方，并按塔的设备要求连接流体输入与各路输出，并在塔底放置符合要求的热源。"],
         tasks=[item("tfmg:gasoline_bucket", 4, title="汽油桶 ×4")],
         rewards=[item("tfmg:industrial_pipe", 32), xp(350), item("tfmg:cast_iron_pipe", 24), item("tfc:metal/ingot/steel", 24)])

ch.quest("napalm", 13.45, 2.225, "混出凝固汽油", icon="immersiveengineering:mixer", deps=["distill"],
         desc=["&6浸没工程混合机&r把&6铝粉 ×3&r混入&6500 mB 汽油&r，产出&6500 mB 凝固汽油&r。",
               "",
               "&e做法：&r给混合机接通电力，放入铝粉并输入汽油，确认输出的是 TFMG 凝固汽油，再送入火箭燃料精炼线。",
               "&a小技巧：&r分别储存汽油与凝固汽油，精炼厂需要同时接收这两路流体。"],
         tasks=[checkmark("我用混合机做出了凝固汽油")],
         rewards=[item("immersiveengineering:dust_aluminum", 32), xp(400), item("tfc:metal/ingot/steel", 24), item("tfmg:industrial_pipe", 24)])

ch.quest("refine_fuel", 15.65, 2.225, "精炼火箭燃料", icon="immersiveengineering:refinery", deps=["napalm"],
         shape="hexagon", size=1.25,
         desc=["&6火箭燃料&r在&6浸没工程精炼厂&r制作：&610 mB 凝固汽油 + 15 mB 汽油&r，产出&625 mB 火箭燃料&r。",
               "&c还有一个必要条件：&r精炼厂的催化剂槽必须放入&6火箭燃料组分&r（kubejs:fuel_component）。",
               "",
               "&e催化剂来源：&r把硫粉与反物质送入 Mekanism 的&6反质子核合成器&r。反物质需继续追溯 SPS 等后期设备，先核对整条产线。",
               "&e试运行：&r接好精炼厂两路输入、催化剂与输出，确认储罐中确实出现 Ad Astra 火箭燃料。",
               "&a出发前：&r准备起飞与返程的燃料余量，燃料用量以火箭界面和当前配置为准。"],
         tasks=[item("kubejs:fuel_component", title="火箭燃料组分"), checkmark("我已用精炼厂产出火箭燃料")],
         rewards=[item("tfmg:industrial_pipe", 48), xp(900), item("tfmg:cast_iron_pipe", 32), item("tfc:metal/ingot/steel", 48), item("tfc:metal/ingot/copper", 32)])

ch.quest("tank", 17.85, 2.225, "钢燃料储罐", icon="ad_astra:steel_tank", deps=["titanium", "hastelloy"], hide_lines=True,
         any_dep=False,
         desc=["名称虽然是&6钢燃料储罐&r，本包的配方使用&6钛板&r、&6哈氏合金工程块&r和 Mekanism 的&6终极流体储罐&r。",
               "&e装配：&r使用 Create 的&6机械合成&r，按 R 核对完整图案与数量。",
               "",
               "&a后续：&r戴斯、紫金、耐热金属储罐保留了这套核心机器材料，外层板材改为对应星球金属。一阶火箭需要钢燃料储罐 ×2。"],
         tasks=[item("ad_astra:steel_tank", 2, title="钢燃料储罐 ×2")],
         rewards=[item("immersivegeology:ingot_titanium", 24), xp(500), item("immersivegeology:ingot_hastelloy", 16), item("tfc:metal/ingot/steel", 32)])
# ============================================================ C · NASA 工作台与一阶火箭
ch.quest("rocket_parts", 1.2, 8.45, "鼻锥与尾翼", icon="ad_astra:rocket_nose_cone", deps=["titanium", "hastelloy"], hide_lines=True,
         desc=["各阶火箭都需要&6鼻锥 ×1、尾翼 ×4&r。本包两种部件均用 Create 的&6机械合成&r制作。",
               "&7- 鼻锥：钛板、不锈钢板、哈氏合金板、不锈钢铆钉、避雷针与不锈钢工程块。",
               "&7- 尾翼：钛板、哈氏合金板、不锈钢铆钉与钨工程块。",
               "",
               "&e备料：&r分别按 R 查看两张机械合成图案，先凑齐工程块和板材，再装配完整的一套。"],
         tasks=[item("ad_astra:rocket_nose_cone", title="火箭鼻锥"),
                item("ad_astra:rocket_fin", 4, title="火箭尾翼 ×4")],
         rewards=[item("immersivegeology:ingot_titanium", 32), xp(650), item("immersivegeology:ingot_hastelloy", 24), item("immersivegeology:ingot_stainless_steel", 24)])

ch.quest("steel_engine", 1.2, 10.45, "钢引擎", icon="ad_astra:steel_engine", deps=["titanium", "hastelloy"], hide_lines=True,
         desc=["&6钢引擎&r是本包跨模组的&6机械合成&r产物，外层同样用钛板。",
               "&7- TFMG：引擎控制器、涡轮引擎、大型引擎。",
               "&7- Refined Storage：接口、控制器、探测器。",
               "&7- Mekanism：终极感应元件、动态储罐。",
               "&7- IG：不锈钢工程块。",
               "",
               "&e装配：&r按 R 查看图案与数量。后续高阶引擎仍需要这些核心机器，只是外层换成戴斯、紫金或耐热金属板。"],
         tasks=[item("ad_astra:steel_engine", title="钢引擎")],
         rewards=[item("immersivegeology:ingot_titanium", 32), xp(750), item("immersivegeology:ingot_hastelloy", 24), item("tfc:metal/ingot/copper", 48)])

ch.quest("nasa_workbench", 3.4, 9.45, "NASA 工作台", icon="ad_astra:nasa_workbench", deps=["rocket_parts", "tank"], hide_lines=True,
         shape="gear", size=1.5,
         subtitle="半个模组列表合出来的一台机器",
         desc=["&o&7「造火箭的工作台，本身也是一次工业总动员。」&r",
               "",
               "&6NASA 工作台&r用 Create 的&6机械合成&r制造，材料横跨多个工业模组：",
               "&7- 气动工艺：装配激光、装配钻头、压力室壁、可编程控制器。",
               "&7- 浸没工程：康铜板金属块、重型机械组件。",
               "&7- Refined Storage：便携网络、合成器、硬盘管理器。",
               "&7- Mekanism：感应外壳、核聚变反应堆框架。",
               "{@pagebreak}",
               "&e做法：&r按 R 查看完整机械合成图案，将各家部件凑齐后再装配。核聚变框架与存储设备都有自己的上游材料门槛。",
               "&a使用：&r工作台成品负责组装火箭机体；鼻锥、尾翼、引擎、储罐等零件仍在各自的配方设备中制作。"],
         tasks=[item("ad_astra:nasa_workbench", title="NASA 工作台")],
         rewards=[item("immersivegeology:ingot_titanium", 48), xp(1200), item("immersivegeology:ingot_hastelloy", 32), item("immersivegeology:ingot_stainless_steel", 32), item("immersiveengineering:graphite_electrode", 4)])

ch.quest("rover", 5.6, 8.45, "一阶漫游车", icon="ad_astra:tier_1_rover", deps=["nasa_workbench"], optional=True,
         shape="diamond",
         desc=["&6一阶漫游车&r在本包用 Create 的&6机械合成&r制作，可用于星球表面的运输。",
               "配方包括 SPS 外壳、精英化学品储罐、太阳能板、轮子、压缩板杆与航空引擎等部件，按 R 查看完整图案。",
               "",
               "&e使用前：&r给车辆加好燃料，并保留自己的航天服氧气。漫游车不代替真空环境下的个人防护。"],
         tasks=[item("ad_astra:tier_1_rover", title="一阶漫游车")],
         rewards=[item("immersivegeology:ingot_titanium", 24), xp(600), item("immersivegeology:ingot_hastelloy", 16), item("firstaid:bandage", 16)])

ch.quest("tier1_rocket", 5.6, 10.45, "组装一阶火箭", icon="ad_astra:tier_1_rocket", deps=["nasa_workbench", "rocket_parts", "tank", "steel_engine"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=["在 NASA 工作台上，用&6鼻锥 ×1、尾翼 ×4、钢燃料储罐 ×2、钢引擎 ×1&r，"
               "再加&6钛储物块 ×2 + 不锈钢储物块 ×2 + 哈氏合金储物块 ×2&r 合出&6一阶火箭&r。",
               "",
               "&c注意：&r这里的「不锈钢」同样是统一化的 &6#forge:storage_blocks/stainless_steel&r，"
               "具体来源详见 JEI（按 R 查看配方）。",
               "&a提示：&r一阶火箭只能去&6月球&r，更远的星球要更高阶的火箭。"],
         tasks=[item("ad_astra:tier_1_rocket", title="一阶火箭")],
         rewards=[item("immersivegeology:ingot_titanium", 48), xp(1200), item("immersivegeology:ingot_hastelloy", 32), item("immersivegeology:ingot_stainless_steel", 32), item("minecraft:golden_apple", 8)])

ch.quest("launch_pad", 7.8, 9.45, "发射台", icon="ad_astra:launch_pad", deps=["tier1_rocket"], optional=False,
         shape="hexagon",
         desc=["&6发射台是放置并发射火箭的必要设备&r。按 R 查看配方，先制作发射台物品。",
               "&e放置：&r在平坦、周围有空地的位置放下发射台，再将火箭放在中心。为火箭加油后登上火箭，按&6跳跃键&r开始发射。",
               "",
               "&c返程准备：&r随身带好发射台、返程燃料与足够氧气。到达目的地后收回着陆器中的火箭和物资，才能再次起飞。"],
         tasks=[item("ad_astra:launch_pad", title="发射台")],
         rewards=[item("minecraft:glowstone", 32), xp(300), item("tfc:metal/ingot/steel", 24), item("tfc:food/cooked_beef", 16)])
# ============================================================ D · 氧气与登月
ch.quest("oxygen_gear", 11.125, 9.45, "供氧设备与航天服", icon="ad_astra:space_suit", deps=["tier1_rocket"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=["&6基础航天服四件都要穿齐&r：面罩、胸甲、裤子与靴子。氧气储存在航天服胸甲里，供氧设备是合成元件。",
               "&e1.&r 准备对应的&6MekaSuit 四件&r，分别作为 Create 序列组装的输入；过程中使用熔融塑料、HDPE、能量板与富集精炼黑曜石等材料，按 R 核对各件步骤。",
               "&e2.&r 制作&6氧气装载机&r，接通电力并供水，机器从水中生产氧气。把航天服胸甲放入对应槽位充氧。",
               "&e3.&r 出发前检查四件均已穿戴、胸甲氧量充足，并携带兼容的备用氧气储罐。",
               "",
               "&c常见的坑：&r只拿着航天服或供氧设备无法保护自己；氧气耗尽也需要及时补充。"],
         tasks=[item("ad_astra:space_helmet", title="航天面罩"), item("ad_astra:space_suit", title="航天服胸甲"), item("ad_astra:space_pants", title="航天裤"), item("ad_astra:space_boots", title="航天靴"), item("ad_astra:oxygen_loader", title="氧气装载机"), checkmark("我已给胸甲充氧，并穿齐四件航天服")],
         rewards=[item("firstaid:bandage", 24), xp(700), item("mekanism:hdpe_pellet", 32), item("tfc:food/cooked_beef", 24)])

ch.quest("oxygen_base", 13.325, 8.45, "氧气装载机与分配器", icon="ad_astra:oxygen_distributor", deps=["moon"], hide_lines=True,
         optional=True, shape="diamond",
         desc=["&6氧气装载机&r用来生产和装载氧气；&6氧气分配器&r则能在有水和电力时为密闭房间供氧。",
               "分配器配方需要&6戴斯板&r等材料，登陆月球并加工戴斯后再准备。",
               "",
               "&e检查：&r搭好密闭房间，给分配器供水和电力，使用界面中的显示功能确认房间已被覆盖，发现漏气提示就补好孔洞。",
               "&c注意：&r房间的氧气不代替高温或低温防护，出门前仍要穿好适合目标星球的装备。"],
         tasks=[item("ad_astra:oxygen_distributor", title="氧气分配器"),
                item("ad_astra:oxygen_loader", title="氧气装载机")],
         rewards=[item("minecraft:glass", 64), xp(500), item("immersivegeology:ingot_titanium", 24), item("tfc:metal/ingot/copper", 32)])

ch.quest("moon", 13.325, 10.45, "登陆月球", icon="ad_astra:raw_desh", deps=["oxygen_gear", "launch_pad", "refine_fuel"], hide_lines=True, shape="hexagon",
         size=1.25,
         desc=["穿齐已充氧的航天服，把加好燃料的一阶火箭放在&6发射台&r上。登上火箭后按&6跳跃键&r起飞，在行星菜单选择&6月球&r。",
               "&c随身携带：&r返程发射台、燃料、备用氧气、食物、工具与不依赖氧气的照明。落地后收回着陆器中的火箭和物资。",
               "",
               "&6戴斯&r是月球的关键矿产。本包加工链为：",
               "&e1.&r 粗戴斯在&6反质子核合成器&r里配合反物质，得到戴斯粉。",
               "&e2.&r 戴斯粉与水、硫酸气体在&6加压反应室&r里处理成纯净戴斯粉。",
               "&e3.&r 纯净粉送入&6电弧炉&r炼成戴斯锭，再加工储物块、板材和二阶火箭部件。",
               "&c月球没有可呼吸的氧气：&r出舱前查看胸甲氧量，及时补充。"],
         tasks=[dimension("ad_astra:moon", title="登陆月球")],
         rewards=[item("firstaid:bandage", 24), item("immersivegeology:ingot_titanium", 32), xp(1200), item("immersivegeology:ingot_hastelloy", 24), item("minecraft:golden_apple", 8)])

ch.quest("tier2_rocket", 15.525, 9.45, "二阶火箭：戴斯机体", icon="ad_astra:tier_2_rocket", deps=["moon"],
         desc=["先沿&6反质子核合成器 → 加压反应室 → 电弧炉&r的路线加工月球粗戴斯，准备戴斯锭、储物块和板材。",
               "&e机体材料：&r通用鼻锥 ×1、尾翼 ×4、戴斯储罐 ×2、戴斯引擎 ×1、戴斯储物块 ×4、哈氏合金储物块 ×2。",
               "引擎与储罐仍用&6机械合成&r，整枚火箭在&6NASA 工作台&r组装，数量与图案按 R 核对。",
               "",
               "&a下一站：&r二阶火箭可到达&6火星&r，继续寻找紫金矿。"],
         tasks=[item("ad_astra:tier_2_rocket", title="二阶火箭")],
         rewards=[item("immersivegeology:ingot_titanium", 48), xp(1500), item("immersivegeology:ingot_hastelloy", 48), item("mekanism:hdpe_pellet", 48), item("minecraft:golden_apple", 12)])
# ============================================================ E · 远征与终章
ch.quest("mars", 18.85, 8.575, "远征火星", icon="ad_astra:raw_ostrum", deps=["tier2_rocket"], shape="hexagon",
         size=1.25,
         desc=["&6火星&r是二阶火箭的目的地，这里没有可呼吸的氧气，继续穿齐已充氧的航天服。",
               "&6粗紫金&r是下一阶机体的原料。与戴斯一样，本包需要&6反质子核合成器&r将原矿变为粉，再用&6加压反应室&r净化，最后由&6电弧炉&r冶炼。",
               "",
               "&a备料：&r三阶火箭需要紫金储物块和板材；金星、水星的高温防护服也要用到紫金板，别只备火箭那一份。"],
         tasks=[dimension("ad_astra:mars", title="登陆火星")],
         rewards=[item("firstaid:bandage", 32), xp(1500), item("mekanism:hdpe_pellet", 48), item("immersivegeology:ingot_hastelloy", 32), item("tfc:food/cooked_beef", 32)])

ch.quest("tier3_rocket", 21.05, 9.575, "三阶火箭：紫金机体", icon="ad_astra:tier_3_rocket", deps=["mars"],
         desc=["在&6NASA 工作台&r中使用鼻锥 ×1、尾翼 ×4、紫金储罐 ×2、紫金引擎 ×1、紫金储物块 ×4、哈氏合金储物块 ×2，组装&6三阶火箭&r。",
               "",
               "&a目的地：&r三阶火箭可前往&6金星与水星&r；&6金星的耐热金属矿&r是四阶机体的关键资源。",
               "&c先升级防护：&r按 R 查看整套&6下界合金航天服&r，本包用基础航天服、紫金板、戴斯板及供氧部件等进行升级。普通航天服不能提供这两颗高温星球所需的防护。"],
         tasks=[item("ad_astra:tier_3_rocket", title="三阶火箭")],
         rewards=[item("immersivegeology:ingot_titanium", 64), xp(1800), item("immersivegeology:ingot_hastelloy", 48), item("mekanism:hdpe_pellet", 64), item("minecraft:golden_apple", 12)])

ch.quest("mercury_venus", 23.25, 8.575, "水星与金星", icon="ad_astra:raw_calorite", deps=["tier3_rocket"],
         shape="hexagon", size=1.25,
         desc=["&6金星与水星&r都是高温、缺氧的目的地，出发前制作并穿齐&6下界合金航天服四件&r，给升级后的胸甲补充氧气。",
               "&e资源目标：&r寻找&6金星耐热金属矿&r，保留粗耐热金属。其加工仍沿&6核合成 → 加压反应净化 → 电弧炉&r的路线，详见 JEI。",
               "",
               "&c检查：&r防护、氧气与返程燃料缺一不可。装备升级后重新确认氧量，别只凭穿着基础航天服的经验出发。",
               "&a本任务：&r收集完整高温防护装备，并分别登陆金星和水星。"],
         tasks=[item("ad_astra:netherite_space_helmet", title="下界合金航天面罩"), item("ad_astra:netherite_space_suit", title="下界合金航天服胸甲"), item("ad_astra:netherite_space_pants", title="下界合金航天裤"), item("ad_astra:netherite_space_boots", title="下界合金航天靴"), dimension("ad_astra:mercury", title="登陆水星"), dimension("ad_astra:venus", title="登陆金星")],
         rewards=[item("firstaid:bandage", 32), xp(2000), item("immersivegeology:ingot_hastelloy", 48), item("mekanism:hdpe_pellet", 64), item("firstaid:morphine", 8)])

ch.quest("tier4_rocket", 25.45, 9.575, "四阶火箭：耐热机体", icon="ad_astra:tier_4_rocket", deps=["mercury_venus"],
         shape="hexagon", size=1.25,
         desc=["加工金星的粗耐热金属，准备&6耐热金属板&r和储物块，再用机械合成制作对应引擎与储罐。",
               "&eNASA 工作台：&r鼻锥 ×1、尾翼 ×4、耐热金属储罐 ×2、耐热金属引擎 ×1、耐热金属储物块 ×4、哈氏合金储物块 ×2。",
               "",
               "&a目的地：&r四阶火箭可以前往比邻星系的&6霜原星（Glacio）&r。抵达新环境后仍要检查氧气与温度，火箭阶数本身不提供个人防护。"],
         tasks=[item("ad_astra:tier_4_rocket", title="四阶火箭")],
         rewards=[item("immersivegeology:ingot_titanium", 64), xp(2500), item("immersivegeology:ingot_hastelloy", 64), item("immersivegeology:ingot_stainless_steel", 64), item("mekanism:hdpe_pellet", 64), item("tfc:gem/diamond", 16)])

ch.quest("glacio", 27.65, 9.575, "霜原星 Glacio", icon="ad_astra:oxygen_gear", deps=["tier4_rocket"], optional=True,
         shape="diamond",
         desc=["&6霜原星&r位于比邻星系，需要&6四阶火箭&r。它的大气中有可呼吸的氧气，但环境寒冷。",
               "",
               "&e出发前：&r准备适合寒冷环境的装备与补给，带好返程所需的火箭、发射台和燃料。",
               "&a落地后：&r先建立安全落脚点，再探索冰原、矿产与当地结构。按当前环境提示检查防护是否足够。"],
         tasks=[dimension("ad_astra:glacio", title="登陆 Glacio")],
         rewards=[item("tfc:food/cooked_beef", 32), xp(1600), item("firstaid:bandage", 32), item("immersivegeology:ingot_titanium", 48), item("immersivegeology:ingot_hastelloy", 32)])

ch.quest("space_station", 18.85, 10.575, "轨道空间站", icon="ad_astra:tier_1_rocket", deps=["moon"], hide_lines=True,
         optional=True, shape="diamond",
         desc=["&6轨道空间站&r可在&6行星选择界面&r中用材料创建。查看界面要求，备齐材料后在目标天体的轨道生成基础结构。",
               "",
               "&e落脚点：&r扩建密闭舱室、接通供电与氧气分配器，再建立仓储与返程准备区。轨道中仍需要供氧防护。",
               "&c注意：&r轨道重力与地面不同，先熟悉移动方式并记录空间站位置，避免飘离安全范围。"],
         tasks=[checkmark("我已经了解空间站的建造方式")],
         rewards=[xp(225), item("minecraft:glass", 32), item("tfc:metal/ingot/steel", 24), item("minecraft:glowstone", 16)])

ch.quest("finale", 23.25, 10.575, "星辰大海", icon="ad_astra:tier_4_rocket", deps=["tier4_rocket"],
         shape="gear", size=1.75,
         subtitle="从一块石头到四级火箭，这是人类文明的完整缩影",
         desc=["&o&7「从第一块石头，到一枚可以跨越恒星系的火箭。」&r",
               "",
               "你已经建立跨模组合金产线、石油到火箭燃料的链条，制作 NASA 工作台与完整航天防护，并走过月球、火星、金星和水星。",
               "&6四阶火箭&r已经完成，霜原星与轨道基地可以作为后续探索目标。",
               "&a另一道门：&r保留 Ad Astra 的粗戴斯、粗紫金、粗耐热金属与寒冰碎片，查看&6魔法暮色水晶&r的压力室配方，继续暮色森林章节。",
               "&a后续：&r完善反物质、化工、供电和仓储，让星球资源能稳定回流基地。"],
         tasks=[checkmark("我已完成四阶火箭并建立航天产线")],
         rewards=[item("immersivegeology:ingot_titanium", 64), levels(40), item("immersivegeology:ingot_hastelloy", 64), item("immersivegeology:ingot_stainless_steel", 64), item("mekanism:hdpe_pellet", 64), item("tfc:gem/diamond", 24)])

ch.section("第一节 · 起点与新金属", ["start", "titanium", "hastelloy", "steel_check"])
ch.section("第二节 · 石油与燃料", ["oil_find", "distill", "napalm", "refine_fuel", "tank"])
ch.section("第三节 · NASA 工作台与一阶火箭",
           ["rocket_parts", "steel_engine", "nasa_workbench", "rover", "tier1_rocket", "launch_pad"])
ch.section("第四节 · 氧气与登月", ["oxygen_gear", "oxygen_base", "moon", "tier2_rocket"])
ch.section("第五节 · 远征与终章",
           ["mars", "tier3_rocket", "mercury_venus", "tier4_rocket", "glacio", "space_station", "finale"])
