from typing import Any
from math import floor

from rule_builder.rules import Has
from worlds.AutoWorld import World

from .rules import SplasherPowerRules, SplasherRule
from .utils import SplasherUtils
from .web import SplasherWebWorld
from . import regions
from .items import SplasherCheckpoint, SplasherCheckpointLevel, SplasherFiller, SplasherItem, SplasherKey, SplasherPowerItem, SplasherZoneKey
from .locations import SplasherLocation, SplasherLocationOnEachLevel, SplasherPowerLocation, SplashersLocation
from .options import CheckpointSanity, IncludeKeys, IncludeMedals, SplasherOptions, RandomizePowers, CheckpointPacks

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
        self.__set_power_rules()

    def create_item(self, name: str) -> SplasherItem:
        return SplasherItem(name, self.player, self.options)

    def create_items(self) -> None:
        total_in_pool = SplasherUtils.regular_splashers
        required_in_pool = self.options.splashers_goal.value
        if self.options.randomize_golden_splashers:
            total_in_pool += SplasherUtils.golden_splashers
        else:
            required_in_pool -= SplasherUtils.golden_splashers # because we already force-place those

        filler_in_pool = floor((total_in_pool - required_in_pool) * (100 - self.options.splasher_pool.value) / 100.)
        itempool: list[SplasherItem] = [SplasherItem(SplasherUtils.splasher, self.player, self.options) for _ in range(total_in_pool - filler_in_pool)]

        match self.options.randomize_powers:
            case RandomizePowers.option_progressive: itempool += [
                SplasherItem(SplasherItem.progressive_power, self.player, self.options)
                for _ in range(5 if self.options.progressive_water else 3)
            ]
            case RandomizePowers.option_on_except_water: itempool += [
                SplasherItem(name, self.player, self.options) 
                for name in SplasherPowerItem.pool(2 if self.options.progressive_water else None)
            ]
            case RandomizePowers.option_on: itempool += [
                SplasherItem(name, self.player, self.options) 
                for name in SplasherPowerItem.pool(3 if self.options.progressive_water else 0)
            ]
            case _: pass

        match(self.options.include_keys):
            case IncludeKeys.option_level:
                itempool += [SplasherItem(x, self.player, self.options) for x in SplasherKey.keys(False)]
                if self.options.include_speedrun_keys.value > 0 and self.options.include_medals > IncludeMedals.option_off:
                    itempool += [SplasherItem(x, self.player, self.options) for x in SplasherKey.keys(True)]
            case IncludeKeys.option_zone: 
                itempool += [SplasherItem(x, self.player, self.options) for x in SplasherZoneKey.keys(False)]
                if self.options.include_speedrun_keys.value > 0 and self.options.include_medals > IncludeMedals.option_off:
                    itempool += [SplasherItem(x, self.player, self.options) for x in SplasherZoneKey.keys(True)]
            case _:
                pass

        if (self.options.checkpoint_sanity > CheckpointSanity.option_off):
            print(self.options.checkpoint_packs)
            match(self.options.checkpoint_packs):
                case CheckpointPacks.option_singular:
                    itempool += [SplasherItem(x, self.player, self.options) for x in SplasherCheckpoint.items()]
                case CheckpointPacks.option_level:
                    itempool += [SplasherItem(x, self.player, self.options) for x in SplasherCheckpointLevel.items()]
                case _:
                    pass

        itempool += SplasherFiller.get_remaining(
            self.player, self.options,
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

    def __set_power_rules(self):
        self.__add_splasher_goal_rules()
        self.get_location(
            SplasherLocationOnEachLevel.CLEAR.fullname(21)
        ).place_locked_item(
            SplasherItem(SplasherItem.victory, self.player, self.options)
        )

        if (self.options.randomize_powers == RandomizePowers.option_off):
            self.get_location(
                SplasherPowerLocation.STICKINK.fullname()
            ).place_locked_item(
                SplasherItem(SplasherPowerItem.STICKY, self.player, self.options)
            )

            self.get_location(
                SplasherPowerLocation.BOUNCINK.fullname()
            ).place_locked_item(
                SplasherItem(SplasherPowerItem.BOUNCY, self.player, self.options)
            )

            self.get_location(
                SplasherPowerLocation.WATER.fullname()
            ).place_locked_item(
                SplasherItem(SplasherPowerItem.WATER, self.player, self.options)
            )
    
        elif (self.options.randomize_powers == RandomizePowers.option_on_except_water):
            item = SplasherPowerItem.PROGRESSIVE_WATER if self.options.progressive_water else SplasherPowerItem.WATER
            self.get_location(
                SplasherPowerLocation.WATER.fullname()
            ).place_locked_item(
                SplasherItem(item, self.player, self.options)
            )

        for i in range(SplasherUtils.level_count):
            self.__set_speedrun_rule(i)  

        if not (self.options.randomize_golden_splashers):
            for i in range(22):
                self.get_location(
                    SplashersLocation.fullname(i, None)
                ).place_locked_item(SplasherItem(SplasherUtils.splasher, self.player, self.options))

        SplasherRule.apply(self)

    def __add_splasher_goal_rules(self):
        rule = Has(SplasherUtils.splasher, self.options.splashers_goal.value)
        for i in range(6):
            SplasherRule.set(SplashersLocation.fullname(21, i), rule)

        SplasherRule.set(SplashersLocation.fullname(21, None), rule)
        SplasherRule.set(SplasherLocationOnEachLevel.CLEAR.fullname(21), rule)

    def __set_speedrun_rule(self, lvl: int):
        r = SplasherPowerRules.clean_water
        if (lvl < 5):
            r &= SplasherPowerRules.sticky
        if (lvl < 13):
            r &= SplasherPowerRules.bouncy

        for lit in [
            SplasherLocationOnEachLevel.BRONZE, SplasherLocationOnEachLevel.SILVER, 
            SplasherLocationOnEachLevel.GOLD, SplasherLocationOnEachLevel.PLATINUM
        ]:
            SplasherRule.set(lit.fullname(lvl), r.get(self.options.randomize_powers, self.options.progressive_water == 1))
