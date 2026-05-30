from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from rule_builder.rules import Has, HasAll, Rule
from worlds.splasher.items import SplasherItem, SplasherPowerItem
from worlds.splasher.locations import SplasherLocationOnEachLevel, SplasherPowerLocation, SplashersLocation
from worlds.splasher.options import RandomizePowers
from worlds.splasher.utils import SplasherUtils

if TYPE_CHECKING:
    from .world import SplasherWorld

class SplasherRules:
    @classmethod
    def set_rules(cls, world: SplasherWorld):
        cls.__add_splashers_rules(world)

        print(world.get_locations())

        world.get_location(
            SplasherLocationOnEachLevel.CLEAR.fullname(21)
        ).place_locked_item(
            SplasherItem(SplasherItem.victory, world.player)
        )

        if (world.options.randomize_powers < RandomizePowers.option_on):
            world.get_location(
                SplasherPowerLocation.WATER.fullname()
            ).place_locked_item(
                SplasherItem(SplasherPowerItem.WATER, world.player)
            )

            world.get_location(
                SplasherPowerLocation.STICKINK.fullname()
            ).place_locked_item(
                SplasherItem(SplasherPowerItem.STICKY, world.player)
            )

            world.get_location(
                SplasherPowerLocation.BOUNCINK.fullname()
            ).place_locked_item(
                SplasherItem(SplasherPowerItem.BOUNCY, world.player)
            )
        else:
            cls.__add_power_rules()

        if not (world.options.randomize_golden_splashers):
            for i in range(22):
                world.get_location(
                    SplashersLocation.fullname(i, None)
                ).place_locked_item(SplasherItem(SplasherUtils.splasher, world.player))

        _Rule.apply(world)

    # TODO - define entrance keys logic (set rules on region directly)

    @staticmethod
    def __add_splashers_rules(world: SplasherWorld):
        rule = Has(SplasherUtils.splasher, world.options.splashers_goal.value)
        for i in range(6):
            _Rule.set(SplashersLocation.fullname(21, i), rule)

        _Rule.set(SplashersLocation.fullname(21, None), rule)
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(21), rule)


    @staticmethod
    def __add_power_rules():
        _Rule.set(SplashersLocation.fullname(0, 4), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(0, 5), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(0, None), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(0), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(0), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(0), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(0), Has(SplasherPowerItem.WATER))

        _Rule.set(SplashersLocation.fullname(1, 0), Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(1, 1), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(1, 2), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(1, 3), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(1, 4), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(1, 5), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(1, None), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(1), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(1), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(1), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(1), Has(SplasherPowerItem.WATER))
        
        _Rule.set(SplashersLocation.fullname(2, 0), Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.BOUNCY)) # hard with Bouncink
        _Rule.set(SplashersLocation.fullname(2, 1), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(2, 2), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(2, 3), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(2, 4), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(2, 5), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(2, None), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(2), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(2), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(2), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(2), Has(SplasherPowerItem.WATER))

        _Rule.set(SplashersLocation.fullname(3, 0), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(3, 1), Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(3, 2), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(3, 3), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(3, 4), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(3, 5), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(3, None), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(3), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(3), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(3), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(3), Has(SplasherPowerItem.WATER))

        _Rule.set(SplashersLocation.fullname(4, 0), Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(4, 1), Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(4, 2), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(4, 3), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(4, 4), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(4, 5), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(4, None), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(4), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(4), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(4), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(4), Has(SplasherPowerItem.WATER))

        _Rule.set(SplashersLocation.fullname(5, 0), Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(5, 1), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(5, 2), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(5, 3), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(5, 4), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(5, 5), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(5, None), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherPowerLocation.STICKINK.fullname(), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))

        _Rule.set(SplashersLocation.fullname(6, 0), Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(6, 1), Has(SplasherPowerItem.BOUNCY) | HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(6, 2), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(6, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(6, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(6, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(6, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(6), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(6), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(6), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(6), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))

        _Rule.set(SplashersLocation.fullname(7, 0), Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(7, 1), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)))
        _Rule.set(SplashersLocation.fullname(7, 2), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)))
        _Rule.set(SplashersLocation.fullname(7, 3), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)))
        _Rule.set(SplashersLocation.fullname(7, 4), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)))
        _Rule.set(SplashersLocation.fullname(7, 5), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)))
        _Rule.set(SplashersLocation.fullname(7, None), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(7), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(7), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(7), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(7), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))

        _Rule.set(SplashersLocation.fullname(8, 0), Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(8, 1), Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(8, 2), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)))
        _Rule.set(SplashersLocation.fullname(8, 3), Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(8, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(8, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(8, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(8), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(8), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(8), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(8), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))

        _Rule.set(SplashersLocation.fullname(9, 0), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(9, 1), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(9, 2), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(9, 3), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(9, 4), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(9, 5), Has(SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(9, None), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(9), Has(SplasherPowerItem.WATER))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(9), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(9), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(9), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))

        _Rule.set(SplashersLocation.fullname(10, 0), Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(10, 1), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(10, 2), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(10, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(10, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(10, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(10, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(10), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(10), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(10), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(10), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))

        _Rule.set(SplashersLocation.fullname(11, 0), Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(11, 1), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)))
        _Rule.set(SplashersLocation.fullname(11, 2), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)))
        _Rule.set(SplashersLocation.fullname(11, 3), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)))
        _Rule.set(SplashersLocation.fullname(11, 4), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)))
        _Rule.set(SplashersLocation.fullname(11, 5), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)))
        _Rule.set(SplashersLocation.fullname(11, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(11), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(11), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(11), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(11), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))

        _Rule.set(SplashersLocation.fullname(12, 0), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)))
        _Rule.set(SplashersLocation.fullname(12, 1), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)))
        _Rule.set(SplashersLocation.fullname(12, 2), Has(SplasherPowerItem.WATER) & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)))
        _Rule.set(SplashersLocation.fullname(12, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(12, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(12, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(12, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(12), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(12), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(12), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(12), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))

        # Need to further investigate behavior when Bouncink is already unlocked 
        _Rule.set(SplashersLocation.fullname(13, 0), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(13, 1), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(13, 2), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(13, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(13, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(13, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(13, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(13), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherPowerLocation.BOUNCINK.fullname(), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(13), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(13), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(13), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))

        _Rule.set(SplashersLocation.fullname(14, 0), Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(14, 1), Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(14, 2), Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(14, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(14, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(14, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(14, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(14), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(14), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(14), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(14), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))

        _Rule.set(SplashersLocation.fullname(15, 0), Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(15, 1), Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(15, 2), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(15, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(15, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(15, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(15, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(15), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(15), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(15), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(15), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))

        _Rule.set(SplashersLocation.fullname(16, 0), HasAll(SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(16, 1), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(16, 2), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(16, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(16, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(16, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(16, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(16), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(16), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(16), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(16), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))

        _Rule.set(SplashersLocation.fullname(17, 0), HasAll(SplasherPowerItem.BOUNCY, SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(17, 1), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(17, 2), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(17, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(17, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(17, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(17, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(17), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(17), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(17), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(17), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))

        _Rule.set(SplashersLocation.fullname(18, 0), HasAll(SplasherPowerItem.BOUNCY, SplasherPowerItem.WATER))
        _Rule.set(SplashersLocation.fullname(18, 1), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(18, 2), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(18, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(18, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(18, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(18, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(18), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(18), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(18), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(18), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))

        _Rule.set(SplashersLocation.fullname(19, 0), Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(19, 1), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(19, 2), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(19, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(19, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(19, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(19, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(19), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(19), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(19), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(19), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))

        _Rule.set(SplashersLocation.fullname(20, 0), Has(SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(20, 1), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(20, 2), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(20, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(20, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(20, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY))
        _Rule.set(SplashersLocation.fullname(20, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(20), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(20), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(20), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(20), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))

        _Rule.set(SplashersLocation.fullname(21, 0), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(21, 1), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(21, 2), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(21, 3), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(21, 4), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(21, 5), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplashersLocation.fullname(21, None), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(21), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.BOUNCY, SplasherPowerItem.STICKY))
        _Rule.set(SplasherLocationOnEachLevel.BRONZE.fullname(21), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.SILVER.fullname(21), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))
        _Rule.set(SplasherLocationOnEachLevel.GOLD.fullname(21), HasAll(SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY))

class _Rule:
    __rules: ClassVar[dict[str, Rule[SplasherWorld]]] = {}

    @classmethod
    def set(cls, name: str, rule: Rule[SplasherWorld]):
        if name in cls.__rules:
            cls.__rules[name] &= rule
        else:
            cls.__rules[name] = rule
            
    @classmethod
    def apply(cls, world: SplasherWorld):
        locations = frozenset([l.name for l in world.get_locations()])
        
        for name,rule in cls.__rules.items():
            if not name in locations:
                continue # if location not included by options

            world.set_rule(world.get_location(name), rule)

    

        
