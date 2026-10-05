from qlib import *

ch = Chapter("pneumatic", "气动工艺", icon="pneumaticcraft:air_compressor", group="industry", order=3,
             theme="pneumatic", subtitle="压缩空气里，藏着下一代工业的血管")

# ============================================================ A · 压缩铁与压力室
ch.quest("start", 1.45, 2.35, "压缩铁：一切的起点", icon="pneumaticcraft:ingot_iron_compressed", shape="gear", size=1.5,
         deps=["steel_age:finale"],
         subtitle="PneumaticCraft：Repressurized 的大门",
         desc=["&o&7「让锻铁经历一次爆炸，才有资格关住下一次爆炸。」&r",
               "",
               "&6气动工艺&r围绕压缩空气运作：压缩机产生空气，管道连接设备，压力室消耗空气加工材料。",
               "&c本包的压缩铁配方已经修改。&r起始材料是&6锻铁双锭&r，不能拿普通铁锭照搬原版。",
               "",
               "&e1.&r 把锻铁双锭丢在地上，在安全位置引爆 TNT 等爆炸，得到第一批压缩铁锭；配方损耗率为&633%&r，先做少量试验。",
               "&e2.&r 建好压力室后，以&62 bar&r把一枚锻铁双锭加工成一枚压缩铁锭，避开爆炸损耗。",
               "",
               "&a先准备钢砧：&r压缩铁板、线材与网要走本包的 TFC 锻造链，压力室外壳也要用它们。按 R 查看 JEI 配方树，准备足够的锻铁双锭。"],
         tasks=[item("pneumaticcraft:ingot_iron_compressed", 8, title="压缩铁锭 ×8")],
         rewards=[item("tfc:metal/ingot/wrought_iron", 24), xp(100), item("tfc:metal/ingot/copper", 8)])

ch.quest("reinforced", 3.65, 2.35, "强化石与压力室墙壁", icon="pneumaticcraft:reinforced_bricks", deps=["start"],
         desc=["&6强化石与强化砖&r是压力设备的基础建材，本包改成了&6Create 物品应用&r。",
               "",
               "&7- 石头 + &6压缩铁网&r → 强化石",
               "&7- 石砖 + &6压缩铁网&r → 强化砖",
               "",
               "&e起步做网：&r先锻出压缩铁线，在&6钢级或更高的砧&r上焊接两根线，一次得到&64 张压缩铁网&r。压力室建成后还有 4.5 bar 的加工路线。",
               "&c常见的坑：&r本包的强化砖不是把四块强化石拼在一起。使用 JEI 所列的石砖与网完成物品应用，机械手可以自动化这一步。"],
         tasks=[item("pneumaticcraft:reinforced_bricks", 16, title="强化砖 ×16")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 12), xp(150), item("minecraft:glass", 16)])

ch.quest("pc_wall", 5.85, 2.35, "压力室墙壁与玻璃", icon="pneumaticcraft:pressure_chamber_wall", deps=["reinforced"],
         desc=["&e本包的外壳配方：&r",
               "",
               "&7- &6强化砖 + 压缩铁板&r → 压力室墙壁",
               "&7- &6玻璃 + 压缩铁板&r → 压力室玻璃",
               "",
               "两者都是&6Create 物品应用&r。压缩铁板来自压缩铁双锭的 TFC 砧加工，钢级砧即可制作；也可查看本包其它加工配方。",
               "&a建议：&r最小压力室总共占 27 格，其中 1 格是空腔，外壳共 26 格；阀门和接口会替换部分外壳。此任务要求多备一些墙壁，留作扩建。"],
         tasks=[item("pneumaticcraft:pressure_chamber_wall", 27, title="压力室墙壁 ×27")],
         rewards=[item("minecraft:glass", 24), xp(150), item("pneumaticcraft:ingot_iron_compressed", 16)])

ch.quest("pc_valve", 8.05, 2.35, "压力室阀门与接口", icon="pneumaticcraft:pressure_chamber_valve", deps=["pc_wall", "pressure_tube"], hide_lines=True,
         desc=["&6压力室阀门&r负责连接外部气源，&c每个压力室至少一个&r。本包用&6机械手&r把一根压力管道部署到压力室墙壁上，制成阀门。",
               "",
               "&6压力室接口&r用于进出料：以&6漏斗 + 压力室墙壁&r完成 Create 物品应用。建议做两个，外侧&6蓝色&r用于输入，外侧&6橙色&r用于输出。",
               "&e自动化：&r用漏斗或物品管道把原料送入输入接口；输出接口可把产物推入相邻容器。界面里可设置输出过滤。",
               "",
               "&c开盖会泄压：&r手动拆墙放料可以起步，但连续加工时应使用接口，每次进出料也会消耗空气。"],
         tasks=[item("pneumaticcraft:pressure_chamber_valve", title="压力室阀门")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 16), xp(175), item("minecraft:redstone", 16)])

ch.quest("pc_build", 10.25, 2.35, "搭建压力室", icon="pneumaticcraft:pressure_chamber_wall", deps=["pc_valve"],
         shape="hexagon", size=1.25,
         desc=["&6压力室&r是一个&c空心&r的多方块结构：",
               "&71.&r 外部尺寸为&63×3×3、4×4×4 或 5×5×5&r立方体。",
               "&72.&r 棱与角使用压力室墙壁或压力室玻璃。",
               "&73.&r 面上还可以安装阀门和接口，至少一个阀门；一进一出的两个接口更方便。",
               "",
               "&a最小结构：&r3×3×3 共 27 格，中央留空，&626 格外壳&r中替换一格为阀门、两格为接口。",
               "&e检查：&r打开阀门界面确认结构有效，再把压缩机连到阀门。气源和管道的耐压上限也要一起检查。"],
         tasks=[checkmark("我已经搭好了一座压力室")],
         rewards=[item("pneumaticcraft:pressure_chamber_wall", 24), xp(300), item("pneumaticcraft:ingot_iron_compressed", 24), item("minecraft:coal", 32)])

ch.quest("manual_compressor", 12.45, 2.35, "手摇压缩机：第一口气", icon="pneumaticcraft:pressure_tube",
         deps=["pc_build"],
         desc=["&6手摇压缩机&r不需要燃料，适合首次充气或紧急补气。配方是&6石质底座、压力管道、压缩铁齿轮×2、压缩铁锭×1、红色染料×2&r，摆法详见 JEI。",
               "",
               "&e用法：&r连接压力管道或压力室阀门，右键摇动手柄产生空气，留意压力表变化。",
               "&a后续升级：&r需要持续生产时，改用烧固体燃料的空气压缩机，或查看旋转压缩机等其它气源。"],
         tasks=[item("pneumaticcraft:manual_compressor", title="手摇压缩机")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 12), xp(125), item("minecraft:coal", 16)])
# ============================================================ B · 管道与压缩机
ch.quest("pressure_tube", 15.65, 4.1, "压力管道", icon="pneumaticcraft:pressure_tube", deps=["start"], hide_lines=True,
         desc=["&6压力管道&r连接压缩机、压力室和各类气动设备。本包有两条制作路线：",
               "",
               "&7- &6TFC 砧加工&r：压缩铁板在&6钢级砧&r上以两次弯曲收尾，做一根管道。",
               "&7- &6Create 接续组装&r：压缩铁板滚压两次、冲压三次，一轮得到三根管道。",
               "",
               "&c漏气与超压：&r未连接的管端会漏气，能听到嘶声并看到粒子。用扳手关闭多余开口；普通压力管道属于&65 bar&r档，不能直接接高压网络。"],
         tasks=[item("pneumaticcraft:pressure_tube", 16, title="压力管道 ×16")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 12), xp(125), item("minecraft:glass", 16)])

ch.quest("air_compressor", 17.85, 4.1, "空气压缩机", icon="pneumaticcraft:air_compressor", deps=["pressure_tube"],
         shape="hexagon", size=1.25,
         desc=["&6空气压缩机&r使用固体燃料持续产生压缩空气。配方为&6强化石砖类材料×6、熔炉×1、压力管道×1&r，摆法详见 JEI。",
               "",
               "&e用法：&r把燃料放入压缩机界面的燃料槽，接好管道，空气会向较低压力的设备流动并逐渐平衡。",
               "&c常见的坑：&r普通空气压缩机不接受岩浆桶等液体燃料；停工时仍可能继续充气。用红石控制或安全模块限制压力，别让管网进入压力表红区。"],
         tasks=[item("pneumaticcraft:air_compressor", title="空气压缩机")],
         rewards=[item("minecraft:coal", 64), xp(250), item("pneumaticcraft:ingot_iron_compressed", 16)])

ch.quest("pressure_gauge", 20.05, 2.1, "压力表：看懂数字", icon="pneumaticcraft:pressure_gauge", deps=["air_compressor"],
         optional=True, shape="diamond",
         desc=["&6压力表&r是安装在&6压力管道&r上的模块，可显示管内压力，并输出与压力有关的红石信号。机器自身的界面也有压力条。",
               "",
               "&6压力&r = 储存空气量 / 容积 - 1，0 bar 代表大气压。多数机器有最低工作压力；压力表红色区域表示存在爆炸风险。",
               "&a安装后观察：&r加工和接口出料都会消耗空气，压力低于配方要求时应补气；关闭气源、留好控制，再离开产线。"],
         tasks=[item("pneumaticcraft:pressure_gauge", 2, title="压力表 ×2")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 8), xp(100), item("minecraft:redstone", 16)])

ch.quest("air_canister", 20.05, 4.1, "空气罐：便携气源", icon="pneumaticcraft:air_canister", deps=["air_compressor"],
         desc=["&6空气罐&r是气动工具的合成部件，也能储存压缩空气。配方是&6压力管道×1、压缩铁锭×4、红石×2&r，详见 JEI。",
               "",
               "&e充气方法：&r制作&6充能站&r并接入气源，把空气罐或气动工具放入站内充气。充能站与物品会平衡压力，因此气源压力不足时也无法充满。",
               "&a工具升级也在这里：&r把工具放入充能站，点击物品槽上方的升级按钮。空气罐用于合成时会保留其中的空气，成品仍可继续在站内充气。"],
         tasks=[item("pneumaticcraft:air_canister", 2, title="空气罐 ×2")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 12), xp(150), item("minecraft:redstone", 16)])

ch.quest("heat_concept", 20.05, 6.1, "热：气动工艺的隐藏变量", icon="minecraft:furnace", deps=["air_compressor"],
         optional=True, shape="diamond",
         desc=["气动工艺有自己的&6热量系统&r。热量从高温设备传向低温设备，只会在支持这套系统的相邻方块之间传递。",
               "",
               "&7- 岩浆、火、岩浆块等可提供热量，但部分热源会冷却或熄灭。",
               "&7- &6涡流管&r可把压缩空气转成热端与冷端，注意散热。",
               "&7- &6压缩铁块与热管&r可以传热，热沉帮助散热。",
               "",
               "&a实际用途：&r蚀刻槽加热后加工更快；不同机器需要的温度不同。用界面读数和 PneumaticCraft 手册确认，不要把任意 TFC 高温设备都当作可用热源。"],
         tasks=[checkmark("我了解了气动工艺的热系统")],
         rewards=[item("minecraft:coal", 16), xp(75), item("tfc:metal/ingot/copper", 8)])
# ============================================================ C · 塑料与印刷电路板
ch.quest("plastic", 1.2, 11.2, "塑料：电路板的新原料", icon="pneumaticcraft:plastic", deps=["air_compressor"],
         hide_lines=True,
         desc=["&6塑料&r是空白电路板的核心材料。本包的熔融塑料与 TFMG 化工链相通，可以按已有产线选路线。",
               "",
               "&7- &6热气动处理工厂&r：100 mB LPG + 煤，或 100 mB 生物柴油 + 木炭，在&6100℃及以上&r加工成 1000 mB 熔融塑料，另有沥青副产物。",
               "&7- &6TFMG 加热化学缸&r：焦炭粉与乙烯或丙烯加工成熔融塑料，数量及设备配置详见 JEI。",
               "",
               "&e本任务需要气动塑料物品：&r熔融塑料倒入世界会凝固成&6pneumaticcraft:plastic&r，也有热框架冷却路线。TFMG 铸造台产出的塑料片是另一个物品，不能直接拿来完成本任务。",
               "&c注意：&r本包删除了气动炼油厂，不能照原版手册先搭它取 LPG。燃料与化工原料来源应继续追查本包 JEI。"],
         tasks=[item("pneumaticcraft:plastic", 4, title="塑料锭 ×4")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 24), xp(200), item("minecraft:redstone", 24)])

ch.quest("empty_pcb", 3.4, 11.2, "空白电路板", icon="pneumaticcraft:empty_pcb", deps=["plastic", "pc_build"], hide_lines=True,
         shape="hexagon", size=1.25,
         desc=["在&6压力室&r中以&61.5 bar&r处理以下材料，一次得到&63 片空白电路板&r：",
               "&7- 红石火把×2",
               "&7- &6气动布线标签&r内的线材×3（可用材料按 JEI 展开标签）",
               "&7- 气动塑料×1",
               "",
               "&6空白电路板&r需要曝光和蚀刻，变成&6未组装的电路板&r。更高级的装配激光也能完成这一转换；先走下面的化学路线入门。"],
         tasks=[item("pneumaticcraft:empty_pcb", 3, title="空白电路板 ×3")],
         rewards=[item("minecraft:redstone", 32), xp(250), item("pneumaticcraft:plastic", 12), item("pneumaticcraft:ingot_iron_compressed", 16)])

ch.quest("uv_etch", 5.6, 11.2, "紫外线灯箱与蚀刻槽", icon="pneumaticcraft:uv_light_box", deps=["empty_pcb"],
         desc=["&e化学蚀刻流程：&r",
               "&e1.&r 制作紫外线灯箱，放入空白电路板，接好压缩空气。&c本包灯箱配方已改&r，需要荧石粉、干净紫水晶粉、电路板蓝图等，详见 JEI。",
               "&e2.&r 等待曝光；无速度升级时完整曝光最多需要&610 分钟&r。曝光越完整，蚀刻成功率越高，完整曝光对应 100% 成功率。",
               "&e3.&r 把曝光后的板放入装有&6蚀刻酸&r的蚀刻槽。无加热时约&6150 秒&r，加热可缩短至最快&630 秒&r，但会额外消耗少量蚀刻酸。",
               "",
               "&e回收失败板：&rJEI 有失败电路板的高炉熔炼配方，可还原成空白板；这是原版高炉加工类型，&c不是本包被禁用的 IE 多方块高炉&r。",
               "&a稳定生产：&r先等完整曝光，再蚀刻，留好酸液与空气补给。"],
         tasks=[item("pneumaticcraft:unassembled_pcb", title="未组装的电路板")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 24), xp(300), item("pneumaticcraft:etching_acid_bucket", 4)])

ch.quest("assembly_laser", 7.8, 10.2, "装配激光：更快的电路板", icon="pneumaticcraft:unassembled_pcb",
         deps=["uv_etch"], optional=True, shape="diamond",
         desc=["&6装配激光&r能把空白电路板直接加工成未组装电路板，不需要紫外曝光和化学蚀刻。",
               "",
               "&e装配系统：&r准备控制器、平台、激光以及一进一出的&6两个装配 IO 单元&r，按手册摆放相邻设备；激光必须紧挨平台，IO 单元要能碰到平台和容器。",
               "&e运行：&r给控制器供气，插入激光程序，将空白电路板放入输入容器。界面诊断会提示缺失设备或连接问题。",
               "",
               "&a先了解即可：&r这条路线需要更多设备投入，等初始电路板产线稳定后再建设。配方与程序详见 JEI 和手册「装配系统」。"],
         tasks=[checkmark("我了解了装配系统这条捷径")],
         rewards=[item("minecraft:redstone", 16), xp(125), item("pneumaticcraft:plastic", 8)])

ch.quest("pcb_final", 7.8, 12.2, "成品电路板", icon="pneumaticcraft:printed_circuit_board", deps=["uv_etch"],
         desc=["&6未组装的电路板&r居中，上下放&6晶体管×2&r，左右放&6电容器×2&r，合成成品电路板。",
               "&c本包使用电子元件标签：&r气动原版晶体管与电容器的压力室配方已删除，实际可用元件来自本包其它电子产线，按 JEI 展开标签确认。",
               "",
               "&6成品电路板&r用于高阶气动设备和装备；&6RS 处理器&r接续组装用的是&6未组装电路板&r，所以两种板都要保留库存。"],
         tasks=[item("pneumaticcraft:printed_circuit_board", title="成品电路板")],
         rewards=[item("tfmg:capacitor_item", 8), xp(350), item("tfmg:transistor_item", 8), item("pneumaticcraft:ingot_iron_compressed", 24)])
# ============================================================ D · 处理器产线：通往数字仓库
ch.quest("binding", 11.125, 10.325, "处理器粘合物：压力室的新配方", icon="pneumaticcraft:pressure_chamber_wall", hide_lines=True,
         deps=["pc_build"], shape="hexagon", size=1.25,
         desc=["&6处理器粘合物&r是本包 RS 半成品处理器的材料，制作路线接在压力室后面。",
               "",
               "压力室以&62 bar&r处理&6线×2 + 粘液球×1&r，一次产出&66 个处理器粘合物&r。可用线材和粘液替代物以 JEI 标签为准。",
               "",
               "&a批量准备：&r每个未处理处理器都要消耗一个粘合物，先做一批再安排其它配方，注意出料接口过滤。"],
         tasks=[item("refinedstorage:processor_binding", 6, title="处理器粘合物 ×6")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 16), xp(200), item("tfc:metal/ingot/wrought_iron", 16)])

ch.quest("raw_processor", 13.325, 10.325, "未处理基础处理器", icon="refinedstorage:processor_binding", deps=["binding"],
         shape="hexagon", size=1.25,
         desc=["压力室以&62 bar&r处理以下材料，得到&61 个未处理基础处理器&r：",
               "&7- 处理器粘合物×1",
               "&7- 铁粉×1",
               "&7- 硅×1（来源见「仓储与物流 · 硅与富石英铁」）",
               "&7- 红石×1",
               "",
               "&e下一步在仓储章节：&r以&6未组装电路板&r为起始件，用 Create 机械手依次装上&6未处理基础处理器、铜线、红石、铜线&r，最后冲压，得到基础处理器。",
               "&c两条产线要汇合：&r只做这个半成品还不够，紫外曝光与蚀刻得到的未组装板同样不可少。"],
         tasks=[item("refinedstorage:raw_basic_processor", title="未处理基础处理器")],
         rewards=[item("minecraft:redstone", 32), xp(275), item("refinedstorage:processor_binding", 24), item("tfc:metal/ingot/copper", 16)])
# ============================================================ E · 装备与自动化（选修）
ch.quest("pneumatic_wrench", 16.65, 10.2, "气动扳手", icon="pneumaticcraft:pneumatic_wrench", deps=["pcb_final"], hide_lines=True,
         optional=True, shape="diamond",
         desc=["&6气动扳手&r自身需要在&6充能站&r充气，使用时消耗储存的空气。",
               "",
               "&7- &e右键&r方块：旋转支持旋转的方块。",
               "&7- &e潜行右键&r气动机器：收回机器，保留内部升级和空气。",
               "&7- &e右键&r压力管道：关闭或重新打开连接段，隔离管网、处理漏气。",
               "",
               "&a维护时先隔离气源：&r保留机器里的空气并不等于能随意拆开带压管网。确认连接和压力后再重新接通。"],
         tasks=[item("pneumaticcraft:pneumatic_wrench", title="气动扳手")],
         rewards=[item("pneumaticcraft:air_canister", 2), xp(175), item("pneumaticcraft:ingot_iron_compressed", 16)])

ch.quest("pneumatic_armor", 16.65, 12.2, "气动盔甲与升级", icon="pneumaticcraft:pneumatic_helmet", hide_lines=True,
         deps=["pcb_final", "air_canister"], optional=True, shape="diamond",
         desc=["&6气动盔甲&r由压缩铁盔甲件、成品电路板和空气罐等材料合成，各部件用量详见 JEI。它需要持续补充压缩空气才能使用各项能力。",
               "",
               "&e安装升级：&r把盔甲放进&6充能站&r，点击物品槽上方的升级按钮。升级界面会列出该部件支持的升级与效果。",
               "&a按部件选择：&r头盔可装实体追踪、方块追踪等；喷气靴等能力属于其它部件。安装后用控制设置里的气动盔甲选项键调整开关。",
               "&c常见的坑：&r只有头盔不能直接获得飞行能力。升级矩阵是升级件的制作材料，实际安装操作在充能站完成。"],
         tasks=[item("pneumaticcraft:pneumatic_helmet", title="气动头盔")],
         rewards=[item("pneumaticcraft:air_canister", 3), xp(300), item("firstaid:bandage", 12), item("pneumaticcraft:ingot_iron_compressed", 24)])

ch.quest("drone_intro", 16.65, 14.2, "编程器与无人机", icon="pneumaticcraft:programmable_controller", hide_lines=True,
         deps=["pcb_final"], optional=True, shape="diamond",
         desc=["&6无人机&r是可编程的飞行机器人，能执行挖掘、搬运、种植等自动化动作。它需要先写入程序并充气。",
               "",
               "&e入门：&r制作&6编程器&r，在界面里拼接程序拼块；把无人机放入无人机槽，写入程序，再用充能站补气后放出。编程器本身不需要压力。",
               "&a建立补气点：&r装有发射器升级的充能站可以给无人机补气，供气不足时无人机无法继续工作。",
               "&c可编程控制器&r是另一类设备，不是安装到无人机身上的必需部件。具体程序和调试方法详见手册「编程」。"],
         tasks=[item("pneumaticcraft:drone", title="无人机")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 24), xp(300), item("pneumaticcraft:plastic", 16), item("minecraft:redstone", 24)])

ch.quest("finale", 18.85, 12.2, "压力之上，数据之下", icon="pneumaticcraft:advanced_air_compressor", hide_lines=True,
         deps=["raw_processor", "pcb_final", "air_compressor"], shape="gear", size=1.75,
         subtitle="下一步：把这些半成品接进 Refined Storage 的产线",
         desc=["&o&7「空气把原料压成半成品，机械手再把它们接成数据。」&r",
               "",
               "你已经走通了&6压力室与气源&r、&6未组装电路板与成品板&r、&6处理器粘合物与未处理基础处理器&r三条基础链。",
               "",
               "&a下一步：&r打开「仓储与物流」章节，把未组装板和半成品处理器送上&6Create 接续组装&r产线，装入铜线、红石并冲压，做出数字仓库所需的基础处理器。"],
         tasks=[checkmark("我已经打通了气动工艺的基础产线")],
         rewards=[item("pneumaticcraft:ingot_iron_compressed", 64), item("refinedstorage:processor_binding", 32), levels(16), item("pneumaticcraft:plastic", 24), item("pneumaticcraft:pressure_tube", 24)])

ch.section("第一节 · 压缩铁与压力室", ["start", "reinforced", "pc_wall", "pc_valve", "pc_build", "manual_compressor"])
ch.section("第二节 · 管道与压缩机", ["pressure_tube", "air_compressor", "pressure_gauge", "air_canister", "heat_concept"])
ch.section("第三节 · 塑料与印刷电路板", ["plastic", "empty_pcb", "uv_etch", "assembly_laser", "pcb_final"])
ch.section("第四节 · 处理器产线", ["binding", "raw_processor"])
ch.section("第五节 · 装备与自动化", ["pneumatic_wrench", "pneumatic_armor", "drone_intro", "finale"])
