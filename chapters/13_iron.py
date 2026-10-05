from qlib import *

ch = Chapter("iron_age", "铁器时代", icon="tfc:metal/anvil/wrought_iron", group="ages", order=3,
             theme="iron", subtitle="炉火更旺，文明的骨架开始生长")

# ============================================================ A · 寻铁与火砖
ch.quest("start", 1.45, 3.1, "三种铁矿", icon="tfc:ore/normal_hematite", shape="gear", size=1.5,
         deps=["bronze_age:finale"],
         subtitle="青铜之后，真正的硬骨头来了",
         desc=["&o&7「铁比铜锡更常见，却难伺候得多。」&r",
               "",
               "本章要找的是&6铁矿&r，一共三种，熔化后都得到&6铸铁&r：",
               "&7- &6赤铁矿&r —— 喷出岩地表附近的大型矿脉",
               "&7- &6磁铁矿&r —— 沉积岩地表附近的大型矿脉",
               "&7- &6褐铁矿&r —— 沉积岩地表附近的大型矿脉",
               "",
               "&a小技巧：&r这三种矿的地表矿粒都长得差不多发黑发红，勘矿镐这时就很有用了。"],
         tasks=[tag("forge:ores/iron", 8, title="任意铁矿石 ×8")],
         rewards=[item("tfc:powder/flux", 8), xp(30)])

ch.quest("melt_iron", 3.65, 3.1, "熔出铸铁", icon="tfc:metal/ingot/cast_iron", deps=["start"],
         desc=["&6铁矿石熔化后得到的是&c铸铁&r，不是锻铁！&r这是本章最容易踩的坑。",
               "",
               "&e步骤和铜一样：&r小缸/坩埚装矿 → 坑窑或木炭炉加热 → 超过熔点后流出铸铁液。",
               "",
               "&c铸铁又脆又硬，直接拿去做工具会很快碎掉。&r它只是半成品，"
               "下一步要靠&6锻铁炉&r把它变成能用的&6锻铁&r。"],
         tasks=[item("tfc:metal/ingot/cast_iron", 4, title="铸铁锭 ×4")],
         rewards=[item("minecraft:clay_ball", 16), xp(30)])

ch.quest("graphite", 5.85, 2.1, "石墨", icon="tfc:ore/graphite", deps=["melt_iron"],
         desc=["&6石墨&r是耐火黏土的原料之一，生成在 y=60 以下的&6片麻岩、大理岩、石英岩、片岩&r中。",
               "",
               "",
               "&e变成石墨粉（洗矿流程）：&r",
               "&e1.&r 石墨矿 + 锤子合成 → &6含岩石墨碎块&r",
               "&e2.&r 放进&6洗矿槽&r冲洗 → &6石墨碎块&r",
               "&e3.&r 手推磨磨碎 → &6含杂石墨粉&r，再进洗矿槽 → &6石墨粉&r",
               "&7- 有了机械动力后也可以用鼓风机+水（批量洗涤）代替洗矿槽",
               "",
               "&a小技巧：&r石墨矿脉里常常伴生&6烟煤&r，挖到一处往往两样都有。"],
         tasks=[item("tfc:ore/graphite", 4, title="石墨 ×4")],
         rewards=[item("minecraft:charcoal", 16), xp(20)])

ch.quest("kaolinite", 5.85, 4.1, "高岭土与高岭石粉", icon="tfc:kaolin_clay", deps=["melt_iron"],
         desc=["&6高岭土&r生成在高海拔的高原、古老山脉、高地，或气候合适的火山地带，"
               "地表长着&6血百合&r的地方往下挖就对了。",
               "",
               "&e加热高岭土&r（坑窑或木炭炉）可以得到&6高岭石粉&r，但&c这道工艺还不成熟，产率只有约 20%&r，"
               "&a建议多挖几组再去烧&r。"],
         tasks=[item("tfc:powder/kaolinite", 8, title="高岭石粉 ×8")],
         rewards=[item("minecraft:clay_ball", 16), xp(30)])

ch.quest("fire_clay", 8.05, 3.1, "耐火黏土", icon="tfc:fire_clay", deps=["graphite", "kaolinite"],
         shape="hexagon", size=1.25,
         desc=["&6石墨粉 + 高岭石粉 + 黏土球&r合成&6耐火黏土&r（详见 JEI 的具体比例）。",
               "",
               "耐火黏土比普通黏土耐受更高的温度，是通往高级设备的门票：",
               "&7- 塑形出&6坩埚&r（未烧制）",
               "&7- 敲打出&6耐火砖&r（钢铁时代建高炉要用）",
               "&7- 塑形出&6耐火铸锭模具&r（比普通模具更耐用，损坏率只有 1% 而非 10%）",
               "",
               "&a建议：&r多做一些，坩埚和耐火砖都要消耗大量耐火黏土。"],
         tasks=[item("tfc:fire_clay", 12, title="耐火黏土 ×12")],
         rewards=[item("minecraft:clay_ball", 16), xp(40)])

ch.quest("crucible", 10.25, 3.1, "坩埚", icon="tfc:crucible", deps=["fire_clay"],
         desc=["手持耐火黏土塑形出&6未烧制的坩埚&r，再用坑窑或木炭炉烧制成&6坩埚&r。",
               "",
               "&e用途：&r右键坩埚打开界面——比小缸更快地批量熔炼、合金化金属，"
               "而且&a配比允许一定误差&r，调配合金比小缸轻松得多。",
               "",
               "&a小技巧：&r坩埚要加热才能用，放在木炭炉上方或炭堆旁，底下任意发热方块都能当热源。"],
         tasks=[item("tfc:crucible", title="坩埚")],
         rewards=[item("tfc:powder/flux", 8), xp(40)])
# ============================================================ B · 锻铁炉
ch.quest("bronze_sheets", 13.45, 2.1, "青铜双层薄板", icon="tfc:metal/double_sheet/bronze", deps=["crucible"],
         desc=["&c搭建锻铁炉之前先备好材料：&r需要 &68 张青铜双层薄板&r，在工作台上围成"
               "3×3 的空心框（中心格留空，详见 JEI 配方）。",
               "",
               "青铜双层薄板的制作：青铜锭 → 砧上锻打成青铜薄板 → 两张薄板焊接成双层薄板"
               "（详见 JEI 配方，流程与铜双锭焊接类似）。",
               "",
               "&a建议：&r一次性锻够 8 张，省得来回跑炉子和砧。"],
         tasks=[item("tfc:metal/double_sheet/bronze", 8, title="青铜双层薄板 ×8")],
         rewards=[item("tfc:powder/flux", 8), xp(40)])

ch.quest("bloomery", 15.65, 3.1, "搭建锻铁炉", icon="tfc:bloomery", deps=["bronze_sheets"],
         shape="hexagon", size=1.25,
         desc=["&o&7「铁块塔在炉里静静燃烧了十五个小时，像一次漫长的等待。」&r",
               "",
               "&e1.&r 用 8 张青铜双层薄板合成&6锻铁炉&r方块，放置在地面",
               "&e2.&r 锻铁炉上方需要&6烟囱&r：每层用非可燃方块（岩石等）围成空心柱，往上堆",
               "&e3.&r &e爬到顶部&r向炉内&e丢入&r（Q 键）&6铁矿石&r（赤铁矿/磁铁矿/褐铁矿均可，"
               "小粒矿、矿石方块都行）和&6木炭&r",
               "{@pagebreak}",
               "&6配比：&r每消耗 &61 份木炭粉&r和 &6100 mB 铸铁&r（约 10 颗矿粒或对应矿石方块），"
               "就能产出 &61 块方坯&r。炉子最多容纳 48 件投入物，烟囱每层能存 16 件，装不下会从正面吐出来。",
               "&e4.&r &e用起火器点燃&r锻铁炉方块，等待 &615 小时&r（游戏时间）完成冶炼",
               "",
               "&c常见的坑：&r",
               "&7- 炉子熄火后会留下一座&6方坯方块&r，&e用镐反复挖掘&r才能把&6生铁方坯&r一块块取出来",
               "&7- 没点燃时想取回投入的矿石，直接&c挖掉锻铁炉方块&r即可，别去挖那座矗立的塔"],
         tasks=[checkmark("我点燃了一座锻铁炉，并等它完成了冶炼")],
         rewards=[item("minecraft:charcoal", 32), xp(60)])

ch.quest("raw_bloom", 17.85, 3.1, "取出生铁方坯", icon="tfc:raw_iron_bloom", deps=["bloomery"],
         desc=["熄火的锻铁炉会留下一座&6方坯方块&r，&e用镐反复挖掘&r它，直到挖空为止，"
               "每次都会掉落一块&6生铁方坯&r。",
               "",
               "&c注意：&r生铁方坯&c还不是锻铁&r！它只是半成品，必须上砧锻打才能变成真正可用的锻铁。"],
         tasks=[item("tfc:raw_iron_bloom", 4, title="生铁方坯 ×4")],
         rewards=[item("minecraft:charcoal", 16), xp(30)])

ch.quest("stone_anvil2", 13.45, 4.1, "备好一座能用的砧", icon="tfc:metal/anvil/bronze", deps=["start"], hide_lines=True,
         optional=True, shape="diamond",
         desc=["锻打方坯需要在&6砧&r上进行，青铜砧或更硬的砧都能用。",
               "",
               "&c如果你还没有砧：&r回顾青铜时代「铜砧」一节的做法——"
               "先用未加工火成岩敲出石砧，焊双锭，再合成金属砧。",
               "",
               "&a小技巧：&r砧的等级决定能加工的金属上限，青铜砧刚好够用来处理方坯。"],
         tasks=[tag("tfc:bronze_anvils", title="任意青铜砧")],
         rewards=[item("tfc:powder/flux", 4), xp(20)])
# ============================================================ C · 锻造锻铁
ch.quest("refine_bloom", 1.325, 10.2, "精炼方坯", icon="tfc:refined_iron_bloom", deps=["raw_bloom"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=["&e1.&r 把&6生铁方坯&r加热到可锻造的温度（木炭炉）",
               "&e2.&r 趁热放上&6砧&r，&e右键&r打开锻造界面，按提示敲打",
               "&e3.&r 完成后得到&6精铁方坯&r——方坯锻造要敲&c两轮&r才能变成锭，这是第一轮",
               "",
               "&c常见的坑：&r和锻锭一样，金属冷却后锻造界面会锁死，&c凉了就放回炉里再加热&r。"],
         tasks=[item("tfc:refined_iron_bloom", 2, title="精铁方坯 ×2")],
         rewards=[item("minecraft:charcoal", 16), xp(40)])

ch.quest("wrought_ingot", 3.525, 10.2, "锻铁锭", icon="tfc:metal/ingot/wrought_iron", deps=["refine_bloom"],
         shape="hexagon", size=1.25,
         desc=["把&6精铁方坯&r重新加热、上砧，再锻打一轮，终于得到&6锻铁锭&r。",
               "",
               "&a恭喜：&r从矿石到锻铁锭，一共经历了&6熔炼 → 锻铁炉 → 精炼 → 锻造&r四个阶段，"
               "这是本整合包里最长的一条生产链之一。",
               "&e目标：&r攒够 &614 块锻铁锭&r——锻铁砧要 7 块双锭，刚好 14 块锭。"],
         tasks=[item("tfc:metal/ingot/wrought_iron", 14, title="锻铁锭 ×14")],
         rewards=[item("tfc:ceramic/ingot_mold", 2), xp(50)])

ch.quest("wrought_anvil", 5.725, 10.2, "锻铁砧", icon="tfc:metal/anvil/wrought_iron", deps=["wrought_ingot"],
         shape="hexagon", size=1.25,
         desc=["焊 7 块&6锻铁双锭&r（锻铁炉旁的砧上焊接，流程同铜双锭），"
               "摆成「工」字形合成&6锻铁砧&r。",
               "",
               "&a为什么升级：&r锻铁砧的&6等级更高&r，能锻造的金属种类和工具上限都比青铜砧高，"
               "后续的钢、黑钢都要靠它或更高级的砧。"],
         tasks=[item("tfc:metal/anvil/wrought_iron", title="锻铁砧")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 4), item("minecraft:charcoal", 16), xp(60)])

ch.quest("iron_pickaxe", 7.925, 8.2, "锻铁镐与工具", icon="tfc:metal/pickaxe/wrought_iron", deps=["wrought_anvil"],
         desc=["在锻铁砧上打出全套&6锻铁工具&r：镐、斧、锄、铲、锤、锯、凿、刀……",
               "",
               "锻铁工具的&6耐久和效率&r比青铜高出一大截，挖矿、砍树、种地都轻松不少。",
               "&a小技巧：&r先打一把镐，深层矿脉（锡、铁、后面的煤）很多要挖穿岩层才能到。"],
         tasks=[tag("tfc:axes", title="任意斧"), tag("tfc:hoes", title="任意锄"), tag("tfc:shovels", title="任意锹")],
         rewards=[item("tfc:wood/support/oak", 8), xp(40)])

ch.quest("iron_knife_hammer", 7.925, 10.2, "锻铁刀与锻铁锤", icon="tfc:metal/hammer/wrought_iron",
         deps=["wrought_anvil"],
         desc=["&6锻铁锤&r是锻造的必需品，&6锻铁刀&r切割效率更高、更耐用。",
               "",
               "&a小技巧：&r给工具架腾个位置，常用的锤子、刀挂出来，拿取更方便。"],
         tasks=[tag("tfc:knives", title="任意刀"), tag("tfc:hammers", title="任意锤")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 2), xp(30)])

ch.quest("iron_armor", 7.925, 12.2, "锻铁护甲", icon="tfc:metal/chestplate/wrought_iron", deps=["wrought_anvil"],
         optional=True, shape="diamond",
         desc=["&6锻铁护甲&r需要先在砧上打出「未完成的」部件，再到&6锻造台&r上完成最后一步"
               "（和铜/青铜护甲流程一致）。",
               "",
               "&a小技巧：&r熟练的铁匠会尽量用最少的锤击次数完成锻造，成品质量越高、属性越好。"],
         tasks=[tag("tfc:mob_head_armor", title="头盔"), tag("tfc:mob_chest_armor", title="胸甲"),
                tag("tfc:mob_leg_armor", title="护腿"), tag("tfc:mob_feet_armor", title="靴子")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 4), item("firstaid:bandage", 4), xp(50)])

ch.quest("propick_iron", 10.125, 10.2, "锻铁勘矿镐", icon="tfc:metal/propick/wrought_iron", deps=["wrought_anvil"],
         optional=True, shape="diamond",
         desc=["升级一把&6锻铁勘矿镐&r，探测范围和精度比青铜版更好，适合继续深挖铁矿和即将要找的&6煤矿&r。"],
         tasks=[item("tfc:metal/propick/wrought_iron", title="锻铁勘矿镐")],
         rewards=[item("tfc:powder/flux", 4), xp(30)])
# ============================================================ D · 锻铁的用途
ch.quest("iron_lamp", 13.325, 8.2, "锻铁灯", icon="tfc:metal/lamp/wrought_iron", deps=["wrought_anvil"], hide_lines=True,
         desc=["&6锻铁灯&r需要先锻出&6未完成的锻铁灯&r，再到锻造台上完成。",
               "",
               "&e使用：&r放置后&e右键&r加入&6燃料（如橄榄油）&r并点燃，比火把更持久、更亮，还不会熄灭。",
               "&a小技巧：&r适合放在室内或矿道深处当长期照明。"],
         tasks=[item("tfc:metal/lamp/wrought_iron", title="锻铁灯")],
         rewards=[item("minecraft:charcoal", 16), xp(30)])

ch.quest("iron_bars_chain", 13.325, 10.2, "锻铁棒、锁链与栅栏", icon="tfc:metal/chain/wrought_iron", hide_lines=True,
         deps=["wrought_anvil"], optional=True, shape="diamond",
         desc=["锻铁棒是很多后续配方的基础材料；&6锻铁栅栏&r防动物效果比木栅栏好，"
               "&6锁链&r可以用来做装饰性的悬挂结构或拴住某些生物。"],
         tasks=[tag("forge:rods/wrought_iron", title="锻铁棒"), item("tfc:metal/chain/wrought_iron", title="锻铁锁链")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 2), xp(20)])

ch.quest("iron_tool_molds", 13.325, 12.2, "耐火模具", icon="tfc:ceramic/fire_ingot_mold", deps=["fire_clay"], hide_lines=True,
         optional=True, shape="diamond",
         desc=["普通陶土模具浇铸锻铁时损坏率较高，用&6耐火黏土&r塑形的&6耐火铸锭/工具模具&r"
               "更耐用：破损率只有约 &61%&r（普通模具约 10%）。",
               "",
               "&a适合：&r打算长期批量铸造金属锭或工具头的话，换上耐火模具很划算。"],
         tasks=[item("tfc:ceramic/fire_ingot_mold", title="耐火铸锭模具")],
         rewards=[item("tfc:fire_clay", 8), xp(20)])

ch.quest("fire_bricks", 15.525, 9.2, "耐火砖：为钢铁时代预热", icon="tfc:ceramic/fire_brick", deps=["fire_clay"], hide_lines=True,
         optional=True, shape="diamond",
         desc=["手持耐火黏土塑形并烧制出&6耐火砖&r——这是&6钢铁时代&r建造&6高炉&r的必需隔热材料。",
               "",
               "&a提前囤一批：&r高炉用量很大，趁现在手里耐火黏土充足，不妨多烧一些存起来。"],
         tasks=[item("tfc:ceramic/fire_brick", 8, title="耐火砖 ×8")],
         rewards=[item("tfc:fire_clay", 8), xp(30)])

ch.quest("finale", 15.525, 11.2, "通向钢铁的门", icon="tfc:metal/anvil/wrought_iron", deps=["iron_pickaxe", "iron_knife_hammer"], hide_lines=True,
         shape="gear", size=1.75,
         subtitle="方坯燃尽处，是更坚硬的明天",
         desc=["&o&7「从矿石到锻铁，你烧穿了四道工序；而钢，还要再烧穿一道。」&r",
               "",
               "你已经拥有：&a锻铁砧&r、&a坩埚&r、&a耐火黏土与耐火砖&r、&a全套锻铁工具和护甲&r。",
               "",
               "下一步是&6生铁&r与&6钢&r：需要搭建更庞大的多方块结构——&6高炉&r，"
               "靠&6风箱&r把炉温推到熔炼生铁所需的高度，再精炼成钢。",
               "",
               "&a下一步：&r带上耐火砖和锻铁工具，进入「钢铁时代」。"],
         tasks=[checkmark("我已经准备好建造高炉了")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 6), item("tfc:powder/flux", 8), levels(6)])

ch.section("第一节 · 寻铁与火砖", ["start", "melt_iron", "graphite", "kaolinite", "fire_clay", "crucible"])
ch.section("第二节 · 锻铁炉", ["bronze_sheets", "bloomery", "raw_bloom", "stone_anvil2"])
ch.section("第三节 · 锻造锻铁", ["refine_bloom", "wrought_ingot", "wrought_anvil", "iron_pickaxe",
                                "iron_knife_hammer", "iron_armor", "propick_iron"])
ch.section("第四节 · 锻铁的用途", ["iron_lamp", "iron_bars_chain", "iron_tool_molds", "fire_bricks", "finale"])
