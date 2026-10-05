from qlib import *

ch = Chapter("00_welcome", "启程指南", icon="akashictome:tome", group="", order=0,
             theme="guide", subtitle="在群峦之间活下去，从读懂这本书开始")

ch.quest("welcome", 0, 0, "欢迎来到群峦", icon="ftbquests:book", shape="gear", size=2.0,
         subtitle="点我开始",
         desc=["&o&7「这片土地不欢迎冒失的旅人。」&r",
               "",
               "这是一个以 &6TerraFirmaCraft&r 为核心、极度写实的生存整合包。没有工作台上的一键合成，没有熔炉里的魔法冶炼："
               "你需要亲手&6敲打石头&r、&6烧制陶器&r、&6熔炼矿石&r，一步步从石器时代走到星辰大海。",
               "",
               "这本任务书就是你的&e生存手册&r。每个任务都会告诉你：&a做什么&r、&a为什么&r、&a怎么做&r，以及&c常见的坑&r。",
               "{@pagebreak}",
               "&l&6阅读图例&r",
               "&e◆ 齿轮 / 大图标&r —— 主线里程碑，完成后会开启新的章节或阶段",
               "&e● 圆形&r —— 普通任务，按顺序推进即可",
               "&e◇ 菱形（可选）&r —— 支线 / 知识点，不影响主线",
               "",
               "按 &6快捷键&r（默认在 选项 → 控制 → 按键绑定 → FTB 任务书）可以随时打开本书，不必一直带着任务书。",
               "完成任务后请记得&a点击领取奖励&r：奖励&e不会自动发放&r。多人游戏时奖励以队伍为单位发放。"],
         tasks=[checkmark("我已准备好")],
         rewards=[item("tfc:food/barley_bread", 8), item("firstaid:bandage", 2), xp(50)])

ch.quest("tome", -3, -2, "阿卡什宝典", icon="akashictome:tome", deps=["welcome"],
         desc=["开局物品栏里那本厚重的书就是&6阿卡什宝典&r，它把整合包里所有说明书合并成了一本：",
               "&7- &6TFC 野外指南&r（最重要！）",
               "&7- 工程师手册、气动工艺书、安全工艺指南、食物清单……",
               "",
               "&a用法：&r手持宝典&e右键&r打开选择界面，点选你要的书即可变形为那本书；变形后&e潜行+左键空气&r可变回宝典。",
               "",
               "&c弄丢了？&r在 JEI 中搜索「阿卡什宝典」查看配方，或领取本任务奖励的备用本。"],
         tasks=[item("akashictome:tome", title="阿卡什宝典")],
         rewards=[item("akashictome:tome")])

ch.quest("field_guide", -5, -2, "TFC 野外指南", icon="patchouli:guide_book", deps=["tome"], size=1.25,
         desc=["&6野外指南&r是这个世界的百科全书。它的内容随你的进度解锁，涵盖：",
               "&7- 世界生成、岩层、气候与季节",
               "&7- 石器塑形、陶器、冶金、锻造、焊接",
               "&7- 农业、食物腐烂与保存、动物养殖",
               "",
               "&a小技巧：&r也可以在物品栏右侧的&6标签页&r直接打开它，不需要手持书本。",
               "本任务书的很多任务会写「见野外指南的 XX 条目」，遇到不懂的机制先查这里。"],
         tasks=[checkmark("我知道去哪里查资料了")],
         rewards=[xp(30)])

ch.quest("jei", -3, 0, "JEI：你的配方百科", icon="minecraft:knowledge_book", deps=["welcome"],
         desc=["屏幕右侧的物品列表是 &6JEI&r。本整合包大量修改了配方，&c请不要凭原版经验合成&r。",
               "",
               "&e鼠标悬停物品后：&r",
               "&7- &6R&r 查看它的配方（怎么做出来）",
               "&7- &6U&r 查看它的用途（能拿来做什么）",
               "&7- 按住 &6W&r（机械动力物品）可以观看思索动画演示",
               "",
               "搜索栏支持拼音首字母（例如 &6tg&r = 铜锭），前缀 &6@&r 按模组搜索，&6#&r 按标签搜索。"],
         tasks=[checkmark("已了解")],
         rewards=[xp(30)])

ch.quest("hud", -3, 2, "读懂你的状态栏", icon="cold_sweat:thermometer", deps=["welcome"],
         desc=["屏幕上比原版多了不少指示器，它们都关系到你的生死：",
               "&6❤ 生命&r —— 分部位计算（急救系统），按 &6Ctrl+H&r 查看各部位伤势",
               "&6◆ 口渴&r —— 在饥饿条旁，喝水回复（不要喝咸水！）",
               "&6◆ 体温&r —— 快捷栏旁的小人：&9蓝色在降温&r，&e黄色&r/&c红色在过热&r",
               "&6◆ 理智&r —— 左侧大脑图标：黑暗、怪物、饥饿会降低它",
               "&6◆ 氧气&r —— 高山与深矿空气稀薄，需要呼吸设备",
               "",
               "后续的「生存之道」章节会逐一讲解每个系统。"],
         tasks=[checkmark("已了解")],
         rewards=[item("cold_sweat:waterskin"), xp(30)])

ch.quest("death", 0, 3, "死亡不是儿戏", icon="minecraft:skeleton_skull", deps=["welcome"], shape="diamond",
         desc=["&c本整合包对死亡有额外惩罚。&r",
               "",
               "&7- 生命归零时你会先进入&6倒地状态&r，队友可以在限时内靠近并&a救起&r你；单人游戏时请格外谨慎。",
               "&7- 被救起或重生后会附带虚弱、饥饿等负面效果，生命值与饱食度也只剩一小部分。",
               "&7- &c岩浆、虚空&r等环境伤害会直接致死，无法被救。",
               "&7- 你的物品会留在原地的尸体/坟墓里，请尽快回去取回。",
               "",
               "&a建议：&r出远门之前在床（或干草床）上设置重生点，并随身携带绷带与夹板。"],
         tasks=[checkmark("我会小心的")],
         rewards=[item("firstaid:bandage", 4), item("firstaid:plaster", 4)])

ch.quest("first_year", 3, 0, "第一年的建议", icon="tfc:food/blueberry", deps=["welcome"], size=1.25,
         desc=["&o&7「冬天来得比你想象的快。」&r",
               "",
               "游戏从&6夏初&r开始。第一年请专注于：",
               "&e1.&r 找到靠近&6淡水&r（河流/湖泊）的营地 —— 水源、鱼和未来的水车动力都在这里",
               "&e2.&r 做出石器、生火、烧陶，准备好储物与做饭的容器",
               "&e3.&r 大量采集食物并学会&6保存&r它们（食物会腐烂！）",
               "&e4.&r 搞到兽皮/羊毛，在入冬前做好&6保暖衣物&r",
               "&e5.&r 用石头或砖头建一座房子 —— 木屋扛不住龙卷风",
               "",
               "&c不要急着探索远方或深入地下&r，世界上有很多会把你当晚餐的东西。"],
         tasks=[checkmark("记住了")],
         rewards=[item("tfc:food/barley_bread", 6), item("tfc:powder/salt", 8)])

ch.quest("roadmap", 6, 0, "前方的路", icon="ad_astra:tier_1_rocket", deps=["first_year"], shape="gear", size=1.5,
         desc=["本任务书分为四大篇章：",
               "",
               "&6生存之道&r —— 体温、饮水、食物、医疗、导航、危险生物",
               "&6金属时代&r —— 石器 → 铜 → 青铜 → 铁 → 钢，TFC 的核心冶金线",
               "&6工业革命&r —— 机械动力、沉浸工程、气动工艺、通用机械、仓储物流",
               "&6远方与星辰&r —— 船与车、地下城与暮色森林、最终飞向太空",
               "",
               "每个章节顶部都有标题横幅，章节内用&e面板&r划分小节。&a从「石器时代」开始你的旅程吧！&r"],
         tasks=[checkmark("出发！")],
         rewards=[xp(100)])

ch.quest("team", 3, 3, "组队与领地", icon="minecraft:white_banner", deps=["welcome"], shape="diamond", optional=True,
         desc=["多人游戏时：",
               "&7- 打开任务书左上角的&6队伍&r按钮（或 &6/ftbteams&r）创建队伍并邀请朋友，任务进度与奖励队伍共享。",
               "&7- 在地图界面可以&6认领区块&r保护你的基地，并&6强制加载&r区块让机器持续运行（数量有限）。",
               "&7- 支持语音聊天（默认按键 &6V&r 打开设置）。"],
         tasks=[checkmark("已了解")],
         rewards=[xp(20)])

ch.section("入门须知", ["tome", "field_guide", "jei", "hud"])
