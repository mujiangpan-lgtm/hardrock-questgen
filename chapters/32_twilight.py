from qlib import *

ch = Chapter("twilight", "暮色森林", icon="twilightforest:naga_scale", group="frontier", order=2,
             theme="twilight", subtitle="群星换来钥匙，进度指引森林中的道路")

# ============================================================ A · 水晶与传送门
ch.quest("start", 1.45, 3.1, "来自群星的钥匙", icon="kubejs:magic_crystal", shape="gear", size=1.5,
         deps=["space:finale"], subtitle="先走过星球，再打开森林的门",
         desc=["&o&7「有些门，要用整个工业体系的积累换来钥匙。」&r", "",
               "&6暮色森林&r是一处独立维度。这里的首领、结构与区域保护按&6暮色森林进度页&r推进，遇到魔法屏障时先检查前置进度。",
               "&c本包修改了传送门激活物：&r钻石不再生效，必须使用&6魔法暮色水晶&r。", "",
               "&e材料路线：&r压力室配方需要宝石粉、粗戴斯、粗紫金、粗耐热金属与寒冰碎片，标示压力为 &64.5 bar&r。Ad Astra 的戴斯主要在月球，紫金在火星，耐热金属在金星；寒冰碎片也可从对应星球的寒冰碎片矿取得。",
               "&a操作前：&r按 R 查看水晶的 JEI 配方，核对实际显示的原料和压力，并用压力室接口装卸物品。"],
         tasks=[item("kubejs:magic_crystal", title="魔法暮色水晶")],
         rewards=[item("minecraft:glowstone", 24), xp(300), item("firstaid:bandage", 16), item("tfc:food/cooked_beef", 16)])

ch.quest("portal", 3.65, 3.1, "开门：水与花", icon="tfc:wood/sapling/oak", deps=["start"],
         shape="hexagon", size=1.25,
         desc=["&e1.&r 在&6主世界&r挖一个 &62×2 水池&r，填满水；周围一圈使用泥土或草方块。本包也允许相应的 TFC 泥土、草地与耕地方块作为池岸。",
               "&e2.&r 在&6池岸上&r摆放传送门标签接受的花、树苗等植物。装饰围着水池放，水面留空。",
               "&e3.&r 把&6魔法暮色水晶丢进水里&r，等待传送门激活。", "",
               "&c常见的坑：&r检查水池、池岸和装饰是否完整，并确认使用的是水晶。先在门旁做好标记，再进入森林，方便回程寻找出口。"],
         tasks=[checkmark("我点亮了暮色森林传送门")],
         rewards=[item("minecraft:golden_apple", 4), xp(175), item("minecraft:arrow", 32), item("firstaid:bandage", 8)])

ch.quest("enter", 5.85, 3.1, "踏入浓雾", icon="twilightforest:time_sapling", deps=["portal"],
         shape="hexagon", size=1.25,
         desc=["&o&7「树冠之下，是永远的黄昏。」&r", "",
               "穿过传送门进入&6暮色森林&r。先记录返程门的坐标，带好食物、绷带、照明与备用工具。",
               "&6魔法地图&r可帮助寻找首领结构；迷宫还有专门的迷宫地图。制作方式按 R 查看 JEI。",
               "&a推进方法：&r先找娜迦庭院，再挑战巫妖塔。巫妖之后分成沼泽、黑暗森林与雪原三条路线；森林里的区域保护由游戏进度控制，任务书的解锁不能代替对应进度。",
               "&c战利品：&r本包开启了首领战利品箱。战斗结束后检查生成点附近的箱子，并拾取奖杯。"],
         tasks=[dimension("twilightforest:twilight_forest", title="抵达暮色森林")],
         rewards=[item("firstaid:bandage", 24), item("tfc:food/cooked_beef", 24), xp(400), item("minecraft:arrow", 64)])

ch.quest("moonworm", 8.05, 2.1, "月光蠕虫女王", icon="twilightforest:moonworm_queen", deps=["enter"],
         optional=True, shape="diamond",
         desc=["&6月光蠕虫女王&r是一件照明工具，可在探索大型空心山丘的宝箱时找到。",
               "手持它对方块使用，可以放置会发光的月光蠕虫，沿路留下标记。", "",
               "&a小技巧：&r把标记放在岔路同一侧，回程时更容易辨认。女王工具与放置后的月光蠕虫是两个不同物品，本任务检查的是女王工具。"],
         tasks=[item("twilightforest:moonworm_queen", title="月光蠕虫女王")],
         rewards=[item("minecraft:glowstone_dust", 32), xp(200), item("tfc:food/cooked_beef", 16)])

ch.quest("ore_magnet", 8.05, 4.1, "空心山丘里的矿石磁铁", icon="twilightforest:ore_magnet", deps=["enter"],
         optional=True, shape="diamond",
         desc=["&6矿石磁铁&r可从空心山丘的宝箱中找到，是一件采矿辅助工具。",
               "手持它蓄力使用，能够把探测到的、可移动的矿石拉近地表。", "",
               "&c注意：&r它的识别范围和可移动方块由模组机制与标签决定。先在安全地点试用，别把它当成能搬运所有 TFC 矿脉的通用机器。"],
         tasks=[item("twilightforest:ore_magnet", title="矿石磁铁")],
         rewards=[item("immersivegeology:ingot_titanium", 16), xp(350), item("firstaid:bandage", 12), item("tfc:powder/flux", 32)])

# ============================================================ B · 娜迦、巫妖与沼泽
ch.quest("naga_courtyard", 11.25, 2.225, "娜迦庭院", icon="twilightforest:naga_scale",
         deps=["enter"], hide_lines=True,
         desc=["首领路线从&6娜迦庭院&r开始。寻找四周有石墙、内部开阔的庭院。",
               "&6娜迦&r是一条身体分节的巨蛇，会冲撞并破坏场地。留出移动空间，观察冲锋间隙再进攻。", "",
               "战利品包含&6娜迦鳞片&r与奖杯，鳞片可以制作相应胸甲和护腿。",
               "&a下一步：&r确认暮色进度页中的娜迦进度已完成，再前往巫妖塔。"],
         tasks=[advancement("twilightforest:progress_naga", title="完成娜迦进度")],
         rewards=[item("minecraft:arrow", 64), xp(700), item("minecraft:golden_apple", 6), item("tfc:metal/ingot/copper", 48), item("firstaid:bandage", 16)])

ch.quest("lich_tower", 11.25, 4.225, "巫妖塔", icon="twilightforest:lich_trophy", deps=["naga_courtyard"],
         desc=["完成娜迦进度后，探索&6巫妖塔&r并到达塔顶。", "",
               "&6巫妖&r的战斗分阶段进行：护盾阶段要把它射出的可反弹魔法弹打回去；随后处理召唤物，再完成最后的近战阶段。",
               "战利品包括&6权杖&r与&6巫妖奖杯&r。拾取后检查进度页，之后沼泽、黑暗森林和雪原三路可以分别推进。",
               "&c常见的坑：&r有护盾时一味近身砍击无效。留意真正的巫妖与它的分身。"],
         tasks=[advancement("twilightforest:progress_lich", title="完成巫妖进度")],
         rewards=[item("minecraft:golden_apple", 8), xp(900), item("tfc:gem/diamond", 8), item("firstaid:bandage", 16), item("firstaid:morphine", 4)])

ch.quest("labyrinth", 13.45, 4.225, "迷宫与米诺菇", icon="twilightforest:minoshroom_trophy", deps=["lich_tower"],
         desc=["在暮色沼泽寻找&6地下迷宫&r，沿路做好标记，深入第二层寻找&6米诺菇&r。",
               "它的战利品包括&6牛头人沙拉酱肉&r、钻石米诺陶战斧和奖杯。", "",
               "&e关键动作：&r击败米诺菇后，&6吃下牛头人沙拉酱肉&r，完成对应迷宫进度。这是解除火焰沼泽保护、继续挑战九头蛇的门槛。",
               "&c常见的坑：&r只拿奖杯还不够。若火焰沼泽仍阻止进入，先查看是否完成了吃肉的进度。"],
         tasks=[kill("twilightforest:minoshroom", 1, title="击败米诺菇"),
                advancement("twilightforest:progress_labyrinth", title="吃下牛头人沙拉酱肉并完成进度")],
         rewards=[item("minecraft:glowstone", 32), item("firstaid:bandage", 24), xp(900), item("tfc:food/cooked_beef", 32), item("immersivegeology:ingot_hastelloy", 16)])

ch.quest("hydra_lair", 13.45, 2.225, "火焰沼泽：九头蛇", icon="twilightforest:hydra_trophy", deps=["labyrinth"],
         shape="hexagon", size=1.25,
         desc=["完成迷宫进度后，进入&6火焰沼泽&r，寻找地表的&6九头蛇巢穴&r。",
               "&6九头蛇&r会喷火、吐出爆炸攻击并咬击。观察各个头部的动作，避开攻击再寻找反击机会。", "",
               "战利品包括&6炽热血液&r、九头蛇肉排与奖杯；炽热血液可参与制作炽铁锭。",
               "&a下一步：&r九头蛇是通往高地的三条首领路线之一，还需要暮初恶魂与冰雪女王的进度。"],
         tasks=[advancement("twilightforest:progress_hydra", title="完成九头蛇进度")],
         rewards=[item("tfc:food/cooked_beef", 32), xp(1250), item("minecraft:golden_apple", 8), item("immersivegeology:ingot_titanium", 32), item("firstaid:bandage", 24)])

# ============================================================ C · 装备与黑暗森林
ch.quest("ironwood_gear", 1.2, 9.325, "铁木与钢叶装备", icon="twilightforest:ironwood_sword",
         deps=["enter"], hide_lines=True, optional=True, shape="diamond",
         desc=["&6铁木&r的材料路线与地下的&6活根&r有关。JEI 中可以查看活根、铁与金参与的制作路线；本包还增加了电弧炉处理活根的配方。",
               "&6钢叶&r可在迷宫与空心山丘等结构的宝箱中找到，再制作对应装备。", "",
               "迷宫宝箱本身也有机会出现铁木剑、钢叶镐等成品，可以边探索边收集。",
               "&a小技巧：&r先查成品的 R 配方和材料的 U 用途，选择已有设备能完成的路线。"],
         tasks=[item("twilightforest:ironwood_sword", title="铁木剑"), item("twilightforest:steeleaf_pickaxe", title="钢叶镐")],
         rewards=[item("tfc:metal/ingot/nickel", 24), xp(450), item("tfc:metal/ingot/copper", 32), item("tfc:powder/flux", 32)])

ch.quest("trophy_room", 3.4, 8.325, "奖杯基座：打开要塞", icon="twilightforest:trophy_pedestal",
         deps=["lich_tower"], hide_lines=True,
         desc=["完成巫妖进度后，在&6黑暗森林&r寻找&6地精骑士要塞&r入口。",
               "把已获得的首领奖杯放上入口的&6奖杯基座&r，完成基座进度并打开要塞通道。", "",
               "&a收藏：&r娜迦、巫妖等首领奖杯也可带回基地展示。推进路线时先留好能用于入口基座的奖杯。",
               "&c常见的坑：&r在家里摆一排奖杯不等于已解开要塞入口。以暮色进度页的基座进度为准。"],
         tasks=[advancement("twilightforest:progress_trophy_pedestal", title="在奖杯基座上放置奖杯并完成进度")],
         rewards=[item("minecraft:glowstone", 32), xp(300), item("minecraft:arrow", 48), item("firstaid:bandage", 12)])

ch.quest("knight_stronghold", 5.6, 9.325, "地精骑士要塞：幻影骑士", icon="twilightforest:knight_phantom_trophy",
         deps=["trophy_room"], shape="hexagon", size=1.25,
         desc=["进入黑暗森林地下的&6地精骑士要塞&r，探索至首领房间，挑战一组&6幻影骑士&r。",
               "&e目标：&r完成整场战斗，再检查首领战利品箱与暮色进度页。击败其中一名骑士还不算走完这条路线。", "",
               "首领箱提供骑士金属武器与幻影装备等奖励。普通要塞敌人还会提供&6盔甲碎片&r，可以制作碎片簇；本包加入了碎片簇配合金粒的电弧炉骑士金属配方。",
               "&a下一步：&r幻影骑士进度解锁黑暗高塔的后续挑战。"],
         tasks=[advancement("twilightforest:progress_knights", title="完成幻影骑士进度")],
         rewards=[item("immersivegeology:ingot_hastelloy", 32), xp(1250), item("immersivegeology:ingot_titanium", 24), item("firstaid:bandage", 24), item("minecraft:golden_apple", 8)])

ch.quest("ur_ghast", 7.8, 9.325, "黑暗高塔：暮初恶魂", icon="twilightforest:ur_ghast_trophy",
         deps=["knight_stronghold"], shape="hexagon", size=1.25,
         desc=["完成幻影骑士进度后攀登&6黑暗高塔&r，塔顶的&6暮初恶魂&r是这条路线的首领。",
               "留意塔内机关与&6恶魂陷阱&r，观察它们在战斗中的作用，同时躲避火球与小恶魂。", "",
               "首领战利品包含&6炽热之泪&r、&6砷铅铁&r与奖杯。炽热之泪可参与制作炽铁锭，砷铅铁用于暮色森林的机关材料。",
               "&a下一步：&r确认暮初恶魂进度完成；它与九头蛇、冰雪女王共同构成高地的前置。"],
         tasks=[advancement("twilightforest:progress_ur_ghast", title="完成暮初恶魂进度")],
         rewards=[item("tfc:gem/diamond", 12), xp(1500), item("immersivegeology:ingot_hastelloy", 32), item("firstaid:bandage", 24), item("firstaid:morphine", 6)])

# ============================================================ D · 雪原与战利品
ch.quest("yeti_glacier", 11, 9.575, "雪原洞穴：雪怪首领", icon="twilightforest:alpha_yeti_trophy",
         deps=["lich_tower"], hide_lines=True,
         desc=["完成巫妖进度后，探索&6雪原&r中的雪怪洞穴，挑战&6雪怪首领&r。",
               "它会投掷冰块、抓取玩家，并让洞穴中的冰块坠落。保持移动，留意头顶与脚下。", "",
               "战利品包括&6雪怪首领毛皮&r、冰炸弹与奖杯。毛皮用于&6雪怪系列装备&r，具体效果查看物品提示。",
               "&a下一步：&r完成雪怪进度后，继续寻找冰川上的极光宫殿。"],
         tasks=[advancement("twilightforest:progress_yeti", title="完成雪怪首领进度")],
         rewards=[item("tfc:food/cooked_beef", 32), xp(1000), item("firstaid:bandage", 24), item("tfc:metal/ingot/nickel", 32), item("minecraft:golden_apple", 8)])

ch.quest("snow_queen", 13.2, 9.575, "极光宫殿：冰雪女王", icon="twilightforest:snow_queen_trophy",
         deps=["yeti_glacier"], shape="hexagon", size=1.5,
         desc=["在冰川上找到&6极光宫殿&r，沿内部通道登高，寻找&6冰雪女王&r。",
               "她会召唤冰晶、俯冲并以冰束攻击。观察阶段变化，带好远程武器与治疗物资。", "",
               "战利品包括奖杯，以及&6追踪弓或三发弓&r。拾取后确认冰川进度已完成。",
               "&a下一步：&r九头蛇、暮初恶魂、冰雪女王三条路线汇合后，才能继续高地的巨人与巨魔洞窟。"],
         tasks=[advancement("twilightforest:progress_glacier", title="完成冰雪女王进度")],
         rewards=[item("minecraft:golden_apple", 12), xp(1500), item("tfc:gem/diamond", 12), item("immersivegeology:ingot_titanium", 32), item("firstaid:bandage", 24)])

ch.quest("hunting_gear", 15.4, 8.575, "追踪弓与三发弓", icon="twilightforest:seeker_bow",
         deps=["snow_queen"], optional=True, shape="diamond",
         desc=["冰雪女王的战利品里有&6追踪弓与三发弓&r两种特殊远程武器，值得收集并试用。",
               "&7- 追踪弓：射出的箭具有追踪能力。", "&7- 三发弓：一次射出多支箭。", "",
               "&a探索工具：&r渡鸦羽毛的另一项用途是合成&6魔法地图核心&r，配合火炬浆果与荧石粉，帮助制作森林探索所需的魔法地图。详细配方按 R 查看。"],
         tasks=[item("twilightforest:seeker_bow", title="追踪弓")],
         rewards=[item("minecraft:arrow", 64), xp(450), item("minecraft:golden_apple", 4), item("firstaid:bandage", 12)])

ch.quest("fiery_realm", 15.4, 10.575, "炽铁：血液与眼泪", icon="twilightforest:fiery_ingot",
         deps=["hydra_lair", "ur_ghast"], any_dep=True, hide_lines=True, optional=True, shape="diamond",
         desc=["&6炽铁&r的原料来自首领：九头蛇提供&6炽热血液&r，暮初恶魂提供&6炽热之泪&r。",
               "这些材料与铁锭可制作&6炽铁锭&r，再加工成暮色装备。", "",
               "&e做法：&r按 R 查看炽铁锭，再查看目标装备的配方。本包替换了部分炽铁装备配方，制作时以当前 JEI 显示的材料为准。",
               "&a建议：&r先保留一批首领原料，确认想做的装备再加工，避免把战利品全部消耗掉。"],
         tasks=[item("twilightforest:fiery_ingot", 4, title="炽铁锭 ×4")],
         rewards=[item("tfc:metal/ingot/nickel", 24), xp(600), item("tfc:metal/ingot/copper", 32), item("tfc:powder/flux", 48)])

# ============================================================ E · 高地与余烬之灯
ch.quest("giant_ruins", 18.6, 9.575, "高地云端的巨人", icon="twilightforest:giant_pickaxe",
         deps=["hydra_lair", "ur_ghast", "snow_queen"], hide_lines=True, shape="hexagon", size=1.25,
         desc=["完成九头蛇、暮初恶魂与冰雪女王三路进度后，前往&6高地&r。",
               "探索巨魔洞窟寻找&6魔豆&r，在肥沃土上种出豆茎，登上云层中的巨人区域。", "",
               "&6巨人矿工&r的战利品是&6巨人镐&r，装甲巨人则提供巨人剑。巨人镐用于处理巨型方块，也是打开巨魔宝库的重要工具。",
               "&a下一步：&r带着巨人镐回到高地洞窟，寻找用巨型黑曜石封住的宝库。"],
         tasks=[item("twilightforest:giant_pickaxe", title="巨人镐")],
         rewards=[item("immersivegeology:ingot_titanium", 32), xp(1200), item("immersivegeology:ingot_hastelloy", 24), item("firstaid:bandage", 24), item("firstaid:morphine", 4)])

ch.quest("lamp_of_cinders", 20.8, 9.575, "巨魔宝库：余烬之灯", icon="twilightforest:lamp_of_cinders",
         deps=["giant_ruins"], shape="hexagon", size=1.25,
         desc=["&6余烬之灯&r藏在&6高地巨魔洞窟的宝库&r中。带着巨人镐打开巨型黑曜石封存的宝库，检查宝箱，寻找灯。", "",
               "&e用途：&r使用余烬之灯烧掉&6荆棘&r，继续前往荆棘高地。拿到灯后检查暮色进度页中的巨魔进度。",
               "&c常见的坑：&r直接砍荆棘会妨碍通行。先取得灯，再按它的用途清理道路。"],
         tasks=[item("twilightforest:lamp_of_cinders", title="余烬之灯")],
         rewards=[item("tfc:gem/diamond", 16), xp(1500), item("minecraft:golden_apple", 12), item("firstaid:bandage", 32), item("minecraft:glowstone", 32)])

ch.quest("finale", 23, 9.575, "暮色加冕", icon="twilightforest:knightmetal_sword", deps=["lamp_of_cinders"],
         shape="gear", size=1.75, subtitle="三路首领汇合，灯火照亮高地的道路",
         desc=["&o&7「从水池边的第一颗水晶，到荆棘前的一盏灯。」&r", "",
               "你已经走过娜迦与巫妖，完成沼泽、黑暗森林和雪原三条路线，并从高地宝库取得余烬之灯。",
               "&a后续：&r继续探索荆棘高地、更多遗迹与宝箱，收集不同装备和装饰。本章记录的是当前版本可完成的主要首领路线，森林里仍有许多值得寻找的细节。",
               "&c若本任务没有完成：&r打开暮色森林进度页，检查九头蛇、暮初恶魂、冰雪女王与巨魔进度，确认三路前置和余烬之灯均已被游戏识别。"],
         tasks=[advancement("twilightforest:progress_troll", title="完成余烬之灯与高地的进度")],
         rewards=[item("tfc:gem/diamond", 24), item("tfc:gem/emerald", 32), levels(30), item("immersivegeology:ingot_titanium", 48), item("immersivegeology:ingot_hastelloy", 48), item("minecraft:golden_apple", 16)])

ch.section("第一节 · 水晶与传送门", ["start", "portal", "enter", "moonworm", "ore_magnet"])
ch.section("第二节 · 娜迦、巫妖与沼泽", ["naga_courtyard", "lich_tower", "labyrinth", "hydra_lair"])
ch.section("第三节 · 装备与黑暗森林", ["ironwood_gear", "trophy_room", "knight_stronghold", "ur_ghast"])
ch.section("第四节 · 雪原与战利品", ["yeti_glacier", "snow_queen", "hunting_gear", "fiery_realm"])
ch.section("第五节 · 高地与余烬之灯", ["giant_ruins", "lamp_of_cinders", "finale"])
