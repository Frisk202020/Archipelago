from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Tuple, cast
from rule_builder.rules import Has, Rule

from .items import SplasherItem, SplasherPowerItem
from .options import RandomizePowers

if TYPE_CHECKING:
    from .world import SplasherWorld

class SplasherPowerRules:
    polluted_water: SplasherPowerRules
    clean_water: SplasherPowerRules
    speed_water: SplasherPowerRules
    sticky: SplasherPowerRules
    bouncy: SplasherPowerRules
    unstick_rule: SplasherPowerRules
    non_water: SplasherPowerRules
    all_polluted: SplasherPowerRules

    __standard: Rule
    __progressive: int
    __progressive_with_water: int

    def __init__(self, standard: Rule, progressive: int, progressive_with_water: int):
        self.__standard = standard
        self.__progressive = progressive
        self.__progressive_with_water = progressive_with_water

    def get(self, powers_opt: RandomizePowers, progressive_water: bool) -> Rule:
        match(powers_opt):
            case RandomizePowers.option_progressive:
                return \
                    Has(SplasherItem.progressive_power, self.__progressive_with_water) if progressive_water \
                    else Has(SplasherItem.progressive_power, self.__progressive)
            
            case _: return self.__standard

    def __and__(self, other: SplasherPowerRules):
        return SplasherPowerRules(
            self.__standard & other.__standard, 
            max(self.__progressive, other.__progressive), 
            max(self.__progressive_with_water, other.__progressive_with_water)
        )
    
    def __or__(self, other: SplasherPowerRules):
        return SplasherPowerRules(
            self.__standard | other.__standard, 
            min(self.__progressive, other.__progressive), 
            min(self.__progressive_with_water, other.__progressive_with_water)
        )

SplasherPowerRules.polluted_water = SplasherPowerRules(Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.PROGRESSIVE_WATER), 1, 1)
SplasherPowerRules.clean_water = SplasherPowerRules(Has(SplasherPowerItem.WATER) | \
    Has(SplasherPowerItem.PROGRESSIVE_WATER, 2) | \
    (Has(SplasherPowerItem.PROGRESSIVE_WATER, 1) & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY))), 2, 2)

SplasherPowerRules.speed_water = SplasherPowerRules(Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.PROGRESSIVE_WATER, 3), 3, 3)
SplasherPowerRules.sticky = SplasherPowerRules(Has(SplasherPowerItem.STICKY), 2, 4)
SplasherPowerRules.bouncy = SplasherPowerRules(Has(SplasherPowerItem.BOUNCY), 3, 5)
SplasherPowerRules.unstick_rule = SplasherPowerRules(Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.PROGRESSIVE_WATER, 2) | Has(SplasherPowerItem.BOUNCY), 1, 2)
SplasherPowerRules.non_water = SplasherPowerRules(Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY), 2, 4)
SplasherPowerRules.all_polluted = SplasherPowerRules.polluted_water & SplasherPowerRules.sticky & SplasherPowerRules.bouncy

class SplasherRule:
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

            #print(f"{world.get_location(name)} : {rule}\n\n")
            world.set_rule(world.get_location(name), rule)


class SplasherArea: 
    __checkpoint_rules: list[list[Tuple[int|None, SplasherPowerRules]]] = [
        # Welcome to Inkorp
        [
            (None, SplasherPowerRules.clean_water)
        ],
        # Potatoes Ink
        [
            (0, SplasherPowerRules.polluted_water),
            (1, SplasherPowerRules.clean_water)
        ],
        # Stick To The Plan
        [
            (0, SplasherPowerRules.polluted_water)
        ],
        # Let It Bounce
        [
            (0, SplasherPowerRules.polluted_water | SplasherPowerRules.non_water),
            (1, SplasherPowerRules.polluted_water)
        ],
        # Jump On The Water
        [
            (0, SplasherPowerRules.polluted_water | SplasherPowerRules.non_water),
            (1, SplasherPowerRules.polluted_water)
        ],
        # A Bad Encounter
        [
            (0, SplasherPowerRules.polluted_water)
        ],
        # There Will Be Fries
        [
            (0, SplasherPowerRules.non_water),
            (1, SplasherPowerRules.sticky & (SplasherPowerRules.bouncy | SplasherPowerRules.polluted_water))
        ],
        # Ray Man Origin
        [
            (0, SplasherPowerRules.polluted_water & SplasherPowerRules.non_water)
        ],
        # Stick On The Water
        [
            (0, SplasherPowerRules.non_water),
            (3, SplasherPowerRules.polluted_water & SplasherPowerRules.sticky)
        ],
        # Ink In  Park
        [
            (0, SplasherPowerRules.polluted_water & SplasherPowerRules.non_water)
        ],
        # Wind Walker
        [
            (0, SplasherPowerRules.sticky),
            (1, SplasherPowerRules.polluted_water & SplasherPowerRules.sticky)
        ],
        # Troopers Please
        [
            (0, SplasherPowerRules.polluted_water & SplasherPowerRules.non_water)
        ],
        # Water Is Coming
        [
            (0, SplasherPowerRules.polluted_water & SplasherPowerRules.non_water)
        ],
        # Inkorp Express
        [
            (0, SplasherPowerRules.non_water),
            (1, SplasherPowerRules.speed_water & SplasherPowerRules.non_water),
            (None, SplasherPowerRules.speed_water & SplasherPowerRules.bouncy)
        ],
        # Big Bounce Theory
        [
            (0, SplasherPowerRules(Has(SplasherPowerItem.BOUNCY), 3, 5)),
            (2, SplasherPowerRules.polluted_water & SplasherPowerRules.bouncy)
        ],
        # Toxink Bubbles
        [
            (0, SplasherPowerRules(Has(SplasherPowerItem.BOUNCY), 3, 5)),
            (2, SplasherPowerRules.polluted_water & SplasherPowerRules.bouncy),
            (3, SplasherPowerRules.all_polluted)
        ],
        # Storm Wind
        [
            (0, SplasherPowerRules.all_polluted)
        ],
        # Ray Man Legend
        [
            (0, SplasherPowerRules.all_polluted)
        ],
        # Toxink Avenger
        [
            (0, SplasherPowerRules.all_polluted)
        ],
        # The Glados Principle
        [
            (0, SplasherPowerRules.polluted_water & SplasherPowerRules.bouncy)
        ],
        # Apocalink Now
        [
            (0, SplasherPowerRules.polluted_water & SplasherPowerRules.bouncy)
        ],
        # Good Luck Splasher
        [
            (0, SplasherPowerRules.speed_water & SplasherPowerRules.sticky & SplasherPowerRules.bouncy)
        ]
    ]

    @classmethod
    def get_areas(cls, world: SplasherWorld):
        return [[x[1].get(world.options.randomize_powers, world.options.progressive_water == 1) for x in y] for y in cls.__checkpoint_rules]

    @classmethod
    def get_area(cls, level: int, ckp: int|None) -> tuple[int, bool]:
        end_area_id = len(cls.__checkpoint_rules[level]) - 1
        if (ckp is None): return (end_area_id, True)

        for i in range(0, end_area_id):
            area_ckp_id = cast(int, cls.__checkpoint_rules[level][i][0])
            if (ckp >= area_ckp_id): return (i, False)

        return (end_area_id, True)