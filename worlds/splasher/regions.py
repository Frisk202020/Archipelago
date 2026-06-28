from __future__ import annotations
from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import Has

from .items import SplasherKey, SplasherZoneKey
from .options import IncludeKeys
from .utils import SplasherUtils

if TYPE_CHECKING:
    from .world import SplasherWorld

def create_all_regions(world: SplasherWorld):
    world.multiworld.regions += [Region(SplasherUtils.origin, world.player, world.multiworld)]
    world.multiworld.regions += [
        Region(x, world.player, world.multiworld) for x in SplasherUtils.level_names
    ]

def __define_rule(world: SplasherWorld, level: int):
    if level == 0:
        return None
    
    match(world.options.include_keys):
        case IncludeKeys.option_level:
            return Has(SplasherKey.key(level))
        case IncludeKeys.option_zone:
            return Has(SplasherZoneKey.key(level))
        case _:
            return None

def connect_regions(world: SplasherWorld):
    hub = world.get_region(SplasherUtils.origin)
    for i in range(SplasherUtils.level_count):
        level = SplasherUtils.level(i)
        hub.connect(world.get_region(level), f"{level} : Entrance", __define_rule(world, i))
