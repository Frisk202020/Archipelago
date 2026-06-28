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
    level_count: ClassVar[int] = 22

    @classmethod
    def level(cls, i: int):
        if (i < 0 or i > 21):
            return f"Invalid level ({i})"
        return cls.level_names[i]