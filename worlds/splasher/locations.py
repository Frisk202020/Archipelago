from __future__ import annotations
from abc import ABC, abstractmethod
from typing import ClassVar, NamedTuple

from BaseClasses import Location
from enum import StrEnum

from worlds.splasher.items import PowerItem, SplasherItem
from .regions import SplasherLevelName
from .world import SplasherWorld
from .options import RandomizePowers,IncludeMedals

class SplasherLocation(Location):
    game = "Splasher"
    def __init__(self, world: SplasherWorld, data: _LocationData):
        Location.__init__(self, world.player, data.name, data.code, world.get_region(data.region))

    @staticmethod
    def get_code_table() -> dict[str, int]:
        return _LocationData.name_to_id

    @staticmethod
    def _from_list(world: SplasherWorld, data: list[_LocationData]) -> list[SplasherLocation]:
        return [SplasherLocation(world, x) for x in data]
    
    @staticmethod
    def create_locations(world: SplasherWorld) -> list[SplasherLocation]:
        locations: list[SplasherLocation] = SplasherLocation._from_list(world, _Clears.get())
        locations[21].place_locked_item(SplasherItem(SplasherItem.victory, world.player)) # place on last level clear

        splashers_classes: list[type[_Splasher]] = [
            _FirstSplasher, _SecondSplasher, _ThirdSplasher, 
            _FourthSplasher, _FifthSplasher, _SixthSplasher
        ]
        for x in splashers_classes:
            locations += SplasherLocation._from_list(world, x.get())

        if world.options.randomize_powers >= RandomizePowers.option_on:
            locations += SplasherLocation._from_list(world, _Powers.get())

        if world.options.randomize_golden_splashers:
            locations += SplasherLocation._from_list(world, _GoldenSplashers.get())

        if world.options.include_medals == IncludeMedals.option_platinum:
            locations += SplasherLocation._from_list(world, _Platinums.get())
        if world.options.include_medals >= IncludeMedals.option_gold:
            locations += SplasherLocation._from_list(world, _Golds.get())
        if world.options.include_medals >= IncludeMedals.option_silver:
            locations += SplasherLocation._from_list(world, _Silvers.get())
        if world.options.include_medals >= IncludeMedals.option_silver:
            locations += SplasherLocation._from_list(world, _Bronzes.get())

        return locations

class _LocationName(StrEnum):
    CLEAR = "Clear"
    SPLASHER = "Splasher"
    BRONZE = "Bronze Medal"
    SILVER = "Silver Medal"
    GOLD = "Gold Medal"
    PLATINUM = "Platinum Medal"
    WATER = "Water Gun Unlock"
    STICKY = "Sticky Paint Unlock"
    BOUNCY = "BouncyPaintUnlock"

class _InnerLocationData(NamedTuple):
    level_id: int
    required_items: list[PowerItem]
    require_splashers: bool = False

class _LocationData:
    name: str
    region: str
    code: int
    required_items: list[PowerItem]
    name_to_id: ClassVar[dict[str, int]] = {}
    __next: ClassVar[int] = SplasherWorld.base_id

    def __init__(self, name: _LocationName, inner: _InnerLocationData, name_suffix: str|None):
        region = SplasherLevelName.level(inner.level_id)
        self.name = f"{region} : {name}{"" if name_suffix is None else f'({name_suffix})'}"
        self.region = region
        self.code = _LocationData.__next
        self.required_items

        _LocationData.__next += 1
        _LocationData.name_to_id[name] = self.code

class _LocationDataContainer(ABC):
    _data: list[_InnerLocationData]

    @classmethod
    def get(cls) -> list[_LocationData]:
        if (len(cls._data) == 0):
            cls.init()

        return [_LocationData(cls.name(), x, cls.suffix()) for x in cls._data]
    
    @staticmethod
    def suffix() -> str|None:
        return None
    
    @abstractmethod
    @staticmethod
    def name() -> _LocationName:
        ...

    @abstractmethod
    @classmethod
    def init(cls) -> None:
        ...

class _Splasher(_LocationDataContainer):
    @staticmethod
    def name() -> _LocationName:
        return _LocationName.SPLASHER

class _GoldenSplashers(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "Gold"

    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _FirstSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "(First)"

    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(0, [])
        ] + [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _SecondSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "(Second)"
    
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(0, [])
        ] + [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _ThirdSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "(Third)"
    
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(0, [])
        ] + [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _FourthSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "(Fourth)"
    
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(0, [])
        ] + [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _FifthSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "(Fifth)"
    
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _SixthSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "(Sixth)"
    
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _Clears(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _Platinums(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _Golds(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _Silvers(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _Bronzes(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [PowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [PowerItem.WATER, PowerItem.STICKY, PowerItem.BOUNCY], True)
        ]

class _Powers(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls.__data = [
            _InnerLocationData(0, []), _InnerLocationData(5, [PowerItem.WATER]), _InnerLocationData(13, [PowerItem.WATER, PowerItem.STICKY])
        ]