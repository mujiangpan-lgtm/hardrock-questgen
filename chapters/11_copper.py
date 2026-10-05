from qlib import *

ch = Chapter("copper_age", "铜器时代", icon="tfc:metal/pickaxe/copper", group="ages", order=1,
             theme="copper", subtitle="第一次把石头变成金属")

# ============================================================ A · 寻铜与熔炼
ch.quest("start", 0, 0, "地表的铜粒", icon="tfc:ore/small_native_copper", shape="gear", size=1.5,
         deps=["stone_age:finale"],
         subtitle="金属时代的第一步，是学会看懂地表",
         desc=["&o&7「地上一块发绿的小石子，可能是一整条铜脉的路标。」&r",
               "",
               "&cTFC 没有石镐&r——在拿到铜镐之前，你挖不动任何矿石方块。早期的铜全靠&6地表矿粒&r：",
               "&7- 四处走动时留意地面上的&6原生铜粒&r，直接&e右键/打掉&r即可拾取",
               "&7- 矿粒只出现在&6同种矿脉的正上方&r，看到它就说明脚下有铜，记下坐标以后再来开采",
               "",
               "&e数一数：&r每颗铜粒熔化后得到 &610 mB&r 铜，一块铜锭需要 &6100 mB&r，"
               "也就是 &610 颗铜粒 = 1 块铜锭&r。",
               "&a小技巧：&r河边、山坡等地表裸露处最容易看到矿粒，趁天亮出门，带满小缸。"],
         tasks=[item("tfc:ore/small_native_copper", 10, title="原生铜粒 ×10")],
         rewards=[item("tfc:ceramic/vessel"), xp(30)])

ch.quest("prospecting", 2, -1.5, "勘矿镐", icon="tfc:metal/propick/copper", deps=["start"],
         optional=True, shape="diamond",
         desc=["有了第一批铜之后，可以在砧上锻一把&6勘矿镐&r，系统地寻找矿脉。",
               "",
               "&e用法：&r手持勘矿镐&e右键&r任意方块，它会报告附近一定范围内是否有矿、大致有多少。",
               "沿直线每隔一段距离探测一次，信号变强的方向就是矿脉所在。",
               "",
               "&a小技巧：&r勘矿镐要在本章「铜砧」之后才能锻造，先把它记在心上。"],
         tasks=[tag("tfc:propicks", title="任意勘矿镐")],
         rewards=[item("tfc:food/barley_bread", 4), xp(30)])

ch.quest("melting", 2, 1.5, "熔铜", icon="tfc:ceramic/vessel", deps=["start"], shape="hexagon", size=1.25,
         desc=["&o&7「把石头放进火里，等它流出光来。」&r",
               "",
               "&e1.&r 把铜粒放进&6小缸&r（&e右键&r打开，4 个格子，每格可叠放）",
               "&e2.&r 把小缸放进&6坑窑&r一起烧，或之后放进&6木炭炉&r加热",
               "&e3.&r 温度超过 &61080℃&r 后，缸内矿石化为&6液态铜&r（悬停小缸可查看）",
               "&e4.&r 趁热&e右键&r打开小缸，把&6铸锭模具&r放进界面里的槽位，铜水就会倒进模具",
               "",
               "&c常见的坑：&r小缸冷却后金属会凝固在缸里，下次加热还能再倒，不会浪费；"
               "但&c不同金属会在缸内混合成合金或杂质&r，别把别的矿一起放进去。"],
         tasks=[checkmark("我把铜水倒进了铸锭模具")],
         rewards=[item("minecraft:clay_ball", 16), xp(40)])

ch.quest("first_ingots", 4, 0, "第一块铜锭", icon="tfc:metal/ingot/copper", deps=["melting"],
         desc=["模具里的铜水冷却凝固后，把&6铸锭模具放进合成栏&r，就能取出&6铜锭&r。",
               "",
               "&c注意：&r取锭时模具有一定几率损坏，多备几个（石器时代「模具与大缸」）。",
               "",
               "&e目标：&r攒到 &614 块铜锭&r——第一座铜砧要 7 块铜双锭，正好 14 块铜锭。",
               "打工具还要更多，所以继续捡铜粒，或者先做出铜镐去开矿脉。"],
         tasks=[item("tfc:metal/ingot/copper", 14, title="铜锭 ×14")],
         rewards=[item("tfc:ceramic/ingot_mold", 2), xp(40)])

ch.quest("tool_molds", 4, -2.5, "工具模具", icon="tfc:ceramic/pickaxe_head_mold", deps=["first_ingots"],
         optional=True, shape="diamond",
         desc=["除了铸锭模具，还可以用黏土塑形出&6工具头模具&r（镐、斧、锯、锤……），"
               "把铜水直接铸成&6工具头&r，跳过砧上锻打。",
               "",
               "&c取舍：&r铸造的工具头没有锻造品质加成；在砧上锻造并打出好的手法能得到更耐用的工具。",
               "&a适合：&r砧还没做出来、急需一把镐的时候。"],
         tasks=[item("tfc:ceramic/pickaxe_head_mold", title="镐头模具")],
         rewards=[item("minecraft:clay_ball", 16), xp(20)])
# ============================================================ B · 炭火与焊接
ch.quest("charcoal", 7, 0, "烧制木炭", icon="minecraft:charcoal", deps=["first_ingots"],
         desc=["篝火太弱，焊接和锻造需要更高的温度，燃料要换成&6木炭&r。",
               "",
               "&e1.&r 手持原木&e潜行+右键&r地面放下&6原木堆&r，继续潜行右键往里加原木，可以堆多层",
               "&e2.&r 用泥土、岩石等&6不可燃方块&r把原木堆四面和顶部封严，只留一个面点火",
               "&e3.&r 用起火器点燃，再把那一面也封上，等它闷烧成&6木炭堆&r",
               "&e4.&r 用铲子挖开木炭堆，获得&6木炭&r",
               "",
               "&c常见的坑：&r没封严的原木堆会直接烧成灰；离家太近可能引燃房子。"],
         tasks=[item("minecraft:charcoal", 32, title="木炭 ×32")],
         rewards=[item("tfc:firestarter"), item("tfc:wood/log/oak", 16), xp(30)])

ch.quest("forge", 9, 0, "木炭炉", icon="minecraft:charcoal", deps=["charcoal"], shape="hexagon", size=1.25,
         desc=["&6木炭炉&r是金属加工的核心热源：加热锻件、熔化矿石、焊接都靠它。",
               "",
               "&e搭建：&r往地上堆 &67~8 层木炭堆&r（手持木炭潜行右键），用 &65 块岩石&r"
               "包住它的四面和底部，顶上露天，然后用起火器点燃。",
               "",
               "&e使用：&r下面 5 格放燃料（木炭/煤），上面 5 格放要加热的物品，"
               "右侧槽位放小缸或模具，炉内熔化的金属会自动流进去。",
               "&c注意：&r炉子上方必须是空气，周围十字两格内至少一格露天，否则不工作。"],
         tasks=[checkmark("我搭好并点燃了木炭炉")],
         rewards=[item("minecraft:charcoal", 16), xp(40)])

ch.quest("stone_anvil", 9, -2.5, "石砧", icon="tfc:rock/anvil/basalt", deps=["forge"],
         desc=["第一座砧不用金属：找一块&6未加工的火成岩&r方块（花岗岩、闪长岩、辉长岩、玄武岩、"
               "安山岩、流纹岩、英安岩），手持&6锤子&e右键&r它，就会变成&6石砧&r。",
               "",
               "&c重要：&r石砧&c只能焊接&r，不能锻造工具。它唯一的使命是帮你焊出铜双锭，做出真正的铜砧。"],
         tasks=[checkmark("我敲出了一座石砧")],
         rewards=[item("tfc:powder/flux", 8), xp(30)])

ch.quest("welding", 11, -1.5, "焊接铜双锭", icon="tfc:metal/double_ingot/copper", deps=["stone_anvil"],
         desc=["&e1.&r 把两块铜锭放进&6木炭炉&r加热，直到悬停显示&6「可焊接」&r",
               "&e2.&r 趁热&e右键&r石砧，把两块铜锭放进左侧两个槽位，再放入&6助焊剂&r",
               "&e3.&r 点击界面上的&6焊接&r按钮，得到一块&6铜双锭&r",
               "",
               "&6助焊剂&r：把石灰岩、白云岩、大理岩等&6熔剂石&r加工成粉（详见 JEI）。",
               "&c常见的坑：&r金属降温很快，从炉里拿出来就要马上焊；冷了就放回去再加热。"],
         tasks=[item("tfc:metal/double_ingot/copper", 7, title="铜双锭 ×7")],
         rewards=[item("tfc:powder/flux", 8), item("minecraft:charcoal", 16), xp(50)])

ch.quest("copper_anvil", 13, 0, "铜砧", icon="tfc:metal/anvil/copper", deps=["welding"],
         shape="hexagon", size=1.25,
         desc=["&o&7「石头能焊，但只有金属砧才能真正塑造金属。」&r",
               "",
               "&e合成：&r7 块&6铜双锭&r在工作台上摆成「工」字形（上三、中一、下三），得到&6铜砧&r。",
               "",
               "&6锻造：&r把加热到「可锻造」的锭放到砧上，&e右键&r打开界面，选择要做的工具，"
               "然后组合拉伸、敲击、弯折等动作，让绿色指针对准红色目标；"
               "&a最后几步按配方要求的顺序打完&r，质量越高的手法做出的工具越好。",
               "{@pagebreak}",
               "&a小技巧：&r锻造前先看配方要求的「最后三步」，提前把指针调到目标附近再收尾，"
               "能稳定打出更高品质。"],
         tasks=[item("tfc:metal/anvil/copper", title="铜砧")],
         rewards=[item("tfc:metal/ingot/copper", 4), item("minecraft:charcoal", 16), xp(60)])
# ============================================================ C · 铜制工具
ch.quest("copper_pickaxe", 16, -3, "铜镐", icon="tfc:metal/pickaxe/copper", deps=["copper_anvil"],
         shape="hexagon", size=1.25,
         desc=["在铜砧上锻出&6铜镐头&r（或用镐头模具铸造），和木棍合成&6铜镐&r。",
               "",
               "这是你&6第一把能挖矿的镐子&r：矿石方块、岩石方块终于都能挖了。",
               "&c警告：&r挖开岩石会引发塌方，下矿前带足&6支撑梁&r（石器时代）。"],
         tasks=[item("tfc:metal/pickaxe/copper", title="铜镐")],
         rewards=[item("tfc:wood/support/oak", 8), xp(40)])

ch.quest("mine_ore", 18, -3, "开采矿脉", icon="tfc:ore/rich_native_copper/granite", deps=["copper_pickaxe"],
         desc=["顺着地表铜粒往下挖，找到成片的&6铜矿脉&r。矿石分三档品级，熔化产量不同：",
               "&7- &6贫瘠&r 15 mB · &6普通&r 25 mB · &6富集&r 35 mB（小粒只有 10 mB）",
               "",
               "铜矿不只有&6原生铜&r，&6孔雀石&r、&6黝铜矿&r同样熔出纯铜，产量一样，见到就挖。",
               "&a小技巧：&r富集矿 3 块就差不多是一块锭，优先挖富集矿。"],
         tasks=[tag("tfc:ores/copper/normal", 8, title="普通品级铜矿石 ×8")],
         rewards=[item("tfc:wood/support/oak", 8), item("tfc:torch", 8), xp(40)])

ch.quest("copper_chisel", 16, -1, "铜凿", icon="tfc:metal/chisel/copper", deps=["copper_anvil"],
         desc=["&6凿&r有两个重要用途：",
               "&7- &e右键&r岩石/砖块，把它凿成台阶、楼梯或磨制石（切换模式见按键提示）",
               "&7- 背包里同时带着&6凿&r和&6刮制兽皮或皮革&r时，石头才能打开&6精确塑形&r界面"
               "（本整合包的改动），按图案敲出石器",
               "",
               "&a小技巧：&r凿过的磨制石是砌墙的好材料，也不容易塌方。"],
         tasks=[item("tfc:metal/chisel/copper", title="铜凿")],
         rewards=[item("tfc:metal/ingot/copper", 2), xp(30)])

ch.quest("copper_hammer", 16, 1, "铜锤", icon="tfc:metal/hammer/copper", deps=["copper_anvil"],
         desc=["锻造时必须&6手持锤子&r才能在砧上敲打，石锤也能用，但铜锤耐久高得多。",
               "",
               "&a小技巧：&r锤子还能把矿石方块、岩石敲碎，也是做石砧的工具。"],
         tasks=[item("tfc:metal/hammer/copper", title="铜锤")],
         rewards=[item("tfc:metal/ingot/copper", 2), xp(30)])

ch.quest("copper_saw", 16, 3, "铜锯", icon="tfc:metal/saw/copper", deps=["copper_anvil"], shape="hexagon",
         size=1.25,
         desc=["&6锯&r是木工的钥匙：把&6锯 + 原木&r放进合成栏，一根原木出 &68 块木材&r（锯会损耗耐久）。",
               "",
               "木材用来做&6工作台、箱子、大桶、工具架、捕兽箱&r……这一章剩下的内容几乎都靠它。"],
         tasks=[item("tfc:metal/saw/copper", title="铜锯")],
         rewards=[item("tfc:wood/log/oak", 8), xp(40)])
# ============================================================ D · 木工与储物
ch.quest("lumber", 13, 9.5, "锯出木材", icon="tfc:wood/lumber/oak", deps=["copper_saw"], hide_lines=True,
         desc=["&e锯 + 任意原木&r → &68 块对应木种的木材&r。",
               "",
               "&a建议：&r一次多锯一些，工作台、箱子、大桶、风箱都要用，"
               "而且不同木种的木材通常都能混用（悬停配方看要求）。"],
         tasks=[tag("tfc:lumber", 32, title="任意木材 ×32")],
         rewards=[item("tfc:wood/log/oak", 8), xp(20)])

ch.quest("workbench", 11, 8, "工作台", icon="tfc:wood/planks/oak_workbench", deps=["lumber"],
         desc=["TFC 的背包合成栏只有 2×2，&63×3 配方必须用工作台&r，比如铜砧、风箱、大桶。",
               "",
               "&a小技巧：&r把工作台放在木炭炉和砧旁边，锻造、组装一条龙。"],
         tasks=[tag("forge:workbench", title="任意工作台")],
         rewards=[item("tfc:wood/lumber/oak", 8), xp(20)])

ch.quest("chest", 11, 11, "箱子", icon="tfc:wood/chest/oak", deps=["lumber"],
         desc=["木材做出的&6箱子&r是最基础的储物方块。",
               "",
               "&c注意：&rTFC 的物品有&6尺寸&r，过大的物品（比如大缸）放不进箱子，只能摆在地上。",
               "&a建议：&r矿石、燃料、工具分箱存放，后期接物流系统会轻松很多。"],
         tasks=[tag("forge:chests", title="任意箱子")],
         rewards=[item("tfc:wood/lumber/oak", 8), xp(20)])

ch.quest("barrel", 9, 9.5, "大桶", icon="tfc:wood/barrel/oak", deps=["lumber"], shape="hexagon", size=1.25,
         desc=["&6大桶&r是 TFC 里最万能的加工设备：&61 格物品 + 一桶液体&r，密封后按配方慢慢转化。",
               "",
               "&e用途：&r制作石灰水、鞣酸，腌制、浸泡兽皮，酿造……（详见 JEI 的「大桶」分类）",
               "&e用法：&r&e右键&r打开，放入物品和液体，然后点击&6密封&r按钮开始计时。",
               "",
               "&c常见的坑：&r大多数配方必须&c密封&r才会进行；密封期间不能再取放东西。"],
         tasks=[tag("tfc:barrels", title="任意大桶")],
         rewards=[item("tfc:powder/flux", 4), xp(30)])

ch.quest("tool_rack", 15, 9.5, "工具架", icon="tfc:wood/planks/oak_tool_rack", deps=["lumber"],
         optional=True, shape="diamond",
         desc=["&6工具架&r可以挂 4 件工具，取用方便，也是很好的装饰。",
               "",
               "&e合成：&r木材制作，详见 JEI。"],
         tasks=[tag("tfc:tool_racks", title="任意工具架")],
         rewards=[item("tfc:wood/lumber/oak", 8), xp(20)])
# ============================================================ E · 制革与风箱
ch.quest("soak_scrape", 6, 9.5, "浸泡与刮制", icon="tfc:large_scraped_hide", deps=["barrel"],
         desc=["&6TFC 生兽皮&r要经过&6浸泡 → 刮制 → 预制 → 鞣制 → 上油 → 再刮 → 裁剪&r，先做前两步。",
               "",
               "如果手里是&6牛皮&r或彩色兽皮，先按「石器时代 · 兽皮刮制」铺原木刮制，转成 TFC 生兽皮。",
               "&c那次刮制只是转换原料；下面是石灰水浸泡后的第二次操作。&r",
               "",
               "&e1.&r &6石灰水&r：大桶装水，放入&6助焊剂&r即可（每 500 mB 水 1 份）",
               "&e2.&r 把&6生兽皮&r放进装石灰水的大桶，&6密封等待约 8 个游戏小时&r，得到&6浸泡兽皮&r",
               "&e3.&r 把浸泡兽皮&e右键&r铺在&6原木顶面&r，原木上方必须空着",
               "&e4.&r 手持&6TFC 石刀或金属刀&r，&6右键刮完皮面 4×4 的 16 个格子&r，再打掉兽皮，捡起&6刮制兽皮&r",
               "",
               "&cJEI 的「刮制配方」要在原木上操作；不要放工作台，也不要贴原木侧面。&r",
               "&a小技巧：&r兽皮分小/中/大三种尺寸，大兽皮最终产出的皮革最多。"],
         tasks=[tag("tfc:scraped_hides", title="任意刮制兽皮")],
         rewards=[item("tfc:bucket/tannin"), xp(30)])

ch.quest("tanning", 4, 9.5, "预制与鞣制", icon="tfc:large_prepared_hide", deps=["soak_scrape"],
         desc=["&e5.&r 刮制兽皮放进&6装盐水&r的大桶，密封约 8 个游戏小时 → &6预制兽皮&r",
               "&c本包这一阶段要求盐水，不是淡水。&r可从海边取盐水；液体用量按兽皮尺寸查看 JEI。",
               "&e6.&r 预制兽皮放进&6装鞣酸&r的大桶，密封约 8 个游戏小时 → &6鞣制兽皮&r",
               "",
               "&6本包鞣酸配方：&r把&6树皮粉&r放进装&6淡水&r的大桶，密封加工。每份树皮粉配 200 mB 水，",
               "得到对应量的鞣酸；树皮粉的来源对物品按 &eR&r 查看。",
               "",
               "&c鞣制兽皮仍不是皮革。&r继续做下一任务的上油、刮制与裁剪，才能用于皮革制品。",
               "",
               "&c常见的坑：&r每次换液体前把桶里旧液体倒干净，否则配方对不上。"],
         tasks=[tag("tfc:tanned_hides", title="任意鞣制兽皮")],
         rewards=[item("tfc:bucket/olive_oil_water"), xp(30)])

ch.quest("leather", 2, 9.5, "上油、刮制与裁剪", icon="minecraft:leather", deps=["tanning"],
         shape="hexagon", size=1.25,
         desc=["&o&7「水、碱、酸、油，一张兽皮要洗礼七次才配叫皮革。」&r",
               "",
               "&e7.&r 用&6搅拌碗&r（Firmalife）把鞣制兽皮和 &61000 mB 毛橄榄油&r或&6种子油水&r"
               "搅拌，得到&6上油兽皮&r。要用对应油水混合液，具体对上油兽皮按 &eR&r 查看。",
               "&7- 一批放&6小皮 3 张 / 中皮 2 张 / 大皮 1 张&r，每批都需 1000 mB 油水",
               "&e8.&r 上油兽皮铺到&6原木顶面&r，用 TFC 刀&6右键刮完 16 格&r，再打掉取回&6整张皮革&r",
               "&e9.&r 在&6缝纫工作站&r（SewingKit）上用&6剪刀&r裁剪：小 / 中 / 大整张皮革 → &61 / 2 / 3 张普通皮革&r",
               "{@pagebreak}",
               "&6早期上油材料：种子油水&r",
               "&e1.&r 用&6手推磨&r把可用树种种子磨成&6树种糊&r，具体种子见 JEI",
               "&e2.&r 陶锅装 &61000 mB 淡水&r，放 &64 份树种糊 + 1 份树皮粉&r，加热至 &6300°C&r并等配方完成",
               "&e3.&r 得到的种子油水可装走，供上面的搅拌碗配方使用",
               "",
               "&6首次裁剪可用燧石剪刀&r：&62 份燧石碎片 + 2 份植物线&r无序合成，具体材料对剪刀按 &eR&r 查看。",
               "&c裁剪设备要看配方：&r这是 JEI 的&6缝纫&r配方，别与 Cold Sweat 改造保暖衣物的&6特制裁缝台&r混淆。",
               "按 &eR&r 查&6整张皮革产普通皮革&r所需的工作站和材料；不必先做需要皮革绳的金属剪刀。",
               "",
               "&a小技巧：&r多张兽皮可以同时在一个大桶里泡，攒一批一起做最省时间。"],
         tasks=[item("minecraft:leather", 6, title="皮革 ×6")],
         rewards=[item("tfc:wood/lumber/oak", 6), xp(50)])

ch.quest("bellows", 0, 11.5, "风箱", icon="tfc:bellows", deps=["leather"], shape="hexagon", size=1.25,
         desc=["&e合成：&r3 块皮革夹在上下各 3 块木材中间（上木材、中皮革、下木材）。",
               "",
               "&e安装：&r把风箱放在&6木炭炉上方一格的相邻位置&r，对着炉子；"
               "&e右键&r拉动风箱，炉子的最高温度会在一段时间内提升。",
               "",
               "&a为什么要它：&r铜和青铜不靠风箱也能熔，但&6铁&r需要更高的温度，"
               "风箱是迈向铁器时代必备的设备。&c代价：&r温度越高，木炭烧得越快。"],
         tasks=[item("tfc:bellows", title="风箱")],
         rewards=[item("minecraft:charcoal", 32), xp(40)])

ch.quest("finale", 0, 8.5, "青铜时代的门槛", icon="tfc:metal/anvil/copper", deps=["bellows"],
         shape="gear", size=1.75,
         subtitle="合金，是文明真正的加速器",
         desc=["&o&7「纯铜软而易得，合金才是真正的突破。」&r",
               "",
               "你已经拥有：&a铜砧&r、&a木炭炉 + 风箱&r、&a铜镐和全套铜工具&r、&a大桶与皮革&r。",
               "",
               "纯铜工具太软，下一步是&6合金&r：把铜和&6锡&r、&6铋&r或&6锌&r等按比例一起熔化，"
               "就能得到&6青铜&r等更硬的金属——还能锻出更高级的砧。",
               "",
               "&a下一步：&r带上勘矿镐去找&6锡石&r（锡矿），进入「青铜时代」。"],
         tasks=[checkmark("我已经准备好冶炼合金了")],
         rewards=[item("tfc:metal/ingot/copper", 6), item("tfc:powder/flux", 8), levels(5)])

ch.section("第一节 · 寻铜与熔炼", ["start", "prospecting", "melting", "first_ingots", "tool_molds"])
ch.section("第二节 · 炭火与焊接", ["charcoal", "forge", "stone_anvil", "welding", "copper_anvil"])
ch.section("第三节 · 铜制工具", ["copper_pickaxe", "mine_ore", "copper_chisel", "copper_hammer", "copper_saw"])
ch.section("第四节 · 木工与储物", ["lumber", "workbench", "chest", "barrel", "tool_rack"])
ch.section("第五节 · 制革与风箱", ["soak_scrape", "tanning", "leather", "bellows", "finale"])
