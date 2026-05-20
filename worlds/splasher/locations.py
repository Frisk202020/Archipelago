from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, NamedTuple
from enum import StrEnum

from BaseClasses import Location
from rule_builder.rules import Has, HasAll
from worlds.splasher.items import SplasherPowerItem, SplasherItem
from worlds.splasher.utils import SplasherUtils
from .regions import SplasherLevelName
from .options import RandomizePowers,IncludeMedals

if TYPE_CHECKING:
    from .world import SplasherWorld

class SplasherLocation(Location):
    game = SplasherUtils.splasher
    def __init__(self, world: SplasherWorld, data: _LocationData):
        Location.__init__(self, world.player, data.name, data.code, world.get_region(data.region))
        
        access_rule = HasAll(*SplasherPowerItem.literals())
        if data.require_splashers:
            access_rule &= Has(SplasherUtils.splasher, world.options.splashers_goal.value)

    @staticmethod
    def get_code_table() -> dict[str, int]:
        return _LocationData.name_to_id

    @staticmethod
    def _from_list(world: SplasherWorld, data: list[_LocationData]) -> list[SplasherLocation]:
        return [SplasherLocation(world, x) for x in data]
    
    # need to add locations to regions instead of returning
    @staticmethod
    def create_locations(world: SplasherWorld) -> None:
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

        for location in  locations:
            if location.parent_region is not None:
                location.parent_region.locations.append(location)

class _LocationName(StrEnum):
    CLEAR = "Clear"
    SPLASHER = SplasherUtils.splasher
    BRONZE = "Bronze Medal"
    SILVER = "Silver Medal"
    GOLD = "Gold Medal"
    PLATINUM = "Platinum Medal"
    WATER = "Water Gun Unlock"
    STICKY = "Sticky Paint Unlock"
    BOUNCY = "BouncyPaintUnlock"

class _InnerLocationData(NamedTuple):
    level_id: int
    required_items: list[SplasherPowerItem]
    require_splashers: bool = False

class _LocationData:
    name: str
    region: str
    code: int
    required_items: list[SplasherPowerItem]
    require_splashers: bool

    name_to_id: ClassVar[dict[str, int]] = {}
    __next: ClassVar[int] = SplasherUtils.base_id

    def __init__(self, name: _LocationName, inner: _InnerLocationData, name_suffix: str|None):
        region = SplasherLevelName.level(inner.level_id)
        self.name = f"{region} : {name}{"" if name_suffix is None else f'({name_suffix})'}"
        self.region = region
        self.code = _LocationData.__next
        self.required_items = inner.required_items
        self.require_splashers = inner.require_splashers

        _LocationData.__next += 1
        _LocationData.name_to_id[name] = self.code

class _LocationDataContainer(ABC):
    _data: list[_InnerLocationData]|None = None

    @classmethod
    def get(cls) -> list[_LocationData]:
        if (cls._data is None):
            cls.init()

        return [] if cls._data is None else [_LocationData(cls.name(), x, cls.suffix()) for x in cls._data]
    
    @staticmethod
    def suffix() -> str|None:
        return None

    @staticmethod
    @abstractmethod
    def name() -> _LocationName:
        ...

    @classmethod
    @abstractmethod
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
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _FirstSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "First"

    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(0, [])
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _SecondSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "Second"
    
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(0, [])
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _ThirdSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "Third"
    
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(0, [])
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _FourthSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "Fourth"
    
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(0, [])
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _FifthSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "Fifth"
    
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _SixthSplasher(_Splasher):
    @staticmethod
    def suffix() -> str | None:
        return "Sixth"
    
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(1, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _Clears(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

    @staticmethod
    def name() -> _LocationName:
        return _LocationName.CLEAR

class _Platinums(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _Golds(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _Silvers(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _Bronzes(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls._data = [
            _InnerLocationData(i, [SplasherPowerItem.WATER]) for i in range(0, 5)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY]) for i in range(5, 14)
        ] + [
            _InnerLocationData(i, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY]) for i in range(14, 21)
        ] + [
            _InnerLocationData(21, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY, SplasherPowerItem.BOUNCY], True)
        ]

class _Powers(_LocationDataContainer):
    @classmethod
    def init(cls) -> None:
        cls.__data = [
            _InnerLocationData(0, []), _InnerLocationData(5, [SplasherPowerItem.WATER]), _InnerLocationData(13, [SplasherPowerItem.WATER, SplasherPowerItem.STICKY])
        ]