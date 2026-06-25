from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar
from BaseClasses import Region
from rule_builder.rules import Has
from worlds.splasher.options import IncludeKeys
from worlds.splasher.utils import SplasherUtils 

if TYPE_CHECKING:
    from .world import SplasherWorld

class SplasherLevelName:
    __level_name: ClassVar[list[str]] = [
        "Welcome to Inkorp", "Potatoes Ink", "Stick To The Plan",
        "Let It Bounce", "Jump On The Water", "A Bad Encounter",
        "There Will Be Fries", "Ray Man Origin", "Stick On The Water",
        "Ink In  Park", "Wind Walker", "Troopers Please",
        "Water Is Coming", "Inkorp Express", "Big Bounce Theory",
        "Toxink Bubbles", "Storm Wind", "Ray Man Legend",
        "Toxink Avenger", "The Glados Principle", "Apocalink Now",
        "Good Luck Splasher"
    ]

    level_count: ClassVar[int] = 22

    @staticmethod
    def level(i: int):
        if (i < 0 or i > 21):
            return f"Invalid level ({i})"
        return SplasherLevelName.__level_name[i]
    
    @staticmethod
    def entrance_key(i: int) -> str:
        return f"{SplasherLevelName.level(i)} : Entrance Key"
    
    @classmethod
    def all_entrance_keys(cls):
        return [cls.entrance_key(i) for i in range(1, cls.level_count)]
    
    @classmethod
    def all_regions(cls, world: SplasherWorld):
        return [Region(x, world.player, world.multiworld) for x in cls.__level_name]

def create_all_regions(world: SplasherWorld):
    world.multiworld.regions += [Region(SplasherUtils.origin, world.player, world.multiworld)]
    world.multiworld.regions += SplasherLevelName.all_regions(world)

def __define_rule(world: SplasherWorld, level: int):
    if level == 0:
        return None

    match(world.options.include_keys):
        case IncludeKeys.option_zone:
            return None
        case IncludeKeys.option_level:
            return Has(SplasherLevelName.entrance_key(level))
        case _:
            return None

def connect_regions(world: SplasherWorld):
    hub = world.get_region(SplasherUtils.origin)
    for i in range(SplasherLevelName.level_count):
        level = SplasherLevelName.level(i)
        print(__define_rule(world, i))
        hub.connect(world.get_region(level), f"{level} : Entrance", __define_rule(world, i))
