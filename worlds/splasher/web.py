from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld
from worlds.splasher.utils import SplasherUtils
from .options import SplasherOptionExports


class SplasherWebWorld(WebWorld):
    game = SplasherUtils.splasher
    theme = "partyTime"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Splasher for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Frisk"],
    )
    setup_fr = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Splasher for MultiWorld.",
        "French",
        "setup_fr.md",
        "setup/fr",
        ["Frisk"],
    )

    tutorials = [setup_en, setup_fr]
    option_groups = SplasherOptionExports.option_groups
    options_presets = {}
