from typing import Any
from math import floor

from rule_builder.rules import Has
from worlds.AutoWorld import World

from .rules import SplasherRules
from .utils import SplasherUtils
from .web import SplasherWebWorld
from . import regions
from .items import SplasherFiller, SplasherItem, SplasherKey, SplasherPowerItem, SplasherZoneKey
from .locations import SplasherLocation
from .options import IncludeKeys, IncludeMedals, SplasherOptions,RandomizePowers

class SplasherWorld(World):
    """
    Splasher is a 2D action-platformer ...
    """
    game = SplasherUtils.splasher
    web = SplasherWebWorld()

    origin_region_name = SplasherUtils.origin

    options_dataclass = SplasherOptions
    options: SplasherOptions # type: ignore

    item_name_to_id = {name:SplasherItem.get_code(name) for name in SplasherItem.keys()}
    item_name_groups = SplasherItem.group_table()
    location_name_to_id = SplasherLocation.name_to_id()
    

    def create_regions(self) -> None:
        regions.create_all_regions(self)
        regions.connect_regions(self)
        SplasherLocation.create_locations(self)
        SplasherRules.set_rules(self)

    def create_item(self, name: str) -> SplasherItem:
        return SplasherItem(name, self.player)

    def create_items(self) -> None:
        total_in_pool = SplasherUtils.regular_splashers
        required_in_pool = self.options.splashers_goal.value
        if self.options.randomize_golden_splashers:
            total_in_pool += SplasherUtils.golden_splashers
        else:
            required_in_pool -= SplasherUtils.golden_splashers # because we already force-place those

        filler_in_pool = floor((total_in_pool - required_in_pool) * (100 - self.options.splasher_pool.value) / 100.)
        itempool: list[SplasherItem] = [SplasherItem(SplasherUtils.splasher, self.player) for _ in range(total_in_pool - filler_in_pool)]

        match self.options.randomize_powers:
            case RandomizePowers.option_progressive: itempool += [
                SplasherItem(SplasherItem.progressive_power, self.player)
                for _ in range(5 if self.options.progressive_water else 3)
            ]
            case RandomizePowers.option_on_except_water: itempool += [
                SplasherItem(name, self.player) 
                for name in SplasherPowerItem.pool(2 if self.options.progressive_water else None)
            ]
            case RandomizePowers.option_on: itempool += [
                SplasherItem(name, self.player) 
                for name in SplasherPowerItem.pool(3 if self.options.progressive_water else 0)
            ]
            case _: pass

        match(self.options.include_keys):
            case IncludeKeys.option_level:
                itempool += [SplasherItem(x, self.player) for x in SplasherKey.keys(False)]
                if self.options.include_speedrun_keys.value > 0 and self.options.include_medals > IncludeMedals.option_off:
                    itempool += [SplasherItem(x, self.player) for x in SplasherKey.keys(True)]
            case IncludeKeys.option_zone: 
                itempool += [SplasherItem(x, self.player) for x in SplasherZoneKey.keys(False)]
                if self.options.include_speedrun_keys.value > 0 and self.options.include_medals > IncludeMedals.option_off:
                    itempool += [SplasherItem(x, self.player) for x in SplasherZoneKey.keys(True)]
            case _:
                pass

        itempool += SplasherFiller.get_remaining(
            self.player, 
            len(self.multiworld.get_unfilled_locations(self.player)) - len(itempool), 
            self.options.trap_chance.value,
            self.options.essence_storage.value,
            self.options.essence_traps.value,
            self.multiworld.random
        )

        self.multiworld.itempool += itempool

    def fill_slot_data(self) -> dict[str, Any]:
        option_names = [key for key in SplasherOptions.__annotations__.keys()]
        data=  self.options.as_dict(*option_names)  
        data["seed"] = str(self.multiworld.seed)
        data["location_count"] = SplasherLocation.count

        return data     

    def set_rules(self):
        self.set_completion_rule(Has(SplasherItem.victory)) 
