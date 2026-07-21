from typing import ClassVar
from dataclasses import dataclass

from Options import DefaultOnToggle, OptionGroup, Choice, Range, PerGameCommonOptions, Toggle

from .utils import SplasherUtils

class IncludeKeys(Choice):
    """
    Determine if levels should be locked behind keys
    If enabled, the first level will still be unlocked

    Off - Do not include keys : every level is unlocked from start
    Zone - Include thematic keys : each key unlocks from 3 to 5 levels
    Level - Include a key for each level : each key unlocks one level
    """
    display_name = "Include Keys"
    option_off = 0
    option_zone = 1
    option_level = 2

class IncludeSpeedrunKeys(Toggle):
    """
    Determine if time attack should have its own keys. This is only relevant if `Include Keys` is enabled.

    Off - A key unlocks a level in both modes
    On - Include keys specific to Time Attack. Key pattern will match the one of `Include Keys` (Off, Zone or Level)
    """
    display_name = "Include Speedrun Keys"

# Will be implemented in future updates
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
    default = option_off

class IncludeEssenceItem(DefaultOnToggle):
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
    On Except Water - Randomize Stickink and Bouncink, but unlock Water as normal. This prevents the early game to be too restrictive.
    Progressive - Powers are randomized as progressive items : water, then stickink, then bouncink
    """
    display_name = "Randomize Powers"
    option_off = 0
    option_on = 1
    option_on_except_water = 2
    option_progressive = 3
    default = option_on

class RandomizeGoldenSplashers(DefaultOnToggle):
    """
    Determine if golden splashers are added in the item pool
    """
    display_name = "Randomize Golden Splashers"

# Traps will be implemented in a future update
class TrapChance(Range):
    """
    Average amount of traps in the filler pool
    """
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 0

class DeathLink(Range):
    """
    Determine how to enable death link

    0 or less : disabled
    1 or more : number of deaths to trigger a death link (max 100)
    """
    display_name = "DeathLink"
    range_start = 0
    range_end = 100
    default = 0

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
    default = option_off

class SplashersGoal(Range):
    """
    Determine how many splashers are needed to unlock the final level
    """
    display_name = "Splashers Goal"
    range_start = 0
    range_end = SplasherUtils.regular_splashers + SplasherUtils.golden_splashers 
    default = 80

class HeroMode(Toggle):
    """
    Enable Hero Mode, in which killing a Splasher triggers a death for the player as well.
    Notice this counts towards Death Link if enabled
    """
    display_name = "Hero Mode"

# Will be implemented in future updates
@dataclass
class EssenceSanity(Choice):
    """
    Turn essence count (in each level) into a location of its own.

    Off - Disabled, only the golden splasher is a location (if enabled)
    On - Each 100-points milestone is a location : this adds 154 locations
    Madness - Each 10-points milestone is a location : this adds 1540 locations
    Insanity - Every single new milestone is a location : this adds 15400 locations
    """
    display_name = "Essence Sanity"
    option_off = 0
    option_on = 1
    option_madness = 2
    option_insanity = 3

@dataclass
class SplasherOptions(PerGameCommonOptions):
    # randomize_checkpoints: RandomizeCheckpoints
    include_essence_items: IncludeEssenceItem
    randomize_powers: RandomizePowers
    randomize_golden_splashers: RandomizeGoldenSplashers
    splashers_goal: SplashersGoal
    include_medals: IncludeMedals
    trap_chance: TrapChance
    death_link: DeathLink
    hero_mode: HeroMode
    include_keys: IncludeKeys
    include_speedrun_keys: IncludeSpeedrunKeys
    # essence_sanity: EssenceSanity

# Can't attach option_groups in SplasherOptions as it crashes Generate Template Options
class SplasherOptionExports:
    option_groups: ClassVar[list[OptionGroup]] = [
        OptionGroup(
            "Randomizer options",
            [RandomizePowers, RandomizeGoldenSplashers, IncludeKeys]
        ), OptionGroup(
            "Goal",
            [SplashersGoal]
        ), OptionGroup(
            "Optional items",
            [IncludeEssenceItem]
        ), OptionGroup(
            "Making your life miserable",
            [HeroMode, TrapChance, DeathLink]
        )
    ]