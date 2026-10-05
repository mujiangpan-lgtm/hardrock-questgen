def mek(st):
    sc = st["scene"]
    L = sc["layers"]
    for i in range(5, 17):
        L[i]["alpha"] = 0
    for i in range(20, 26):
        L[i]["alpha"] = 0
    sc["shadow"] = 0.6
    sc["light"] = {"dir": [-1, -1], "color": [170, 255, 180], "tint": 0.08, "rim": 0.5, "shade": 0.3}
    L.insert(17, {"motif": "blocks", "x": 0.22, "y": 0.62, "w": 15, "h": 18,
                  "rows": ["SPS", "SCS", "SVS", "SSS"], "k": 6,
                  "legend": {"S": "mekanism:block/block_steel", "P": "mekanism:block/induction_port",
                             "C": "mekanism:block/basic_induction_cell",
                             "V": "mekanism:block/basic_induction_provider"}})
    cas = "mekanism:block/steel_casing"
    L.append({"motif": "blocks", "x": 0.77, "y": 0.74, "w": 15, "h": 10, "k": 6,
              "rows": ["abc", "def"],
              "legend": {c: {"front": f, "top": cas, "side": cas} for c, f in zip("abcdef", [
                  "mekanism:block/combiner/front_active", "mekanism:block/osmium_compressor/front_active",
                  "mekanism:block/chemical_injection_chamber/front_active",
                  "mekanism:block/energized_smelter/front_active",
                  "mekanism:block/factory/enriching/enriching_factory_front_active",
                  "mekanism:block/crusher/front_active"])}})


def welcome(st):
    sc = st["scene"]
    sc["pixelate"] = 4
    sc["texel"] = 6
    sc["shadow"] = 0.5
    sc["light"] = {"dir": [-1, -0.3], "color": [255, 210, 150], "tint": 0.1, "rim": 0.5, "shade": 0.3}
    sc["lights"] = [{"x": 0.2, "y": 0.6, "radius": 0.2, "strength": 0.6, "color": [255, 190, 120]}]


PATCH = {"mekanism": mek, "00_welcome": welcome}
