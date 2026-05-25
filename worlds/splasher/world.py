from typing import Any

from Options import Toggle
from rule_builder.rules import Has
from worlds.AutoWorld import World
from worlds.splasher.rules import SplasherRules
from worlds.splasher.utils import SplasherUtils
from worlds.splasher.web import SplasherWebWorld
from . import regions
from .items import SplasherItem, SplasherItemGroupName
from .locations import SplasherLocation
from .options import SplasherOptions,RandomizePowers

class SplasherWorld(World):
    """
    Splasher is a 2D action-plateformer ...
    """
    game = SplasherUtils.splasher
    web = SplasherWebWorld()

    origin_region_name = SplasherUtils.origin

    options_dataclass = SplasherOptions
    options: SplasherOptions # type: ignore

    item_name_to_id = {name:SplasherItem.get_code(name) for name in SplasherItem.keys()}
    location_name_to_id = SplasherLocation.name_to_id()
    

    def create_regions(self) -> None:
        regions.create_all_regions(self)
        regions.connect_regions(self)
        SplasherLocation.create_locations(self)
        SplasherRules.set_rules(self)

    def create_item(self, name: str) -> SplasherItem:
        return SplasherItem(name, self.player)

    def create_items(self) -> None:
        total_splashers = SplasherUtils.regular_splashers + SplasherUtils.golden_splashers if self.options.randomize_golden_splashers else SplasherUtils.regular_splashers
        itempool: list[SplasherItem] = [SplasherItem(SplasherUtils.splasher, self.player) for _ in range(total_splashers)]

        for name,enabled in {
            SplasherItemGroupName.POWERS: self.options.randomize_powers >= RandomizePowers.option_on,
        }.items():  
            if enabled:
                itempool += name.create_items(self.player)


        itempool += [
            SplasherItem(
                SplasherItemGroupName.TRAPS.get_random(self.multiworld.random) 
                    if self.multiworld.random.randint(0, 99) <= self.options.trap_chance 
                    else SplasherItemGroupName.get_filler(
                        self.multiworld.random, 
                        self.options.include_essence_items == Toggle.option_true
                    ), 
                self.player
            ) for _ in range(len(self.multiworld.get_unfilled_locations(self.player)))
        ]

        self.multiworld.itempool += itempool

    def fill_slot_data(self) -> dict[str, Any]:
        option_names = [key for key in SplasherOptions.__annotations__.keys()]
        return self.options.as_dict(*option_names)       

    def set_rules(self):
        self.set_completion_rule(Has(SplasherItem.victory)) 
