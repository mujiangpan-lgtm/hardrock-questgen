from qlib import *

ch = Chapter("storage", "仓储与物流", icon="refinedstorage:controller", group="survival", order=4,
             theme="storage", subtitle="从一只木箱，到一张能装下整个世界的网络")

# ============================================================ A · 体积、重量与早期储物
ch.quest("start", 1.45, 3.1, "装不下，也扛不动", icon="tfc:wood/chest/oak", shape="gear", size=1.5,
         deps=["stone_age:finale"],
         subtitle="在造终端之前，先搞懂东西为什么装不进箱子",
         desc=["&o&7「仓库不是终点，是让你少跑几次路的工具。」&r",
               "",
               "本整合包里，每件物品都有自己的&6体积 ⇲&r和&6重量 ⚖&r（悬停物品、按住 Shift 查看）：",
               "&7- &6体积&r决定能不能装进某种容器——极小/非常小的东西随便哪个容器都能装；"
               "小型及以下才能塞进&6小缸&r；普通及以下才能塞进&6大缸&r；大型及以下才能塞进&6箱子&r；"
               "非常大的东西（如大缸本身）只能单独放在&6坑窑&r里烧；极大的东西干脆进不了任何容器，背着走还会超重",
               "&7- &6重量&r决定一组最多叠多少：非常轻 64 / 轻 32 / 中等 16 / 重 4 / 非常重 1，"
               "大部分物品都是「非常轻」，方块基本是「中等」",
               "",
               "&c常见的坑：&r身上带 1 件极大且非常重的东西就会&c疲惫&r，带 2 件以上直接&c负担过重&r，"
               "行动和饥饿消耗都会变差。&6钻、密封的大桶、装满东西的大缸&r都属于这一类，别背太多。",
               "&a这一章要做的事：&r从木箱、大桶这些你已经会用的容器开始，一路升级到&6精炼存储（RS）&r"
               "的数字化网络——让「找东西」这件事彻底消失。",
               "&a精炼存储的入口在第三节：&r做出 Create 的&6机械压力机&r和&6机械手&r后就会开启，"
               "硅、富石英铁这些基础材料可以先备着，不必等到气动工艺。"],
         tasks=[checkmark("我已经读懂了体积与重量的规则")],
         rewards=[item("tfc:wood/chest/oak"), xp(20)])

ch.quest("more_chests", 3.65, 2.1, "分类存放", icon="tfc:wood/chest/oak", deps=["start"],
         desc=["铜器时代学过的&6箱子&r依然是最基础的储物方块，&627 格&r，可以用&6锁&r锁上防止他人翻动。",
               "",
               "&a小技巧：&r矿石、燃料、食物、工具分开装箱，贴上告示牌或者摆成固定布局，"
               "比把所有东西堆进一个箱子省心得多——尤其是接下来要接物流系统的时候。"],
         tasks=[tag("forge:chests", 2, title="箱子 ×2")],
         rewards=[item("tfc:wood/lumber/oak", 8), xp(20)])

ch.quest("vessels", 3.65, 4.1, "小缸与大缸", icon="tfc:ceramic/vessel", deps=["start"],
         desc=["&6小缸&r（陶器时代就有）能装 4 格&6小型及以下&r的物品，还能&a延缓食物腐烂&r，"
               "密封后甚至可以带着熔化的金属走。",
               "",
               "&6大缸&r是陶土塑形出的大容器：9 格，能装&6普通及以下&r的物品，密封后防腐效果更好，"
               "也能背在身上——但装满了别忘了它本身很重。",
               "",
               "&a建议：&r小缸适合随身携带的应急存储，大缸适合家里的食物仓。"],
         tasks=[tag("tfc:vessels", title="任意小缸"), tag("tfc:large_vessels", title="任意大缸")],
         rewards=[item("minecraft:clay_ball", 16), xp(20)])

ch.quest("barrels2", 5.85, 3.1, "大桶仓", icon="tfc:wood/barrel/oak", deps=["more_chests", "vessels"],
         desc=["铜器时代的&6大桶&r除了加工配方，密封起来也是不错的&6液体仓&r——"
               "一桶水、一桶橄榄油、一桶卤水，排成一排清清楚楚。",
               "",
               "&c注意：&r大桶、装满的大缸都&6非常重&r，仓库里堆放没问题，别一次背太多件上路。"],
         tasks=[tag("tfc:barrels", 2, title="大桶 ×2")],
         rewards=[item("tfc:powder/flux", 4), xp(20)])

ch.quest("toolbelt", 8.05, 2.1, "工具皮带与皮带袋", icon="toolbelt:belt", deps=["barrels2"], shape="hexagon",
         desc=["&6工具皮带&r（Toolbelt 模组）穿在腰上，提供&64 个快捷槛位&r，放镰刀、锤子、火把之类常用工具，"
               "不用再占背包格子，也不用来回切换快捷栏。",
               "",
               "&c注意：&r本整合包装了&6Sewing Kit&r，所以工具皮带/皮带袋&c不走普通合成栏&r，"
               "要用缝纫工具按配方缝制（皮革条/皮革片为主，还要搭一点金属线），具体用量&c详见 JEI&r。",
               "装备后再做&6皮带袋&r挂在皮带上，能再多装一些杂物，"
               "且不计入体积限制（视模组设置，实际容量详见 JEI 悬停提示）。",
               "",
               "&a小技巧：&r矿工、农夫、猎人可以各配一条装备不同工具的皮带，出门直接换皮带比翻箱子快得多。"],
         tasks=[item("toolbelt:belt", title="工具皮带")],
         rewards=[item("minecraft:leather", 4), xp(30)])

ch.quest("bundle", 8.05, 4.1, "收纳袋", icon="minecraft:bundle", deps=["barrels2"], optional=True, shape="diamond",
         desc=["原版的&6收纳袋&r可以把多种零散小物品塞进一个格子里随身携带，&e右键&r打开取放，"
               "适合浆果、种子、箭矢之类的杂物——具体合成材料详见 JEI。",
               "",
               "&7这不是本章的重点，顺手带一个在身上即可。"],
         tasks=[item("minecraft:bundle", title="收纳袋")],
         rewards=[item("tfc_stone_tools:plant_string", 8), xp(20)])
ch.quest("sacks", 3.65, 6.1, "草篮与麻袋", icon="sns:straw_basket", deps=["vessels"],
         desc=["还没有皮革也不要紧：&6草篮&r用稻草和纤维就能编，能让同类物品"
               "&a占用更少负重&r地堆叠携带，适合装谷物、蔬菜等杂物。",
               "",
               "&a小技巧：&r皮革到手后（见「铜器时代 · 制革与风箱」），可以进一步做&6麻袋&r、"
               "&6皮革袋&r、&6矿石袋&r——矿石袋专为挖矿囤矿石设计，长途下矿必备。"],
         tasks=[item("sns:straw_basket", title="草篮")],
         rewards=[item("tfc:straw", 16), xp(30)])

ch.quest("frame_pack", 5.85, 6.1, "大背包", icon="sns:frame_pack", deps=["sacks"], shape="hexagon",
         desc=["&6大背包&r是最值得优先做的负重装备：背上之后能大幅扩展随身携带的容量，"
               "且不易像箱子一样占用负重。",
               "",
               "&a适合：&r长途探索、搬家、第一次去挖矿囤矿石，都该带它。"],
         tasks=[item("sns:frame_pack", title="大背包")],
         rewards=[item("tfc:food/barley_bread", 4), xp(30)])

ch.quest("ore_sack", 8.05, 6.1, "矿石袋", icon="sns:ore_sack", deps=["frame_pack", "copper_age:leather"], optional=True,
         shape="diamond",
         desc=["有了皮革之后，&6矿石袋&r能让矿石堆叠携带，大幅降低挖矿远征时的负重压力。",
               "",
               "&7同系列还有&6麻袋&r（杂物）、&6皮革袋&r（通用），详见 JEI。"],
         tasks=[item("sns:ore_sack", title="矿石袋")],
         rewards=[item("minecraft:leather", 4), xp(20)])
# ============================================================ B · 食物仓与自动化搬运
ch.quest("food_shelf", 11.25, 3.1, "食物架", icon="firmalife:wood/food_shelf/oak", deps=["start"], hide_lines=True,
         desc=["Firmalife 的&6食物架&r能展示并保存食物，&c和悬挂架一样只能放在有效的地窖多方块结构里用&r"
               "——四周被&6密封砖&r或&6密封门&r完全封闭、还贴墙放了一台&6气象站&r的空间，"
               "单放在普通房间里是不会生效的。",
               "",
               "&e合成：&r木板 + 木材（lumber），详见 JEI。"],
         tasks=[tag("firmalife:food_shelves", title="任意食物架")],
         rewards=[item("tfc:food/barley_bread", 4), xp(20)])

ch.quest("hanger", 13.45, 2.1, "悬挂架：腌肉房", icon="firmalife:wood/hanger/pine", deps=["food_shelf"],
         desc=["&6悬挂架&r用来挂肉类或大蒜，&c只能在有效的地窖多方块结构里使用&r："
               "一个完全由&6密封砖&r或&6密封门&r封闭的空间，还要配一台&6气象站&r贴墙放置。",
               "",
               "存在有效悬挂架里的食物，防腐效果&a比食物架或小缸都更好&r：地窖平均温度越低越好，"
               "0℃ 以下有明显加成，-12℃ 以下效果更佳。",
               "",
               "&a小技巧：&r把地窖挖进山体或建在阴面，天然就更冷，蜂蜡也能用来给熟化中的奶酪封顶。"],
         tasks=[tag("firmalife:hangers", title="任意悬挂架")],
         rewards=[item("tfc:powder/salt", 4), xp(30)])

ch.quest("jarbnet", 13.45, 4.1, "罐头柜", icon="firmalife:wood/jarbnet/pine", deps=["food_shelf"],
         desc=["&6罐头柜&r是存放&6罐子&r、蜡烛和水壶的装饰性储物方块，"
               "空手潜行&e右键&r开关柜门，放蜡烛进去还能点燃当灯用。",
               "",
               "&e合成：&r木材为主，详见 JEI。配合&6装罐台&r腌渍食物、酿酒后，罐头柜就是储藏室的标配。"],
         tasks=[tag("firmalife:jarbnets", title="任意罐头柜")],
         rewards=[item("minecraft:glass_bottle", 4), xp(20)])

ch.quest("woodenhopper", 15.65, 3.1, "木漏斗：第一步自动化", icon="woodenhopper:wooden_hopper", deps=["jarbnet"],
         shape="hexagon",
         desc=["&c本整合包移除了原版漏斗的早期合成&r，取而代之的是&6木漏斗&r（WoodenHopper 模组）：",
               "&6木材 + 箱子 + 小齿轮&r 拼出来，小齿轮来自&6Create&r，所以要先接上 Create 齿轮生产线。",
               "",
               "木漏斗功能和原版漏斗一样，能从上方容器收集物品、往下方漏斗/容器搬运，"
               "是搭建简易自动化产线（炉子出料、分拣）的起点。",
               "",
               "&a进阶：&r往木漏斗上贴一片&6双层板&r（Create 配方）可以升级成&6原版铁漏斗&r，"
               "能对接更多模组管道。更大规模的物品搬运，见「机械时代」章节的传送带与漏斗矩阵。"],
         tasks=[item("woodenhopper:wooden_hopper", title="木漏斗")],
         rewards=[item("tfc:wood/lumber/oak", 8), xp(30)])
# ============================================================ C · 精炼存储：控制器与网络
ch.quest("rs_start", 1.45, 11.2, "精炼存储：数字仓库", icon="refinedstorage:controller",
         deps=["create:press", "create:deployer"],
         shape="gear", size=1.5,
         subtitle="材料一齐，就能开始搭网络",
         desc=["&o&7「不再翻箱子找东西，而是问网络要东西。」&r",
               "",
               "&6精炼存储（Refined Storage，RS）&r是一套把所有存储整合成一张网络的模组："
               "装好之后，用一个&6终端&r就能看到、存取、合成全仓库的物品。",
               "",
               "&c本整合包改了 RS 的核心配方，它不是一条单独的线，而是几条产线汇合：&r",
               "&7- &6Create&r：富石英铁、机器外壳，以及把处理器半成品装配成型的机械手（从本节开始）",
               "&7- &6PneumaticCraft&r：处理器粘合物、未处理处理器、未组装电路板、线缆，都要在压力室里压出来（见气动工艺章）",
               "&7- &6硅&r：所有处理器的基础材料，来源见下一任务",
               "{@pagebreak}",
               "&e推荐顺序：&r",
               "&e1.&r 下一任务先备好&6硅&r和&6富石英铁&r——气动章的「未处理基础处理器」也要消耗硅，别等做到那里才发现缺",
               "&e2.&r 去气动章做压力室、空气压缩机、空白电路板和紫外蚀刻，再回来做三档处理器",
               "&e3.&r 控制器 → 磁盘驱动器 → 终端 → 总线 → 自动合成",
               "",
               "&a这一节的目标：&r造出第一台&6控制器&r和&6磁盘驱动器&r，组一张最小的网络。"],
         tasks=[checkmark("我知道 RS 需要哪些前置，开始分头准备")],
         rewards=[item("minecraft:redstone", 48), xp(175), item("tfc:metal/ingot/copper", 24)])

ch.quest("silicon", 3.65, 11.2, "硅与富石英铁", icon="refinedstorage:silicon", deps=["rs_start"],
         desc=["RS 的处理器、控制器、线缆，都从这两样材料开始。",
               "",
               "&6硅&r——本包有三条路线：",
               "&7- &6动力筛子&r（Create 筛子）：&6黄铜筛网&r筛&6石英岩砂砾&r，有 &62%&r 概率出硅。最早就能走，适合接上自动化慢慢攒",
               "&7- &6电弧炉&r（IE）：&6石英粉 + 焦炭粉&r，更靠后",
               "&7- &6TFMG&r：石英粉熔成&6液态硅&r，再用 TFC 浇铸出硅，更靠后",
               "&c常见的坑：&rTiny Redstone 自带的硅，本包已移除合成，别按旧攻略把它丢进焦炉。",
               "{@pagebreak}",
               "&6富石英铁&r走 Create 的接续组装：",
               "&e1.&r &6石英粉&r在 TFC 里加热到 &6930°C&r 左右，熔成&6熔融石英&r（25 mB / 份）",
               "&e2.&r 以&6铁锭&r为起点，按配方交替&6注入熔融石英&r和&6压制&r，循环两轮",
               "&e3.&r 机器摆放与液体搬运方式，按 &eR&r 查看富石英铁的配方",
               "",
               "&a小技巧：&r控制器、磁盘驱动器、装配室、存储盘都要成批的富石英铁，一次多做几组。"],
         tasks=[item("refinedstorage:silicon", 4, title="硅 ×4"),
                item("refinedstorage:quartz_enriched_iron", 4, title="富石英铁 ×4")],
         rewards=[item("minecraft:redstone", 32), xp(225), item("refinedstorage:processor_binding", 24), item("tfc:metal/ingot/copper", 16)])

ch.quest("processor_chain", 5.85, 11.2, "处理器三部曲", icon="refinedstorage:processor_binding",
         deps=["silicon", "pneumatic:uv_etch", "pneumatic:raw_processor"],
         shape="hexagon", size=1.25,
         desc=["RS 的核心零件是&6三档处理器&r，做法一致：&e气压机压出未处理半成品，Create 机械手装配成型。&r",
               "",
               "&e1.&r &6处理器粘合物&r：气压机 2 bar（线 ×2 + 粘液球），一次出 6 个（气动章已教）",
               "&e2.&r &6未处理处理器&r：气压机，粘合物 + &6硅&r + 红石 + 一种粉：",
               "&7- &6基础&r：铁粉（2 bar） · &6进阶&r：金粉（2 bar） · &6高级&r：钻石粉（&64 bar&r）",
               "&e3.&r 以气动章蚀刻出的&6未组装电路板&r为起点，Create 机械手依次装上&6未处理处理器、线材、红石、线材&r，最后压制",
               "&7- 线材：基础用&6铜线&r · 进阶用&6金线&r · 高级用&6电金线&r",
               "{@pagebreak}",
               "&c只做基础处理器远远不够：&r控制器、磁盘驱动器、合成终端要&6高级处理器&r，终端、总线、装配室也离不开"
               "&6进阶处理器&r；基础处理器主要用来蚀刻成型核心。",
               "",
               "&c常见的坑：&r每个成品都要消耗一块未组装电路板，别忘了气动章那条紫外曝光 + 蚀刻线的产量。",
               "&a建议：&r三档先各备两三个，之后按需补。"],
         tasks=[item("refinedstorage:basic_processor", 4, title="基础处理器 ×4"),
                item("refinedstorage:improved_processor", 2, title="进阶处理器 ×2"),
                item("refinedstorage:advanced_processor", 2, title="高级处理器 ×2")],
         rewards=[item("minecraft:redstone", 48), xp(300), item("refinedstorage:silicon", 24), item("refinedstorage:processor_binding", 24)])

ch.quest("quartz_grow", 8.05, 10.2, "成型核心与破坏核心", icon="refinedstorage:construction_core",
         deps=["processor_chain"],
         desc=["&6成型核心&r和&6破坏核心&r是&6终端、输入/输出总线、装配室&r的关键零件，不是可选项。",
               "",
               "&e做法：&r在气动章的装配系统里，用&6激光&r程序蚀刻处理器：",
               "&7- &6成型核心&r ← &6基础处理器&r（输出总线、终端、装配室要用）",
               "&7- &6破坏核心&r ← &6进阶处理器&r（输入总线、终端、装配室要用）",
               "",
               "&7装配平台和激光的搭建见气动工艺章，具体配方按 &eR&r 查看。"],
         tasks=[item("refinedstorage:construction_core", title="成型核心"),
                item("refinedstorage:destruction_core", title="破坏核心")],
         rewards=[item("minecraft:redstone", 32), xp(175), item("refinedstorage:basic_processor", 8)])

ch.quest("controller", 8.05, 12.2, "控制器：网络的心脏", icon="refinedstorage:controller", deps=["processor_chain"],
         shape="hexagon", size=1.25,
         desc=["&6控制器&r是整张 RS 网络的供电核心，所有网络方块必须直接或通过&6线缆&r"
               "连到控制器才会工作。",
               "",
               "&e合成：&r&6富石英铁 ×4 + 高级处理器 + 硅 ×2 + 机器外壳&r（工作台）。",
               "&7- &6机器外壳&r：以列车机壳为起点，用熔融富石英铁和铁板做 Create 接续组装，按 &eR&r 查看",
               "",
               "&6线缆&r有两条路线：",
               "&7- 气压机 &64.5 bar&r：电金线、铜线、铝线各一 + 玻璃 ×3 + 微型红石粉 ×2 + 富石英铁",
               "&7- Create 接续组装：以&6硅&r为起点，装线材、注熔融玻璃、激光切割、充能，循环 5 轮得 5 根",
               "&7- &6微型红石粉&r：红石 + 硅（任意来源）无序合成，一次 8 个",
               "",
               "&c注意：&r控制器有&6容量上限&r（接入设备数会消耗「用电量」），具体数值详见 JEI 悬停提示；"
               "挂的设备太多会亮红灯提示超载。"],
         tasks=[item("refinedstorage:controller", title="控制器")],
         rewards=[item("refinedstorage:cable", 24), xp(350), item("refinedstorage:basic_processor", 8), item("refinedstorage:silicon", 16)])
# ============================================================ D · 磁盘、终端与自动合成
ch.quest("disk_drive", 11.375, 12.2, "磁盘驱动器与存储盘", icon="refinedstorage:disk_drive", deps=["controller"],
         desc=["&6磁盘驱动器&r插上&6存储盘&r才是网络真正的「仓库」：驱动器本身只是插槽，"
               "容量看里面插的盘。",
               "",
               "&e合成：&r&6磁盘驱动器&r = 富石英铁 ×6 + 箱子 + 机器外壳 + 高级处理器。",
               "",
               "&6存储盘&r分 1k / 4k / 16k / 64k 几档，数字是能存放的&6物品总件数&r（1k 约 1000 件），"
               "不看堆叠上限，种类也不限。",
               "&7- &61k 存储元件&r：气压机 2 bar，未处理进阶处理器 + 铁粉 + 石英粉 + 红石",
               "&7- &61k 存储磁盘&r：玻璃 ×2 + 红石 ×2 + 存储元件 + 富石英铁 ×3（工作台）",
               "",
               "&a小技巧：&r前期几块 1k 盘够用，等东西多了再换大盘；"
               "旧盘里的东西可以直接插进新驱动器，不会丢失。"],
         tasks=[item("refinedstorage:disk_drive", title="磁盘驱动器"),
                item("refinedstorage:1k_storage_part", title="1k 存储元件"),
                item("refinedstorage:1k_storage_disk", title="1k 存储磁盘")],
         rewards=[item("refinedstorage:cable", 24), xp(350), item("refinedstorage:basic_processor", 12), item("minecraft:glass", 32)])

ch.quest("grid", 13.575, 11.2, "终端：看见整张网络", icon="refinedstorage:grid", deps=["disk_drive"], shape="hexagon",
         desc=["&6终端&r接入网络后，&e右键&r打开就能看到&c所有&r存储盘里的物品，"
               "直接取放、搜索、按模组/数量排序，比翻箱子快得多。",
               "",
               "&e合成：&r&6进阶处理器 ×2 + 成型核心 + 破坏核心 + 玻璃 ×3 + 富石英铁 + 机器外壳&r（工作台）。",
               "",
               "&6便携式终端&r是能装进背包随身带着用的版本（需要耗电或装电池，详见 JEI）。",
               "&a建议：&r终端装在控制器旁边，布线越短越整齐，以后扩展网络也方便追踪。"],
         tasks=[item("refinedstorage:grid", title="终端")],
         rewards=[item("refinedstorage:cable", 24), xp(300), item("refinedstorage:basic_processor", 8), item("minecraft:glass", 24)])

ch.quest("importer_exporter", 13.575, 13.2, "输入/输出总线：自动进出货", icon="refinedstorage:importer",
         deps=["disk_drive"],
         desc=["&6输入总线&r贴在箱子/机器背面，会把里面的物品自动吸入网络；"
               "&6输出总线&r反过来，把网络里的指定物品自动吐进相邻容器或机器。",
               "",
               "&e合成（无序）：&r&6线缆 + 进阶处理器 + 核心&r——输入总线用&6破坏核心&r，输出总线用&6成型核心&r。",
               "",
               "&e典型用法：&r输出总线对着炉子投矿石，输入总线接在炉子出料口收锭，"
               "配合「木漏斗」或 Create 的传送带把物理搬运也接进网络两端。",
               "",
               "&a小技巧：&r给总线加&6过滤升级&r可以精确指定物品种类，别让它把你想留着的东西也吸走。"],
         tasks=[item("refinedstorage:importer", title="输入总线"),
                item("refinedstorage:exporter", title="输出总线")],
         rewards=[item("refinedstorage:cable", 32), xp(350), item("refinedstorage:basic_processor", 12), item("minecraft:redstone", 32)])

ch.quest("crafting_grid", 15.775, 12.2, "合成终端：按配方点一下", icon="refinedstorage:crafting_grid",
         deps=["grid"],
         desc=["&6合成终端&r是终端的升级版：自带 3×3 合成栏，材料直接从网络里取，"
               "不用再把一堆矿锭搬来搬去凑合成栏。",
               "",
               "&e合成（无序）：&r&6终端 + 高级处理器 + 工作台&r。",
               "",
               "&c注意：&r它本身&c不会自动合成&r，仍然要你手动点一下——真正的自动合成要看下一个任务。"],
         tasks=[item("refinedstorage:crafting_grid", title="合成终端")],
         rewards=[item("refinedstorage:cable", 24), xp(350), item("refinedstorage:basic_processor", 12), item("refinedstorage:silicon", 24)])

ch.quest("autocrafting", 17.975, 12.2, "装配室与自动合成", icon="refinedstorage:crafter",
         deps=["crafting_grid", "importer_exporter"], shape="hexagon", size=1.25,
         desc=["&6装配室&r是网络里的「自动合成单元」：把&6模板&r（记录了某个配方的物品）放进装配室，"
               "网络就能按模板自动拼装产物并存回网络。",
               "",
               "&e合成：&r&6装配室&r = 富石英铁 ×4 + 成型核心 + 破坏核心 + 高级处理器 ×2 + 机器外壳。",
               "&6模板&r = 玻璃 ×3 + 红石 ×3 + 富石英铁 ×3。",
               "",
               "&e搭建思路：&r",
               "&e1.&r 做空白&6模板&r，用&6样板终端&r（配方见 JEI）或按提示给每个目标配方设定好",
               "&e2.&r 把模板放进&6装配室&r；装配室多了，可以接一台&6合成管理器&r在一个界面里统一查看",
               "&e3.&r 在终端里对着目标物品点&6合成&r，网络会自动算需要多少原料、依次做下去",
               "",
               "&c常见的坑：&r原料不够或装配室放不下就会卡在「等待材料」，"
               "&6合成监控处理器&r能让你看清卡在哪一步。"],
         tasks=[item("refinedstorage:crafter", title="装配室"),
                item("refinedstorage:pattern", title="模板")],
         rewards=[item("refinedstorage:cable", 48), levels(8), item("refinedstorage:basic_processor", 16), item("minecraft:redstone", 48)])

ch.quest("extra_storage", 20.175, 10.2, "Extra Storage：更深的仓库", icon="extrastorage:iron_crafter",
         deps=["autocrafting"], optional=True, shape="diamond",
         desc=["&6Extra Storage&r是 RS 的扩展模组：提供&6铁/金/钻石/下界合金装配室&r等更强的自动合成单元，"
               "以及更高级输入/输出总线。",
               "",
               "它的&6神经处理器&r同样是 Create + PneumaticCraft 的联合产物"
               "（气压机压粗制处理器 → Create 世界图纸嵌入进阶/高级处理器压制成型），"
               "适合网络规模已经很大、需要更快总线和更多并发装配室的后期玩家。"],
         tasks=[item("extrastorage:iron_crafter", title="铁装配室")],
         rewards=[item("refinedstorage:cable", 32), xp(450), item("refinedstorage:basic_processor", 16), item("refinedstorage:silicon", 32)])

ch.quest("create_logistics", 20.175, 12.2, "别忘了 Create 的物理物流", icon="woodenhopper:wooden_hopper",
         deps=["autocrafting"], optional=True, shape="diamond", hide_lines=True,
         desc=["RS 擅长「数字化」的物品存取和自动合成，但&6传送带、漏斗矩阵、机械臂&r这类"
               "&6物理搬运&r依然是 Create 的强项，两者接口（输入/输出总线对接传送带末端）配合使用效果最好。",
               "",
               "&7详见「机械时代」章节。"],
         tasks=[checkmark("我知道 Create 物流和 RS 可以互相对接")],
         rewards=[xp(150), item("refinedstorage:cable", 16), item("tfc:metal/ingot/copper", 16)])

ch.quest("finale", 20.175, 14.2, "一张永不丢失的网络", icon="refinedstorage:crafter_manager", deps=["autocrafting"],
         shape="gear", size=1.75,
         subtitle="找东西，从此只是输入几个字",
         desc=["&o&7「文明的仓库，最终变成了一张会自己整理的网络。」&r",
               "",
               "你已经拥有：&a控制器 + 磁盘驱动器&r、&a终端&r、&a输入/输出总线&r、&a装配室自动合成&r。"
               "矿石、锭、零件进了网络就再也不用翻箱子找。",
               "",
               "&a继续扩展：&r&6中继器&r分流大网络、&6无线访问点&r在基地外也能用终端、"
               "&6安全管理器&r给多人服务器分权限——这些都在 RS 的后续科技树里，按 JEI 慢慢点。"],
         tasks=[checkmark("我已经建好了一张可用的 RS 网络")],
         rewards=[item("refinedstorage:cable", 64), levels(16), item("refinedstorage:basic_processor", 24), item("refinedstorage:silicon", 32), item("minecraft:redstone", 64)])

ch.section("第一节 · 体积、重量与背负", ["start", "more_chests", "vessels", "barrels2", "toolbelt", "bundle",
                              "sacks", "frame_pack", "ore_sack"])
ch.section("第二节 · 食物仓与自动化搬运", ["food_shelf", "hanger", "jarbnet", "woodenhopper"])
ch.section("第三节 · 精炼存储：控制器与网络",
           ["rs_start", "silicon", "processor_chain", "quartz_grow", "controller"])
ch.section("第四节 · 磁盘、终端与自动合成",
           ["disk_drive", "grid", "importer_exporter", "crafting_grid", "autocrafting",
            "extra_storage", "create_logistics", "finale"])
