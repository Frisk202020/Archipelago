from __future__ import annotations
from enum import IntEnum, StrEnum
from typing import TYPE_CHECKING, ClassVar

from BaseClasses import Location

from .options import IncludeMedals, SplasherOptions
from .utils import SplasherUtils

if TYPE_CHECKING:
    from .world import SplasherWorld

class SplasherLocation(Location):
    game = SplasherUtils.splasher
    count: ClassVar[int] = 0

    @staticmethod
    def name_to_id() -> dict[str, int]:
        return _LocationData.name_to_id()
    
    @staticmethod
    def create_locations(world: SplasherWorld) -> None:      
        for data in _LocationData.data():
            if data.include(world.options):
                SplasherLocation(world, data)
                SplasherLocation.count += 1

    def __init__(self, world: SplasherWorld, data: _LocationData) -> None:
        region = world.get_region(data.region)
        Location.__init__(self, world.player, data.name, data.id, region)
        region.locations.append(self)
        
class _LocationType(IntEnum):
    CLEAR = 0
    SPLASHER = 1
    SPLASHER_GOLD = 2
    BRONZE = 3
    SILVER = 4
    GOLD = 5
    PLATINUM = 6
    POWER = 7

class _LocationData:
    __type: _LocationType
    id: int
    name: str
    region: str
    def __init__(self, type: _LocationType, name: str, level_id: int, speedrun: bool=False) -> None:
        self.name = name
        self.__type = type
        self.id = _LocationData.__next_id
        self.region = SplasherUtils.level(level_id, speedrun)

        _LocationData.__next_id += 1
        _LocationData.__name_to_id[name] = self.id

    def include(self, options: SplasherOptions) -> bool:
        match(self.__type):
            case _LocationType.BRONZE: return options.include_medals > IncludeMedals.option_off
            case _LocationType.SILVER: return options.include_medals > IncludeMedals.option_bronze
            case _LocationType.GOLD: return options.include_medals > IncludeMedals.option_silver
            case _LocationType.PLATINUM: return options.include_medals == IncludeMedals.option_platinum
            case _:  return True

    __data: ClassVar[list[_LocationData]] =  []
    __name_to_id: ClassVar[dict[str, int]] = {}
    __next_id: ClassVar[int] = SplasherUtils.base_id

    @classmethod
    def __init_data(cls) -> None:
        cls.__data = [
            _LocationData(_LocationType.POWER, SplasherPowerLocation.WATER.fullname(), 0),
            _LocationData(_LocationType.POWER, SplasherPowerLocation.STICKINK.fullname(), 5),
            _LocationData(_LocationType.POWER, SplasherPowerLocation.BOUNCINK.fullname(), 13)
        ]
        
        for i in range(22):
            cls.__data += [_LocationData(_LocationType.SPLASHER, SplashersLocation.fullname(i, j), i) for j in range(6)]
            cls.__data.append(_LocationData(_LocationType.SPLASHER_GOLD, SplashersLocation.fullname(i, None), i))

        cls.__data += [_LocationData(
            SplasherLocationOnEachLevel.CLEAR.type(), 
            SplasherLocationOnEachLevel.CLEAR.fullname(i), 
            i
        ) for i in range(22)]

        for name in [
            SplasherLocationOnEachLevel.BRONZE, 
            SplasherLocationOnEachLevel.SILVER, 
            SplasherLocationOnEachLevel.GOLD, 
            SplasherLocationOnEachLevel.PLATINUM
        ]:
            cls.__data += [_LocationData(name.type(), name.fullname(i), i, True) for i in range(22)]
            
    
    @classmethod
    def data(cls) -> list[_LocationData]:
        if (len(cls.__data) == 0):
            cls.__init_data()
                
        return cls.__data
    
    @classmethod
    def name_to_id(cls) -> dict[str, int]:
        if (len(cls.__name_to_id) == 0):
            cls.__init_data()

        return cls.__name_to_id

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
    PLATINUM = "Platinum Medal"

    def type(self) -> _LocationType:
        match(self):
            case SplasherLocationOnEachLevel.CLEAR: return _LocationType.CLEAR
            case SplasherLocationOnEachLevel.BRONZE: return _LocationType.BRONZE
            case SplasherLocationOnEachLevel.SILVER: return _LocationType.SILVER
            case SplasherLocationOnEachLevel.GOLD: return _LocationType.GOLD
            case SplasherLocationOnEachLevel.PLATINUM: return _LocationType.PLATINUM

    def fullname(self, level_id: int):
        return f"{SplasherUtils.level(level_id, False)} : {self.value}"
    
class SplashersLocation:
    @classmethod
    def fullname(cls, level_id: int, splasher_id: int|None):
        return f"{SplasherUtils.level(level_id, False)} : Splasher ({"Gold" if splasher_id is None else splasher_id+1})"