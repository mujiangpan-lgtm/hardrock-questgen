def stone(st):
    for l in st["scene"]["layers"]:
        if l["motif"] == "campfire":
            l["pixelate"] = 4
            l["colors"] = 16
        if l["motif"] == "arrowhead":
            l["pixelate"] = 4
            l["outline"] = 0.8


def farming(st):
    for l in st["scene"]["layers"]:
        if l["motif"] == "tree":
            l["pixelate"] = 4
            l["outline"] = 0.6
        if l["motif"] == "livestock":
            l["pixelate"] = 3


PATCH = {"stone_age": stone, "farming": farming}
