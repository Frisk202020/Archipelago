from __future__ import annotations
from typing import ClassVar

class SplasherUtils:
    splasher: ClassVar[str] = "Splasher"
    base_id: ClassVar[int] = 0xF4A201
    regular_splashers: ClassVar[int] = 132
    golden_splashers: ClassVar[int] = 22
    origin = "Hub"

    level_names: ClassVar[list[str]] = [
        "Welcome to Inkorp", "Potatoes Ink", "Stick To The Plan",
        "Let It Bounce", "Jump On The Water", "A Bad Encounter",
        "There Will Be Fries", "Ray Man Origin", "Stick On The Water",
        "Ink In  Park", "Wind Walker", "Troopers Please",
        "Water Is Coming", "Inkorp Express", "Big Bounce Theory",
        "Toxink Bubbles", "Storm Wind", "Ray Man Legend",
        "Toxink Avenger", "The Glados Principle", "Apocalink Now",
        "Good Luck Splasher"
    ]
    speedrun_names: ClassVar[list[str]] = [f"{x} - Time Attack" for x in level_names]

    level_count: ClassVar[int] = 22

    @classmethod
    def level(cls, i: int, speedrun: bool):
        if (i < 0 or i > 21):
            return f"Invalid level ({i})"
        return cls.speedrun_names[i] if speedrun else cls.level_names[i]

    zone_names: ClassVar[list[str]]  = [
        "Reception Hub", "Water Pool", 
        "Ray Man Paradise", "Toxink Hell",
        "Inkorp Outskirts", "Fun Park",
        "Docteur's Office"
    ]

    @classmethod
    def zone_for_level(cls, level: int):
        match(level):
            case 0 | 1 | 2 | 6 : return 0
            case 4 | 5 | 8 | 12 : return 1
            case 7 | 11 | 17 | 19 : return 2
            case 15 | 18 | 20 : return 3
            case 10 | 13 | 16 : return 4
            case 3 | 9 | 14 : return 5
            case 21 : return 6
            case _ : raise Exception(f"Unrecognized level id : {level}")