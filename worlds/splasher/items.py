from __future__ import annotations
from _collections_abc import dict_keys
from typing import ClassVar
from enum import StrEnum
from random import Random

from BaseClasses import Item,ItemClassification

from .utils import SplasherUtils

class SplasherKey:
    @staticmethod
    def key(i: int, speedrun: bool) -> str:
        return f"{SplasherUtils.level(i, speedrun)} : Entrance Key"
    
    @classmethod
    def keys(cls, speedrun: bool):
        return [cls.key(i, speedrun) for i in range(1, SplasherUtils.level_count)]
    
class SplasherZoneKey:
    __keys: ClassVar[list[str]] = [f"{x} : Zone Keys" for x in [
        "Reception Hub", "Water Pool", 
        "Ray Man Paradise", "Toxink Hell",
        "Inkorp Outskirts", "Fun Park",
        "Docteur's Office"
    ]]

    @staticmethod
    def __key_name(key: str, speedrun: bool) -> str:
        return f"{key} - Time Attack" if speedrun else key

    @classmethod
    def keys(cls, speedrun: bool) -> list[str]:
        if speedrun: return [cls.__key_name(key, speedrun) for key in cls.__keys]
        return cls.__keys

    @classmethod
    def key(cls, id: int, speedrun: bool) -> str:
        match(id):
            case 1 | 2 | 6 : i = 0
            case 4 | 5 | 8 | 12 : i = 1
            case 7 | 11 | 17 | 19 : i = 2
            case 15 | 18 | 20 : i = 3
            case 10 | 13 | 16 : i = 4
            case 3 | 9 | 14 : i = 5
            case 21 : i = 6
            case _ : return ""
        return cls.__key_name(cls.__keys[i], speedrun)
    
class SplasherFiller:
    filler: ClassVar[list[str]] = ["Job Promotion"]
    trap: ClassVar[list[str]] = ["Paint Swap", "Body Aches"]
    essence: ClassVar[list[str]] = [f"Essence ({x})" for x in [1, 10, 25, 50]]

    @classmethod
    def get(cls, trap_chance: int, include_essence: bool, rng: Random) -> str:
        if trap_chance > 0 and rng.randint(0, 99) < trap_chance:
            return cls.trap[rng.randint(0, len(cls.trap)-1)]

        if include_essence:
            i = rng.randint(0, len(cls.filler) + len(cls.essence) - 1)
            if i < len(cls.filler):
                return cls.filler[i]
            return cls.essence[i - len(cls.filler)]
        
        return cls.filler[rng.randint(0, len(cls.filler) - 1)]
        
class SplasherPowerItem(StrEnum):
    WATER = "Water Unlock"
    STICKY = "Sticky Paint Unlock"
    BOUNCY = "Bouncy Paint Unlock"

    @classmethod
    def literals_except_water(cls) -> list[str]:
        return [cls.STICKY.value, cls.BOUNCY.value]

    @classmethod
    def literals(cls) -> list[str]:
        return [item.value for item in cls]
    
class _ItemData:
    code: int
    classification: ItemClassification
    __next: ClassVar[int] = SplasherUtils.base_id

    def __init__(self, classification: ItemClassification = ItemClassification.progression):
        self.code = _ItemData.__next
        self.classification = classification
        _ItemData.__next += 1

    __data_table: dict[str, _ItemData] = {}

    @classmethod
    def data_table(cls) -> dict[str, _ItemData]: 
        if (len(cls.__data_table) > 0): return cls.__data_table

        cls.__data_table[SplasherItem.victory] = _ItemData()
        cls.__data_table[SplasherUtils.splasher] = _ItemData()
        cls.__data_table[SplasherItem.progressive_power] = _ItemData()

        for name in SplasherPowerItem.literals():
            cls.__data_table[name] = _ItemData()

        for name in SplasherFiller.filler:
            cls.__data_table[name] = _ItemData(ItemClassification.filler)

        for name in SplasherFiller.essence:
            cls.__data_table[name] = _ItemData(ItemClassification.filler)

        for name in SplasherFiller.trap:
            cls.__data_table[name] = _ItemData(ItemClassification.trap)

        for name in SplasherKey.keys(False):
            cls.__data_table[name] = _ItemData()

        for name in SplasherZoneKey.keys(False):
            cls.__data_table[name] = _ItemData()

        for name in SplasherKey.keys(True):
            cls.__data_table[name] = _ItemData()

        for name in SplasherZoneKey.keys(True):
            cls.__data_table[name] = _ItemData()

        return _ItemData.__data_table

class SplasherItem(Item):
    game = SplasherUtils.splasher
    victory: ClassVar[str] = "Freedom"
    progressive_power: ClassVar[str] = "Progressive Power Unlock"

    def __init__(self, name: str, player: int):
        data = _ItemData.data_table()[name]
        Item.__init__(self, name, data.classification, data.code, player)

    @staticmethod
    def get_code(name: str) -> int:
        return _ItemData.data_table()[name].code
    
    @staticmethod
    def keys() -> dict_keys[str, _ItemData]:
        return _ItemData.data_table().keys()   
