from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Optional, Tuple, cast
from rule_builder.rules import Has, Rule

from .items import SplasherCheckpoint, SplasherItem, SplasherPowerItem
from .locations import SplasherLocationOnEachLevel, SplasherPowerLocation, SplashersLocation
from .options import CheckpointSanity, RandomizePowers
from .utils import SplasherUtils

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

# class _CheckpointRule:
#     __power_rules: ClassVar[dict[int, dict[int | None, SplasherPowerRules]]] = {
#         0: {
#             None: SplasherPowerRules.clean_water
#         },
#         1: {
#             0: SplasherPowerRules.polluted_water,
#             1: SplasherPowerRules.clean_water
#         },
#         2: {
#             0: SplasherPowerRules.polluted_water
#         },
#         3: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water | Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY), 1, 1),
#             1: SplasherPowerRules.polluted_water
#         },
#         4: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water | Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY), 1, 1),
#             1: SplasherPowerRules(SplasherPowerRules.polluted_water, 1, 1)
#         },
#         5: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water, 1, 1)
#         },
#         6: {
#             0: SplasherPowerRules(Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY), 2, 4),
#             1: SplasherPowerRules(Has(SplasherPowerItem.STICKY) & (Has(SplasherPowerItem.BOUNCY) | SplasherPowerRules.polluted_water), 2, 4)
#         },
#         7: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)), 2, 4)
#         },
#         8: {
#             0: SplasherPowerRules(Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY), 2, 4),
#             3: SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4)
#         },
#         9: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)), 2, 4)
#         },
#         10: {
#             0: SplasherPowerRules(Has(SplasherPowerItem.STICKY), 2, 4),
#             1: SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4)
#         },
#         11: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)), 2, 4)
#         },
#         12: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)), 2, 4)
#         },
#         13: {
#             0: SplasherPowerRules(Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY), 2, 4),
#             1: SplasherPowerRules(SplasherPowerRules.speed_water & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)), 2, 4)
#         },
#         14: {
#             0: SplasherPowerRules(Has(SplasherPowerItem.BOUNCY), 3, 5),
#             2: SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY), 3, 5)
#         },
#         15: {
#             0: SplasherPowerRules(Has(SplasherPowerItem.BOUNCY), 3, 5),
#             2: SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY), 3, 5),
#             3: SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY) & Has(SplasherPowerItem.BOUNCY), 3, 5)
#         },
#         16: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY) & Has(SplasherPowerItem.BOUNCY), 3, 5)
#         },
#         17: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY) & Has(SplasherPowerItem.BOUNCY), 3, 5)
#         },
#         18: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY) & Has(SplasherPowerItem.BOUNCY), 3, 5)
#         },
#         19: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY), 3, 5)
#         },
#         20: {
#             0: SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY), 3, 5)
#         },
#         21: {
#             0: SplasherPowerRules(SplasherPowerRules.speed_water & Has(SplasherPowerItem.STICKY) & Has(SplasherPowerItem.BOUNCY), 3, 5)
#         }
#     }

#     @classmethod
#     def get_areas(cls, progressive_power: RandomizePowers, progressive_water: bool) -> list[list[Tuple[int, Rule]]]:
#         return [[(x[0], x[1].get(progressive_power, progressive_water)) for x in y] for y in cls.__p_rules]

    # @classmethod
    # def get(cls, level: int, id: int | None, progressive_power: RandomizePowers, progressive_water: bool) -> Optional[Rule]:
    #     r = cls.__power_rules.get(level)
    #     if (r is None): return None

    #     r = r.get(id)
    #     if (r is None): return None

    #     return r.get(progressive_power, progressive_water)

    # @classmethod
    # def __get_power_rule(cls, level: int, id: int | None) -> SplasherPowerRules | None:
    #     level_rules = cls.__power_rules.get(level)
    #     if (level_rules is None): return None

    #     rule = level_rules.get(id)
    #     if (rule is not None): return rule

    #     start = SplasherCheckpoint.id_range(level) if id is None else id - 1
    #     for i in range(start, -1, -1):
    #         rule = level_rules.get(i)
    #         if (rule is not None): return rule

    #     return None

    # @classmethod
    # def get(cls, level: int, id: int | None, powers_opt: RandomizePowers, progressive_water: bool, ckp_required: bool):
    #     ckp_item_rule = None if not ckp_required or id is None else Has(SplasherCheckpoint.name(level, id))
    #     power_rule = cls.__get_power_rule(level, id)

    #     if (power_rule is not None): power_rule = power_rule.get(powers_opt, progressive_water)

    #     if ckp_item_rule is None:
    #         ckp_item_rule = power_rule
    #     elif power_rule is not None:
    #         ckp_item_rule &= power_rule
            
    #     return ckp_item_rule

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

            #print(f"{world.get_location(name)} : {rule}\n\n")
            world.set_rule(world.get_location(name), rule)


class SplasherRules: 
    powers_opt: ClassVar[RandomizePowers]
    progressive_water: bool
    ckp_required: bool

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
    def get_areas(cls):
        return [[x[1].get(cls.powers_opt, cls.progressive_water) for x in y] for y in cls.__checkpoint_rules]

    @classmethod
    def get_area(cls, level: int, ckp: int|None) -> tuple[int, bool]:
        end_area_id = len(cls.__checkpoint_rules[level]) - 1
        if (ckp is None): return (end_area_id, True)

        for i in range(0, end_area_id):
            area_ckp_id = cast(int, cls.__checkpoint_rules[level][i][0])
            if (ckp >= area_ckp_id): return (i, False)

        return (end_area_id, True)

    @classmethod
    def set_rules(cls, world: SplasherWorld):
        cls.__add_splasher_goal_rules(world)
        cls.powers_opt = world.options.randomize_powers
        cls.progressive_water = world.options.progressive_water == 1
        cls.ckp_required = world.options.checkpoint_sanity == CheckpointSanity.option_progression

        world.get_location(
            SplasherLocationOnEachLevel.CLEAR.fullname(21)
        ).place_locked_item(
            SplasherItem(SplasherItem.victory, world.player)
        )

        if (world.options.randomize_powers == RandomizePowers.option_off):
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

            world.get_location(
                SplasherPowerLocation.WATER.fullname()
            ).place_locked_item(
                SplasherItem(SplasherPowerItem.WATER, world.player)
            )
    
        elif (world.options.randomize_powers == RandomizePowers.option_on_except_water):
            item = SplasherPowerItem.PROGRESSIVE_WATER if world.options.progressive_water else SplasherPowerItem.WATER
            world.get_location(
                SplasherPowerLocation.WATER.fullname()
            ).place_locked_item(
                SplasherItem(item, world.player)
            )

        cls.__add_power_rules()  
        cls.__add_ckp_rules(world)  

        location_name = "Potatoes Ink : Splasher (2)"
        location = world.multiworld.get_location(location_name, world.player)
        print(f" -> Location access_rule function: {location.access_rule}")

        if not (world.options.randomize_golden_splashers):
            for i in range(22):
                world.get_location(
                    SplashersLocation.fullname(i, None)
                ).place_locked_item(SplasherItem(SplasherUtils.splasher, world.player))

        _Rule.apply(world)

    # @classmethod
    # def __add_ckp_rules(cls, world: SplasherWorld):
    #     for lvl in range(0, SplasherUtils.level_count):
    #         r = _CheckpointRule.get(lvl, None, cls.powers_opt, cls.progressive_water, False)
    #         if (r is not None): _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(lvl), r)

    #         if (world.options.checkpoint_sanity > CheckpointSanity.option_off):
    #             for i in range(SplasherCheckpoint.id_range(lvl)):
    #                 r = _CheckpointRule.get(lvl, i, cls.powers_opt, cls.progressive_water, False)
    #                 if (r is not None): _Rule.set(SplasherCheckpoint.name(lvl, i), r)

    @staticmethod
    def __add_splasher_goal_rules(world: SplasherWorld):
        rule = Has(SplasherUtils.splasher, world.options.splashers_goal.value)
        for i in range(6):
            _Rule.set(SplashersLocation.fullname(21, i), rule)

        _Rule.set(SplashersLocation.fullname(21, None), rule)
        _Rule.set(SplasherLocationOnEachLevel.CLEAR.fullname(21), rule)

    @classmethod
    def __set_splasher_rule(cls, lvl: int, min_ckp_id: int | None, splasher_ids: list[int|None], splasher_rule: SplasherPowerRules | None = None):
        ckp_rule = _CheckpointRule.get(lvl, min_ckp_id, cls.powers_opt, cls.progressive_water, cls.ckp_required)
        s_rule = None if splasher_rule is None else splasher_rule.get(cls.powers_opt, cls.progressive_water)

        if min_ckp_id is not None:
            for i in range(min_ckp_id + 1, SplasherCheckpoint.id_range(lvl)):
                or_rule = _CheckpointRule.get(lvl, i, cls.powers_opt, cls.progressive_water, cls.ckp_required)
                if (or_rule is not None):
                    if (ckp_rule is None): ckp_rule = or_rule
                    else: ckp_rule |= or_rule

        if (ckp_rule is not None):
            if s_rule is None: s_rule = ckp_rule
            else: s_rule &= ckp_rule

        if (s_rule is not None):
            for i in splasher_ids:
                _Rule.set(SplashersLocation.fullname(lvl, i), s_rule)

    # For vortex splashers or levels with invisible checkpoints
    @classmethod
    def __set_splasher_rule_no_ckp(cls, lvl: int, splasher_ids: list[int|None], rule: SplasherPowerRules):
        r = rule.get(cls.powers_opt, cls.progressive_water)
        for i in splasher_ids:
            _Rule.set(SplashersLocation.fullname(lvl, i), r)

    @classmethod
    def __set_speedrun_rule(cls, lvl: int, rule: SplasherPowerRules):
        r = rule.get(cls.powers_opt, cls.progressive_water)
        for lit in [
            SplasherLocationOnEachLevel.BRONZE, SplasherLocationOnEachLevel.SILVER, 
            SplasherLocationOnEachLevel.GOLD, SplasherLocationOnEachLevel.PLATINUM
        ]:
            _Rule.set(lit.fullname(lvl), r)
    
    @classmethod
    def __add_power_rules(cls):
        cls.__set_splasher_rule(0, None, [5, None], SplasherPowerRules(SplasherPowerRules.clean_water, 1, 2))
        cls.__set_speedrun_rule(0, SplasherPowerRules(SplasherPowerRules.clean_water, 1, 2))

        cls.__set_splasher_rule_no_ckp(1, [0], SplasherPowerRules(SplasherPowerRules.polluted_water | Has(SplasherPowerItem.BOUNCY), 1, 1))
        cls.__set_splasher_rule(1, 1, [1])
        cls.__set_splasher_rule(1, 3, [2])
        cls.__set_splasher_rule(1, 4, [3], unstick_rule)
        cls.__set_splasher_rule(1, 4, [4])
        cls.__set_splasher_rule(1, None, [5, None], SplasherPowerRules(SplasherPowerRules.clean_water, 1, 2))
        cls.__set_speedrun_rule(1, SplasherPowerRules(SplasherPowerRules.clean_water, 1, 2))

        # hard with Bouncink
        cls.__set_splasher_rule_no_ckp(2, [0], SplasherPowerRules(SplasherPowerRules.polluted_water | Has(SplasherPowerItem.BOUNCY), 1, 1))
        cls.__set_splasher_rule(2, 1, [1])
        cls.__set_splasher_rule(2, 2, [2])
        cls.__set_splasher_rule_no_ckp(2, [3], SplasherPowerRules(SplasherPowerRules.polluted_water, 1, 1))
        cls.__set_splasher_rule(2, 4, [4])
        cls.__set_splasher_rule(2, None, [5, None])
        cls.__set_speedrun_rule(2, SplasherPowerRules(SplasherPowerRules.polluted_water, 1, 1))

        cls.__set_splasher_rule(3, 0, [0], SplasherPowerRules(SplasherPowerRules.polluted_water, 1, 1))
        cls.__set_splasher_rule(3, 1, [1])
        cls.__set_splasher_rule_no_ckp(3, [2], SplasherPowerRules(SplasherPowerRules.polluted_water, 1, 1))
        cls.__set_splasher_rule(3, 3, [3])
        cls.__set_splasher_rule_no_ckp(3, [4], SplasherPowerRules(SplasherPowerRules.polluted_water, 1, 1))
        cls.__set_splasher_rule(3, None, [5, None])
        cls.__set_speedrun_rule(3, SplasherPowerRules(SplasherPowerRules.polluted_water, 1, 1))

        cls.__set_splasher_rule(4, 0, [0])
        cls.__set_splasher_rule_no_ckp(4, [1], SplasherPowerRules(SplasherPowerRules.polluted_water | Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY), 1, 1))
        cls.__set_splasher_rule(4, 2, [2])
        cls.__set_splasher_rule_no_ckp(4, [3], SplasherPowerRules(SplasherPowerRules.polluted_water, 1, 1))
        cls.__set_splasher_rule(4, 4, [4])
        cls.__set_splasher_rule(4, None, [5, None])
        cls.__set_speedrun_rule(4, SplasherPowerRules(SplasherPowerRules.polluted_water, 1, 1))

        cls.__set_splasher_rule_no_ckp(5, [0], SplasherPowerRules(SplasherPowerRules.polluted_water | Has(SplasherPowerItem.BOUNCY), 1, 1))
        cls.__set_splasher_rule(5, None, [1, 2, 3, 4, 5, None])
        cls.__set_speedrun_rule(5, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4))

        cls.__set_splasher_rule(6, 0, [0])
        cls.__set_splasher_rule_no_ckp(6, [1], SplasherPowerRules(Has(SplasherPowerItem.BOUNCY) | (SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY)), 2, 4))
        cls.__set_splasher_rule(6, 2, [2])
        cls.__set_splasher_rule_no_ckp(6, [3], SplasherPowerRules(Has(SplasherPowerItem.STICKY) & (SplasherPowerRules.polluted_water | Has(SplasherPowerItem.BOUNCY)), 2, 4))
        cls.__set_splasher_rule(6, 4, [4])
        cls.__set_splasher_rule(6, None, [5, None])
        cls.__set_speedrun_rule(6, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4))

        cls.__set_splasher_rule(7, 0, [0])
        cls.__set_splasher_rule(7, 1, [1], unstick_rule)
        cls.__set_splasher_rule_no_ckp(7, [2, 3], SplasherPowerRules(SplasherPowerRules.polluted_water & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)), 2, 4))
        cls.__set_splasher_rule(7, 4, [4])
        cls.__set_splasher_rule(7, None, [5, None])
        cls.__set_speedrun_rule(7, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4))

        cls.__set_splasher_rule_no_ckp(8, [0, 3], SplasherPowerRules(Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY), 2, 4))
        cls.__set_splasher_rule(8, 1, [1])
        cls.__set_splasher_rule(8, 2, [2], SplasherPowerRules(SplasherPowerRules.polluted_water & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)), 2, 4))
        cls.__set_splasher_rule(8, 4, [4])
        cls.__set_splasher_rule(8, None, [5, None])
        cls.__set_speedrun_rule(8, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4))

        cls.__set_splasher_rule_no_ckp(9, [2, 4], SplasherPowerRules(SplasherPowerRules.polluted_water & (Has(SplasherPowerItem.BOUNCY) | Has(SplasherPowerItem.STICKY)), 2, 4))
        cls.__set_splasher_rule(9, 0, [0])
        cls.__set_splasher_rule(9, 1, [1])
        cls.__set_splasher_rule(9, 3, [3])
        cls.__set_splasher_rule(9, None, [5, None])
        cls.__set_speedrun_rule(9, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4))

        unstick_rule_sticky = SplasherPowerRules(Has(SplasherPowerItem.STICKY) & (Has(SplasherPowerItem.WATER) | Has(SplasherPowerItem.PROGRESSIVE_WATER, 2) | Has(SplasherPowerItem.BOUNCY)), 2, 4)
        cls.__set_splasher_rule_no_ckp(10, [1, 4], SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4))
        cls.__set_splasher_rule(10, 0, [0], unstick_rule_sticky)
        cls.__set_splasher_rule(10, 2, [2], unstick_rule_sticky)
        cls.__set_splasher_rule(10, 3, [3])
        cls.__set_splasher_rule(10, None, [5, None], unstick_rule_sticky)
        cls.__set_speedrun_rule(10, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4))

        cls.__set_splasher_rule_no_ckp(11, [1, 5], SplasherPowerRules(SplasherPowerRules.polluted_water & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)), 2, 4))
        cls.__set_splasher_rule(11, 0, [0])
        cls.__set_splasher_rule(11, 2, [2], unstick_rule)
        cls.__set_splasher_rule(11, 3, [3])
        cls.__set_splasher_rule(11, 4, [4])
        cls.__set_splasher_rule(11, None, [None])
        cls.__set_speedrun_rule(11, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4))

        cls.__set_splasher_rule_no_ckp(12, [2], SplasherPowerRules(SplasherPowerRules.polluted_water & (Has(SplasherPowerItem.STICKY) | Has(SplasherPowerItem.BOUNCY)), 2, 4))
        cls.__set_splasher_rule_no_ckp(12, [3], SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4))
        cls.__set_splasher_rule(12, 0, [0])
        cls.__set_splasher_rule(12, 1, [1])
        cls.__set_splasher_rule(12, 4, [4])
        cls.__set_splasher_rule(12, None, [5, None])
        cls.__set_speedrun_rule(12, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY), 2, 4))

        cls.__set_splasher_rule_no_ckp(13, [0], SplasherPowerRules(SplasherPowerRules.speed_water & Has(SplasherPowerItem.STICKY), 2, 4))
        cls.__set_splasher_rule_no_ckp(13, [1, 2, 3, 4, 5, None], SplasherPowerRules(SplasherPowerRules.speed_water & Has(SplasherPowerItem.STICKY) & Has(SplasherPowerItem.BOUNCY), 3, 5))
        cls.__set_speedrun_rule(13, SplasherPowerRules(SplasherPowerRules.speed_water & Has(SplasherPowerItem.STICKY) & Has(SplasherPowerItem.BOUNCY), 3, 5))

        cls.__set_splasher_rule_no_ckp(14, [3, 5], SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY), 3, 5))
        cls.__set_splasher_rule(14, 0, [0])
        cls.__set_splasher_rule(14, 1, [1])
        cls.__set_splasher_rule(14, 2, [2])
        cls.__set_splasher_rule(14, 4, [4])
        cls.__set_splasher_rule(14, None, [None])
        cls.__set_speedrun_rule(14, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.STICKY) & Has(SplasherPowerItem.BOUNCY), 3, 5))

        cls.__set_splasher_rule_no_ckp(15, [1], SplasherPowerRules(Has(SplasherPowerItem.BOUNCY), 3, 5))
        cls.__set_splasher_rule_no_ckp(15, [3], SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY), 3, 5))
        cls.__set_splasher_rule(15, 0, [0])
        cls.__set_splasher_rule(15, 2, [2])
        cls.__set_splasher_rule(15, 4, [4])
        cls.__set_splasher_rule(15, None, [5, None])
        cls.__set_speedrun_rule(15, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY) & Has(SplasherPowerItem.STICKY), 3, 5))

        cls.__set_splasher_rule_no_ckp(16, [1, 4], SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY) & Has(SplasherPowerItem.STICKY), 3, 5))
        cls.__set_splasher_rule(16, 0, [0])
        cls.__set_splasher_rule(16, 2, [2])
        cls.__set_splasher_rule(16, 3, [3])
        cls.__set_splasher_rule(16, None, [5, None])
        cls.__set_speedrun_rule(16, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY) & Has(SplasherPowerItem.STICKY), 3, 5))

        cls.__set_splasher_rule_no_ckp(16, [1, 3], SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY) & Has(SplasherPowerItem.STICKY), 3, 5))
        cls.__set_splasher_rule(17, 0, [0])
        cls.__set_splasher_rule(17, 2, [2])
        cls.__set_splasher_rule(17, 4, [4])
        cls.__set_splasher_rule(17, None, [5, None])
        cls.__set_speedrun_rule(17, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY) & Has(SplasherPowerItem.STICKY), 3, 5))

        cls.__set_splasher_rule_no_ckp(18, [2, 4], SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY) & Has(SplasherPowerItem.STICKY), 3, 5))
        cls.__set_splasher_rule(18, 0, [0])
        cls.__set_splasher_rule(18, 1, [1])
        cls.__set_splasher_rule(18, 3, [3])
        cls.__set_splasher_rule(18, None, [5, None])
        cls.__set_speedrun_rule(18, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY) & Has(SplasherPowerItem.STICKY), 3, 5))

        cls.__set_splasher_rule_no_ckp(19, [0], SplasherPowerRules(Has(SplasherPowerItem.BOUNCY), 3, 5))
        cls.__set_splasher_rule_no_ckp(19, [4], SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY), 3, 5))
        cls.__set_splasher_rule(19, 1, [1])
        cls.__set_splasher_rule(19, 2, [2])
        cls.__set_splasher_rule(19, 3, [3])
        cls.__set_splasher_rule(19, None, [5, None])
        cls.__set_speedrun_rule(19, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY) & Has(SplasherPowerItem.STICKY), 3, 5))

        cls.__set_splasher_rule_no_ckp(20, [1, 4], SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY), 3, 5))
        cls.__set_splasher_rule(20, 0, [0])
        cls.__set_splasher_rule(20, 2, [2])
        cls.__set_splasher_rule(20, 3, [3])
        cls.__set_splasher_rule(20, None, [5, None])
        cls.__set_speedrun_rule(20, SplasherPowerRules(SplasherPowerRules.polluted_water & Has(SplasherPowerItem.BOUNCY) & Has(SplasherPowerItem.STICKY), 3, 5))

        cls.__set_splasher_rule(21, 1, [0])
        cls.__set_splasher_rule(21, 2, [1])
        cls.__set_splasher_rule(21, 3, [2])
        cls.__set_splasher_rule(21, 4, [3])
        cls.__set_splasher_rule(21, 6, [4, 5])
        cls.__set_splasher_rule(21, None, [None])
        cls.__set_speedrun_rule(21, SplasherPowerRules(SplasherPowerRules.speed_water & Has(SplasherPowerItem.STICKY) & Has(SplasherPowerItem.BOUNCY), 3, 5))