def climate(st):
    sc = st["scene"]
    L = sc["layers"]
    for l in L:
        if l["motif"] == "lightning":
            l["width"] = 1.4
            l["flash"] = 0.6
        if l["motif"] == "sun":
            l["alpha"] = 0
    sc["texel"] = 5
    sc["shadow"] = 0.5
    sc["light"] = {"dir": [1, -1], "color": [190, 220, 255], "tint": 0.15, "rim": 0.6, "shade": 0.3}


def bronze(st):
    sc = st["scene"]
    L = sc["layers"]
    sc["light"] = {"dir": [-1, -0.6], "color": [255, 220, 170], "tint": 0.08, "rim": 0.5, "shade": 0.25}
    sc["shadow"] = 0.5
    sc["texel"] = 5
    for l in L:
        if l["motif"] == "tree":
            l["haze"] = 0.35
            l["haze_color"] = [30, 52, 50]
        if l["motif"] in ("anvil", "mine_entrance"):
            l["lit"] = True
        if l["motif"] == "sprite_row":
            l["arrange"] = "pile"
    L.insert(2, {"motif": "light_rays", "x": 0.35, "y": 0.4, "w": 40, "h": 30, "color": [230, 220, 170],
                 "alpha": 0.35, "src": [0.05, 0.02], "angle": 50, "spread": 30, "count": 6})


def steel(st):
    sc = st["scene"]
    for l in sc["layers"]:
        if l["motif"] == "sprite_row":
            l["arrange"] = "scatter"


PATCH = {"climate": climate, "bronze_age": bronze, "steel_age": steel}
