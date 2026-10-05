from qlib import *

ch = Chapter("farming", "农耕与畜牧", icon="tfc:stone/hoe/sedimentary", group="survival", order=3,
             theme="food", subtitle="把野地变成田野，把野兽变成家畜")

# ============================================================ A · 从野草到田地
ch.quest("start", 1.45, 2.35, "野生作物与种子", icon="tfc:wild_crop/wheat", shape="gear", size=1.5,
         deps=["food:start"],
         subtitle="每一片野草丛里，都藏着明年的粮仓",
         desc=["&o&7「文明的第一块田，是从一撮野草的种子开始的。」&r",
               "",
               "野外散落着不起眼的&6野生作物&r（外观比种植版更隐蔽，容易和杂草混在一起），"
               "&e徒手或用刀破坏&r即可收获，掉落&6种子&r和少量&6农产品&r。",
               "",
               "&6野生作物只在每年 6 月至 10 月之间成熟&r，其余时间看起来像枯萎的杂草，"
               "要等到第二年夏天才会恢复。它们&c不需要灌溉&r，用水完全由当地气候"
               "（温度、降雨量）决定——找作物就该去适合它生长的气候带找。",
               "",
               "&a小技巧：&r种子也能当&6钓鱼鱼饵&r，捡到了别急着全种下去。"],
         tasks=[tag("tfc:wild_crops", 4, title="任意野生作物 ×4"),
                tag("tfc:seeds", 4, title="任意种子 ×4")],
         rewards=[item("tfc:food/barley_bread", 4), xp(30)])

ch.quest("hoe", 3.65, 2.35, "石锄与耕地", icon="tfc:stone/hoe/sedimentary", deps=["start"],
         shape="hexagon",
         desc=["石器时代就能做出&6石锄&r（石锄头 + 木棍）。&e右键&r泥土类方块的表面，"
               "就能把它耕成&6耕地&r，种子只能种在耕地上。",
               "",
               "&6金属锄&r效率更高、耐久更好，铜器时代起每种金属都有对应的锄，"
               "但&c不会提升作物产量&r，纯粹是加快耕地速度。",
               "",
               "&a小技巧：&r锄也能把&6缠根泥土&r转化为&6土&r，方便整地。"],
         tasks=[tag("tfc:hoes", title="任意锄")],
         rewards=[item("tfc:rock/loose/granite", 8), xp(30)])

ch.quest("plant", 5.85, 2.35, "播种", icon="tfc:seeds/wheat", deps=["hoe"], shape="hexagon", size=1.25,
         desc=["手持种子&e右键&r耕地即可播种。作物会随时间经过多个生长阶段，"
               "直到完全成熟才能收获。",
               "",
               "&c常见的坑：&r",
               "&7- 耕地离水源太远会&6缺水&r，生长停滞甚至枯萎",
               "&7- 温度或降雨量超出该作物适应范围，照样种不好，详见下一个任务",
               "&7- 南瓜、西瓜、豆类、西红柿、玉米、黄麻、甘蔗、纸莎草等&6藤蔓/高杆作物&r"
               "有特殊的占地或插木棍要求，&e悬停种子查看提示&r"],
         tasks=[checkmark("我已经在耕地上种下了第一批种子")],
         rewards=[tag("tfc:seeds", 4, title="任意种子 ×4"), xp(30)])

ch.quest("climate_crop", 8.05, 2.35, "温度、降雨与作物", icon="tfc:seeds/barley", deps=["plant"],
         desc=["每种作物都有自己的&6温度区间&r和&6湿度区间&r（悬停种子或在 JEI 中查看），"
               "&c超出范围作物无法正常生长&r，表现为迟迟不进入下一阶段甚至枯死。",
               "",
               "&e举例：&r大麦耐寒耐旱（-8~26℃，湿度 18~75%），适合温带甚至偏冷地区；"
               "水稻则需要温暖且&6种在含水耕地上&r才能生长。",
               "",
               "&a小技巧：&r安顿基地前先看看气候标签页的温度/降雨范围，"
               "决定你能稳定种出哪些作物；跨气候带的作物可以靠&6温室&r（本章后段）打破限制。"],
         tasks=[checkmark("我查看过作物所需的温度和湿度")],
         rewards=[item("tfc:food/barley_bread", 4), xp(30)])

ch.quest("hydration", 10.25, 2.35, "灌溉与保湿", icon="tfc:wooden_bucket", deps=["climate_crop"],
         shape="hexagon",
         desc=["手持锄&e右键&r耕地或作物可以查看当前&6湿度&r（0~100%）。湿度由降雨量提供基础值，"
               "但很多作物需要更高的湿度才能顺利成熟。",
               "",
               "&e提升湿度：&r在耕地&6周围放置水方块&r即可就近提升湿度；"
               "&c湿度不会自然下降&r（除非你搬到降雨更少的地方）。",
               "",
               "&6引水渠&r可以把水源从远处水平引到旱地（石砖+砂浆制作，详见「高级建筑材料」），"
               "沿途接到任意位置的水源或水流侧面即可通水，坏掉后水会立刻消失，不会留下永久水源。"],
         tasks=[checkmark("我知道如何给耕地保湿了")],
         rewards=[item("minecraft:water_bucket"), xp(30)])

ch.quest("nutrients", 12.45, 2.35, "氮磷钾三元素", icon="tfc:powder/sylvite", deps=["hydration"],
         shape="hexagon", size=1.25,
         desc=["&o&7「庄稼要吃饭，吃的就是地里的养分。」&r",
               "",
               "作物&c不施肥也能生长&r，但会慢得多。耕地含有三种营养：&b氮&r、&6磷&r、&d钾&r，"
               "每种作物都偏爱其中&6一种&r（悬停种子查看）。",
               "",
               "&e消耗偏爱的营养能加速生长，并小幅提升收获产量&r；"
               "作物同时也会小幅消耗另外两种营养，所以&c连续种同一种作物会越种越差&r，"
               "记得轮作或施肥补回去。"],
         tasks=[checkmark("我理解了氮磷钾三种营养的作用")],
         rewards=[xp(40)])
# ============================================================ B · 施肥与堆肥
ch.quest("fertilizer_basics", 15.775, 3.225, "施肥：手持右键", icon="minecraft:bone_meal", deps=["nutrients"],
         desc=["手持任意&6肥料&r&e右键&r耕地或作物即可施肥，成功会出现粒子特效。"
               "常见肥料来源各不相同，营养配比也不同：",
               "&7- &6骨粉&r：骨头加工，纯磷",
               "&7- &6硝石粉&r：硝石矿磨碎，偏钾，兼有少量氮",
               "&7- &6钾盐粉&r：钾石盐矿磨碎，纯钾",
               "&7- &6草木灰&r：烧过的篝火灰烬挖出来，磷钾都有，偶尔投火把入水也能得到",
               "&7- &6鸟粪石&r：地下深处和海边岩岸出产，三种营养都给，氮磷钾俱全",
               "",
               "具体数值&a详见 JEI 悬停&r，别死记硬背。"],
         tasks=[item("minecraft:bone_meal", 4, title="骨粉 ×4")],
         rewards=[item("tfc:powder/wood_ash", 4), xp(30)])

ch.quest("composter", 17.975, 2.225, "堆肥桶：变废为宝", icon="tfc:composter", deps=["fertilizer_basics"],
         shape="hexagon", size=1.25,
         desc=["&6堆肥桶&r用木材+土合成，是把厨余和杂物变成肥料的核心设备。"
               "它会把&2绿色&r（草、谷物、果蔬……）和&4棕色&r（干草、落叶、木灰……）物品转化为&6堆肥&r。",
               "",
               "&e产出：&r平均每 &612 天&r出一份堆肥，堆好后外观变成土色并带灰色颗粒特效，"
               "&e潜行+右键&r即可取出。堆肥三种营养都有，是最平民的全营养肥料。",
               "",
               "&c常见的坑：&r&c肉类和骨头会污染堆肥&r，变成红色、带恶心粒子的&6腐烂堆肥&r，"
               "用在作物上会&c直接杀死它&r！另外下雪能提效，但降雨量低于 150mm 或高于 350mm 都会拖慢速度，"
               "紧挨着摆放多个堆肥桶也会相互降低效率。"],
         tasks=[item("tfc:composter", title="堆肥桶")],
         rewards=[item("tfc:compost", 4), xp(40)])

ch.quest("compost_use", 20.175, 3.225, "第一批堆肥", icon="tfc:compost", deps=["composter"],
         desc=["攒够绿色和棕色材料并等待堆肥桶工作，取出&6堆肥&r直接当肥料用。",
               "",
               "&a建议：&r家禽家畜的粪便、割草剩下的草、吃剩的果皮菜叶都别浪费，"
               "顺手丢进堆肥桶，几乎不花额外成本就能稳定供肥。"],
         tasks=[item("tfc:compost", 4, title="堆肥 ×4")],
         rewards=[item("minecraft:bone_meal", 4), xp(30)])

ch.quest("mining_fertilizer", 17.975, 4.225, "矿物肥料：硝石与钾盐", icon="tfc:powder/saltpeter", deps=["fertilizer_basics"],
         optional=True, shape="diamond",
         desc=["如果你已经进入铜器时代并有了勘矿工具，可以专门挖&6硝石矿&r和&6钾石盐矿&r，"
               "磨成粉末使用，供肥效率比堆肥更高、更稳定。",
               "",
               "&a小技巧：&r硝石粉和钾盐粉也是部分化学/军事类配方的材料，&e多备一些总没错&r。"],
         tasks=[item("tfc:powder/saltpeter", 4, title="硝石粉 ×4")],
         rewards=[item("tfc:powder/saltpeter", 4), xp(30)])
# ============================================================ C · 收获与果园
ch.quest("scythe", 1.2, 9.325, "镰刀：高效收割", icon="tfc:metal/scythe/copper", deps=["composter"], hide_lines=True,
         shape="hexagon",
         desc=["&6镰刀&r是铜器时代才有的金属工具（没有石镰刀），&e右键&r成熟作物可以瞬间收获，"
               "也能一次性清理草丛和灌木叶。",
               "",
               "&c常见的坑：&r对未成熟的作物挥镰刀会直接把它铲掉、一无所获，"
               "务必先确认作物已经完全成熟（外观明显变化，悬停查看生长阶段）。"],
         tasks=[tag("tfc:scythes", title="任意镰刀")],
         rewards=[item("minecraft:charcoal", 8), xp(30)])

ch.quest("harvest_loop", 3.4, 8.325, "收获与留种", icon="tfc:food/wheat", deps=["scythe"],
         desc=["收获成熟作物会同时获得&6农产品&r和&6新的种子&r，形成循环：",
               "&e1.&r 用镰刀（或手/刀）收获成熟作物",
               "&e2.&r 把收获的种子重新种回耕地",
               "&e3.&r 剩下的农产品用来做饭、喂养动物或继续堆肥",
               "",
               "&a提示：&r作物&6完全成熟后若错过收获期&r，枯萎时也会自动变回种子，"
               "不会颗粒无收，但产量不如及时收割。"],
         tasks=[tag("tfc:foods", 8, title="任意收获的农产品 ×8")],
         rewards=[tag("tfc:seeds", 4, title="任意种子 ×4"), xp(40)])

ch.quest("wild_fruit", 1.2, 11.325, "野果与浆果灌木", icon="tfc:plant/blueberry_bush", deps=["start"], hide_lines=True,
         desc=["野外的&6浆果灌木&r（蓝莓、黑莓、树莓、鹅莓、蔓越莓等）和&6野生果树&r"
               "（苹果、橙子、桃子、李子……）同样由气候决定分布。",
               "",
               "&e收获：&r灌木成熟时&e右键&r采摘浆果（不会破坏灌木，可持续采collect）；"
               "果树则要等结果后采摘果实。",
               "&a小技巧：&r挖起野生浆果灌木或砍下果树树苗带回家种，就能建立自己的果园。"],
         tasks=[tag("tfc:wild_fruits", 4, title="任意野果/浆果 ×4")],
         rewards=[item("tfc:food/barley_bread", 2), xp(30)])

ch.quest("orchard", 3.4, 10.325, "种果树", icon="tfc:plant/red_apple_sapling", deps=["wild_fruit"],
         shape="hexagon", size=1.25,
         desc=["把果树&6树苗&r种在适宜气候的空地上（周围留出生长空间），"
               "耐心等待数年即可开花结果，此后&6每年固定季节&r持续产出水果。",
               "",
               "果树同样消耗土壤养分（氮为主），&a建议&r在果园周围也放几个堆肥桶或定期施肥。",
               "",
               "&c警告：&r果树怕极端低温，入冬前&6远低于其耐寒下限&r的严寒可能让它减产甚至死亡，"
               "挑选树种前先看清气候范围（详见 JEI / 野外指南）。"],
         tasks=[item("tfc:plant/red_apple_sapling", title="任意果树树苗")],
         rewards=[item("tfc:compost", 4), xp(40)])

ch.quest("berry_farm", 3.4, 12.325, "移栽浆果灌木", icon="tfc:plant/raspberry_bush", deps=["wild_fruit"],
         optional=True, shape="diamond",
         desc=["挖掘野生浆果灌木（通常需要&6铁锹&r且有一定几率获得完整植株）移栽到家附近，"
               "方便就近持续采摘，不用每次都去野外翻找。",
               "",
               "&a小技巧：&r把同类灌木种成一排，采摘和巡视都更方便。"],
         tasks=[tag("tfc:wild_fruits", 4, title="任意野果/浆果 ×4")],
         rewards=[item("minecraft:bone_meal", 4), xp(20)])
# ============================================================ D · 驯养与繁育
ch.quest("taming", 6.85, 10.325, "驯化与亲密度", icon="minecraft:egg", deps=["harvest_loop"], shape="hexagon",
         size=1.25,
         desc=["&o&7「野兽低头吃你手里的食物，就是信任的开始。」&r",
               "",
               "许多动物（牛、羊、猪、鸡、马、驴……）可以被&6驯化&r。对着未成年或成年动物"
               "&e潜行+右键&r手持它喜欢的食物（通常是谷物/种子，具体见野外指南或悬停动物），"
               "就能慢慢提高&6亲密度&r。",
               "",
               "&c常见的坑：&r",
               "&7- 亲密度&6不喂食每天会下降&r，达到一定程度（头顶出现白色心形轮廓）后才会停止衰减",
               "&7- 成年动物&c永远无法&r达到 100% 亲密度，只有&6幼年&r驯服才能封顶",
               "&7- 新生幼崽不会立刻产出资源，也不能繁殖，要等它&6成年&r"],
         tasks=[checkmark("我驯服了第一只动物（亲密度出现白色轮廓）")],
         rewards=[tag("tfc:seeds", 8, title="任意种子 ×8"), xp(40)])

ch.quest("breeding", 9.05, 10.325, "繁育：哺乳与产卵动物", icon="tfc:nest_box", deps=["taming"],
         desc=["动物分两大繁殖方式：",
               "&7- &6哺乳动物&r（牛、羊、猪、马……）：公母亲密度都超过 30% 时，"
               "母畜会&6怀孕&r，数月后直接产下幼崽",
               "&7- &6产卵动物&r（鸡、鸭、鹌鹑）：产下&6蛋&r后需要&6巢箱&r孵化，"
               "蛋也能直接吃（煎蛋/煮蛋）",
               "",
               "&a提示：&r公畜让母畜受精后，母畜下一枚蛋/下一胎才会继续，"
               "注意公母搭配饲养，别只养一种性别。"],
         tasks=[item("tfc:nest_box", title="巢箱")],
         rewards=[item("tfc:food/barley_bread", 4), xp(40)])

ch.quest("aging", 11.25, 8.325, "幼年、成年与衰老", icon="minecraft:egg", deps=["breeding"], optional=True,
         shape="diamond",
         desc=["动物的一生分三阶段：&6幼年 → 成年 → 衰老&r。",
               "",
               "&7- 幼年：不产资源，不能繁殖，长到一定天数后成年",
               "&7- 成年：可以挤奶/剪毛/捡蛋/繁殖，是主力阶段",
               "&7- 衰老：多次产出或繁殖后动物会衰老，衰老的动物&c只能屠宰吃肉&r，不再产出资源",
               "",
               "&a小技巧：&r留几只年轻的做种畜繁殖后代，衰老的及时屠宰补充肉食，"
               "维持畜群的年龄结构。"],
         tasks=[checkmark("我了解动物幼年/成年/衰老的区别")],
         rewards=[xp(20)])

ch.quest("milking", 11.25, 10.325, "挤奶", icon="minecraft:milk_bucket", deps=["breeding"], shape="hexagon",
         desc=["&6产奶动物&r（牛、山羊、牦牛）成年且亲密度足够后，"
               "手持&6木桶&r&e右键&r母畜即可挤奶，得到&6牛奶&r。",
               "",
               "&c注意：&r挤奶有&6冷却时间&r（牛、牦牛约每天一次，山羊反而更慢，约每 3 天一次），"
               "频率因动物而异，详见野外指南「畜牧业」条目。",
               "",
               "牛奶可以直接饮用解渴，也是乳制品的原料。"],
         tasks=[item("minecraft:milk_bucket", title="牛奶桶")],
         rewards=[xp(50)])

ch.quest("shearing", 11.25, 12.325, "剪羊毛", icon="minecraft:shears", deps=["breeding"], shape="hexagon",
         desc=["&6产毛动物&r（绵羊、羊驼、麝牛）成年且毛长够长时，手持&6剪刀&r&e右键&r即可剪毛，"
               "获得&6羊毛/驼毛&r，用于纺线、织布、保暖衣物。",
               "",
               "&c注意：&r剪毛后需要&6等待毛重新长&r才能再剪，不同动物生长速度不同"
               "（羊驼约 6 天最快，麝牛约 4 天，绵羊最慢约 9 天），别竭泽而渔。"],
         tasks=[item("minecraft:shears"), checkmark("我剪过一次羊毛")],
         rewards=[item("minecraft:white_wool", 4), xp(40)])
# ============================================================ E · 乳制品与蜂蜜
ch.quest("cheese", 1.325, 16.55, "奶酪：牛奶的终点", icon="tfc:food/cheese", deps=["milking"], shape="hexagon", hide_lines=True,
         size=1.25,
         desc=["&6大桶&r中按&69 份牛奶 : 1 份醋&r的比例混合（先倒 9 桶奶，再倒 1 桶醋），"
               "密封静置 &68 小时&r，牛奶会凝固成&6酪乳&r。",
               "",
               "&6酪乳继续密封静置 8 小时&r，就会凝固成&6奶酪&r——保质期远比生奶长，"
               "也是三明治等料理的重要食材。",
               "",
               "&c常见的坑：&r比例不对配方就不成立，记得先核对悬停提示或 JEI。"],
         tasks=[item("tfc:food/cheese", title="奶酪")],
         rewards=[item("tfc:powder/salt", 4), xp(40)])

ch.quest("beekeeping", 1.325, 18.55, "养蜂入门", icon="firmalife:beehive", deps=["orchard"], optional=True, hide_lines=True,
         shape="diamond",
         desc=["（Firmalife）&6蜂箱&r内放&6巢脾&r即可招揽野生蜂群：周围&6半径 5 格内有 10 朵以上花&r，"
               "巢脾就有机会被蜂后入住（蜂箱周围出现蜂群粒子特效）。",
               "",
               "&6产出：&r手持空罐&e右键&r满蜜的蜂箱得到&6蜂蜜罐&r（生蜂蜜可代替糖）；"
               "手持小刀对满巢脾&e右键&r能刮出&6蜂蜡&r（防腐木材的原料），&c但会杀死蜂后&r。",
               "",
               "&a小技巧：&r带「作物亲和力」性状的蜂群会帮周围种植盆/耕地偷偷施肥，"
               "果园旁边放几个蜂箱一本万利。"],
         tasks=[item("firmalife:beehive", title="蜂箱")],
         rewards=[item("tfc:compost", 4), xp(30)])

ch.quest("greenhouse", 1.325, 20.55, "温室与种植盆（Firmalife）", icon="firmalife:sealed_bricks", deps=["orchard"], hide_lines=True,
         optional=True, shape="diamond",
         desc=["&6温室&r是全封闭的多方块结构（墙、门、屋顶同属一种温室材质），"
               "内部由&6气象站&r激活后&6全年提供适宜生长环境&r，突破当地气候限制。",
               "",
               "温室里用&6种植盆&r种作物：大型种植盆种单株（谷物需要铜级以上温室），"
               "四槽种植盆同时种四株根茎/果菜类；都要用&6喷壶&r浇水才能生长。",
               "",
               "&a入门建议：&r先用防腐木搭一个最简单的温室试试水，详见 TFC 野外指南"
               "「Firmalife」章节的图文说明，这里不展开搭建细节。"],
         tasks=[checkmark("我了解温室和种植盆的基本用法")],
         rewards=[item("tfc:compost", 4), xp(30)])

ch.quest("irrigation", 3.525, 19.55, "洒水器与管道灌溉（Firmalife）", icon="firmalife:sprinkler",
         deps=["greenhouse"], optional=True, shape="diamond",
         desc=["（进阶，需要铜器时代）&6洒水器&r在砧上用铜板锻造，装在温室里能自动灌溉"
               "周围 5×6×5 范围的种植盆，免去手动浇水。",
               "",
               "洒水器要靠&6铜管&r连接&6灌溉水箱&r或&6水泵站&r供水，水泵站须架在水源正上方并接上动力。",
               "",
               "&a提示：&r这是一套完整的自动化灌溉系统，适合温室规模扩大之后再投入，"
               "现阶段&a详见 TFC 野外指南&r即可，不必急着搭建。"],
         tasks=[checkmark("我了解洒水器灌溉系统的基本原理")],
         rewards=[xp(20)])

ch.quest("finale", 3.525, 17.55, "自给自足的农场", icon="tfc:composter", deps=["cheese", "shearing"], hide_lines=True,
         shape="gear", size=1.75,
         subtitle="从一撮野草种子，到四季不断的粮仓",
         desc=["&o&7「田里有粮，圈里有畜，这才是能扛过寒冬的家。」&r",
               "",
               "你已经学会：&a耕地与播种&r、&a氮磷钾施肥&r、&a镰刀收获留种&r、"
               "&a果树与浆果灌木&r、&a驯化繁育&r、&a挤奶剪毛做奶酪&r。",
               "",
               "&a下一步：&r回到「生存之道」把农场产出做成均衡饮食和耐储粮，"
               "或者去「铜器时代」打一把更快的锄头和镰刀，扩大农场规模。"],
         tasks=[checkmark("我已经建立起稳定的农场")],
         rewards=[item("tfc:compost", 8), item("tfc:food/barley_bread", 8), levels(5)])

# ============================================================ 第六节 · 骑乘与畜力
ch.quest("saddle", 6.85, 17.3, "马鞍：开始骑乘", icon="minecraft:saddle", deps=["taming", "copper_age:leather"],
         shape="hexagon",
         desc=["适合骑乘和驮运的牲畜是&6马、驴、骡&r（骡由马和驴杂交，无法再繁殖）。按「驯化与亲密度」把它喂熟，再配上马鞍。",
               "",
               "&6马鞍&r由&6皮革塑形&r（knapping）敲出图案得到，用法和石器塑形类似，详见 JEI 的图案提示。",
               "",
               "&c骑乘条件：&r马/驴/骡的&6亲密度需达到 15%&r以上才能骑乘，装上马鞍即可骑。",
               "",
               "&a小技巧：&r驴和骡亲密度足够后还能在身上&6放一个箱子或大桶&r（见下一个任务），"
               "一边骑一边运货。"],
         tasks=[item("minecraft:saddle", title="马鞍")],
         rewards=[item("minecraft:leather", 4), xp(40)])

ch.quest("donkey_cargo", 9.05, 17.3, "驴骡驮货", icon="tfc:wood/chest/oak", deps=["saddle"],
         desc=["亲密度够高的&6驴/骡&r身上可以直接挂一个&6箱子&r或&6木桶&r，让它帮你驮东西：",
               "&7- 手持箱子/木桶对准驴骡&e右键&r即可安装",
               "&7- 卸货：&e潜行+右键&r驴骡（手上拿着对应的空手或木桶）即可取下",
               "",
               "&a为什么好用：&r相比自己扛，驮兽能额外带一整个箱子的货物，矿石、建材都靠它。"],
         tasks=[checkmark("我给驴/骡装上了箱子或木桶")],
         rewards=[item("tfc:wood/log/oak", 8), xp(30)])

ch.quest("cart_mats", 11.25, 17.3, "黄铜构件：造车的前提", icon="tfc:brass_mechanisms", deps=["donkey_cargo"],
         desc=["&c接下来的畜力车、犁需要&6黄铜构件&r（brass_mechanisms）！&r",
               "",
               "黄铜构件要在&6青铜时代的二级砧&r上，用&6黄铜锭（铜+锌合金）&r锻造得到。"
               "如果你还没炼出黄铜，请先回头完成「青铜时代」。",
               "",
               "&a小技巧：&r多打几块备用，供应车、畜力车、犁各需要一块。"],
         tasks=[item("tfc:brass_mechanisms", 3, title="黄铜构件 ×3")],
         rewards=[item("tfc:powder/flux", 8), xp(40)])

ch.quest("supply_cart", 13.45, 16.3, "供应车", icon="tfcastikorcarts:supply_cart/oak", deps=["cart_mats"],
         shape="hexagon", size=1.25,
         desc=["&6供应车&r = 木材 + &6黄铜构件&r + &6木轮&r（配方详见 JEI，不同木种外观不同）。",
               "",
               "&e用法：&r放置好车，把&6驯化的马/驴/骡&r牵到车旁，&e按 ]&r 键为它套上挽具，"
               "就能拖着车跑了。供应车自带箱子容量，比驮兽本身还能多拉货。",
               "",
               "&c注意：&r车需要相对平整的地面才好走，陡坡和台阶会卡住它。"],
         tasks=[checkmark("我把供应车做了出来（任意木种）")],
         rewards=[item("tfc:wood/lumber/oak", 8), xp(50)])

ch.quest("animal_cart", 13.45, 18.3, "畜力车与犁", icon="tfcastikorcarts:plow/oak", deps=["cart_mats"],
         optional=True, shape="diamond",
         desc=["同一套&6黄铜构件 + 木材 + 木轮&r 还能做出：",
               "&7- &6畜力车&r：比供应车更简单的运货车",
               "&7- &6犁&r：套上牲畜之后可以&e快速翻耕大片农田&r，比锄头一格一格耕省力得多",
               "",
               "&a小技巧：&r开垦大田的时候套上犁，效率天差地别。"],
         tasks=[checkmark("我做出了畜力车或犁")],
         rewards=[item("tfc:wood/lumber/oak", 8), xp(30)])

ch.section("第一节 · 从野草到田地", ["start", "hoe", "plant", "climate_crop", "hydration", "nutrients"])
ch.section("第二节 · 施肥与堆肥", ["fertilizer_basics", "composter", "compost_use", "mining_fertilizer"])
ch.section("第三节 · 收获与果园", ["scythe", "harvest_loop", "wild_fruit", "orchard", "berry_farm"])
ch.section("第四节 · 驯养与繁育", ["taming", "breeding", "aging", "milking", "shearing"])
ch.section("第五节 · 乳制品与温室", ["cheese", "beekeeping", "greenhouse", "irrigation", "finale"])
ch.section("第六节 · 骑乘与畜力", ["saddle", "donkey_cargo", "cart_mats", "supply_cart", "animal_cart"])
