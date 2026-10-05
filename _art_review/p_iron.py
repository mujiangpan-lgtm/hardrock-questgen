def iron(st):
    sc = st["scene"]
    L = sc["layers"]
    sc["texel"] = 5
    sc["shadow"] = 0.55
    sc["light"] = {"dir": [1, -0.2], "color": [255, 160, 90], "tint": 0.12, "rim": 0.7, "shade": 0.35}
    sc["lights"] = [{"x": 0.8, "y": 0.72, "radius": 0.3, "strength": 0.8, "color": [255, 140, 70]},
                    {"x": 0.5, "y": 0.78, "radius": 0.18, "strength": 0.6, "color": [255, 150, 70]}]
    sc["ambient"] = 0.85
    L[16]["arrange"] = "pile"
    L[26]["arrange"] = "scatter"
    L[28]["pixelate"] = 5
    L[28]["colors"] = 10
    for i in (6, 7, 9):  # chains hang: no contact shadow, a drop shadow on the wall
        L[i]["shadow"] = 0
    for i in (8, 10, 12, 13, 14, 15):
        L[i]["shadow"] = 0
        L[i]["drop"] = 0.5
    blocks = {"motif": "blocks", "x": 0.8, "y": 0.6, "w": 6, "h": 22,
              "rows": ["G", "G", "G", "B"],
              "legend": {"G": "tfc:block/rock/bricks/gabbro",
                         "B": {"front": "tfc:block/devices/bloomery/on", "top": "tfc:block/rock/bricks/gabbro",
                               "side": "tfc:block/rock/bricks/gabbro"}},
              "alpha": 1.0}
    for i in (19, 20, 21, 22):
        L[i]["alpha"] = 0
    L.insert(23, blocks)


PATCH = {"iron_age": iron}
