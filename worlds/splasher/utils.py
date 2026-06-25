from __future__ import annotations
from typing import TYPE_CHECKING, ClassVar
from BaseClasses import Region

if TYPE_CHECKING:
    from .world import SplasherWorld

class SplasherUtils:
    splasher: ClassVar[str] = "Splasher"
    base_id: ClassVar[int] = 0xF4A201
    regular_splashers: ClassVar[int] = 132
    golden_splashers: ClassVar[int] = 22
    origin = "Hub"

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