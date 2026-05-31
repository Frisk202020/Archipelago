from __future__ import annotations

from _collections_abc import dict_keys
from typing import ClassVar
from enum import StrEnum
from random import Random

from BaseClasses import Item,ItemClassification
from worlds.splasher.utils import SplasherUtils
from .regions import SplasherLevelName

class SplasherItemGroupName(StrEnum):
    POWERS = "powers"
    FILLERS = "fillers"
    TRAPS = "traps"
    ESSENCE = "essence"
    KEYS = "keys"

    def create_items(self, player: int) -> list[SplasherItem]:
        return [SplasherItem(x, player) for x in _ItemGroup.group(self).names]
    
    def get_random(self, rng: Random):
        names = _ItemGroup.group(self).names
        return names[rng.randint(0, len(names) - 1)]
    
    @staticmethod
    def get_filler(rng: Random, include_essence: bool) -> str:
        group = [
            SplasherItemGroupName.FILLERS, SplasherItemGroupName.ESSENCE
        ][rng.randint(0, 1)] if include_essence else SplasherItemGroupName.FILLERS

        return group.get_random(rng) 
    
class SplasherPowerItem(StrEnum):
    WATER = "Water Unlock"
    STICKY = "Sticky Paint Unlock"
    BOUNCY = "Bouncy Paint Unlock"

    @classmethod
    def literals(cls) -> list[str]:
        return [item.value for item in cls]

class _ItemGroup:
    classification: ItemClassification
    names: list[str]

    type Group = dict[SplasherItemGroupName, _ItemGroup]
    __groups: ClassVar[Group] = {}

    def __init__(self, names: list[str], classification: ItemClassification=ItemClassification.progression):
        self.names = names
        self.classification = classification        

    @staticmethod
    def groups() -> Group:
        if (len(_ItemGroup.__groups) == 0):
            _ItemGroup.__groups = {
                SplasherItemGroupName.POWERS: _ItemGroup(SplasherPowerItem.literals()), 
                SplasherItemGroupName.FILLERS: _ItemGroup([
                    "Job Promotion"
                ], ItemClassification.filler), SplasherItemGroupName.TRAPS: _ItemGroup([
                    "Paint Swap",
                    "Body Aches"
                ], ItemClassification.trap), SplasherItemGroupName.ESSENCE: _ItemGroup(
                    [f"Essence ({i})" for i in [1, 10, 25, 50]], ItemClassification.filler
                ), SplasherItemGroupName.KEYS: _ItemGroup(SplasherLevelName.for_all(lambda x: f"{x} : Entrance Key"))
            }

        return _ItemGroup.__groups
    
    @staticmethod
    def group(name: SplasherItemGroupName) -> _ItemGroup:
        return _ItemGroup.groups()[name]    
    
class _ItemData:
    code: int
    classification: ItemClassification
    __next: ClassVar[int] = SplasherUtils.base_id

    def __init__(self, classification: ItemClassification = ItemClassification.progression):
        self.code = _ItemData.__next
        self.classification = classification
        _ItemData.__next += 1

    __data_table: dict[str, _ItemData] = {}

    @staticmethod
    def data_table() -> dict[str, _ItemData]: 
        if (len(_ItemData.__data_table) == 0):
            _ItemData.__data_table[SplasherItem.victory] = _ItemData()
            _ItemData.__data_table[SplasherUtils.splasher] = _ItemData()
            _ItemData.__data_table[SplasherItem.progressive_power] = _ItemData()

            for group in _ItemGroup.groups().values():
                for name in group.names:
                    _ItemData.__data_table[name] = _ItemData(group.classification)

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
