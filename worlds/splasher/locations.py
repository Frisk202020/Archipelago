from __future__ import annotations

from enum import IntEnum, StrEnum
from typing import TYPE_CHECKING, ClassVar

from BaseClasses import Location
from worlds.splasher.options import IncludeMedals, SplasherOptions
from worlds.splasher.regions import SplasherLevelName
from worlds.splasher.utils import SplasherUtils

if TYPE_CHECKING:
    from .world import SplasherWorld

class SplasherLocation(Location):
    game = SplasherUtils.splasher

    @staticmethod
    def name_to_id():
        return _LocationData.name_to_id()
    
    @staticmethod
    def create_locations(world: SplasherWorld):        
        for data in _LocationData.data():
            if data.include(world.options):
                SplasherLocation(world, data)

    def __init__(self, world: SplasherWorld, data: _LocationData):
        region = world.get_region(data.region)
        Location.__init__(self, world.player, data.name, data.id, region)
        region.locations.append(self)
        

class _LocationData:
    __data: ClassVar[list[_LocationData]|None] =  None
    __name_to_id: ClassVar[dict[str, int]|None] = None
    __next_id: ClassVar[int] = SplasherUtils.base_id

    @classmethod
    def __init(cls):
        cls.__data = [
            _LocationData(_LocationType.POWER, SplasherPowerLocation.WATER.fullname(), 0),
            _LocationData(_LocationType.POWER, SplasherPowerLocation.STICKINK.fullname(), 5),
            _LocationData(_LocationType.POWER, SplasherPowerLocation.BOUNCINK.fullname(), 13)
        ]
        
        for i in range(22):
            cls.__data += [_LocationData(_LocationType.SPLASHER, SplashersLocation.fullname(i, j), i) for j in range(6)]
            cls.__data.append(_LocationData(_LocationType.SPLASHER_GOLD, SplashersLocation.fullname(i, None), i))

        for name in SplasherLocationOnEachLevel:
            cls.__data += [_LocationData(name.type(), name.fullname(i), i) for i in range(22)]
    
    @classmethod
    def data(cls) -> list[_LocationData]:
        if (cls.__data is None):
            cls.__init()
                
        return cls.__data # type: ignore
    
    @classmethod
    def name_to_id(cls) -> dict[str, int]:
        if (cls.__name_to_id is None):
            cls.__init()

        return cls.__name_to_id # type: ignore
    
    __type: _LocationType
    id: int
    name: str
    region: str
    def __init__(self, type: _LocationType, name: str, level_id: int):
        self.name = name
        self.__type = type
        self.id = _LocationData.__next_id
        self.region = SplasherLevelName.level(level_id)

        _LocationData.__next_id += 1

        if _LocationData.__name_to_id is None:
            _LocationData.__name_to_id = {}       
        _LocationData.__name_to_id[name] = self.id

    def include(self, options: SplasherOptions) -> bool:
        match(self.__type):
            case _LocationType.BRONZE: return options.include_medals > IncludeMedals.option_off
            case _LocationType.SILVER: return options.include_medals > IncludeMedals.option_bronze
            case _LocationType.GOLD: return options.include_medals > IncludeMedals.option_silver
            case _:  return True

class _LocationType(IntEnum):
    CLEAR = 0
    SPLASHER = 1
    SPLASHER_GOLD = 2
    BRONZE = 3
    SILVER = 4
    GOLD = 5
    POWER = 6

class SplasherPowerLocation(StrEnum):
    WATER = "Water"
    STICKINK = "Stickink"
    BOUNCINK = "Bouncink"

    def fullname(self) -> str:
        return f"{self.value} Unlock"

class SplasherLocationOnEachLevel(StrEnum):
    CLEAR = "Clear"
    BRONZE = "Bronze Medal"
    SILVER = "Silver Medal"
    GOLD = "Gold Medal"

    def type(self) -> _LocationType:
        match(self):
            case SplasherLocationOnEachLevel.CLEAR: return _LocationType.CLEAR
            case SplasherLocationOnEachLevel.BRONZE: return _LocationType.BRONZE
            case SplasherLocationOnEachLevel.SILVER: return _LocationType.SILVER
            case SplasherLocationOnEachLevel.GOLD: return _LocationType.GOLD

    def fullname(self, level_id: int):
        return f"{SplasherLevelName.level(level_id)} : {self.value}"
    
class SplashersLocation:
    @staticmethod
    def fullname(level_id: int, splasher_id: int|None):
        return f"{SplasherLevelName.level(level_id)} : Splasher ({"Gold" if splasher_id is None else splasher_id+1})"