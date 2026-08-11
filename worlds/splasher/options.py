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

class EssenceStorage(Choice):
    """
    Determine how to include essence storage items in the pool. Essence storage lowers permanently the goal to save the golden splasher, these are useful items included as filler.
    If enabled, you can choose a balance that avoids essence to be irrelevant when having too few filler or to trivialize essence progression when flooded with fillers.
    Notice that setting higher options only *allows* to include bigger items, but what will actually be chosen is still random.
    
    Off - Do not include these items
    Light - Only include small items (up to 5 essence per item)
    Rich - Include items sending up to 25 essence
    Abundant - Include items sending up to 50 essence
    """
    option_name = "Essence balancing"
    option_off = 0
    option_light = 3
    option_rich = 7
    option_abundant = 10
    default = option_light

class EssenceTraps(Choice):
    """
    Determine how to include essence traps in the pool. Traps will increase back the essence counter, though the goal is capped at 700.
    If essence items are not enabled but this option is, these traps will still be included but have no actual effect (since goal will never drop bellow 700).
    Also, this option will have no effect if trap chance is set to 0 (which is the default).

    Off - Do not include these traps
    Forgiving - Only include small traps (up to 3 lost essence per trap)
    Annoying - Include traps removing up to 10 essence storage
    A Bad Time - Include traps removing up to 25 essence storage
    """
    option_name = "Essence traps balancing"
    option_off = 0
    option_forgiving = 3
    option_annoying = 5
    option_a_bad_time = 8
    default = option_off

class RandomizePowers(Choice):
    """
    Determine how to unlock powers (water and paint) in the game

    Off - Powers aren't randomized : you need to reach the power unlock in the intended level
    On - Power unlocks are randomized into the pool
    On Except Water - Randomize Stickink and Bouncink, but unlock Water as normal. This prevents the early game to be too restrictive.
    Progressive - Powers are randomized as progressive items : progressive water, then stickink, then bouncink
    """
    display_name = "Randomize Powers"
    option_off = 0
    option_on = 1
    option_on_except_water = 2
    option_progressive = 3
    default = option_on

class ProgressiveWater(Toggle):
    """
    Determine if water is progressive. This option is only relevant if `Randomize Powers` is not `Off`.
    If enabled, water now has 3 levels : polluted, clean and speedink
    - Polluted water is a weaker water (25% of the damage) and kills you (and splashers) on contact
    - Clean water is vanilla water, except it can't damage bubons of the Inkorp Express or the Secretaire.
    - Speedink doubles your speed on floor contact and is able to damage bubons. It is required to goal.

    Now, the option you choose for your powers randomization changes how progressive water is placed in the pool :
    - On default randomization, 3 progressive water items are placed along with bouncink and stickink
    - On progressive randomization, progressive water unlocks before the rest. This means stickink is now level 4 and bouncink is level 5
    - On randomization excluding water, the water gun unlock will give you the first level of progressive water. Those remaining are placed into the pool.
    """
    display_name = "Progressive Water"

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

class SplasherPool(Range):
    """
    Define how many splashers, among those unnecessary to reach the goal, are kept as actual splashers.
    The remaining will be converted as filler / essence / traps.

    You define a percentage, so for example 0% means only the exact amount of splashers required by the goal will be placed, 
    while 100% means all 154 splashers will be included in the pool.
    """
    display_name = "Splasher Pool"
    range_start = 0
    range_end = 100
    default = 0

@dataclass
class SplasherOptions(PerGameCommonOptions):
    essence_storage: EssenceStorage
    essence_traps: EssenceTraps
    randomize_powers: RandomizePowers
    randomize_golden_splashers: RandomizeGoldenSplashers
    splashers_goal: SplashersGoal
    include_medals: IncludeMedals
    trap_chance: TrapChance
    death_link: DeathLink
    hero_mode: HeroMode
    include_keys: IncludeKeys
    include_speedrun_keys: IncludeSpeedrunKeys
    progressive_water: ProgressiveWater
    splasher_pool: SplasherPool
    # randomize_checkpoints: RandomizeCheckpoints
    # essence_sanity: EssenceSanity

# Can't attach option_groups in SplasherOptions as it crashes Generate Template Options
class SplasherOptionExports:
    option_groups: ClassVar[list[OptionGroup]] = [
        OptionGroup(
            "Randomizer options",
            [RandomizePowers, ProgressiveWater, RandomizeGoldenSplashers, IncludeMedals, IncludeKeys, IncludeSpeedrunKeys, SplasherPool]
        ), OptionGroup(
            "Goal",
            [SplashersGoal]
        ), OptionGroup(
            "Optional items",
            [EssenceStorage, EssenceTraps]
        ), OptionGroup(
            "Making your life miserable",
            [HeroMode, TrapChance, DeathLink]
        )
    ]