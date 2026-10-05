from qlib import *

ch = Chapter("steel_age", "钢铁时代", icon="tfc:metal/anvil/steel", group="ages", order=4,
             theme="steel", subtitle="炭与风的极限，淬出文明的脊梁")

# ============================================================ A · 高炉与鼓风口
ch.quest("start", 1.45, 4.1, "风箱已够，还差一座高炉", icon="tfc:blast_furnace", shape="gear", size=1.5,
         deps=["iron_age:finale"],
         subtitle="铁器时代的终点，钢铁时代的起点",
         desc=["&o&7「风箱能把炉子吹到 2000℃，但钢，要的是更大的火。」&r",
               "",
               "你已经走出了铁器时代，手握&6锻铁炉&r和&6铁砧&r。但&6生铁&r太脆，"
               "&6锻铁&r太软——真正的&6钢&r只能从一座&6高炉&r中诞生。",
               "",
               "&e高炉需要准备：&r",
               "&7- 2 个&6坩埚&r",
               "&7- 1 根锻造好的&6鼓风口&r（锻铁即可，钢的更好）",
               "&7- 1 个&6风箱&r",
               "&7- 大量&6耐火砖块&r和&6锻铁薄板&r",
               "",
               "&a小技巧：&r这些材料本章接下来会逐一讲解，别急。"],
         tasks=[checkmark("我已经准备好挑战高炉")],
         rewards=[item("minecraft:charcoal", 32), xp(30)])

ch.quest("crucible", 3.65, 2.1, "坩埚", icon="tfc:crucible", deps=["start"],
         desc=["&6坩埚&r是一种耐高温容器，既能在木炭炉里当作普通容器用来熔炼矿石，"
               "也是搭建&6高炉&r的必需部件（整座高炉要用到 2 个）。",
               "",
               "&e合成：&r在工作台上用&6耐火砖&r按配方拼出（详见 JEI）。",
               "&a顺带一提：&r后面制作&6黑钢、蓝钢、红钢&r这些有色钢合金时，"
               "坩埚也是唯一能完成&6合金熔炼&r的容器。"],
         tasks=[item("tfc:crucible", 2, title="坩埚 ×2")],
         rewards=[item("tfc:ceramic/unfired_fire_brick", 8), xp(30)])

ch.quest("fire_bricks", 3.65, 4.1, "耐火砖", icon="tfc:ceramic/fire_brick", deps=["start"],
         desc=["&6耐火砖&r是唯一扛得住炼钢高温的建筑材料，高炉的&6烟囱&r必须用它搭建。",
               "",
               "&e合成：&r&6未烧制的耐火砖&r（黏土 + 耐火土，详见 JEI）在坑窑或炉子里烧制而成，"
               "之后无序合成为&6耐火砖块&r方块。",
               "",
               "&a提前囤货：&r基础高炉的烟囱每多搭 1 层，就要再多 4 块耐火砖块、12 张锻铁薄板，"
               "最多可以叠 5 层。先按最小规模准备，不够再去烧。"],
         tasks=[item("tfc:fire_bricks", 10, title="耐火砖块 ×10")],
         rewards=[item("minecraft:clay_ball", 16), xp(30)])

ch.quest("wrought_sheets", 5.85, 4.1, "锻铁薄板", icon="tfc:metal/sheet/wrought_iron", deps=["fire_bricks"],
         desc=["高炉方块本体要用 1 个&6坩埚&r + 8 张&6锻铁薄板&r合成；"
               "烟囱外层也要用薄板把耐火砖块箍紧固定。",
               "",
               "&e来源：&r锻铁锭在砧上锻成锻铁双层薄板后拆开，或直接用双层薄板做高级配方。",
               "",
               "&a预算：&r基础高炉（无额外烟囱层）至少需要 &68 张锻铁薄板做炉体&r，"
               "外加每层烟囱 12 张——先打一批 20 张起步。",
               "&c升级提示：&r材料富裕时可以用更高级的金属薄板（如&6钢薄板&r）代替锻铁薄板包裹烟囱。"],
         tasks=[tag("forge:sheets/wrought_iron", 20, title="锻铁薄板 ×20")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 4), xp(40)])

ch.quest("tuyere", 3.65, 6.1, "鼓风口", icon="tfc:metal/tuyere/wrought_iron", deps=["start"], shape="hexagon",
         size=1.25,
         desc=["&6鼓风口&r是高炉的「嘴」，没有它，炉内永远烧不到炼钢的温度。",
               "",
               "&e锻造：&r把&6双层薄板&r放上砧，按&6弯曲&r方向敲几下即可打出鼓风口"
               "（锻铁、钢、黑钢、蓝钢、红钢的鼓风口都可以，金属等级越高越耐用）。",
               "",
               "&e安装：&r打开高炉界面，鼓风口放在界面右上角的槛位；"
               "风箱则安装在高炉方块的任意相邻面上，对准它。",
               "&c常见的坑：&r风箱连接到鼓风口才算数，连接到别处无效。"],
         tasks=[tag("tfc:tuyeres", title="任意鼓风口")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 4), xp(40)])

ch.quest("build_bf", 8.05, 4.1, "搭建高炉", icon="tfc:blast_furnace", deps=["crucible", "wrought_sheets", "tuyere"],
         shape="hexagon", size=1.25,
         desc=["&o&7「地基不稳，炼不出好钢。」&r",
               "",
               "&e1.&r 用&61 个坩埚 + 8 张锻铁薄板&r在工作台合成&6高炉&r方块，放置它",
               "&e2.&r 在它上方搭建&6烟囱&r：每层用耐火砖块围成空心方柱，外层用薄板箍住"
               "（具体层数、形状请打开&6TFC 指南&r查看多方块示意图）",
               "&e3.&r 在高炉方块的任意相邻面安装&6风箱&r，并对准&6鼓风口&r槛位放好鼓风口",
               "{@pagebreak}",
               "&6投料：&r从烟囱顶部往里丢&6等量的铁矿石（或可熔化为铸铁的物品）&r和&6助焊剂&r，"
               "再不断从顶部加入&6木炭&r维持燃烧。",
               "",
               "&e4.&r 用起火器或火把点燃高炉方块",
               "&e5.&r 持续拉动风箱，温度够高时矿石开始熔化，变成&6生铁&r流进下方容器（坩埚最合适）",
               "",
               "&c常见的坑：&r",
               "&7- 风箱连不上鼓风口，炉子永远到不了炼钢温度",
               "&7- 忘记持续加木炭，炉温会往下掉",
               "&7- 本整合包装有&6高炉优化模组&r，带来了&6保温耐火砖/高炉保温板&r等额外部件，"
               "按游戏内提示和 JEI 配方使用，可以提升保温与效率"],
         tasks=[checkmark("我点燃了一座能炼钢的高炉")],
         rewards=[item("minecraft:charcoal", 32), item("tfc:powder/flux", 8), xp(60)])

ch.quest("pig_iron", 10.25, 4.1, "生铁", icon="tfc:metal/ingot/pig_iron", deps=["build_bf"],
         desc=["高炉烧出来的&6生铁&r很硬但极脆，&c不能直接做工具或盔甲&r，"
               "必须先经过加工才能变成&6钢&r。",
               "",
               "&e取用：&r高炉下方容器里的生铁水，用铸锭模具舀出凝固，"
               "或直接把模具放进坩埚界面浇铸。",
               "",
               "&a小技巧：&r生铁本身也是后面焊接高碳黑钢/蓝钢/红钢锭的原料之一，"
               "多炼一些存起来。"],
         tasks=[item("tfc:metal/ingot/pig_iron", 8, title="生铁锭 ×8")],
         rewards=[item("tfc:powder/flux", 8), xp(40)])
# ============================================================ B · 从生铁到钢
ch.quest("high_carbon", 13.575, 4.1, "高碳钢：砧上的淬炼", icon="tfc:metal/ingot/high_carbon_steel",
         deps=["pig_iron"], shape="hexagon", size=1.25,
         desc=["&o&7「生铁到钢，中间只差砧上的几次敲击。」&r",
               "",
               "把&6生铁锭&r放上砧，&e先选择&6高碳钢锭&r为目标&r反复锤炼，成功后得到&6高碳钢锭&r。",
               "",
               "&c注意：&r这一步&c没有捷径&r——不经过砧上加工，生铁永远只是生铁。"],
         tasks=[item("tfc:metal/ingot/high_carbon_steel", 4, title="高碳钢锭 ×4")],
         rewards=[item("tfc:powder/flux", 4), xp(50)])

ch.quest("steel_ingot", 15.775, 4.1, "钢锭", icon="tfc:metal/ingot/steel", deps=["high_carbon"], shape="hexagon",
         size=1.25,
         desc=["把&6高碳钢锭&r放上砧，&e再选择&6钢锭&r为目标&r继续锤炼，就能得到真正的&6钢&r。",
               "",
               "&6生铁 → 高碳钢 → 钢&r，两次锻打，缺一不可。",
               "",
               "&a别浪费：&r锤炼手法越好，&a锻造加成&r越高，做出的工具/盔甲基础属性越好——"
               "这一步值得你认真对指针。"],
         tasks=[item("tfc:metal/ingot/steel", 6, title="钢锭 ×6")],
         rewards=[item("tfc:powder/flux", 8), xp(60)])

ch.quest("steel_anvil", 17.975, 4.1, "钢砧", icon="tfc:metal/anvil/steel", deps=["steel_ingot"], shape="hexagon",
         size=1.5,
         desc=["&o&7「钢砧立起来的那一刻，铁器时代彻底翻篇。」&r",
               "",
               "和铜砧一样，先把钢锭焊成&6钢双锭&r（焊接流程见铜器时代笔记），"
               "再用 7 块钢双锭在工作台拼出&6钢砧&r。",
               "",
               "&6钢砧&r是锻造&6黑钢、蓝钢、红钢&r等更高级合金工具的&c必需品&r——"
               "没有它，后面所有有色钢锭都锻不出来。"],
         tasks=[item("tfc:metal/anvil/steel", title="钢砧")],
         rewards=[item("tfc:metal/ingot/steel", 4), item("minecraft:charcoal", 32), xp(70)])

ch.quest("steel_sheet", 20.175, 2.1, "钢薄板：工业的通行证", icon="tfc:metal/sheet/steel", deps=["steel_anvil"],
         optional=True, shape="diamond",
         desc=["&6钢薄板&r由&6钢双锭&r在砧上敲打而成（tier 4 配方）。",
               "",
               "&c这不只是普通材料！&r后面进入&6创造 Mod、沉浸工程、TFMG&r等工业章节时，"
               "大量机器配方都直接认&6forge:sheets/steel&r这个标签——先囤一批钢薄板，"
               "工业时代会轻松很多。"],
         tasks=[tag("forge:sheets/steel", 8, title="钢薄板 ×8")],
         rewards=[item("tfc:metal/ingot/steel", 4), xp(40)])

ch.quest("steel_tools", 20.175, 4.1, "全套钢制工具", icon="tfc:metal/pickaxe/steel", deps=["steel_anvil"],
         desc=["钢锭直接在钢砧（或更高级的砧）上锻出全套工具头，组装方式与之前金属时代相同。",
               "",
               "&a钢制工具的耐久和效率&r比铁制工具高出一大截，挖矿、伐木、战斗都值得全面换装。"],
         tasks=[tag("tfc:pickaxes", title="任意镐"), tag("tfc:axes", title="任意斧"),
                tag("tfc:hammers", title="任意锤")],
         rewards=[item("tfc:metal/ingot/steel", 4), xp(50)])

ch.quest("steel_armor", 20.175, 6.1, "钢制盔甲", icon="tfc:metal/chestplate/steel", deps=["steel_anvil"],
         shape="hexagon", size=1.25,
         desc=["&6双层薄板&r在砧上锻成&6半成品盔甲&r，再用&6毛毡/布料&r等材料在砧上"
               "完成最后一步，做出成套&6钢盔甲&r（详见 JEI 完整流程）。",
               "",
               "&a防御力&r比铁甲高出不少，是你下矿、探索遗迹前最值得优先打的一套装备。"],
         tasks=[item("tfc:metal/chestplate/steel", title="钢胸甲"), item("tfc:metal/helmet/steel", title="钢头盔")],
         rewards=[item("tfc:metal/ingot/steel", 6), xp(60)])
# ============================================================ C · 曲轴与机械风箱
ch.quest("steel_rod", 23.5, 2.1, "钢棒", icon="tfc:metal/rod/steel", deps=["steel_ingot"], optional=True, hide_lines=True,
         shape="diamond",
         desc=["把钢锭在砧上拉伸成&6钢棒&r，是后面&6曲轴&r的连杆材料，也是不少配方的常见原料。"],
         tasks=[item("tfc:metal/rod/steel", 2, title="钢棒 ×2")],
         rewards=[item("tfc:metal/ingot/steel", 2), xp(30)])

ch.quest("crankshaft", 25.7, 2.1, "曲轴：解放双手的风箱", icon="tfc:crankshaft", deps=["steel_rod"],
         optional=True, shape="diamond", hide_lines=True,
         desc=["&6曲轴&r能把&6机械动力&r（水车、风车等旋转动力）转化为&6往复运动&r，"
               "专门用来自动拉动风箱或驱动水泵——再也不用站在炉子边手动拉风箱。",
               "",
               "&e合成：&r用&6黄铜&r制作曲轴基座，放置后再把&61 根钢棒&r作为连杆装上去。",
               "",
               "&e使用：&r曲轴基座必须连接到一根&6传动杆&r（来自水车/风车等动力源）；"
               "连杆末端放&6风箱&r即可自动鼓风——注意&c接上曲轴的风箱不能再手动操作&r。",
               "&a小技巧：&r给高炉和锻铁炉都装上曲轴驱动的风箱，彻底解放双手去做别的事。"],
         tasks=[item("tfc:crankshaft", title="曲轴")],
         rewards=[item("tfc:metal/ingot/steel", 2), xp(40)])
# ============================================================ D · 有色钢：黑钢
ch.quest("weak_steel", 1.325, 10.575, "脆钢：有色合金的起点", icon="tfc:metal/ingot/weak_steel", deps=["steel_anvil"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=["&o&7「传说中最强的合金，都要从一炉不起眼的『脆』开始。」&r",
               "",
               "在&6坩埚&r中按比例熔炼：",
               "&7- &6钢&r 50-70%", "&7- &6镍&r 15-25%", "&7- &6黑铜&r 15-25%",
               "",
               "熔好后用铸锭模具浇铸成&6脆钢锭&r——它还不是黑钢，只是半成品。"],
         tasks=[item("tfc:metal/ingot/weak_steel", 4, title="脆钢锭 ×4")],
         rewards=[item("tfc:metal/ingot/nickel", 8), xp(150), item("tfc:metal/ingot/copper", 16), item("tfc:powder/flux", 16)])

ch.quest("black_steel", 3.525, 10.575, "黑钢", icon="tfc:metal/ingot/black_steel", deps=["weak_steel"], shape="hexagon",
         size=1.5,
         desc=["&e1.&r 把&6脆钢锭&r和&6生铁锭&r一起放上砧&e焊接&r，得到&6高碳黑钢锭&r",
               "&e2.&r 高碳黑钢锭再上砧&e锤炼&r成&6黑钢锭&r",
               "",
               "&6黑钢&r是三种高级有色钢合金里最基础的一种，可以直接做工具、盔甲，"
               "&c更重要的是它是蓝钢和红钢的共同原料&r。"],
         tasks=[item("tfc:metal/ingot/black_steel", 4, title="黑钢锭 ×4")],
         rewards=[item("tfc:metal/ingot/pig_iron", 12), xp(250), item("tfc:metal/ingot/nickel", 8), item("tfc:powder/flux", 24)])

ch.quest("black_steel_anvil", 5.725, 10.575, "黑钢砧", icon="tfc:metal/anvil/black_steel", deps=["black_steel"],
         shape="hexagon", size=1.25,
         desc=["焊接出&6黑钢双锭&r，7 块拼成&6黑钢砧&r——比钢砧更高级，"
               "是锻造蓝钢/红钢系列装备的下一级门槛。"],
         tasks=[item("tfc:metal/anvil/black_steel", title="黑钢砧")],
         rewards=[item("tfc:metal/ingot/black_steel", 12), xp(300), item("minecraft:charcoal", 64), item("tfc:powder/flux", 32)])
# ============================================================ E · 群峦传说：蓝钢与红钢
ch.quest("weak_blue_steel", 9.05, 10.325, "脆蓝钢", icon="tfc:metal/ingot/weak_blue_steel", deps=["black_steel_anvil"],
         optional=True, shape="diamond",
         desc=["&o&7「群峦传说中最强的两种合金之一，蓝钢。」&r",
               "",
               "坩埚中按比例熔炼：",
               "&7- &6黑钢&r 50-55%", "&7- &6钢&r 20-25%", "&7- &6铋铜&r 10-15%", "&7- &6纯银&r 10-15%"],
         tasks=[item("tfc:metal/ingot/weak_blue_steel", 2, title="脆蓝钢锭 ×2")],
         rewards=[item("tfc:metal/ingot/bismuth_bronze", 8), xp(225), item("tfc:metal/ingot/silver", 8), item("tfc:powder/flux", 16)])

ch.quest("blue_steel", 13.45, 11.325, "蓝钢", icon="tfc:metal/ingot/blue_steel", deps=["weak_blue_steel"], optional=True,
         shape="hexagon", size=1.25,
         desc=["&e1.&r &6脆蓝钢锭&r + &6黑钢锭&r 在砧上&e焊接&r成&6高碳蓝钢锭&r",
               "&e2.&r 高碳蓝钢锭再&e锤炼&r成&6蓝钢锭&r",
               "",
               "蓝钢可以做工具、盔甲，还能做出&6蓝钢桶&r——能舀取并转移"
               "&61000 mB 的流体源方块&r，甚至包括&6熔岩&r。"],
         tasks=[item("tfc:metal/ingot/blue_steel", 2, title="蓝钢锭 ×2")],
         rewards=[item("tfc:metal/ingot/black_steel", 12), xp(400), item("firstaid:bandage", 8), item("tfc:powder/flux", 24)])

ch.quest("weak_red_steel", 9.05, 12.325, "脆红钢", icon="tfc:metal/ingot/weak_red_steel", deps=["black_steel_anvil"],
         optional=True, shape="diamond",
         desc=["&o&7「群峦传说中最强的两种合金之一，红钢。」&r",
               "",
               "坩埚中按比例熔炼：",
               "&7- &6黑钢&r 50-55%", "&7- &6钢&r 20-25%", "&7- &6黄铜&r 10-15%", "&7- &6玫瑰金&r 10-15%"],
         tasks=[item("tfc:metal/ingot/weak_red_steel", 2, title="脆红钢锭 ×2")],
         rewards=[item("tfc:metal/ingot/brass", 8), xp(225), item("tfc:metal/ingot/rose_gold", 8), item("tfc:powder/flux", 16)])

ch.quest("red_steel", 13.45, 13.325, "红钢", icon="tfc:metal/ingot/red_steel", deps=["weak_red_steel"], optional=True,
         shape="hexagon", size=1.25,
         desc=["&e1.&r &6脆红钢锭&r + &6黑钢锭&r 在砧上&e焊接&r成&6高碳红钢锭&r",
               "&e2.&r 高碳红钢锭再&e锤炼&r成&6红钢锭&r",
               "",
               "红钢同样可以做工具、盔甲，并能做出&6红钢桶&r——用法与蓝钢桶相同，"
               "可舀取流体源方块（包括熔岩）。"],
         tasks=[item("tfc:metal/ingot/red_steel", 2, title="红钢锭 ×2")],
         rewards=[item("tfc:metal/ingot/black_steel", 12), xp(400), item("firstaid:bandage", 8), item("tfc:powder/flux", 24)])

ch.quest("stainless_steel", 9.05, 14.325, "不锈钢（Firmalife）", icon="firmalife:metal/ingot/stainless_steel", hide_lines=True,
         deps=["black_steel_anvil"], optional=True, shape="diamond",
         desc=["Firmalife 额外带来了&6不锈钢&r这种合金，坩埚中按比例熔炼：",
               "&7- &6钢&r 60-80%", "&7- &6铬&r 20-30%", "&7- &6镍&r 10-20%",
               "",
               "&a用途：&r食品罐头、温室建材等 Firmalife 特色内容会用到它，"
               "具体配方详见 JEI。"],
         tasks=[item("firmalife:metal/ingot/stainless_steel", 2, title="不锈钢锭 ×2")],
         rewards=[item("tfc:metal/ingot/nickel", 12), xp(250), item("tfc:metal/ingot/steel", 16), item("tfc:powder/flux", 24)])

ch.quest("finale", 11.25, 12.325, "钢铁时代", icon="tfc:metal/anvil/blue_steel", deps=["steel_tools", "steel_armor"], hide_lines=True,
         any_dep=True, shape="gear", size=1.75,
         subtitle="下一步，是机械轰鸣的工业时代",
         desc=["&o&7「钢铁撑起了你的工具和盔甲，也将撑起你的第一座工厂。」&r",
               "",
               "你已拥有：&a高炉&r、&a钢砧（也许还有黑钢砧）&r、&a全套钢制工具与盔甲&r，"
               "也许还打出了传说中的&6蓝钢&r或&6红钢&r。",
               "",
               "&6钢薄板（forge:sheets/steel）&r正是通往下一阶段的通行证——"
               "无论是&6创造 Mod&r的机械压床、&6沉浸工程&r的工程师工作台，"
               "还是&6TFMG&r的曲轴、钢筋、重型装甲板，都需要大量钢材打底。",
               "",
               "&a下一步：&r打开「创造」「沉浸工程」或「TFMG」章节，正式迈入机械与电力的工业时代。"],
         tasks=[checkmark("我已准备好迈入工业时代")],
         rewards=[item("tfc:metal/ingot/steel", 32), item("minecraft:charcoal", 64), levels(12), item("tfc:powder/flux", 32), item("tfc:metal/ingot/copper", 16)])

ch.section("第一节 · 高炉与鼓风口", ["start", "crucible", "fire_bricks", "wrought_sheets", "tuyere", "build_bf", "pig_iron"])
ch.section("第二节 · 从生铁到钢", ["high_carbon", "steel_ingot", "steel_anvil", "steel_sheet", "steel_tools", "steel_armor"])
ch.section("第三节 · 曲轴与机械风箱", ["steel_rod", "crankshaft"])
ch.section("第四节 · 群峦传说：黑钢", ["weak_steel", "black_steel", "black_steel_anvil"])
ch.section("第五节 · 蓝钢与红钢", ["weak_blue_steel", "blue_steel", "weak_red_steel", "red_steel", "stainless_steel", "finale"])
