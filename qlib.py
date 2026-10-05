"""Tiny DSL for authoring FTB Quests (1.20.1 / 2001.x) chapters in Python.

Usage in questgen/chapters/<name>.py:

    from qlib import *
    ch = Chapter("stone_age", "石器时代", icon="tfc:stone/axe/sedimentary",
                 group="ages", order=0, theme="stone",
                 subtitle="以石为刃，以火为伴")
    ch.quest("rocks", 0, 0, "捡起石头", icon="tfc:rock/loose/granite",
             desc=["...", "..."],
             tasks=[tag("tfc:rock_knapping", 4, title="任意岩石")],
             rewards=[item("minecraft:bread", 4)],
             deps=["other_key", "copper_age:anvil"], shape="hexagon", size=1.5)
    ch.section("第一节 · 石与火", ["rocks", "sticks", ...])

Ids are derived deterministically from chapter/quest keys, so re-running the
build never breaks player progress as long as keys stay the same.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
_RAW = json.loads((HERE / "registry.json").read_text("utf-8"))
_REG = _RAW["items"]
_PROB = _RAW.get("probable", {})
_TAGS = set(_RAW.get("tags", []))
_HIDDEN = set(_RAW.get("hidden", []))
ERRORS: list[str] = []
WARNINGS: list[str] = []

# primary (panel fill), accent (border/title), text glow
THEMES = {
    "guide":    ((40, 44, 52), (230, 200, 120)),
    "survival": ((44, 38, 30), (214, 168, 96)),
    "food":     ((30, 48, 30), (150, 210, 110)),
    "stone":    ((48, 44, 40), (196, 180, 156)),
    "copper":   ((56, 34, 24), (230, 140, 80)),
    "bronze":   ((52, 42, 20), (226, 186, 90)),
    "iron":     ((34, 38, 46), (176, 190, 210)),
    "steel":    ((26, 30, 40), (130, 170, 220)),
    "create":   ((50, 40, 22), (240, 196, 90)),
    "ie":       ((48, 30, 20), (232, 120, 50)),
    "tfmg":     ((36, 36, 36), (200, 200, 120)),
    "pneumatic":((26, 40, 44), (110, 200, 210)),
    "mekanism": ((20, 36, 46), (90, 200, 240)),
    "storage":  ((34, 30, 50), (170, 150, 230)),
    "transport":((22, 38, 52), (110, 170, 230)),
    "explore":  ((46, 26, 26), (220, 100, 90)),
    "twilight": ((22, 40, 34), (120, 220, 170)),
    "space":    ((16, 16, 40), (170, 140, 255)),
}


# ---------------------------------------------------------------- SNBT types
class D(float):
    """double -> 1.0d"""


class L(int):
    """long -> 5L"""


class B(int):
    """byte -> 1b"""


class Fl(float):
    """float -> 0.0f"""


def hid(*parts: str) -> str:
    h = int(hashlib.sha1("|".join(parts).encode()).hexdigest()[:16], 16)
    h &= 0x7FFFFFFFFFFFFFFF
    h |= 0x1000000000000000  # never zero / never tiny
    return f"{h:016X}"


# ---------------------------------------------------------------- items
def _check(iid: str):
    if iid in _HIDDEN:
        ERRORS.append(f"item is hidden/disabled by the pack (kubejs hide.js): {iid}")
    if iid in _REG:
        return
    if iid in _PROB:
        WARNINGS.append(f"item id only found via lang key (probably fine): {iid}")
    else:
        ERRORS.append(f"unknown item id: {iid}")


def name(iid: str) -> str:
    """Localized name from registry (handy in descriptions)."""
    return _REG.get(iid) or _PROB.get(iid) or iid


def stack(iid: str, nbt: dict | None = None) -> dict:
    _check(iid)
    s = {"Count": B(1) if False else 1, "id": iid}
    if nbt:
        s["tag"] = nbt
    return s


@dataclass
class Item:
    iid: str | None
    count: int = 1
    title: str | None = None
    nbt: dict | None = None
    tag_value: str | None = None
    consume: bool = False

    def stack(self) -> dict:
        if self.tag_value:
            return {"Count": 1, "id": "itemfilters:tag", "tag": {"value": self.tag_value}}
        return stack(self.iid, self.nbt)


def item(iid: str, count: int = 1, title: str | None = None, nbt: dict | None = None, consume=False) -> Item:
    return Item(iid, count, title, nbt, consume=consume)


def tag(tag_value: str, count: int = 1, title: str | None = None) -> Item:
    if tag_value not in _TAGS:
        ERRORS.append(f"unknown item tag: #{tag_value}")
    if not title:
        WARNINGS.append(f"tag task without title: {tag_value}")
    return Item(None, count, title, tag_value=tag_value)


# ---------------------------------------------------------------- tasks / rewards
@dataclass
class Task:
    data: dict


def checkmark(title: str | None = None) -> Task:
    d = {"type": "checkmark"}
    if title:
        d["title"] = title
    return Task(d)


def dimension(dim: str, title: str | None = None) -> Task:
    d = {"type": "dimension", "dimension": dim}
    if title:
        d["title"] = title
    return Task(d)


def kill(entity: str, count: int = 1, title: str | None = None) -> Task:
    d = {"type": "kill", "entity": entity, "value": L(count)}
    if title:
        d["title"] = title
    return Task(d)


def advancement(adv: str, title: str | None = None) -> Task:
    d = {"type": "advancement", "advancement": adv, "criterion": ""}
    if title:
        d["title"] = title
    return Task(d)


def biome(b: str, title: str | None = None) -> Task:
    d = {"type": "biome", "biome": b}
    if title:
        d["title"] = title
    return Task(d)


@dataclass
class Reward:
    data: dict


def xp(amount: int) -> Reward:
    return Reward({"type": "xp", "xp": amount})


def levels(amount: int) -> Reward:
    return Reward({"type": "xp_levels", "xp_levels": amount})


# ---------------------------------------------------------------- chapter
@dataclass
class Quest:
    key: str
    x: float
    y: float
    title: str
    subtitle: str | None = None
    desc: list[str] = field(default_factory=list)
    tasks: list = field(default_factory=list)
    rewards: list = field(default_factory=list)
    deps: list[str] = field(default_factory=list)
    icon: str | dict | None = None
    shape: str | None = None
    size: float = 1.0
    optional: bool = False
    any_dep: bool = False  # only one dependency needed
    hide_lines: bool = False


@dataclass
class Section:
    title: str
    keys: list[str]
    pad: float = 0.7


CHAPTERS: dict[str, "Chapter"] = {}


class Chapter:
    def __init__(self, key, title, icon, group="", order=0, theme="guide",
                 subtitle: str | list[str] = "", default_shape="circle"):
        self.key, self.title, self.icon = key, title, icon
        self.group, self.order, self.theme = group, order, theme
        self.subtitle = [subtitle] if isinstance(subtitle, str) and subtitle else (subtitle or [])
        self.default_shape = default_shape
        self.quests: dict[str, Quest] = {}
        self.sections: list[Section] = []
        self.extra_images: list[dict] = []
        self.autofocus: str | None = None
        CHAPTERS[key] = self

    def quest(self, key, x, y, title, **kw) -> Quest:
        if key in self.quests:
            ERRORS.append(f"{self.key}: duplicate quest key {key}")
        q = Quest(key, x, y, title, **kw)
        self.quests[key] = q
        if self.autofocus is None:
            self.autofocus = key
        return q

    def section(self, title: str, keys: list[str], pad: float = 0.7):
        self.sections.append(Section(title, keys, pad))

    def image(self, image: str, x, y, w, h, hover=None, click=None):
        img = {"image": image, "x": D(x), "y": D(y), "width": D(w), "height": D(h), "rotation": D(0)}
        if hover:
            img["hover"] = hover if isinstance(hover, list) else [hover]
        if click:
            img["click"] = click
        self.extra_images.append(img)

    def qid(self, ref: str) -> str:
        if ":" in ref:
            ck, qk = ref.split(":", 1)
        else:
            ck, qk = self.key, ref
        return hid("quest", ck, qk)
