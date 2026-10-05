from qlib import *

ch = Chapter("bronze_age", "青铜时代", icon="tfc:metal/anvil/bronze", group="ages", order=2,
             theme="bronze", subtitle="合金，是文明真正的加速器")

# ============================================================ A · 寻矿与勘探
ch.quest("start", 1.45, 4.1, "合金的三种材料", icon="tfc:ore/small_cassiterite", shape="gear", size=1.5,
         deps=["copper_age:finale"],
         subtitle="纯铜太软，合金才是下一个台阶",
         desc=["&o&7「铜加上一点别的东西，就不再是铜了。」&r",
               "",
               "青铜时代要找的三种新矿石，和铜矿一样会在地表留下&6小矿粒&r：",
               "&7- &6锡石&r（Cassiterite）—— 炼&6锡&r，普通青铜的关键原料",
               "&7- &6辉铋矿&r（Bismuthinite）—— 炼&6铋&r，铋铜的原料",
               "&7- &6闪锌矿&r（Sphalerite）—— 炼&6锌&r，黑铜、黄铜的原料",
               "",
               "&a小技巧：&r这三种矿粒和铜粒一样，&e直接走过去打掉/右键&r即可拾取，"
               "看到矿粒就说明脚下有矿脉。"],
         tasks=[item("tfc:ore/small_cassiterite", 5, title="锡石粒 ×5")],
         rewards=[item("tfc:ceramic/vessel"), xp(30)])

ch.quest("bronze_propick", 3.65, 2.1, "青铜勘矿镐", icon="tfc:metal/propick/bronze", deps=["start"],
         optional=True, shape="diamond",
         desc=["铜砧已经能锻&6勘矿镐&r了（铜器时代遗留的任务）。进入本章后，"
               "更耐用的&6青铜勘矿镐&r是系统性寻矿的标配。",
               "",
               "&e用法：&r手持勘矿镐&e右键&r任意方块，沿直线每隔几格探测一次，"
               "根据提示信号强弱判断矿脉方向和距离。",
               "",
               "&a建议：&r锡矿、铋矿、锌矿往往比铜矿更稀少分散，没有勘矿镐基本靠运气。"],
         tasks=[item("tfc:metal/propick/bronze", title="青铜勘矿镐")],
         rewards=[item("tfc:torch", 8), xp(30)])

ch.quest("panning", 3.65, 4.1, "淘金盘：河床淘矿", icon="tfc:pan/empty", deps=["start"],
         desc=["河床、湖底常有&6矿床&r（砂砾沉积物），用&6黏土塑形&r做出&6淘金盘&r并&6烧制&r后就能用。",
               "",
               "&e用法：&r",
               "&e1.&r 对着含矿沉积物方块&e使用&r淘金盘拾取沉积物",
               "&e2.&r 站在水里，手持淘金盘&e按住右键&r淘洗",
               "&e3.&r 走动一段时间后，有机会获得矿粒、石子或宝石",
               "",
               "&a产物概率：&r矿石 50%、石子 25%、宝石 1%。",
               "&c小心：&r矿床附近水域可能有食人鱼，淘洗前先观察。"],
         tasks=[item("tfc:pan/empty", title="淘金盘")],
         rewards=[item("minecraft:clay_ball", 16), xp(30)])

ch.quest("sluice", 5.85, 4.1, "洗矿槽：批量处理", icon="tfc:wood/sluice/oak", deps=["panning"],
         optional=True, shape="diamond",
         desc=["&6洗矿槽&r效果和淘金盘一样，但不用自己站在水里淘，适合&6批量处理&r沉积物。",
               "",
               "&e安装：&r放置后占两格，顶部必须有&6流动的水&r流过并从底部流出，出口要留出空位让水流走。",
               "&e用法：&r把沉积物&e丢入&r上游的水中，水流会把它冲进洗矿槽，产物从下方溢出。",
               "",
               "&6产物概率略高于淘金盘：&r矿石 55%、石子 22.5%、宝石 0.9%。"],
         tasks=[tag("tfc:sluices", title="任意洗矿槽")],
         rewards=[item("tfc:wood/lumber/oak", 8), xp(30)])

ch.quest("mine_cassiterite", 3.65, 6.1, "开采锡矿脉", icon="tfc:ore/rich_cassiterite/granite", deps=["start"],
         shape="hexagon", size=1.25,
         desc=["顺着地表矿粒往下挖，用&6铜镐&r（或更好的镐）开采成片的&6锡石矿脉&r。",
               "",
               "矿石分三档品级，熔化产量不同：",
               "&7- &6贫瘠&r 15 mB · &6普通&r 25 mB · &6富集&r 35 mB（小粒只有 10 mB）",
               "",
               "&6100 mB&r 熔化为 1 块锭。做青铜大约每 10 份铜要配 1 份锡，&a提前囤够锡矿&r。",
               "&c记得带支撑梁&r，矿脉常年深埋地下，塌方风险不低。"],
         tasks=[tag("tfc:ores/tin/normal", 6, title="普通品级锡石 ×6")],
         rewards=[item("tfc:wood/support/oak", 8), xp(40)])
# ============================================================ B · 熔炼与合金
ch.quest("melt_tin", 9.05, 2.1, "熔锡成锭", icon="tfc:metal/ingot/tin", deps=["mine_cassiterite"], hide_lines=True,
         desc=["和熔铜一样：把锡石放进&6小缸&r，在&6木炭炉&r里加热到 &6锡的熔点&r，趁热倒进铸锭模具。",
               "",
               "&c常见的坑：&r小缸里&c不要把锡矿和铜矿混在一起&r烧——那样会直接自动合金化，"
               "配比不受你控制，很可能比例不对做不出青铜（见下一个任务）。",
               "&a正确做法：&r先分别炼出纯&6锡锭&r和纯&6铜锭&r，再按比例混合。"],
         tasks=[item("tfc:metal/ingot/tin", 4, title="锡锭 ×4")],
         rewards=[item("minecraft:clay_ball", 16), xp(30)])

ch.quest("bronze_alloy", 11.25, 3.1, "小缸合金：青铜", icon="tfc:metal/ingot/bronze", deps=["melt_tin"],
         shape="hexagon", size=1.25,
         desc=["&o&7「把铜和锡一起熔化，流出来的不再是铜，是青铜。」&r",
               "",
               "&6青铜配方（按金属含量百分比）：&r",
               "&7- &6铜&r：88% ~ 92%",
               "&7- &6锡&r：8% ~ 12%",
               "",
               "&e操作：&r把铜锭和锡锭按比例放进&6同一个小缸&r（例如 9 铜 + 1 锡），"
               "一起加热到熔化，&c只要总占比落在区间内&r，出来的液体就会自动变成青铜。",
               "",
               "&c常见的坑：&r比例算错会得到&c纯铜&r或者&c废弃合金&r（不在任何配方区间内，"
               "只能当坩埚配重）。倒出来之前先悬停小缸确认名字是不是「青铜」。"],
         tasks=[item("tfc:metal/ingot/bronze", 8, title="青铜锭 ×8")],
         rewards=[item("tfc:powder/flux", 8), xp(50)])

ch.quest("mine_other_ores", 9.05, 4.1, "辉铋矿与闪锌矿", icon="tfc:ore/normal_sphalerite/granite", hide_lines=True,
         deps=["mine_cassiterite"], optional=True, shape="diamond",
         desc=["除了锡，&6铋&r和&6锌&r也值得挖一些，用来做更高级的功能性合金：",
               "&7- &6辉铋矿&r → 铋 → 铋铜",
               "&7- &6闪锌矿&r → 锌 → 黑铜 / 黄铜",
               "",
               "&a小技巧：&r这两种矿不是必需品，但黄铜以后在「创世」等机械模组里用量很大，"
               "提前囤一些不吃亏。"],
         tasks=[tag("tfc:ores/bismuth/normal", 4, title="普通品级辉铋矿 ×4"),
                tag("tfc:ores/zinc/normal", 4, title="普通品级闪锌矿 ×4")],
         rewards=[item("tfc:wood/support/oak", 8), xp(30)])

ch.quest("other_alloys", 13.45, 2.1, "铋铜与黑铜", icon="tfc:metal/ingot/bismuth_bronze",
         deps=["mine_other_ores", "bronze_alloy"], optional=True, shape="diamond",
         desc=["熔出&6铋锭&r和&6锌锭&r后，可以配出另外两种能打工具/盔甲的青铜合金：",
               "",
               "&6铋铜&r：&7铜 50~70% · 锌 20~30% · 铋 10~20%&r",
               "&6黑铜&r：&7铜 50~70% · 银 10~25% · 金 10~25%&r",
               "",
               "&c注意：&r黑铜需要&6银&r和&6金&r，这两种更稀有，暂时找不到也无所谓，"
               "&6铜 / 铋铜&r已经够用到铁器时代了。",
               "&a小技巧：&r三种青铜（普通、铋铜、黑铜）都算作&6#forge:ingots/allbronze&r，"
               "后续很多配方认这个标签，随便哪种青铜都能用。"],
         tasks=[item("tfc:metal/ingot/bismuth_bronze", 4, title="铋铜锭 ×4")],
         rewards=[item("tfc:powder/flux", 8), xp(40)])

ch.quest("brass", 13.45, 4.1, "黄铜：给机器用", icon="tfc:metal/ingot/brass", deps=["mine_other_ores", "bronze_alloy"],
         optional=True, shape="diamond",
         desc=["&6黄铜&r：&7铜 88~92% · 锌 8~12%&r，配比和青铜很像，只是把锡换成了锌。",
               "",
               "&c注意：&r黄铜&c打不出合格的工具/武器&r，它的主要用途是制作各种&6自动化机械的零件&r"
               "（后面的「创世」等章节会大量用到）。先炼一些存着就好。"],
         tasks=[item("tfc:metal/ingot/brass", 4, title="黄铜锭 ×4")],
         rewards=[item("minecraft:clay_ball", 16), xp(30)])
# ============================================================ C · 青铜砧与焊接
ch.quest("weld_double", 1.2, 11.45, "焊接青铜双锭", icon="tfc:metal/double_ingot/bronze", deps=["bronze_alloy"], hide_lines=True,
         desc=["和铜双锭做法一样：",
               "&e1.&r 把两块&6青铜锭&r放进木炭炉加热到「可焊接」",
               "&e2.&r 趁热右键&6石砧或铜砧&r，放入两块锭 + &6助焊剂&r",
               "&e3.&r 点击焊接，得到&6青铜双锭&r",
               "",
               "&a小技巧：&r铜砧也能焊青铜，不必非要用石砧——只是铜砧更耐用。"],
         tasks=[item("tfc:metal/double_ingot/bronze", 7, title="青铜双锭 ×7")],
         rewards=[item("tfc:powder/flux", 8), item("minecraft:charcoal", 16), xp(50)])

ch.quest("bronze_anvil", 3.4, 11.45, "青铜砧", icon="tfc:metal/anvil/bronze", deps=["weld_double"],
         shape="hexagon", size=1.25,
         desc=["&o&7「同样的工字形，更硬的金属，更好的手感。」&r",
               "",
               "&e合成：&r7 块&6青铜双锭&r在工作台上摆成「工」字形，和铜砧配方一致，得到&6青铜砧&r。",
               "",
               "&6在青铜砧上锻造的工具&a上限更高、更耐用&r，而且是打造青铜工具/武器/盔甲的必需品。",
               "",
               "&a小技巧：&r&6#tfc:bronze_anvils&r标签下，普通青铜砧、铋铜砧、黑铜砧都算数，"
               "任意一种青铜都能焊双锭、搭同款的砧。"],
         tasks=[tag("tfc:bronze_anvils", title="任意青铜砧")],
         rewards=[item("tfc:metal/ingot/bronze", 4), item("minecraft:charcoal", 16), xp(60)])

ch.quest("bronze_tools", 5.6, 10.45, "青铜工具", icon="tfc:metal/pickaxe/bronze", deps=["bronze_anvil"],
         shape="hexagon", size=1.25,
         desc=["在青铜砧上锻出&6镐、斧、锄、铲、锤、锯、凿、刀&r等工具头，组装成一整套青铜工具。",
               "",
               "&6相比铜制工具：&r青铜耐久更高、挖掘和砍伐效率更好，&c但依然挖不动需要铁镐才能"
               "开采的矿石&r（见铁器时代）。",
               "",
               "&a建议：&r先锻一把&6青铜镐&r，矿脉挖起来会快很多。"],
         tasks=[tag("tfc:metal_item/bronze_tools", title="任意青铜工具")],
         rewards=[item("tfc:wood/support/oak", 8), xp(50)])

ch.quest("bronze_weapons", 5.6, 12.45, "青铜武器与盔甲", icon="tfc:metal/sword/bronze", deps=["bronze_anvil"],
         optional=True, shape="diamond",
         desc=["&6青铜剑、标枪、狼牙棒&r是比石标枪强得多的近战武器；"
               "青铜盔甲（头盔/胸甲/护腿/靴）能大幅减少受到的伤害。",
               "",
               "&c警告：&r熊、狼群、狮子依然危险，有了青铜装备也别单挑大型掠食者。"],
         tasks=[item("tfc:metal/sword/bronze", title="青铜剑"),
                item("tfc:metal/javelin/bronze", title="青铜标枪")],
         rewards=[item("firstaid:bandage", 4), xp(40)])
# ============================================================ D · 坩埚与精炼（选学）
ch.quest("graphite", 8.925, 10.325, "石墨与高岭土", icon="tfc:powder/graphite", deps=["bronze_tools"],
         optional=True, shape="diamond",
         desc=["想造&6坩埚&r，得先搞到&6耐火黏土&r，它由&6石墨粉&r + &6高岭石粉&r + &6黏土球&r合成。",
               "",
               "&e石墨：&rY=60 以下的&6石英岩、片岩、片麻岩、大理岩&r中成脉状分布，"
               "常与烟煤同脉——用勘矿镐找石墨矿脉。",
               "&e石墨粉要洗矿：&r石墨矿 + 锤子 → &6含岩石墨碎块&r → &6洗矿槽&r冲洗 → &6石墨碎块&r"
               " → 手推磨 → &6含杂石墨粉&r → 再进洗矿槽 → &6石墨粉&r。",
               "&e高岭土：&r生成于海拔较高处（高原、古老山脉、高地），要求年均温至少 18℃、"
               "降雨量至少 300mm。地表长&6血百合&r的地方下面往往有高岭土。",
               "",
               "&c注意：&r高岭土加热转化为高岭石粉的产率只有约 20%，&a多挖几组再去烧&r。"],
         tasks=[item("tfc:powder/graphite", 4, title="石墨粉 ×4"),
                item("tfc:powder/kaolinite", 4, title="高岭石粉 ×4")],
         rewards=[item("tfc:torch", 8), xp(30)])

ch.quest("fire_clay", 11.125, 10.325, "耐火黏土与坩埚", icon="tfc:crucible", deps=["graphite"],
         optional=True, shape="diamond",
         desc=["&6石墨粉 + 高岭石粉 + 黏土球&r在工作台合成&6耐火黏土&r，再像普通黏土一样&6塑形&r成"
               "未烧制的坩埚，用坑窑或木炭炉烧制。",
               "",
               "&6坩埚的优势：&r比小缸能一次合金化更大批量的金属，而且&a允许的比例误差更大&r，"
               "新手配比不精确时更容易成功。",
               "",
               "&e使用：&r给坩埚下方提供热源（木炭炉最合适），右键打开界面，"
               "按配方比例把金属锭/矿石放进去即可。破坏坩埚不会损失里面的金属，"
               "可以用来搬运合金。"],
         tasks=[item("tfc:crucible", title="坩埚")],
         rewards=[item("tfc:fire_clay", 8), xp(40)])

ch.quest("finale", 14.7, 10.7, "通往黑暗的矿脉", icon="tfc:metal/anvil/bronze", deps=["bronze_tools"], hide_lines=True,
         shape="gear", size=1.75,
         subtitle="青铜之后，是铁与火的试炼",
         desc=["&o&7「青铜打开了文明的门，但真正的力量藏在赭红色的矿石里。」&r",
               "",
               "你已经拥有：&a青铜砧&r、&a整套青铜工具/武器/盔甲&r、&a合金冶炼的全部经验&r。",
               "",
               "下一步是&6铁&r——但铁矿石&c不能直接靠加热熔化&r，需要用&6锻铁炉&r（多方块结构）"
               "把矿石炼成&6粗铁方坯&r，再反复锻打除渣，才能得到&6锻铁&r。",
               "",
               "&a下一步：&r带上勘矿镐去找&6赤铁矿、褐铁矿、磁铁矿&r，搭建你的第一座锻铁炉，"
               "进入「铁器时代」。"],
         tasks=[checkmark("我已经准备好炼铁了")],
         rewards=[item("tfc:metal/ingot/bronze", 6), item("tfc:powder/flux", 8), levels(5)])

ch.section("第一节 · 寻矿与勘探", ["start", "bronze_propick", "panning", "sluice", "mine_cassiterite"])
ch.section("第二节 · 熔炼与合金", ["melt_tin", "bronze_alloy", "mine_other_ores", "other_alloys", "brass"])
ch.section("第三节 · 青铜砧与焊接", ["weld_double", "bronze_anvil", "bronze_tools", "bronze_weapons"])
ch.section("第四节 · 坩埚与精炼", ["graphite", "fire_clay"])
ch.section("第五节 · 终章", ["finale"])
