from qlib import *

ch = Chapter("climate", "气候与衣物", icon="cold_sweat:thermometer", group="survival", order=0,
             theme="survival", subtitle="寒来暑往，衣不蔽体者先亡")

# ============================================================ A · 读懂体温
ch.quest("start", 0, 0, "你的体温", icon="cold_sweat:thermometer", shape="gear", size=1.5,
         deps=["00_welcome:hud"],
         subtitle="冷热都会杀死你",
         desc=["&o&7「群峦不欢迎衣衫单薄的旅人。」&r",
               "",
               "本整合包用 &6Cold Sweat&r 模组模拟体温。快捷栏旁边的&6小人图标&r显示你的体温状态：",
               "&7- &9偏蓝&r —— 正在失温，体温过低会持续受伤甚至致命",
               "&7- &e偏黄 / &c偏红&r —— 正在过热，中暑同样危险",
               "&7- 不显色 —— 体温正常，安全区间",
               "",
               "影响体温的因素：&6气温（季节+时间+生物群系+海拔）&r、&6是否被淋湿&r、&6靠近热源/冷源&r、"
               "&6身上的衣物&r、&6是否在室内&r。",
               "",
               "&e完成方式：&r找到体温指示、读懂冷热提示后，点击下方的勾选任务确认；&a开局不需要制作温度计&r。",
               "&a进阶工具：&r实体&6温度计&r可显示精确的&6环境温度与体温&r数值。它需要金片与红石粉，"
               "进入金属加工阶段后再按 JEI 配方制作，放进&6快捷栏、副手或 Curios 饰品栏&r使用即可。"],
         tasks=[checkmark("我已找到体温指示并读懂冷热提示")],
         rewards=[item("cold_sweat:waterskin"), xp(30)])

ch.quest("seasons", 2, -1.5, "季节与纬度", icon="firmaciv:sextant", deps=["start"],
         desc=["TFC 的世界有真实的&6四季&r与&6气候带&r：",
               "&7- 季节影响温度曲线，也决定哪些作物、果树能生长、动物能繁殖",
               "&7- 纬度（南北位置）决定你所在气候带的冷暖基调 —— 越靠近两极越冷",
               "&7- 海拔越高越冷，深入地下反而相对恒温",
               "",
               "&e查看方法：&r打开物品栏上方的&6气候标签页&r查看当前季节与平均气温；"
               "&6六分仪&r（探索章节）可以测量纬度。",
               "",
               "&a游戏从夏初开始&r——第一年看起来很暖和，但冬天比想象中来得快，务必提前准备。"],
         tasks=[checkmark("我知道去哪查看气候信息了")],
         rewards=[xp(30)])

ch.quest("shelter_warm", 2, 1.5, "室内更暖和", icon="tfc:thatch", deps=["start"],
         desc=["&6待在室内&r（有顶、三面以上有墙的封闭空间）能显著减缓体温流失，比露天扛风雪划算得多。",
               "",
               "&6热源&r同样重要：",
               "&7- 篝火、壁炉在附近就能取暖，是最早也最可靠的热源",
               "&7- 岩浆是更强力的热源，冬天靠着它过夜很有效，但别离太近烧伤自己",
               "",
               "&c常见的坑：&r四面透风的茅草棚几乎没有保温效果，入冬前至少砌起墙和屋顶。"],
         tasks=[checkmark("我有一个能挡风的屋子")],
         rewards=[item("tfc:thatch", 8), xp(30)])

ch.quest("wet", 4, 0, "淋湿与寒风", icon="minecraft:water_bucket", deps=["seasons", "shelter_warm"], any_dep=True,
         desc=["&c身上淋湿会大幅加快失温&r，下雨、游泳、瀑布都会让你变湿。",
               "",
               "&e应对：&r",
               "&7- 尽快找屋檐或洞穴躲雨，靠近火源可以烘干衣物",
               "&7- 恶劣天气（暴雨、暴雪）出门前先检查天气预报",
               "&7- 湿透的状态下别在暴雪夜出门"],
         tasks=[checkmark("下雨时我会找地方躲雨")],
         rewards=[item("firstaid:bandage", 2), xp(20)])
# ============================================================ B · 保暖衣物
ch.quest("plant_recap", 7, 0, "起步：植物衣物", icon="tfc_stone_tools:plant_chestplate", deps=["wet"],
         desc=["石器时代做的&6植物衣物&r（稻草+纤维缝制）聊胜于无，保暖性很差，&c撑不过真正的寒冬&r。",
               "",
               "把它们当作&6衣物的骨架&r：之后可以在&6缝纫台&r上给它们加装保暖材料，不必推倒重做。"],
         tasks=[checkmark("我已经有一套基础衣物（植物/麻布/皮革）")],
         rewards=[item("tfc_stone_tools:plant_string", 8), xp(20)])

ch.quest("hides_leather", 9, -1.5, "鞣制：生皮到皮革", icon="minecraft:leather", deps=["plant_recap"],
         desc=["狩猎得到的&6生皮&r需要在木桶里浸泡、刮制、鞣制才能变成&6皮革&r，"
               "完整流程见「铜器时代」（需要木桶）。",
               "",
               "皮革可以做出皮甲，是比植物衣物更好的基础衣物，之后还能在缝纫台上继续加装保暖部件。",
               "",
               "&a提示：&r大型生皮产量稀少，优先用在衣物和床上。"],
         tasks=[item("minecraft:leather", 4, title="皮革 ×4")],
         rewards=[item("firstaid:bandage", 2), xp(30)])

ch.quest("wool", 9, 1.5, "羊毛与羊毛布", icon="tfc:wool_cloth", deps=["plant_recap"],
         desc=["&6剪羊毛&r（剪刀右键羊、羊驼等）得到&6羊毛&r，纺成&6羊毛布&r后可以缝出整套保暖衣物，"
               "也是缝纫台上最常见的&6保暖部件&r之一。",
               "",
               "&e来源：&r驯养绵羊/羊驼（见「务农」章节的畜牧部分），或猎杀野生个体直接获取羊毛。",
               "",
               "&a小技巧：&r定期剪毛不会伤害动物，驯养一群羊是稳定保暖材料的来源。"],
         tasks=[item("tfc:wool_cloth", 4, title="羊毛布 ×4")],
         rewards=[item("tfc:wool", 4), xp(30)])

ch.quest("fur_hunt", 11, -1.5, "毛皮猎手", icon="cold_sweat:goat_fur", deps=["hides_leather"],
         desc=["&6山羊毛皮&r（猎杀山羊获得）可以直接合成一整套&6毛皮大衣&r：帽/衣/裤/靴，"
               "是前期获取门槛最低、保暖效果拔群的御寒装备。",
               "",
               "&e其他毛皮：&r熊、狮、虎、冰原狼、驯鹿等猛兽会掉落各自的&6毛皮&r，"
               "&e毛皮 + 刀&r无序合成可以得到一张&6大型生皮&r，是稳定的大生皮来源。",
               "",
               "&c警告：&r熊、狼、狮、虎等毛皮主人同时也是危险掠食者，狩猎前备好标枪或更好的武器，别单挑。"],
         tasks=[item("cold_sweat:goat_fur_chestplate", title="毛皮大衣"),
                item("cold_sweat:goat_fur_helmet", title="毛皮帽"),
                item("cold_sweat:goat_fur_leggings", title="毛皮裤"),
                item("cold_sweat:goat_fur_boots", title="毛皮靴")],
         rewards=[item("firstaid:bandage", 2), xp(50)])

ch.quest("sewing_table", 13, 0, "缝纫台：改造衣物", icon="cold_sweat:sewing_table", deps=["wool", "fur_hunt"],
         shape="hexagon", size=1.25,
         desc=["&6缝纫台&r（本整合包为 Cold Sweat 的特制裁缝台，木制缝纫桌也可用）是衣物系统的核心："
               "&e把一件衣物 + 一个保暖/降温部件放进去&r，就能把部件的属性&6附加&r到那件衣物上，"
               "而不必整件衣服重做。",
               "",
               "&e保暖部件（&9hardrock:cold_insulator&r）：&r羊毛、羊毛布、棉布、原始保暖夹层、山羊毛皮等",
               "&e降温部件（&9hardrock:warm_insulator&r）：&r亚麻布、丝绸、黏土、耐火泥、疣猪兽皮等",
               "{@pagebreak}",
               "&a实用技巧：&r",
               "&7- 一件衣服能加装的部件数量有限，悬停衣物可查看当前保暖值与剩余槽位",
               "&7- 想拆下部件？&e用剪刀右键&r这件衣物即可取下，不会损坏衣物本体",
               "&7- 毛皮/羊毛类装备本身自带保暖，无需额外再缝一层，省下材料给别的衣物"],
         tasks=[item("cold_sweat:sewing_table", title="缝纫台")],
         rewards=[item("tfc:wool_cloth", 4), xp(40)])

ch.quest("winter_ready", 15.25, 0, "入冬检查清单", icon="cold_sweat:goat_fur_chestplate", deps=["sewing_table"],
         shape="hexagon",
         desc=["&c入冬前的最后检查：&r",
               "&e1.&r 四个部位（头/身/腿/脚）都有保暖衣物，没有裸露部位",
               "&e2.&r 至少一件衣物在缝纫台加过保暖部件，双重保险",
               "&e3.&r 家里有篝火或壁炉，墙壁屋顶封闭完整",
               "&e4.&r 根据体温图标观察冷热变化；有&6温度计&r后可辅助查看&6环境温度&r",
               "",
               "&a小技巧：&r体温刚开始发蓝时及时处理（加衣服/靠近火），别等到饥饿值和生命值一起往下掉。"],
         tasks=[checkmark("我已经准备好过冬了")],
         rewards=[item("tfc:food/barley_bread", 6), item("tfc:powder/salt", 4), xp(40)])
# ============================================================ C · 酷热与特殊环境
ch.quest("heat_cooling", 6.5, 6.5, "酷暑降温", icon="minecraft:ice", deps=["wet"], hide_lines=True,
         desc=["夏天、沙漠、靠近熔炉和岩浆都会让你&c过热&r，图标变黄甚至变红就要注意了。",
               "",
               "&e降温手段：&r",
               "&7- 跳进水里，或躲进阴凉的室内、地下",
               "&7- 远离篝火、熔炉等热源",
               "&7- 在缝纫台给衣物缝上降温部件（亚麻布、丝绸、黏土……见「缝纫台」任务）",
               "",
               "&a提示：&r别只准备保暖不准备降温，炎热的沙漠和夏季同样会要命。"],
         tasks=[checkmark("我知道怎么应对过热了")],
         rewards=[item("tfc:food/barley_bread", 4), xp(20)])

ch.quest("waterskin", 8.5, 6.5, "水袋：随身调温", icon="cold_sweat:waterskin", deps=["heat_cooling"],
         desc=["&6水袋&r（起步奖励已发放）在水源处&e右键&r装水，可以随身带着走。",
               "",
               "装满的水袋有自己的&6水温&r，会慢慢趋向周围环境温度。"
               "&e使用水袋&r会把水浇在自己身上：&6冷水&r帮你降温，&6热水&r帮你暖身。"
               "具体效果悬停水袋查看。",
               "",
               "&c注意：&r生水要煮沸后才能安全饮用（见「生存之道 · 饮水与食物」）。"],
         tasks=[item("cold_sweat:waterskin", title="水袋")],
         rewards=[item("cold_sweat:waterskin"), xp(30)])

ch.quest("nether_end", 10.5, 6.5, "下界的酷热", icon="cold_sweat:soulspring_lamp", deps=["waterskin"],
         optional=True, shape="diamond",
         desc=["下界环境酷热，会持续让你&c过热&r。",
               "",
               "&e应对：&r",
               "&7- 出发前把衣物换成&6降温&r组合（缝纫台加装降温部件）",
               "&7- 携带&6灵魂泉灯&r，以&6灵魂嫩芽&r为燃料，可以在炎热环境中为你降温（悬停查看）"],
         tasks=[item("cold_sweat:soulspring_lamp", title="灵魂泉灯")],
         rewards=[item("cold_sweat:soul_sprout", 4), xp(30)])
# ============================================================ D · 极端天气
ch.quest("weather_hazard", 0, 6.5, "风暴与龙卷风", icon="weather2:tornado_siren", deps=["start"], hide_lines=True,
         shape="hexagon",
         desc=["这个世界的天气&c不只是降雨降雪&r——某些生物群系会刮起&c龙卷风&r，威力足以掀掉木屋、"
               "卷走未固定的掉落物甚至生物。",
               "",
               "&e预警手段：&r",
               "&7- &6龙卷风传感器&r：探测附近是否正在形成龙卷风",
               "&7- &6天气警报器&r：探测到危险天气后发出警报音，提醒及时避险",
               "&7- &6风速计 / 风向标&r：辅助判断风力和风向",
               "",
               "&c警告：&r茅草屋、单层木板屋在龙卷风面前基本是纸糊的，第一年内尽快换成&6石头或砖&r建筑。",
               "",
               "&8本节不挡主线：警报器要用&6铸铁棒&8和工业警报器，天气预报要用铁、金、红石和指南针，"
               "都是铁器时代以后的东西。先记住避险要点，到时候再回来做。"],
         tasks=[item("weather2:tornado_siren", title="天气警报器")],
         rewards=[item("weather2:tornado_sensor"), xp(40)])

ch.quest("storm_shelter", 2.5, 6.5, "避难所与天气预报", icon="weather2:weather_forecast", deps=["weather_hazard"],
         desc=["&6天气预报&r可以提前查看未来一段时间的天气趋势，远行、出海、下矿前看一眼能避免很多麻烦。",
               "",
               "&e安全屋要点：&r",
               "&7- 石质或砖质结构，墙体厚实、顶部封闭",
               "&7- 半地下或地下室天然免疫龙卷风，是最可靠的避难选择",
               "&7- 贵重物品、矿车、未固定的方块在风暴中可能被卷走或损坏，收好或加固"],
         tasks=[item("weather2:weather_forecast", title="天气预报")],
         rewards=[item("tfc:food/barley_bread", 4), xp(30)])
# ============================================================ E · 心智
ch.quest("sanity", 16.5, 6.5, "理智：别在黑暗中太久", icon="sanitydim:garland", deps=["finale"], optional=True,
         shape="diamond",
         desc=["本整合包有&6理智&r系统（Sanity: Descent Into Madness），HUD 上的大脑图标就是你的理智值。",
               "",
               "&c降低理智：&r长时间待在黑暗中、怪物在附近、受伤、长期不睡觉等",
               "&a恢复理智：&r睡觉、待在光亮处、佩戴&6花冠&r（悬停查看效果）等",
               "",
               "&c常见的坑：&r理智过低会出现幻觉和负面效果。基地里多插火把，别黑灯瞎火地过夜。"],
         tasks=[item("sanitydim:garland", title="花冠")],
         rewards=[item("tfc:torch", 8), xp(30)])

ch.quest("finale", 14, 6.5, "四季轮回，心中有数", icon="cold_sweat:goat_fur_chestplate", deps=["winter_ready"],
         hide_lines=True, shape="gear", size=1.75,
         subtitle="活下来，才有下一步",
         desc=["&o&7「衣能遮体，火能驱寒，而真正让人活下去的，是提前的准备。」&r",
               "",
               "你现在应该已经：&a能看懂体温与理智指示&r、&a有一套应对冬夏的衣物&r、"
               "&a知道风暴来临前该往哪躲&r。",
               "",
               "剩下的生存要素——饮水、食物保存、医疗、农业——分别在&6生存之道&r的后续章节"
               "和&6务农&r章节详述。&a下一步：确保吃饱喝好，别让体温之外的东西先倒下。&r"],
         tasks=[checkmark("我已准备好面对群峦的四季")],
         rewards=[item("cold_sweat:waterskin"), item("firstaid:bandage", 4), levels(5)])

ch.section("第一节 · 读懂体温", ["start", "seasons", "shelter_warm", "wet"])
ch.section("第二节 · 保暖衣物", ["plant_recap", "hides_leather", "wool", "fur_hunt", "sewing_table", "winter_ready"])
ch.section("第四节 · 酷热与特殊环境", ["heat_cooling", "waterskin", "nether_end"])
ch.section("第三节 · 极端天气", ["weather_hazard", "storm_shelter"])
ch.section("第五节 · 四季轮回", ["sanity", "finale"])
