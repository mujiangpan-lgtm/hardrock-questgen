from qlib import *

ch = Chapter("create", "机械动力", icon="create:cogwheel", group="industry", order=0,
             theme="create", subtitle="齿轮一转，文明提速")

# ============================================================ A · 安山合金：机械的起点
ch.quest("start", 1.45, 4.225, "安山石里的秘密", icon="tfc:rock/loose/andesite", shape="gear", size=1.5,
         deps=["bronze_age:finale"],
         subtitle="真正的机械，从一炉特殊的\"石头合金\"开始",
         desc=[
               "&o&7「把石头熔化，再让它带动齿轮。」&r",
               "",
               "本包的&6安山合金&r走 TFC 合金系统：安山石在 &6930℃&r 熔化，再与少量金属混合，最后铸成锭。",
               "&7- 熔融安山石占 &688–92%&r；&6锡、锌或铸铁&r占 &68–12%&r。三条合金配方可任选其一。",
               "&7- 铸铁是 &6Cast Iron&r，和炼钢中间材料&6生铁（Pig Iron）&r不同，别拿错。",
               "",
               "&e准备：&r先收集安山石。不同形态的安山石熔融量不同，一块散石产 &610 mB&r，计算配比时看液体量。",
               "&a提示：&r青铜时代已有锡、锌和铸造工具，用这些材料就能开始机械动力。"],
         tasks=[item("tfc:rock/loose/andesite", 32, title="安山石 ×32")],
         rewards=[item("tfc:metal/ingot/tin", 2), xp(40)])

ch.quest("melt_andesite", 3.65, 4.225, "熬一炉安山石浆", icon="tfc:ceramic/vessel", deps=["start"],
         shape="hexagon", size=1.25,
         desc=[
               "&e1.&r 按 JEI 的合金比例准备安山石与锡、锌或铸铁，使用&6小缸与坑窑&r，或后续的&6坩埚&r熔炼。",
               "&e2.&r 安山石需达到 &6930℃&r；确认液体组成是 &688–92% 安山石 + 8–12% 对应金属&r。",
               "&e3.&r 将&6安山合金&r倒入普通或耐火铸锭模具，每锭 &6100 mB&r，冷却后取出。",
               "",
               "&c常见的坑：&r大缸不是小缸的熔炼替代品。配比不符合合金范围会得到未知合金，先计算各材料的熔融量。",
               "&a检查：&r浇铸前看容器里的液体名称，确认是安山合金；铸造产物应为 Create 的安山合金。"],
         tasks=[checkmark("我熬出了安山合金浆并铸成了锭")],
         rewards=[item("tfc:powder/flux", 8), xp(50)])

ch.quest("andesite_ingot", 5.85, 4.225, "第一批安山合金", icon="create:andesite_alloy", deps=["melt_andesite"],
         desc=[
               "&e目标：&r准备 &616 块安山合金&r，供传动杆和基础机器使用。",
               "",
               "&a建议：&r按液体量规划整炉配比；剩余合金可以在合适容器中保存，重新加热后继续浇铸。",
               "先做少量传动零件并接通动力，再逐步扩建机器，避免一炉材料全用在机壳上。"],
         tasks=[item("create:andesite_alloy", 16, title="安山合金锭 ×16")],
         rewards=[item("tfc:metal/ingot/zinc", 2), xp(40)])

ch.quest("shaft", 8.05, 2.225, "传动杆", icon="create:shaft", deps=["andesite_ingot"], shape="hexagon",
         size=1.25,
         desc=[
               "&6传动杆&r把旋转动力沿轴线传给其他机械，是动力网络的基础。",
               "",
               "&e制作：&r将&6支撑梁&r放到世界中，手持&6安山合金&r右键应用，得到传动杆。详见 JEI 的应用配方。",
               "&e安装：&r让传动杆轴线与动力源或机器的轴线对齐；转弯或改变传动方向需要齿轮、齿轮箱等部件。",
               "&a调试：&r先搭短直线，确认各段转动，再扩展到车间。"],
         tasks=[item("create:shaft", 8, title="传动杆 ×8")],
         rewards=[item("tfc:wood/support/oak", 8), xp(40)])

ch.quest("cogwheel", 8.05, 4.225, "齿轮与大齿轮", icon="create:cogwheel", deps=["shaft"],
         shape="hexagon", size=1.25,
         desc=[
               "&6小齿轮与大齿轮&r可以把旋转动力传给错位的轴，并改变方向或转速。",
               "",
               "&e制作：&r小齿轮用&6传动杆 + 木板&r，大齿轮用&6传动杆 + 两块木板&r；也有部署加工路线，详见 JEI。",
               "&7- 同尺寸齿轮咬合会反向转动。",
               "&7- 小齿轮与大齿轮咬合有 &62∶1&r 的转速比，平行轴也能这样变速。",
               "&7- 大齿轮还能连接互相垂直的轴，具体摆放可查看&6思索（Ponder）&r。",
               "",
               "&c常见的坑：&r同一个动力网络中，把不同转速或方向的两路硬接到一起会导致冲突；先检查齿轮比。"],
         tasks=[item("create:cogwheel", 4, title="齿轮 ×4"),
                item("create:large_cogwheel", 2, title="大齿轮 ×2")],
         rewards=[item("tfc:wood/lumber/oak", 8), xp(40)])

ch.quest("wrench", 8.05, 6.225, "扳手与护目镜", icon="create:wrench", deps=["brass"], optional=True,
         shape="diamond",
         desc=[
               "两件机械师工具，适合在黄铜材料齐备后制作：",
               "&7- &6扳手&r：&e右键&r调整方块朝向，&e潜行右键&r拆下并回收支持拆卸的机械方块。",
               "&7- 本包扳手要在 TFC 砧上用&6黄铜双锭&r锻造，最低砧等级 &61&r，操作规则详见 JEI。",
               "&7- &6护目镜&r：戴上后观察转速、应力和机器状态；本包配方需要镜片、金线、线和皮革条。",
               "",
               "&a建议：&r网络停转时，先看应力是否超载，再检查旋转方向和转速。"],
         tasks=[item("create:wrench", title="扳手"), item("create:goggles", title="护目镜")],
         rewards=[item("create:andesite_alloy", 12), xp(125), item("tfc:metal/ingot/brass", 8)], hide_lines=True)
# ============================================================ B · 第一份动力
ch.quest("water_wheel", 11.5, 2.225, "水车", icon="create:water_wheel", deps=["shaft", "cogwheel"],
         shape="hexagon", size=1.25,
         desc=[
               "&o&7「流水日夜不停，车间就能一直转。」&r",
               "",
               "&e制作：&r用 &68 块 TFC 细木材&r围住 &61 个大齿轮&r，做出水车。",
               "&e安装：&r让水车邻接流动的水，再从轴端接出传动杆；按思索检查朝向和水流布置。",
               "",
               "&c本包变化：&r启用了 Create Picky Wheels，&6群系与附近水体&r会影响水车的转速和应力输出，天然河流是合适的选址。",
               "&a调试：&r用护目镜比较实际输出。给水车更多侧面铺水不会按侧数叠加普通水车的基础输出。"],
         tasks=[item("create:water_wheel", title="水车")],
         rewards=[item("create:shaft", 4), xp(50)])

ch.quest("windmill", 11.5, 4.225, "风车轴承", icon="create:windmill_bearing", deps=["shaft", "cogwheel"],
         optional=True, shape="diamond",
         desc=[
               "&6风车轴承&r将前方的帆结构装配成风车，产生持续的旋转动力。",
               "",
               "&e1.&r 在轴承前方搭帆，至少需要 &68 个帆类方块&r，使用&6强力胶&r把结构连接起来。",
               "&e2.&r &e右键&r轴承启动或停止；停下后可以继续扩建。帆数量影响基础转速。",
               "&c本包变化：&rCreate Picky Wheels 还会检查&6群系、露天空间和高度&r，搭建前给风车留出足够空地。",
               "&a调试：&r先搭能启动的小风车，再扩帆和调整位置，观察护目镜显示的实际输出。"],
         tasks=[item("create:windmill_bearing", title="风车轴承")],
         rewards=[item("create:shaft", 4), xp(30)])

ch.quest("hand_crank", 11.5, 6.225, "手摇曲柄：没有水也能转", icon="create:hand_crank", deps=["shaft", "cogwheel"], hide_lines=True,
         optional=True, shape="diamond",
         desc=[
               "&6手摇曲柄&r适合临时驱动小机器或调试动力网络，长按右键摇动，潜行操作可以改变旋转方向。",
               "",
               "&e制作：&r木齿轮、&6两块 TFC 细木材&r和传动杆，具体摆法见 JEI。",
               "&c注意：&r手摇需要玩家持续操作，长期生产应换成水车、风车或其他动力源。"],
         tasks=[item("create:hand_crank", title="手摇曲柄")],
         rewards=[item("create:andesite_alloy", 2), xp(20)])

ch.quest("belt", 13.7, 4.225, "传送带", icon="create:belt_connector", deps=["water_wheel", "windmill", "hand_crank"], any_dep=True,
         desc=[
               "&6传送带&r既能连接旋转动力，也能沿水平或斜坡运输物品。",
               "",
               "&e制作：&r本包有&6干海带块滚压&r路线；后期还能滚压橡胶板得到传送带连接器，详见 JEI。",
               "&e铺设：&r手持连接器，依次右键两根&6平行轴线的传动杆&r，形成一条带。两端位置必须符合直线或允许的斜坡方向。",
               "&c注意：&r竖直传送带可以传递旋转，不能当普通物品升降带使用。",
               "&a操作：&r潜行右键连接器可以取消已选中的首端；运行方向由输入的旋转方向决定。"],
         tasks=[item("create:belt_connector", title="传送带连接器")],
         rewards=[item("create:shaft", 4), xp(30)])

ch.quest("finale_a", 15.9, 4.225, "动力已经转起来了", icon="create:large_cogwheel", deps=["belt"],
         shape="hexagon", size=1.25,
         desc=["&a恭喜，你已经有了：&r&6安山合金产线&r、&6传动杆与齿轮&r、&6至少一种原动力&r。",
               "",
               "接下来是让这份动力真正&6干活&r——破碎矿石、冲压金属、搬运物品。"],
         tasks=[checkmark("我的第一套动力系统已经转起来")],
         rewards=[item("create:shaft", 4), item("create:cogwheel", 4), xp(50)])
# ============================================================ C · 让动力干活
ch.quest("mixer", 1.325, 10.325, "动力搅拌器", icon="create:mechanical_mixer", deps=["finale_a"], hide_lines=True,
         desc=[
               "&6动力搅拌器&r放在&6工作盆&r上方，通过旋转动力完成混合、合成和部分化工配方。",
               "",
               "&e制作：&r&6安山机壳 + 齿轮 + 搅拌头&r，具体配方见 JEI。",
               "&e使用：&r向工作盆加入材料与液体，接上传动杆或齿轮。配方可能要求最低转速与加热，请逐条查看 JEI。",
               "&a生产：&r先处理一批材料，确认产物和副产物的提取方式，再接漏斗、管道扩成连续产线。"],
         tasks=[item("create:mechanical_mixer", title="动力搅拌器")],
         rewards=[item("create:andesite_alloy", 16), xp(150), item("tfc:metal/ingot/copper", 8)])

ch.quest("press", 1.325, 12.325, "动力冲压机", icon="create:mechanical_press", deps=["finale_a"], hide_lines=True,
         desc=[
               "&6动力冲压机&r通过旋转动力压制物品，常用于板材加工和序列组装。",
               "",
               "&e加工：&r普通冲压和序列步骤在&6置物台或传送带&r上进行；工作盆用于&6压块&r等对应配方。",
               "&e看配方：&r本包金属加工常有加热条件。按 JEI 检查原料温度、设备顺序与循环次数，再让半成品进入产线。",
               "&c常见的坑：&r不能把所有金属放进工作盆反复敲成板；配方类型与原料不符时机器不会加工。"],
         tasks=[item("create:mechanical_press", title="动力冲压机")],
         rewards=[item("create:andesite_alloy", 16), xp(175), item("tfc:metal/ingot/wrought_iron", 12)])

ch.quest("deployer", 1.325, 14.325, "机械手", icon="create:deployer", deps=["finale_a", "brass"], shape="hexagon", hide_lines=True,
         size=1.25,
         desc=[
               "&6机械手&r接上旋转动力后，像玩家一样使用手持物品，也能给传送带或置物台上的半成品添加材料。",
               "",
               "&e制作：&r需要&6安山机壳、电子管与黄铜手&r；本包黄铜手有 TFC 砧上加工路线，详见 JEI。",
               "&e序列组装：&r让半成品依次经过部署、冲压等指定设备，完成规定的循环后才会产出成品。",
               "&c供料：&r原料通常会消耗；工具是否保留、是否损耗由配方决定，不要把所有手持物品都当成一次性材料。"],
         tasks=[item("create:deployer", title="机械手")],
         rewards=[item("create:andesite_alloy", 16), xp(225), item("tfc:metal/ingot/brass", 12)])

ch.quest("crushing_wheel", 3.525, 11.325, "粉碎轮", icon="create:crushing_wheel", deps=["mechanical_crafter", "brass_mechanism", "deployer"],
         desc=[
               "&o&7「两轮反向转，物品从中间进去。」&r",
               "",
               "&e制作：&r先准备&6动力合成器&r，再按 JEI 摆 &65×5&r 配方：硬化岩石、木板、安山合金，中心放&6TFC 黄铜机件&r。每次得到 &61 个粉碎轮&r，需要制作两次。",
               "&e安装：&r两只粉碎轮相对放置、反向旋转，物品从上方进入夹缝，产物从下方排出。按思索检查摆放。",
               "&c用途：&r本包没有通用的 TFC 矿石翻倍规则；先在 JEI 查该物品的粉碎配方，再决定是否加入产线。"],
         tasks=[item("create:crushing_wheel", 2, title="粉碎轮 ×2")],
         rewards=[item("tfc:brass_mechanisms", 6), xp(350), item("create:andesite_alloy", 24), item("tfc:metal/ingot/wrought_iron", 16)], hide_lines=True)

ch.quest("millstone", 3.525, 13.325, "石磨：风车磨面", icon="create:millstone", deps=["finale_a"], optional=True,
         shape="diamond",
         desc=[
               "&6机械石磨&r把旋转动力用于磨粉，适合接到小型动力网络中。",
               "",
               "&e制作：&r在&6TFC 手推磨&r上应用&6十字齿轮箱&r，得到机械石磨，详见 JEI。",
               "&e使用：&r从顶部投料，接上旋转动力，按思索安排成品提取。",
               "&c注意：&r石磨使用&6Create 研磨配方&r，手推磨能磨的物品与产率不一定能直接照搬，先检查 JEI。"],
         tasks=[item("create:millstone", title="机械石磨")],
         rewards=[item("create:shaft", 12), xp(125), item("create:andesite_alloy", 8)], hide_lines=True)

ch.quest("finale_b", 5.725, 12.325, "一条小小的自动化产线", icon="create:mechanical_press", deps=["crushing_wheel", "mixer", "press", "deployer"],
         shape="hexagon", size=1.25,
         desc=[
               "&a核心设备已齐：&r搅拌器、冲压机、机械手和粉碎轮。",
               "",
               "&e实践：&r选一条已确认的配方，用传送带与漏斗串起加工步骤，给材料入口和成品出口安排储存。",
               "&a检查：&r持续输入后机器不超载，半成品按顺序处理，副产物不会堵塞出口。能稳定处理一批材料，就能继续扩厂。"],
         tasks=[checkmark("我搭出了一条能自动运转的小产线")],
         rewards=[item("create:andesite_alloy", 32), xp(400), item("create:shaft", 24), item("create:cogwheel", 16)])
# ============================================================ D · 黄铜与精密零件
ch.quest("brass", 9.175, 10.45, "黄铜：Create 的高级合金", icon="tfc:metal/ingot/brass", deps=["finale_a"],
         shape="hexagon", size=1.25,
         desc=[
               "&o&7「铜与锌熔在一起，机器多了金色的骨架。」&r",
               "",
               "&6黄铜&r走 TFC 合金系统，按铜、锌的合金比例用&6小缸与坑窑或坩埚&r熔炼，再铸成锭。配比详见 JEI 的合金页。",
               "&e用途：&r黄铜机壳、黄铜手、扳手和黄铜机件都需要它。先在砧上做机件，就能启动后续机械合成路线。",
               "&a安排：&r黄铜材料与基础机器可以并行准备，后面的粉碎轮需要黄铜机件，别等产线全部搭好才开始炼黄铜。"],
         tasks=[item("tfc:metal/ingot/brass", 8, title="黄铜锭 ×8")],
         rewards=[item("tfc:metal/ingot/copper", 24), xp(200), item("tfc:powder/flux", 24)], hide_lines=True)

ch.quest("brass_casing", 11.375, 10.45, "黄铜机壳", icon="create:brass_casing", deps=["brass"],
         desc=[
               "&6黄铜机壳&r是高级机器的合成材料，也可用于整理传动装置的外观。",
               "",
               "&e制作：&r将&6去皮原木或去皮木块&r放下，手持&6黄铜锭&r右键应用。安山机壳、铜机壳也有相应的应用配方。",
               "&a用途：&r动力合成器需要黄铜机壳，先准备一批用于制作设备，再考虑包覆传动杆和齿轮。"],
         tasks=[item("create:brass_casing", 4, title="黄铜机壳 ×4")],
         rewards=[item("create:andesite_casing", 12), xp(150), item("tfc:metal/ingot/brass", 8)])

ch.quest("brass_mechanism", 9.175, 12.45, "黄铜零件：精密装置的核心", icon="tfc:brass_mechanisms", deps=["brass"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=[
               "&6TFC 黄铜机件&r是本包大量机械配方的标准零件。优先学会砧上制作，就能避免等待自动化设备。",
               "",
               "&e手工路线：&r&6黄铜杆&r在最低 &61 级砧&r上锻造，规则是&6冲压最后、击打倒数第二、冲压倒数第三&r，详见 JEI。",
               "&e自动化路线：&r黄铜杆经过弯曲，再依次部署&6黄铜雌蕊、铆钉、环和金属粒&r，整组循环 &62 次&r；成品有权重副产物。",
               "&c常见的坑：&r序列组装必须完成完整循环，操作一次不等于完成整条配方。初期用砧先做出粉碎轮需要的机件。"],
         tasks=[item("tfc:brass_mechanisms", 2, title="黄铜零件 ×2")],
         rewards=[item("tfc:metal/ingot/brass", 16), xp(250), item("create:andesite_alloy", 16)])

ch.quest("mechanical_crafter", 11.375, 12.45, "动力合成器", icon="create:mechanical_crafter", optional=False,
         shape="hexagon", deps=["brass_casing"],
         desc=[
               "&6动力合成器&r拼成合成网格，接上旋转动力后完成大型机械合成，粉碎轮就要用到它。",
               "",
               "&e制作：&r&6电子管 + 黄铜机壳 + 工作台&r，一次得到 &63 个&r，详见 JEI。",
               "&e搭建：&r按目标配方铺出网格，用扳手调整箭头，让各格材料汇合并从选定的边缘出口排出。出口不必位于中心。",
               "&a供料：&r先手动摆一轮材料试做，再接漏斗自动输入；复杂网格要留意空格与连接方向。"],
         tasks=[item("create:mechanical_crafter", 3, title="动力合成器 ×3")],
         rewards=[item("tfc:metal/ingot/brass", 16), xp(250), item("create:andesite_alloy", 16), item("tfc:metal/ingot/copper", 12)])

ch.quest("finale", 13.575, 11.45, "蒸汽与铁轨的前夜", icon="create:brass_casing", deps=["finale_b", "brass_mechanism"], any_dep=False,
         shape="gear", size=1.75,
         subtitle="从齿轮到工厂，只差一点蒸汽",
         desc=[
               "&o&7「齿轮把重复劳动接过去，工坊终于能够自己运转。」&r",
               "",
               "你已建立&6安山合金与黄铜材料线&r，掌握传动、动力源、搅拌、冲压、部署、粉碎和机械合成。",
               "&6继续研究：&r",
               "&7- &6动态结构（Contraption）&r：轴承、活塞等带动整片已连接的结构，用于升降机、旋转门等。",
               "&7- &6蒸汽动力&r：流体罐构成锅炉，需要持续供水和符合要求的热源，再由蒸汽引擎输出旋转。",
               "&7- &6列车与铁轨&r：前往交通章节了解车站、组装和路线规划。",
               "",
               "&a下一步：&r前往沉浸工程章节，学习发电、输电与大型工业设施。"],
         tasks=[checkmark("我已经掌握了机械动力的核心玩法")],
         rewards=[item("create:andesite_alloy", 48), item("tfc:brass_mechanisms", 8), levels(12), item("create:shaft", 32), item("tfc:metal/ingot/copper", 24)], hide_lines=True)

ch.section("第一节 · 安山合金：机械的起点", ["start", "melt_andesite", "andesite_ingot", "shaft", "cogwheel", "wrench"])
ch.section("第二节 · 第一份动力", ["water_wheel", "windmill", "hand_crank", "belt", "finale_a"])
ch.section("第三节 · 让动力干活", ["mixer", "press", "deployer", "crushing_wheel", "millstone", "finale_b"])
ch.section("第四节 · 黄铜与精密零件", ["brass", "brass_casing", "brass_mechanism", "mechanical_crafter", "finale"])
