from Options import OptionGroup, Toggle,Choice,Range, PerGameCommonOptions
from dataclasses import dataclass

"""
TODO (future versions) : implement level randomization options:
-> Open World (default) : ideal for non-blocking multiplayer
-> Open : lock levels behind keys, for longer multiplayer sessions
-> Closed : Each level clear unlocks the next, but order is randomized : for solo sessions
"""

class RandomizeCheckpoints(Choice):
    """
    Determine if level checkpoints are added to the item pool

    Off - Not included
    Required - Included in pool, but as a progression item (consider items after a locked checkpoint are unreachable)
    Chaotic - Included in pool, but as an useful item
    """
    display_name = "Randomize level checkpoints"
    option_off = 0
    option_required = 1
    option_chaotic = 2

class IncludeEssenceItem(Toggle):
    """
    Determine if the pool includes essence items in the junk pool. 
    These are stored until a manual release inside a level, upon which these are added to the current counter.
    """
    display_name = "Include essence items"

class RandomizePowers(Choice):
    """
    Determine how to unlock powers (water and paint) in the game

    Off - Powers aren't randomized : you need to reach the power unlock in the intended level
    On - Power unlocks are randomized into the pool
    Progressive - Powers are randomized and fire delay is increased, needing pool items to reach its original balance
    """
    display_name = "Randomize Powers"
    option_off = 0
    option_on = 1
    option_progressive = 2

class RandomizeGoldenSplashers(Toggle):
    """
    Determine if golden splashers are added in the item pool
    """
    display_name = "Randomize Golden Splashers"

class TrapChance(Range):
    """
    Average amount of traps in the filler pool
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100

class IncludeMedals(Choice):
    """
    Determine if speedrun medals should reward a check. If enabled, each tier rewards a check.

    Off - Not included 
    Bronze - Reward up to bronze medals
    Silver - Reward up to silver medals
    Gold - Reward up to gold medals
    Platinum - Reward up to platinum medals
    """
    display_name = "Include Speedrun Medals"
    option_off = 0
    option_bronze = 1
    option_silver = 2
    option_gold = 3
    option_platinum = 4

class SplashersGoal(Range):
    """
    Determine how many splashers are needed to unlock the final level
    """
    display_name = "Splashers Goal"
    range_start = 0
    range_end = 154   

@dataclass
class SplasherOptions(PerGameCommonOptions):
    randomize_checkpoints: RandomizeCheckpoints
    include_essence_items: IncludeEssenceItem
    randomize_powers: RandomizePowers
    randomize_golden_splashers: RandomizeGoldenSplashers
    splashers_goal: SplashersGoal
    include_medals: IncludeMedals
    trap_chance: TrapChance

option_groups = [
    OptionGroup(
        "Randomizer options",
        [RandomizeCheckpoints, RandomizePowers, RandomizeGoldenSplashers]
    ), OptionGroup(
        "Goal",
        [SplashersGoal]
    ), OptionGroup(
        "Optional items",
        [IncludeEssenceItem]
    ), OptionGroup(
        "Traps",
        [TrapChance]
    )
]