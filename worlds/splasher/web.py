from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld
from .options import option_groups

class SplasherWebWorld(WebWorld):
    game = "Splasher"
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
    option_groups = option_groups
    options_presets = {}
