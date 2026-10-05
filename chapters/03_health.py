from qlib import *

ch = Chapter("health", "伤病与医疗", icon="firstaid:bandage", group="survival", order=2,
             theme="survival", subtitle="没有完整的身体，就没有明天")

# ============================================================ A · 分部位的生命
ch.quest("start", 1.45, 3.1, "分部位的生命", icon="firstaid:bandage", shape="gear", size=1.5,
         deps=["00_welcome:death"],
         subtitle="头、躯干、四肢与双脚，分别受伤",
         desc=["&o&7「在这片土地上，每一道伤都要分清楚是哪里受的。」&r",
               "",
               "本整合包用 &6First Aid&r 模组取代了原版的单一生命条：你的身体分成",
               "&6头、躯干、左臂、右臂、左腿、右腿、左脚、右脚&r 八个部位，各自有独立的生命值。",
               "",
               "&e查看伤势：&r按 &6Ctrl+H&r 打开身体界面，逐个部位查看血量。",
               "左下角的小人图标（本包使用四色身体显示）也会实时标出受伤部位。",
               "",
               "&a这一章你会学到：&r&6绷带&r与&6夹板&r怎么做、伤到不同部位会怎样、",
               "倒地后如何被救、死亡的代价有多大。先把身体系统弄明白，再去冒险。"],
         tasks=[checkmark("我已经打开过身体界面（Ctrl+H）")],
         rewards=[item("firstaid:bandage", 4), xp(30)])

ch.quest("part_hp", 3.65, 2.1, "各部位能扛多少伤", icon="minecraft:skeleton_skull", deps=["start"],
         desc=["各部位的&6基础血量配置&r不同，躯干较高：",
               "&7- &6头部&r 4 点",
               "&7- &6躯干&r 6 点",
               "&7- &6左臂 / 右臂&r 各 4 点",
               "&7- &6左腿 / 右腿&r 各 4 点",
               "&7- &6左脚 / 右脚&r 各 4 点（在身体界面里和腿分开显示）",
               "",
               "本包开启了&6随玩家最大生命缩放部位血量&r；TFC 营养等因素会影响上限，"
               "实际数值请看身体界面，不要把上面的基础值当成永久上限。",
               "部位受伤会带来&c负面效果&r，例如手臂伤影响挖掘、腿脚伤导致减速；"
               "本整合包关闭了头部与躯干归零直接致死的规则；但&c全身生命耗尽&r仍会进入"
               "&6Hardcore Revival 的昏迷&r状态，见下面「倒地与救援」。",
               "",
               "&a小技巧：&r先看身体界面里的部位血量，优先处理受伤严重的部位。"],
         tasks=[checkmark("我知道八个部位的基础血量与缩放规则")],
         rewards=[item("firstaid:bandage", 4), xp(30)])

ch.quest("fiber2", 3.65, 4.1, "医疗用植物布料", icon="htm:plant_fabric", deps=["start"],
         desc=["工作台制作绷带用的是&6HTM 植物布料&r（htm:plant_fabric），按下面的路线准备：",
               "&7- &6稻草 ×3&r → &6植物线（HTM） ×1&r",
               "&7- &6植物线（HTM） ×4&r → &6植物网 ×1&r",
               "&7- &6植物网 ×2&r → &6植物布料 ×1&r",
               "",
               "&c常见的坑：&r石器时代的&6绿色植物纤维布&r不是这项配方的布料；"
               "绿色植物线也已从普通植物线标签移除，不能替代 HTM 植物线。",
               "",
               "&a建议：&r多备一些纤维布，绷带是消耗品，用起来比想象中快。"],
         tasks=[tag("forge:fabric/fibers", 4, title="植物布料 ×4")],
         rewards=[item("tfc_stone_tools:plant_fiber", 8), xp(20)])

ch.quest("healing_paste", 5.85, 3.1, "愈伤膏", icon="kubejs:healing_paste", deps=["fiber2"], shape="hexagon",
         size=1.25,
         desc=["绷带和夹板的核心原料是&6愈伤膏&r，由四种半成品合成，缺一不可：",
               "",
               "&e1.&r &6蜂蜡&r —— 来自养蜂（见「务农」章节的蜂箱）",
               "&e2.&r &6医用白粉&r —— 白色系草（&7tfc:plant/white&r 标签）配合&6刀&r合成",
               "&e3.&r &6树皮糊&r —— &6树皮 ×2&r + 刀 + &6黏土&r 合成",
               "&e4.&r &6香蒲根切片&r —— &6香蒲根&r配合刀切出",
               "",
               "把这四样放进合成格，一次得到 &62 份愈伤膏&r。",
               "",
               "&a树皮来源：&r手持 TFC 斧&e右键&r原木剥皮可获得对应的&6TFC Debark 树皮&r，"
               "这些树皮属于配方要求的 &6forge:bark&r 标签；具体可用种类按 &eR&r 查看。"],
         tasks=[item("kubejs:healing_paste", 2, title="愈伤膏 ×2")],
         rewards=[item("kubejs:medical_white_powder", 2), xp(40)])

ch.quest("bandage_make", 8.05, 3.1, "缝一卷绷带", icon="firstaid:bandage", deps=["healing_paste"],
         shape="hexagon",
         desc=["&6绷带&r是最常用的医疗品，两种做法都要用到愈伤膏：",
               "",
               "&e配方一（合成台）：&r&6植物布料（HTM） ×2&r + &6愈伤膏 ×1&r → 1 个绷带",
               "&e配方二（缝纫台 + 剪刀）：&r&6布 ×2&r + &6愈伤膏 ×2&r → 8 个绷带，更省愈伤膏",
               "",
               "&e使用方法：&r手持绷带&e右键&r打开治疗界面，选择受伤部位并完成敷用，"
               "每 &618 秒&r恢复 &61 点&r部位生命，总共 &64 次&r（合计 4 点、72 秒）。",
               "",
               "&a小技巧：&r批量做的话配方二（缝纫台）效率更高，适合在家里囤货。"],
         tasks=[item("firstaid:bandage", 4, title="绷带 ×4")],
         rewards=[item("tfc_stone_tools:plant_fiber", 12), xp(40)])

ch.quest("plaster_make", 10.25, 3.1, "敷一块夹板", icon="firstaid:plaster", deps=["bandage_make"],
         desc=["&6夹板（石膏）&r是另一种部位治疗用品，配方产量更高：",
               "",
               "&e配方一（合成台）：&r&6帆布 ×3&r（forge:canvas）+ &6愈伤膏 ×1&r → 3 个夹板",
               "&e配方二（缝纫台 + 剪刀）：&r&6布 ×1&r + &6愈伤膏 ×2&r → 12 个夹板",
               "",
               "本包每 &622 秒&r恢复 &61 点&r部位生命，总共 &62 次&r（合计 2 点、44 秒）。"
               "单个夹板恢复量少于绷带，也不是瞬间回血。",
               "",
               "&a小技巧：&r按部位缺血量选择用品，轻伤用夹板，较重的伤用绷带并留出恢复时间。"],
         tasks=[item("firstaid:plaster", 3, title="夹板 ×3")],
         rewards=[item("kubejs:medical_white_powder", 4), xp(40)])

ch.quest("morphine", 12.45, 3.1, "吗啡：止痛不是万能", icon="firstaid:morphine", deps=["plaster_make"],
         desc=["&6吗啡&r的配方很简单：&6玻璃瓶&r + &62 个发酵蛛眼&r（无序合成）。",
               "",
               "&e效果：&r服用后会&6暂时抑制生命系统带来的负面效果&r（比如伤势导致的减速、虚弱等"
               "debuff 显示），让你能在重伤状态下继续撑一会儿。",
               "",
               "&c注意：&r吗啡&c不会直接回血&r，也不会让伤口消失——它只是让你暂时感觉不到那么痛。"
               "效果过去之后伤势带来的减益会重新出现，仍需用医疗用品恢复部位生命。",
               "",
               "&a建议：&r留给撤退或等待队友支援的紧急时刻，日常小伤用绷带就够了。"],
         tasks=[item("firstaid:morphine", 1, title="吗啡 ×1")],
         rewards=[item("firstaid:bandage", 4), xp(40)])

# ============================================================ B · 倒地与死亡
ch.quest("knockout", 15.775, 2.225, "倒地与救援", icon="minecraft:totem_of_undying", deps=["start"], shape="hexagon", hide_lines=True,
         size=1.25,
         desc=["当你的&c全身生命总值&r降到 0 时，&c不会立即死亡&r，而是进入&6倒地（K.O.）状态&r：",
               "",
               "&7- 倒地后你会倒在地上，&6最长 120 秒&r内有机会被救",
               "&7- &6队友&r靠近到你身边约 &63 格&r以内，&e长按右键 2 秒&r即可把你救起",
               "&7- 倒地期间不能使用弓、无法用拳头攻击",
               "&7- 如果你不想等，可以主动点「&c接受命运&r」直接死亡",
               "",
               "&c致命例外：&r&6掉进岩浆&r会&c瞬间死亡&r，没有倒地环节，无法被救。",
               "",
               "&a单人游戏请格外小心：&r没有队友意味着倒地后大概率只能等死；"
               "尽量在生命值降到危险线之前就用绷带/夹板止损，而不是指望被救。"],
         tasks=[checkmark("我明白倒地和救援的机制")],
         rewards=[item("firstaid:bandage", 6), xp(40)])

ch.quest("death_penalty", 17.975, 2.225, "死亡的代价", icon="minecraft:wither_rose", deps=["knockout"],
         shape="hexagon", size=1.25,
         desc=["如果没能在倒地时被救起（或主动放弃），你会真正死亡并重生。重生时：",
               "",
               "&7- 死亡惩罚配置的重生状态为&6生命 6、饱食度 8/20、口渴度 50/100&r，恢复后请再看身体界面",
               "&7- 短时间内叠加&c口渴、疲惫、失明、恶心、饥饿、黑暗&r等一连串负面效果",
               "&7- 吃 TFC 生肉本身会触发&6食物中毒&r，本包配置为&6饥饿 III，30 秒&r",
               "&7- 身上的物品留在&6尸体&r原地，本包设置了&62 分钟&r尸体交互冷却；安全返回后等待冷却再取回",
               "",
               "&a恢复步骤：&r找个安全地方坐下，先吃东西、喝水，等负面效果慢慢消退，"
               "&c不要带着一身减益继续冒险&r。",
               "",
               "&a营养不会清零：&r本包开启了死亡后保留 TFC 营养，别把重生时的低生命值误当成营养被清空。"],
         tasks=[checkmark("我知道死亡后会付出什么代价")],
         rewards=[item("tfc:food/barley_bread", 6), item("firstaid:bandage", 4), xp(40)])

# ============================================================ C · 预防与恢复
ch.quest("sleep_rest", 1.2, 8.2, "睡眠与恢复", icon="comforts:sleeping_bag_white", deps=["start"], shape="diamond", hide_lines=True,
         optional=True,
         desc=["睡眠能帮助恢复部位生命，本包 First Aid 的睡眠恢复比例配置为 &625%&r。",
               "&6床&r用于设置重生点；&6睡袋&r可用于临时休息，但&c不会替你设置新的重生点&r。",
               "",
               "&a建议：&r基地里放一张可睡眠的床，长途跋涉回来先检查身体界面，再休息和处理伤势。",
               "",
               "&c注意：&r倒地/死亡时离最近的床越近，重生后处境越安全——详见「死亡的代价」。"],
         tasks=[checkmark("我在床或睡袋上睡过一觉")],
         rewards=[item("tfc:thatch", 4), xp(30)])

ch.quest("armor_basic", 3.8, 8.2, "盔甲：减伤才是省医疗包", icon="minecraft:leather_chestplate", deps=["start"], hide_lines=True,
         shape="diamond", optional=True,
         desc=["&6盔甲&r按部位分别减伤：头盔保护头部，胸甲保护躯干，以此类推。",
               "",
               "&e获取路线：&r",
               "&e1.&r 皮甲（鞣制皮革缝制，见「气候与衣物」章节）",
               "&e2.&r 铜甲（见「铜器时代」）",
               "&e3.&r 铁甲、钢甲（见「铁器时代」「钢铁时代」）",
               "",
               "&a小技巧：&r盔甲减少的是「会不会受伤」，绷带夹板处理的是「受伤之后怎么办」——"
               "两者都备齐才是真正的安全。"],
         tasks=[tag("forge:armors/helmets", title="任意头盔")],
         rewards=[item("firstaid:bandage", 3), xp(30)])

ch.quest("falling_damage", 6.4, 8.2, "坠落与腿脚伤势", icon="minecraft:scaffolding", deps=["start"], hide_lines=True,
         desc=["高处坠落是本包里常见的伤势来源，First Aid 的坠落伤害分配主要涉及双脚与双腿。",
               "",
               "&c避免摔伤：&r",
               "&e1.&r 挖矿、建筑时&e留意脚下&r，别靠边缘太近",
               "&e2.&r 需要下降时用&6楼梯、斜坡或脚手架&r逐级下降，而不是直接跳",
               "&e3.&r 意外坠落时尽量&c落入水面&r，水能大幅减轻摔落伤害",
               "",
               "&a小技巧：&r下矿前检查身体界面确认各部位满状态出发，口袋里带够绷带和夹板。"],
         tasks=[checkmark("我会小心脚下，避免坠落")],
         rewards=[item("firstaid:bandage", 6), xp(30)])

ch.quest("dangerous_mobs", 9, 8.2, "危险生物与远离原则", icon="tfc:metal/javelin/copper", deps=["start"], hide_lines=True,
         desc=["世界上有些生物&c不是用来打的&r，是用来躲的：",
               "",
               "&c大型掠食者：&r熊、狮子、老虎、豹等——移动快、伤害高，",
               "正面硬刚大概率是你先见到身体界面全灰。",
               "&c危险小动物：&r蜘蛛、蛇、水虎鱼等体型虽小但同样能造成重伤。",
               "",
               "&a生存法则：&r天黑前回家、不要独自招惹大型掠食者、看到血条告急立即撤退——"
               "一次伤口处理不如一次不受伤。"],
         tasks=[checkmark("我会主动远离危险的生物")],
         rewards=[item("tfc:torch", 8), xp(30)])

# ============================================================ D · 应急准备
ch.quest("medkit_prep", 12.325, 8.575, "准备应急医疗包", icon="firstaid:bandage", deps=["plaster_make"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=["进入任何危险区域前，先把&6应急医疗包&r填满：",
               "",
               "&6清单：&r",
               "&7- &6绷带 ×10~20&r（单个恢复 4 点）",
               "&7- &6夹板 ×3~5&r（单个恢复 2 点）",
               "&7- &6吗啡 ×1~2&r（撤退或等待救援时的保命手段）",
               "&7- 足量&6食物&r（恢复饱食度，顺带帮助回血）",
               "",
               "&a整理建议：&r在基地多囤一批医疗用品留着补货，每次出门前把包裹填满，",
               "长途冒险中途也要记得检查库存。"],
         tasks=[item("firstaid:bandage", 10, title="绷带 ×10"),
                item("firstaid:plaster", 3, title="夹板 ×3")],
         rewards=[item("tfc:food/barley_bread", 6), item("tfc:torch", 16), xp(50)])

ch.quest("finale", 14.525, 8.575, "生命之书", icon="firstaid:plaster", shape="gear", size=1.75, hide_lines=True,
         deps=["medkit_prep", "death_penalty"],
         desc=["&o&7「在群峦之间活下去的秘诀，就是永远比伤口更快一步。」&r",
               "",
               "你现在已经掌握：",
               "&7- &6分部位生命系统&r的运作机制与各部位血量",
               "&7- 从愈伤膏到&6绷带、夹板、吗啡&r的完整制作链",
               "&7- &6倒地与救援&r的规则，以及死亡要付出的真实代价",
               "&7- 用&6睡眠、盔甲、远离危险&r把伤害挡在发生之前",
               "&7- 一份随时能背上就走的&6应急医疗包&r",
               "",
               "&a接下来，&r去「务农」章节学会稳定产出食物，减少冒险时的后顾之忧。"],
         tasks=[checkmark("我已掌握医疗与生存基础")],
         rewards=[item("firstaid:bandage", 12), item("firstaid:plaster", 8), item("firstaid:morphine", 2),
                  xp(100), levels(3)])

ch.section("第一节 · 身体与药箱", ["start", "part_hp", "fiber2", "healing_paste",
                               "bandage_make", "plaster_make", "morphine"])
ch.section("第二节 · 倒地与死亡", ["knockout", "death_penalty"])
ch.section("第三节 · 预防与恢复", ["sleep_rest", "armor_basic", "falling_damage", "dangerous_mobs"])
ch.section("第四节 · 应急准备", ["medkit_prep", "finale"])
