from typing import Callable, ClassVar

from BaseClasses import Region 
from .world import SplasherWorld

splasher_hub = "HUB"

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

    @staticmethod
    def level(i: int):
        if (i < 0 or i > 21):
            return f"Invalid level ({i})"
        return SplasherLevelName.__level_name[i]
    
    @staticmethod
    def for_all[T](f: Callable[[str], T]) -> list[T]:
        return [f(x) for x in SplasherLevelName.__level_name]

def create_all_regions(world: SplasherWorld):
    world.multiworld.regions += [Region(splasher_hub, world.player, world.multiworld)]
    world.multiworld.regions += SplasherLevelName.for_all(lambda x: Region(x, world.player, world.multiworld))

def connect_regions(world: SplasherWorld):
    hub = world.get_region(splasher_hub)
    SplasherLevelName.for_all(lambda x: hub.connect(world.get_region(x), f"{x} : Entrance"))
