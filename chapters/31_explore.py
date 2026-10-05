from qlib import *

ch = Chapter("explore", "探索与冒险", icon="map_atlases:atlas", group="frontier", order=1,
             theme="explore", subtitle="地图之外，是整片未知的大陆")

# ============================================================ A · 认路与标记
ch.quest("start", 1.45, 3.225, "走出家门", icon="map_atlases:atlas", shape="gear", size=1.5,
         deps=["stone_age:finale"],
         subtitle="在迷路之前，先学会怎么不迷路",
         desc=["&o&7「地图不会替你探险，但没有地图你只会在原地打转。」&r",
               "",
               "本章讲的是&6走出基地之后&r会遇到的一切：怎么认路、能去哪些地方、"
               "会碰上什么人和什么威胁，以及怎么把探险收益变现。",
               "",
               "&c先立好重生点、备好支撑梁和干粮&r（见「石器时代」），再往下看。"],
         tasks=[checkmark("我准备好出发探索了")],
         rewards=[item("tfc:torch", 8), item("tfc:food/barley_bread", 4), xp(20)])

ch.quest("atlas", 3.65, 2.225, "第一本地图册", icon="map_atlases:atlas", deps=["start"], shape="hexagon",
         size=1.25,
         desc=["&6地图册&r（Atlas）是你最早能拿到的导航工具，持有后&e手持使用&r即可记录你走过的地形。",
               "",
               "&e合成：&r&6六分仪&r + &6领航员时计&r + &6书&r（这两件工具见本章「导航三件套」，"
               "详见 JEI；暂时做不出来也不要紧）。",
               "&a更快的办法：&r&6村庄的制图师村民&r经常直接出售地图册，不想自己做就去买一本。",
               "",
               "&6用法：&r打开地图册翻页查看已探索区域；&6空地图&r放进地图册可以增加记录页数，"
               "多备几张空地图再出远门。"],
         tasks=[item("map_atlases:atlas", title="地图册")],
         rewards=[item("minecraft:map", 4), xp(30)])

ch.quest("gps_map", 5.85, 2.225, "GPS 地图模块", icon="kubejs:gps_map", deps=["atlas"], shape="hexagon",
         size=1.25,
         desc=["&c本整合包里，FTB 的世界地图和小地图默认是锁住的&r——这是刻意的后期门槛，"
               "不是没装模组。",
               "",
               "&e合成解锁：&r&6地图册&r + &6GPS 工具&r（pneumaticcraft）+ &6模块扩展卡&r，"
               "拼出一件&6kubejs:gps_map&r（图案详见 JEI）。合成后&a自动解锁 FTB 世界地图和小地图&r，"
               "这件物品本身用不着带在身上。",
               "",
               "&a小技巧：&rGPS 工具和模块扩展卡都是 PneumaticCraft 的中期产物，"
               "如果你还没接触气动科技，先靠地图册和路标撑过去也完全可以。"],
         tasks=[checkmark("我已经合成过一次 GPS 地图模块")],
         rewards=[item("minecraft:paper", 8), xp(40)])

ch.quest("minimap", 8.05, 3.225, "小地图与路径点", icon="minecraft:map", deps=["gps_map"],
         desc=["解锁后，默认键&6小地图&r会出现在屏幕角落，&6世界地图&r可以用快捷键打开（看 FTB 设置）。",
               "",
               "&e用途：&r",
               "&7- 世界地图上&e右键&r可以放置&6路径点&r，标记矿脉、村庄、沉船等重要地点",
               "&7- 小地图能显示周围已探索的地形、方向和高度",
               "&7- 世界地图界面还能&6占领周围区块&r作为领地保护（多人游玩时防止别人在你地基上乱动）",
               "",
               "&a建议：&r给家、矿脉、村庄分别用不同颜色/图标的路径点，省得名字记混。"],
         tasks=[checkmark("我已经在地图上标记了至少一个路径点")],
         rewards=[item("firmaciv:firmaciv_compass"), item("minecraft:paper", 8), xp(30)])

ch.quest("climate_zones", 3.65, 4.225, "读懂气候带", icon="firmaciv:barometer", deps=["start"],
         desc=["TFC 的世界按&6纬度（气温）&r和&6降水量&r划分出完全不同的生物群系与可种作物，"
               "详见「气候与生存」一章——这里只提探险相关的部分：",
               "&7- 纬度越靠近地图南北两端&c越冷&r，赤道附近终年炎热",
               "&7- 降水量决定&6沙漠/草原/雨林&r等群系类型，与温度正交",
               "",
               "&c出远门前&r用&6晴雨表&r或物品栏气候页看一眼目的地天气，"
               "长途跨纬度旅行记得带足&6保暖/降温衣物&r，不然还没到地方就先倒下了。"],
         tasks=[item("firmaciv:barometer", title="晴雨表")],
         rewards=[item("tfc_stone_tools:plant_fiber", 8), xp(20)])

ch.quest("boat", 5.85, 4.225, "独木舟：第一艘船", icon="firmaciv:kayak", deps=["climate_zones"], optional=True,
         shape="diamond",
         desc=["&o&7「河流和湖泊，是比森林更安静的路。」&r",
               "",
               "河流和海洋把大陆切成一块一块，迟早要靠船。&6独木舟&r是最早能造的一艘。",
               "",
               "&e配方：&r&6大型防水兽皮&r + 植物线/弦 + 木材（摆放详见 JEI）。",
               "&6大型防水兽皮&r由&6大型预制兽皮&r涂上多个&6蜂蜡&r制成——需要先拿到蜂蜡（Firmalife 养蜂，见「农耕」）。",
               "",
               "&e用法：&r放到水面上，&e右键&r乘坐，用&6独木舟划桨&r驱动前进。",
               "&a小技巧：&r独木舟轻便，可以直接放进背包随身携带，但只能你自己乘坐，不能运货。要载人载货，看本章「舟楫与天空」里的划艇。",
               "&c注意：&r大型船只拆解后只能拿回建造材料，别指望把船当临时工具拆了换钱。"],
         tasks=[item("firmaciv:kayak", title="独木舟")],
         rewards=[item("firmaciv:kayak_paddle"), xp(40)])
# ============================================================ B · 遗迹与战利品
ch.quest("desert_temple", 11.25, 2.1, "沙漠神殿", icon="tfc_loot:cobble_rock", deps=["start"], shape="hexagon", hide_lines=True,
         desc=["炎热干旱的沙漠地带偶尔会出现金字塔状的&6沙漠神殿&r，内部有陷阱地板和宝箱。",
               "",
               "&c常见的坑：&r神殿中央地下藏着&c压力板陷阱&r，踩中会引爆大量&6TNT&r，"
               "先用方块探测或从上方小心挖掘，别直接站上去。",
               "&a小技巧：&r宝箱里常有绿宝石、马鞍、附魔书等稀有物品，值得专程跑一趟。"],
         tasks=[checkmark("我找到并清理了一座沙漠神殿")],
         rewards=[item("minecraft:emerald", 2), xp(50)])

ch.quest("jungle_temple", 11.25, 4.1, "丛林神殿", icon="tfc_loot:cobble_rock", deps=["start"], shape="hexagon", hide_lines=True,
         desc=["潮湿的丛林里藏着被藤蔓覆盖的石质神殿，内部有&6拉线箭矢陷阱&r和&6藏宝室&r。",
               "",
               "&c警告：&r拉线会同时触发箭矢和开门机关，进门前先观察地面有没有细线。",
               "&a小技巧：&r神殿顶楼常有&6朝对角线放置的青金石方块&r，解谜方式和原版一致。"],
         tasks=[checkmark("我找到并清理了一座丛林神殿")],
         rewards=[item("minecraft:emerald", 2), xp(50)])

ch.quest("swamp_hut", 11.25, 6.1, "沼泽小屋", icon="tfc:thatch", deps=["start"], hide_lines=True,
         desc=["沼泽地表的小木屋，屋内常驻一个&6女巫&r，底下地板偶尔藏着&6猫咪召唤台&r。",
               "",
               "&c警告：&r女巫会投掷&c虚弱、中毒&r等负面药水，近战前先清点好血量和解毒手段。",
               "&a小技巧：&r击败女巫后村庄旁容易出现流浪猫，带回家能防跳蜘蛛进屋。"],
         tasks=[kill("minecraft:witch", 1, title="击败女巫 ×1")],
         rewards=[item("firstaid:bandage", 4), xp(40)])

ch.quest("shipwreck", 13.45, 2.1, "沉船与埋藏的宝藏", icon="firmaciv:kayak", deps=["boat"], hide_lines=True,
         desc=["海岸和近海海底散落着&6沉船&r残骸，船舱和宝箱里常有&6藏宝图&r。",
               "",
               "&e藏宝图&r在地图/世界图上标出一个大致位置，走到标记区域后&e潜行&r能让图标精确显示 X，"
               "挖到底就是一箱财宝（含&6海洋之心&r等稀有材料）。",
               "",
               "&c常见的坑：&r沉船大多在水下，下潜前记得准备好呼吸手段，别缺氧晕过去。",
               "&a小技巧：&r沿海也会生成专门的&6海洋主题村庄&r，常伴生渔夫和制图师，可以顺路补给。"],
         tasks=[checkmark("我打捞了一艘沉船并拿到了藏宝图")],
         rewards=[item("minecraft:spyglass"), xp(50)])

ch.quest("seven_seas", 13.45, 4.1, "海上奇遇：幽灵船队", icon="firmaciv:cannon", deps=["boat"], optional=True, hide_lines=True,
         shape="diamond",
         desc=["开阔海域偶尔会遇到成规模的&6幽灵船只&r（快艇、护卫舰、海盗船……），"
               "船上有武装的敌对船员和成箱的战利品。",
               "",
               "&c警告：&r这些船只火力和数量都不低，&c单人贸然靠近容易被包围&r，"
               "最好先造好自己的武装船，或者叫上同伴一起上船清剿。"],
         tasks=[checkmark("我登上并清理了一艘幽灵船只")],
         rewards=[item("minecraft:emerald", 4), xp(60)])

ch.quest("stronghold", 13.45, 6.1, "要塞、矿井与地牢", icon="tfc_loot:blackstone_rock", deps=["start"], hide_lines=True,
         shape="hexagon",
         desc=["地底深处的&6要塞&r是通往末地的必经之路，内部有图书馆、监牢和&6末地传送门房间&r。",
               "",
               "&e找要塞：&r&6末影之眼&r丢出后会飞向最近的要塞方向，多丢几次校正路线"
               "（具体合成与数量详见 JEI，末影之眼需要末影珍珠）。",
               "&c警告：&r要塞里常有&6伏击刷怪笼&r，走廊狭窄，近战前先确认退路。",
               "",
               "&a顺路收益：&r矿洞深处常见的&6废弹矢坑道&r（木支架+矿车轨道+箱子）和&6地牢&r"
               "（刷怪笼+箱子）也是额外的战利品来源，挖矿时留心。"],
         tasks=[checkmark("我找到了一座要塞")],
         rewards=[item("tfc:torch", 16), xp(50)])
# ============================================================ C · 村庄与贸易
ch.quest("village", 16.775, 2.225, "找到第一座村庄", icon="minecraft:emerald", deps=["start"], shape="hexagon", hide_lines=True,
         size=1.25,
         desc=["&o&7「有村庄的地方，就有现成的补给。」&r",
               "",
               "村庄按气候带分出不同建筑风格，村民职业也五花八门：农夫、渔夫、皮匠、铁匠、"
               "图书管理员、制图师……每种职业有自己专属的交易列表。",
               "",
               "&a小技巧：&r刚进村先看有没有&6铁傀儡&r保护，别惹恼村民招来攻击；"
               "也别乱动村民的床和工作站，否则会干扰他们晚上回家。"],
         tasks=[checkmark("我找到了一座村庄")],
         rewards=[item("tfc:food/barley_bread", 8), xp(40)])

ch.quest("villager_trade", 18.975, 2.225, "村民交易", icon="minecraft:emerald", deps=["village"],
         desc=["&c本整合包重做了全部村民交易！&r原版的绿宝石交易被改成了&6硬币交易&r，"
               "具体每个职业卖什么、要多少钱&c详见 JEI 或直接右键村民查看&r。",
               "",
               "&e规则要点：&r",
               "&7- 一级村民（刚出生、没升级过）的交易可以&6无限刷新&r，慢慢攒好价格再买",
               "&7- 部分装备类商品（盔甲、武器）会随机附带&6锻造纹饰&r，每个村民的花纹是固定的，"
               "换个村民可能开出不同样式",
               "{@pagebreak}",
               "&c注意：&r食物类商品带着&6保质期标记&r，买完别囤太久；酒类商品同理。",
               "",
               "&a建议：&r先去武器匠、盔甲匠逛逛，常能用几枚硬币换到比自己打造的更好的装备。"],
         tasks=[checkmark("我完成了一次村民交易")],
         rewards=[item("tfc:food/barley_bread", 4), xp(30)])

ch.quest("lithiccoins", 21.175, 2.225, "锂币：这个世界的硬通货", icon="lithiccoins:mint", deps=["villager_trade"],
         shape="hexagon",
         desc=["村民交易用的&c不是绿宝石&r，而是&6LithicCoins&r 硬币体系——"
               "铜、银、金、琥珀金……几乎每种金属都能铸币，&6硬币等级越高购买力越强&r。",
               "",
               "&e铸币流程：&r",
               "&e1.&r 把金属锭敲/铸成&6硬币坯&r（粗制 → 精炼 → 硬化，等级依次提升）",
               "&e2.&r 放上&6铸币台&r，配合&6底模&r冲压出带花纹的成品硬币",
               "&e3.&r 具体冲压配方、硬币等级对应购买力&c详见 JEI&r，别自己瞎猜数值",
               "",
               "&a小技巧：&r给村民看病（治疗僵尸村民）或多做几次交易能让其价格更友好；"
               "出远门前记得换算好要带的硬币面值，免得背着一堆大额硬币找不到对的商品。"],
         tasks=[item("lithiccoins:mint", title="铸币台")],
         rewards=[item("tfc:metal/ingot/copper", 4), xp(40)])
# ============================================================ D · 天气与野外威胁
ch.quest("weather_forecast", 1.2, 10.2, "天气预报", icon="weather2:weather_forecast", deps=["climate_zones"], hide_lines=True,
         desc=["&6天气预报&r物品可以提前查看未来一段时间的天气趋势，&e右键&r使用。",
               "",
               "&c警告：&rTFC 的天气比原版剧烈得多，暴雨、强风、&c龙卷风&r都会真实影响建筑和作物。"
               "出远门或者在空地搭建前，先看一眼预报。"],
         tasks=[item("weather2:weather_forecast", title="天气预报")],
         rewards=[item("tfc:torch", 4), xp(20)])

ch.quest("tornado_sensor", 3.4, 11.2, "龙卷风传感器", icon="weather2:tornado_sensor", deps=["weather_forecast"],
         desc=["&6龙卷风传感器&r放置后会监测周围空域，一旦探测到&c龙卷风&r形成就会发出红石信号。",
               "",
               "&a小技巧：&r把传感器的红石信号接到&6天气警报器&r（见下一个任务）上，"
               "就能做一套自动预警系统，不用自己天天盯着天空。"],
         tasks=[item("weather2:tornado_sensor", title="龙卷风传感器")],
         rewards=[item("minecraft:charcoal", 16), xp(30)])

ch.quest("tornado_siren", 5.6, 12.2, "天气警报器：拉响警报", icon="weather2:tornado_siren", deps=["tornado_sensor"],
         shape="hexagon",
         desc=["&o&7「风声渐起时，警报比侥幸更可靠。」&r",
               "",
               "&6天气警报器&r（Tornado Siren）通红石信号触发后会发出远距离可闻的警报声，"
               "提醒附近所有人躲避即将到来的龙卷风或暴风。",
               "",
               "&c警告：&r茅草屋、单层木屋&c扛不住龙卷风&r，第一年内尽快换成石头或砖房；"
               "警报响起时请立刻躲进地下室或坚固建筑，别留在空地上看风景。"],
         tasks=[item("weather2:tornado_siren", title="天气警报器")],
         rewards=[item("tfc:torch", 8), levels(3)])

ch.quest("darkness", 1.2, 12.2, "真正的黑暗", icon="tfc:torch", deps=["climate_zones"], hide_lines=True,
         desc=["本整合包的夜晚和地下&c是真的黑&r（True Darkness 模组）：没有光源的地方，"
               "即使满月也什么都看不见。",
               "",
               "&c常见的坑：&r很多新人死于摸黑走路掉悬崖或撞上怪物，而不是直接被打死。",
               "&a小技巧：&r火把、灵魂灯、安全提灯都要带足；基地周围和探险路线上多插几支火把做路标。"],
         tasks=[item("tfc:torch", 16, title="火把 ×16")],
         rewards=[item("tfc:torch", 16), xp(20)])

ch.quest("wild_predators", 3.4, 13.2, "野外的猛兽", icon="untamedwilds:bear_spawn_egg", deps=["darkness"],
         desc=["Untamed Wilds 给世界添加了大量更危险的野生动物，远不止鸡牛羊：",
               "&7- &c熊、大型猫科动物（狮/虎/豹）&r —— 丛林、针叶林、草原常见，正面打不过就跑",
               "&7- &c河马、犀牛、野猪群&r —— 领地意识强，别靠近它们的幼崽",
               "&7- &c鬣狗、骇鸟&r —— 群居，单挑一只容易被一群包围",
               "",
               "&a小技巧：&r大多数掠食者会被篝火和火把范围吓退；真要对抗，优先用标枪/弓箭打带跑，"
               "别用近战硬刚体型比你大的生物。"],
         tasks=[kill("minecraft:drowned", 3, title="击败溺尸 ×3（水边夜行代表性威胁）")],
         rewards=[item("firstaid:bandage", 4), item("firstaid:plaster", 4), xp(40)])

ch.quest("raiders", 1.2, 14.2, "强盗与袭击者", icon="minecraft:emerald", deps=["village"], hide_lines=True,
         desc=["杀死&6掠夺队长&r（举着旗子的那个）会让你获得&6不祥之兆&r效果，"
               "进入村庄后触发&6袭击事件&r：成波的掠夺者和劫掠兽会攻击村庄。",
               "",
               "&c警告：&r不祥之兆持续期间尽量留在村里和村民、铁傀儡并肩作战，"
               "独自跑去野外反而更危险。",
               "&a好处：&r打完一波袭击通常有不错的装备和经验掉落。"],
         tasks=[kill("minecraft:pillager", 5, title="击败掠夺者 ×5")],
         rewards=[item("minecraft:emerald"), xp(40)])
# ============================================================ E · 武装与远征
ch.quest("spartan_weapons", 8.8, 11.2, "斯巴达武器库", icon="spartanweaponry:bronze_longsword", deps=["start"], hide_lines=True,
         desc=["除了 TFC 原生的剑、标枪，Spartan Weaponry 还提供一整套&6剑、斧、锤、矛、弩&r"
               "等武器类型，每种金属（铜/青铜/黑铜/锻铁/钢……）都能打出对应品质。"
               "配套的 Spartan Shields 还提供同系列的金属&6盾牌&r（部分能格挡箭矢）。",
               "",
               "&c注意：&r石器/木制品质的斯巴达武器在本整合包&c已被屏蔽&r"
               "（TFC 自己的石器体系已经够用），只有金属品质才能打造。",
               "&a小技巧：&r长柄武器（矛、戟、长枪）对付成群小怪或骑乘作战效果更好；"
               "副手持盾、主手持单手武器是稳妥搭配。具体配方&c详见 JEI&r。"],
         tasks=[tag("spartanweaponry:bronze_weapons", title="任意青铜斯巴达武器")],
         rewards=[item("tfc:metal/ingot/copper", 4), item("minecraft:leather", 4), xp(30)])

ch.quest("muskets", 11, 10.2, "火枪时代的前奏", icon="musketmod:musket", deps=["spartan_weapons"], optional=True,
         shape="diamond",
         desc=["本整合包同时装了&6MusketMod&r（枪械本体）和&6tfc_muskets&r（TFC 风味的枪管/枪托/"
               "弹药组件），把黑火药武器纳入了锻造体系。",
               "",
               "&c注意：&r这是比较后期的装备线，需要先解决&6硫磺、硝石&r等黑火药原料的供应，"
               "普通远征阶段用标枪、弓弩和斯巴达武器完全够用。",
               "&a提示：&r枪管、枪托等部件的具体配方&c详见 JEI&r，这里先知道它存在即可。"],
         tasks=[item("tfc_muskets:gunpowder_pinch", title="一撮火药")],
         rewards=[item("tfc:powder/sulfur", 4), xp(30)])

ch.quest("finale", 11, 12.2, "带着地图，走向远方", icon="map_atlases:atlas",
         deps=["lithiccoins", "tornado_siren", "spartan_weapons"], any_dep=False, hide_lines=True,
         shape="gear", size=1.75,
         subtitle="世界比家门口大得多",
         desc=["&o&7「地图册记录你去过的地方，而传说只记录你做过的事。」&r",
               "",
               "你已经学会：&a认路与标点&r、&a辨认遗迹与陷阱&r、&a和村民做生意&r、"
               "&a躲避天气与野兽&r、&a带好武装再出门&r。",
               "",
               "&a下一步：&r带着这些准备，去更远的&6飞地与特殊维度&r看看"
               "（暮色森林、太空），或者回头把探险收获投入下一阶段的工业化。"],
         tasks=[checkmark("我已经准备好远征了")],
         rewards=[item("tfc:food/barley_bread", 8), item("firstaid:bandage", 4), levels(5)])

# ============================================================ 第六节 · 舟楫与天空
ch.quest("rowboat", 15.2, 10.2, "划艇：三人同舟", icon="firmaciv:rowboat_icon_only", deps=["boat"], hide_lines=True,
         shape="hexagon",
         desc=["&6划艇&r比独木舟大得多：3 个座位（玩家或动物，包括马），船尾还能再放 2 个容器。",
               "",
               "&c建造方式比较特殊——详见 TFC 野外指南「FirmaCiv」分类的图文教程：&r",
               "&e1.&r 用&6船匠脚手架&r（firmaciv:watercraft_frame_angled）在 2×3 区域摆出船形骨架",
               "&e2.&r 往脚手架上放硬木木板（橡木、山核桃、枫木等结实木种）",
               "&e3.&r 副手持锤子，往每块木板上打入&6铜螺栓&r（铜棒锻造而成）固定",
               "&e4.&r 船正中央装上&6桨架&r（oarlock）",
               "&e5.&r 用&6船桨&r右键完工的船体，划艇即可下水",
               "",
               "&c常见的坑：&r&6alekiships 的通用脚手架在本整合包已被隐藏/禁用&r，"
               "必须使用 FirmaCiv 自己的&6船匠脚手架&r（firmaciv:watercraft_frame_angled）。"],
         tasks=[checkmark("我造出了一艘划艇")],
         rewards=[item("tfc:wood/lumber/oak", 8), item("tfc:metal/ingot/copper", 4), xp(60)])

ch.quest("sailboat", 17.4, 10.2, "单桅帆船：风来助力", icon="firmaciv:sloop_icon_only", deps=["rowboat"],
         optional=True, shape="diamond",
         desc=["造船技术更熟练后，可以在船体上加装&6三角帆&r（小/中号），让风力分担划桨的辛苦。",
               "",
               "搭配&6船锚&r（下锚固定）、&6缆桩&r（系绳靠岸）使用，长途航海更省心。"],
         tasks=[checkmark("我的船装上了帆")],
         rewards=[item("tfc:metal/ingot/copper", 4), xp(40)])

ch.quest("navigation", 15.2, 12.2, "导航三件套", icon="firmaciv:sextant", deps=["boat"], hide_lines=True,
         desc=["出海或远行前，这三件 FirmaCiv 仪器能帮你认清自己在世界的哪里：",
               "&7- &6六分仪&r（sextant）：手持右键，测&6纬度&r（赤道 0 度，南北极 90 度）",
               "&7- &6领航员时计&r（nav_clock）：手持右键，测&6经度&r（本初子午线 0 度，一圈 360 度）",
               "&7- &6晴雨表&r（barometer）：握在手中测&6海拔&r（以海平面为基准）",
               "",
               "&a小技巧：&r六分仪 + 领航员时计 + 书就能合成上面「第一本地图册」；晴雨表测海拔，但造地图册用不上它。"],
         tasks=[item("firmaciv:sextant", title="六分仪")],
         rewards=[item("minecraft:paper", 8), xp(30)])

ch.quest("glider", 17.4, 12.2, "滑翔伞：换个角度看群峦", icon="vc_gliders:paraglider_wood", deps=["rowboat", "create:start"], hide_lines=True,
         shape="hexagon", size=1.25,
         subtitle="高处的风，是最廉价的交通工具",
         desc=["&o&7「从悬崖边跃下，世界忽然安静了。」&r",
               "",
               "&6基础滑翔伞&r的配方比想象中更重：需要&6大型防水兽皮&r（蜂蜡处理，同独木舟的材料）、"
               "皮革片、&6强化绳线&r、锯子，&c还需要 Create 的帆框架&r，详见 JEI 配方。",
               "",
               "&e用法：&r从高处跳下时&e按住跳跃键&r（默认空格）展开滑翔伞，可以安全地跨越峡谷、"
               "快速从山顶下山，比摔死强得多。",
               "&c注意：&r别一直飘在空中不落地，也不要飞得太久——它终究不是真正的飞行器。",
               "&a小技巧：&r后续可以用铜、铁、金、钻石等材料升级滑翔伞，提升机动性，详见 JEI。"],
         tasks=[item("vc_gliders:paraglider_wood", title="基础滑翔伞")],
         rewards=[item("tfc_stone_tools:plant_fiber", 16), xp(40)])

ch.quest("aircraft_pointer", 19.9, 12.2, "飞行器：留给工业时代", icon="immersive_aircraft:hull",
         deps=["rowboat", "create:finale"], hide_lines=True, optional=True, shape="diamond",
         subtitle="先把动能和钢铁学会，天空会在后面等你",
         desc=["&6Immersive Aircraft&r（飞艇、双翼机、固定旋翼机、四轴飞行器……）是本包里最晚期的"
               "空中载具，造价很高：机身需要 Create 的&6顺序组装&r（木材/木板反复加工），"
               "发动机需要&6锅炉 + 蒸汽机构件 + 钢制双层板&r等重工业产物。",
               "",
               "&c别急：&r这远不是现在就能碰的内容。先把&6「动能时代」（Create）&r和"
               "&6钢铁冶炼&r点亮，材料自然就齐了。",
               "",
               "&a小技巧：&r如果你更想要地面上的铁轨交通，「动能时代」章节后期还会提到"
               "&6Create 火车 / Steam 'n' Rails&r，也是远距离运输的好选择；"
               "本整合包同样提供了热气球和（后期）汽车等思路，详见 JEI 按 R 查询相关配方。"],
         tasks=[checkmark("我知道飞行器要等工业时代")],
         rewards=[item("tfc:powder/flux", 4), xp(20)])

ch.section("第一节 · 认路与标记", ["start", "atlas", "gps_map", "minimap", "climate_zones", "boat"])
ch.section("第二节 · 遗迹与战利品", ["desert_temple", "jungle_temple", "swamp_hut", "shipwreck",
                                "seven_seas", "stronghold"])
ch.section("第三节 · 村庄与贸易", ["village", "villager_trade", "lithiccoins"])
ch.section("第四节 · 天气与野外威胁", ["weather_forecast", "tornado_sensor", "tornado_siren",
                                  "darkness", "wild_predators", "raiders"])
ch.section("第五节 · 武装与远征", ["spartan_weapons", "muskets", "finale"])
ch.section("第六节 · 舟楫与天空", ["rowboat", "sailboat", "navigation", "glider", "aircraft_pointer"])
