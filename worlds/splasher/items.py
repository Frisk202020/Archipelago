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
    filler: ClassVar[list[str]] = ["Job Promotion", "Le Docteur's autograph", "A Secreatire's ticket"]
    trap: ClassVar[list[str]] = ["Paint Swap", "Mad Gun", "Feet State"]
    essence: ClassVar[list[str]] = [
        "Essence drop", "Essence drops", "Broken essence flask",
        "Full essence flask", "Dry essence barrel", "Essence barrel",
        "Overflowing essence barrel", "Goombase essence tank",
        "Secretaire essence tank", "Docteur's essence storage"
    ] # 1, 2, 5, 10, 15, 20, 25, 30, 40, 50
    essence_traps: ClassVar[list[str]] = [
        "Minor essence leak", "Small essence leak", "Noticeable essence leak",
        "Severe essence leak", "Essence container crack", "Forgiving essence fee",
        "Severe essence fee", "Le Docteur's essence tax"
    ] # 1, 2, 3, 5, 10, 15, 20, 25

    @staticmethod
    def random_item(l: list[str], rng: Random) -> str:
        return l[rng.randint(0, len(l)-1)]

    @classmethod
    def get_remaining(cls, player: int, request: int, trap_chance: int, essence_storage: int, essence_traps: int, rng: Random) -> list[SplasherItem]:
        out: list[SplasherItem] = []
        pool = cls.filler + [cls.essence[i] for i in range(essence_storage)]
        trap_pool = cls.trap + [cls.essence_traps[i] for i in range(essence_traps)]

        for _ in range(request):
            item = SplasherFiller.random_item(trap_pool, rng) if rng.randint(0, 99) < trap_chance else SplasherFiller.random_item(pool, rng)
            out.append(SplasherItem(item, player))

        return out
        
class SplasherPowerItem(StrEnum):
    PROGRESSIVE_WATER = "Progressive Water"
    WATER = "Water Gun"
    STICKY = "Stickink Gun"
    BOUNCY = "Bouncink Gun"

    @classmethod
    def literals(cls):
        return [x.value for x in cls]

    @classmethod
    def pool(cls, progressive_water: int | None) -> list[str]:
        match progressive_water:
            case None: return [x.value for x in [cls.STICKY, cls.BOUNCY]] 
            case 0: return [x.value for x in [cls.WATER, cls.STICKY, cls.BOUNCY]]
            case _: return [cls.PROGRESSIVE_WATER for _ in range(progressive_water)] + [x.value for x in [cls.STICKY, cls.BOUNCY]]

class SplasherCheckpoint:
    __specific_ids: ClassVar[dict[int, int]] = {
        0: 3,
        5: 3,
        13: 4,
        14: 4,
        21: 7
    }

    @staticmethod
    def name(level: int, id: int) -> str:
        return f"{SplasherUtils.level_names[level]} - Checkpoint {1 + id}"

    @classmethod
    def id_range(cls, level: int) -> int:
        return cls.__specific_ids.get(level) or 5

    @classmethod
    def items(cls) -> list[str]:
        out: list[str] = []
        for i in range(SplasherUtils.level_count):
            for j in range(cls.id_range(i)): 
                out.append(cls.name(i, j))

        return out
    
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

        for name in SplasherFiller.trap:
            cls.__data_table[name] = _ItemData(ItemClassification.trap)

        for name in SplasherFiller.essence:
            cls.__data_table[name] = _ItemData(ItemClassification.useful)

        for name in SplasherFiller.essence_traps:
            cls.__data_table[name] = _ItemData(ItemClassification.trap)

        for name in SplasherKey.keys(False):
            cls.__data_table[name] = _ItemData()

        for name in SplasherZoneKey.keys(False):
            cls.__data_table[name] = _ItemData()

        for name in SplasherKey.keys(True):
            cls.__data_table[name] = _ItemData()

        for name in SplasherZoneKey.keys(True):
            cls.__data_table[name] = _ItemData()

        for name in SplasherCheckpoint.items():
            cls.__data_table[name] = _ItemData(ItemClassification.useful)

        return _ItemData.__data_table
    
    @classmethod
    def group_table(cls) -> dict[str, set[str]]:
        out: dict[str, set[str]] = {}
        out["Powers"] = set(SplasherPowerItem.literals())
        out["Filler"] = set(SplasherFiller.filler)
        out["Traps"] = set(SplasherFiller.trap)
        out["Essence"] = set(SplasherFiller.essence)
        out["Level Keys"] = set(SplasherKey.keys(False))
        out["Level Keys - Time Attack"] = set(SplasherKey.keys(True))
        out["Zone Keys"] = set(SplasherZoneKey.keys(False))
        out["Zone Keys - Time Attack"] = set(SplasherZoneKey.keys(True))
        out["Checkpoints"] = set(SplasherCheckpoint.items())

        return out

class SplasherItem(Item):
    game = SplasherUtils.splasher
    victory: ClassVar[str] = "Freedom"
    progressive_power: ClassVar[str] = "Progressive Power Unlock"

    def __init__(self, name: str, player: int):
        data = _ItemData.data_table()[name]
        Item.__init__(self, name, data.classification, data.code, player)

    @staticmethod
    def group_table():
        return _ItemData.group_table()

    @staticmethod
    def get_code(name: str) -> int:
        return _ItemData.data_table()[name].code
    
    @staticmethod
    def keys() -> dict_keys[str, _ItemData]:
        return _ItemData.data_table().keys()   
