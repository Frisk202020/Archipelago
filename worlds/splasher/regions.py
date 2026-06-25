from __future__ import annotations

from typing import TYPE_CHECKING
from BaseClasses import Region
from rule_builder.rules import Has
from worlds.splasher.items import SplasherZoneKey
from worlds.splasher.options import IncludeKeys
from worlds.splasher.utils import SplasherUtils,SplasherLevelName

if TYPE_CHECKING:
    from .world import SplasherWorld

def create_all_regions(world: SplasherWorld):
    world.multiworld.regions += [Region(SplasherUtils.origin, world.player, world.multiworld)]
    world.multiworld.regions += SplasherLevelName.all_regions(world)

def __define_rule(world: SplasherWorld, level: int):
    if level == 0:
        return None
    
    match(world.options.include_keys):
        case IncludeKeys.option_level:
            return Has(SplasherLevelName.entrance_key(level))
        case IncludeKeys.option_zone:
            return Has(SplasherZoneKey.zone_for_level(level))
        case _:
            return None

def connect_regions(world: SplasherWorld):
    hub = world.get_region(SplasherUtils.origin)
    for i in range(SplasherLevelName.level_count):
        level = SplasherLevelName.level(i)
        hub.connect(world.get_region(level), f"{level} : Entrance", __define_rule(world, i))
