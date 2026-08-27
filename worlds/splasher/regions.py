from __future__ import annotations
from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.rules import Has

from .rules import SplasherRules
from .items import SplasherCheckpoint, SplasherKey, SplasherZoneKey
from .options import CheckpointSanity, IncludeKeys, IncludeMedals
from .utils import SplasherUtils

if TYPE_CHECKING:
    from .world import SplasherWorld

def splasher_area_name(lvl: str, id: int|None):
    return lvl if id is None else f"{lvl} : Area {id}"

def splasher_ckp_region_name(lvl: str, id: int):
    return f"{lvl} : Checkpoint {id+1} juridiction"

def create_all_regions(world: SplasherWorld):
    areas = SplasherRules.get_areas()
    region_names = [SplasherUtils.origin]

    for lvl in range(SplasherUtils.level_count):
        level = SplasherUtils.level(lvl, False)
        region_names.append(level)
        region_names.append(SplasherUtils.level(lvl, True))

        for area_id in range(len(areas[lvl])):
            region_names.append(splasher_area_name(level, area_id))

        if world.options.checkpoint_sanity == CheckpointSanity.option_progression:
            for ckp_id in range(SplasherCheckpoint.id_range(lvl)):
                region_names.append(splasher_ckp_region_name(level, ckp_id))

    world.multiworld.regions += [
        Region(x, world.player, world.multiworld) for x in region_names
    ]

def __define_key_rule(world: SplasherWorld, level: int, speedrun: bool):
    if level == 0:
        return None
    
    use_speedrun = speedrun and world.options.include_speedrun_keys.value > 0 and world.options.include_medals > IncludeMedals.option_off
    match(world.options.include_keys):
        case IncludeKeys.option_level:
            return Has(SplasherKey.key(level, use_speedrun))
        case IncludeKeys.option_zone:
            return Has(SplasherZoneKey.key(level, use_speedrun))
        case _:
            return None

def connect_regions(world: SplasherWorld):
    areas = SplasherRules.get_areas()
    hub = world.get_region(SplasherUtils.origin)

    for lvl in range(SplasherUtils.level_count):
        level = SplasherUtils.level(lvl, True)
        hub.connect(world.get_region(level), f"{level} : Entrance (Time Attack)", __define_key_rule(world, lvl, True))

        level = SplasherUtils.level(lvl, False)
        level_region = world.get_region(level)

        hub.connect(level_region, f"{level} : Entrance", __define_key_rule(world, lvl, False))
        level_areas: list[Region] = []

        for area_id in range(len(areas[lvl])):
            area_name = splasher_area_name(level, area_id)
            area = world.get_region(area_name)
            previous_area = level_region if len(level_areas) == 0 else level_areas[area_id - 1]
            previous_area.connect(area, f"{area_name} : Entrance", areas[lvl][area_id])
            level_areas.append(area)

        if (world.options.checkpoint_sanity == CheckpointSanity.option_progression):
            prev_ckp: tuple[str, Region]|None = None
            prev_area_id: int = -1
            
            for ckp_id in range(SplasherCheckpoint.id_range(lvl)):
                (area_id, is_exit_area) = SplasherRules.get_area(lvl, ckp_id)
                ckp_region_name = splasher_ckp_region_name(level, ckp_id)
                ckp_region = world.get_region(ckp_region_name)

                rule = None if is_exit_area else Has(SplasherCheckpoint.name(lvl, ckp_id))
                level_areas[area_id].connect(ckp_region, f"{level} : validate checkpoint {ckp_id}", rule)

                if (is_exit_area): continue
                if (prev_area_id == area_id and prev_ckp is not None):
                    ckp_region.connect(prev_ckp[1], f"{prev_ckp[0]} - Recursive entrance")

                prev_ckp = (ckp_region_name, ckp_region)
                prev_area_id = area_id