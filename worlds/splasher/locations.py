from __future__ import annotations
from enum import IntEnum, StrEnum
from typing import TYPE_CHECKING, Callable, ClassVar, Optional

from BaseClasses import Location
from rule_builder.rules import Rule

from worlds.splasher.items import SplasherCheckpoint
from worlds.splasher.regions import splasher_area_name, splasher_ckp_region_name
from worlds.splasher.rules import SplasherArea, SplasherPowerRules

from .options import CheckpointSanity, IncludeMedals, SplasherOptions
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
        for data in _BaseLocationData.data():
            if data.include(world.options):
                SplasherLocation(world, data)
                SplasherLocation.count += 1

    def __init__(self, world: SplasherWorld, data: _BaseLocationData) -> None:
        region = world.get_region(data.region(world.options))
        Location.__init__(self, world.player, data.name, data.id, region)

        if data.rule is not None:
            r = data.rule(world.options)
            if r is not None:
                world.set_rule(self, r)

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
    CHECKPOINT = 8

class _BaseLocationData:
    __type: _LocationType
    id: int
    name: str
    region: Callable[[SplasherOptions], str]
    rule: Optional[Callable[[SplasherOptions], Optional[Rule]]]

    def __init__(self, type: _LocationType, name: str, region: Callable[[SplasherOptions], str], rule: Optional[Callable[[SplasherOptions], Optional[Rule]]]) -> None:
        self.name = name
        self.__type = type
        self.region = region
        self.rule = rule
        
        id = _BaseLocationData.__name_to_id.get(name)
        if id is None:
            self.id = _BaseLocationData.__next_id
            _BaseLocationData.__next_id += 1
            _BaseLocationData.__name_to_id[name] = self.id
        else:
            self.id = id

    def include(self, options: SplasherOptions) -> bool:
        match(self.__type):
            case _LocationType.BRONZE: return options.include_medals > IncludeMedals.option_off
            case _LocationType.SILVER: return options.include_medals > IncludeMedals.option_bronze
            case _LocationType.GOLD: return options.include_medals > IncludeMedals.option_silver
            case _LocationType.PLATINUM: return options.include_medals == IncludeMedals.option_platinum
            case _LocationType.CHECKPOINT: return options.checkpoint_sanity > CheckpointSanity.option_off
            case _:  return True

    __data: ClassVar[list[_BaseLocationData]] =  []
    __name_to_id: ClassVar[dict[str, int]] = {}
    __next_id: ClassVar[int] = SplasherUtils.base_id

    @classmethod
    def __init_data(cls) -> None:
        cls.__data = [_PowerCheckpoint(x) for x in SplasherPowerLocation]
        cls.__data += [
            _Splasher(0, 0, 0),
            _Splasher(0, 1, 1),
            _Splasher(0, 2, 2),
            *_Vortex.many(0, 0, 3, 4),
            *_Splasher.many(0, None, 5, None),

            _Vortex(1, None, 0, SplasherPowerRules.polluted_water | SplasherPowerRules.bouncy),
            _Splasher(1, 1, 1),
            _Splasher(1, 3, 2),
            _Splasher(1, 4, 3, SplasherPowerRules.unstick_rule),
            _Splasher(1, 4, 4),
            *_Splasher.many(1, None, 5, None),

            _Vortex(2, None, 0, SplasherPowerRules.polluted_water | SplasherPowerRules.bouncy),
            _Splasher(2, 1, 1),
            _Splasher(2, 2, 2),
            _Vortex(2, 0, 3),
            _Splasher(2, 4, 4),
            *_Splasher.many(2, None, 5, None),

            _Splasher(3, 0, 0, SplasherPowerRules.polluted_water),
            _Splasher(3, 1, 1),
            _Vortex(3, 1, 2),
            _Splasher(3, 3, 3),
            _Vortex(3, 1, 4),
            *_Splasher.many(3, None, 5, None),

            _Splasher(4, 0, 0),
            _Vortex(4, 1, 1),
            _Splasher(4, 2, 2),
            _Vortex(4, 1, 3),
            _Splasher(4, 4, 4),
            *_Splasher.many(4, None, 5, None),

            _Vortex(5, None, 0, SplasherPowerRules.polluted_water | SplasherPowerRules.bouncy),
            *_Splasher.many(5, None, 1, 2, 3, 4, 5, None),

            _Splasher(6, 0, 0),
            _Vortex(6, 1, 1),
            _Splasher(6, 2, 2),
            _Vortex(6, 1, 3),
            _Splasher(6, 4, 4),
            *_Splasher.many(6, None, 5, None),

            _Splasher(7, 0, 0),
            _Splasher(7, 1, 1, SplasherPowerRules.unstick_rule),
            *_Vortex.many(7, 0, 2, 3),
            _Splasher(7, 4, 4),
            *_Splasher.many(7, None, 5, None),

            _Vortex(8, 0, 0),
            _Splasher(8, 1, 1),
            _Splasher(8, 2, 2, SplasherPowerRules.polluted_water & SplasherPowerRules.non_water),
            _Vortex(8, 0, 3),
            _Splasher(8, 4, 4),
            *_Splasher.many(8, None, 5, None),

            _Splasher(9, 0, 0),
            _Splasher(9, 1, 1),
            _Vortex(9, 0, 2),
            _Splasher(9, 3, 3),
            _Vortex(9, 0, 4),
            *_Splasher.many(9, None, 5, None),

            _Splasher(10, 0, 0, SplasherPowerRules.unstick_rule),
            _Vortex(10, 1, 1),
            _Splasher(10, 2, 2, SplasherPowerRules.unstick_rule),
            _Splasher(10, 3, 3),
            _Vortex(10, 1, 4),
            *_Splasher.many_with_rule(10, None, SplasherPowerRules.unstick_rule, 5, None),

            _Splasher(11, 0, 0),
            _Vortex(11, 0, 1),
            _Splasher(11, 2, 2, SplasherPowerRules.unstick_rule),
            _Splasher(11, 3, 3),
            _Splasher(11, 4, 4),
            _Vortex(11, 0, 5),
            _Splasher(11, None, None),

            _Splasher(12, 0, 0),
            _Splasher(12, 1, 1),
            _Vortex(12, 0, 2),
            _Vortex(12, 0, 3, SplasherPowerRules.polluted_water & SplasherPowerRules.sticky),
            _Splasher(12, 4, 4),
            *_Splasher.many(12, None, 5, None),

            _Vortex(13, 1, 0),
            *_Splasher.many(13, None, 1, 2, 3, 4, 5, None),

            _Splasher(14, 0, 0),
            _Splasher(14, 1, 1),
            _Splasher(14, 2, 2),
            _Vortex(14, 1, 3),
            _Splasher(14, 4, 4),
            _Vortex(14, 1, 5),
            _Splasher(14, None, None),

            _Splasher(15, 0, 0),
            _Vortex(15, 0, 1),
            _Splasher(15, 2, 2),
            _Vortex(15, 1, 3),
            _Splasher(15, 4, 4),
            *_Splasher.many(15, None, 5, None),

            _Splasher(16, 0, 0),
            _Vortex(16, 0, 1),
            _Splasher(16, 2, 2),
            _Splasher(16, 3, 3),
            _Vortex(16, 0, 4),
            *_Splasher.many(16, None, 5, None),

            _Splasher(17, 0, 0),
            _Vortex(17, 0, 1),
            _Splasher(17, 2, 2),
            _Vortex(17, 0, 3),
            _Splasher(17, 4, 4),
            *_Splasher.many(17, None, 5, None),

            _Splasher(18, 0, 0),
            _Splasher(18, 1, 1),
            _Vortex(18, 0, 2),
            _Splasher(18, 3, 3),
            _Vortex(18, 0, 4),
            *_Splasher.many(18, None, 5, None),

            _Vortex(19, None, 0, SplasherPowerRules.bouncy),
            _Splasher(19, 1, 1),
            _Splasher(19, 2, 2),
            _Splasher(19, 3, 3),
            _Vortex(19, 0, 4),
            *_Splasher.many(19, None, 5, None),

            _Splasher(20, 0, 0),
            _Vortex(20, 0, 1),
            _Splasher(20, 2, 2),
            _Splasher(20, 3, 3),
            _Vortex(20, 0, 4),
            *_Splasher.many(20, None, 5, None),

            _Splasher(21, 1, 0),
            _Splasher(21, 2, 1),
            _Splasher(21, 3, 2),
            _Splasher(21, 4, 3),
            *_Splasher.many(21, 6, 4, 5),
            _Splasher(21, None, None)
        ]

        for name in [
            SplasherLocationOnEachLevel.BRONZE, 
            SplasherLocationOnEachLevel.SILVER, 
            SplasherLocationOnEachLevel.GOLD, 
            SplasherLocationOnEachLevel.PLATINUM
        ]:
            cls.__data += [_LocationData(name.type(), name.fullname(i), i, True) for i in range(22)]

        # external loop for easier client implementation (see Archipelago.Data.Locations.LocationType.cs)
        for i in range(SplasherUtils.level_count):
            cls.__data.append(_Checkpoint(i, None))     

        for i in range(SplasherUtils.level_count):
            for j in range(SplasherCheckpoint.id_range(i)):
                cls.__data.append(_Checkpoint(i, j)) 
    
    @classmethod
    def data(cls) -> list[_BaseLocationData]:
        if (len(cls.__data) == 0):
            cls.__init_data()
                
        return cls.__data
    
    @classmethod
    def name_to_id(cls) -> dict[str, int]:
        if (len(cls.__name_to_id) == 0):
            cls.__init_data()

        return cls.__name_to_id

class _LocationData(_BaseLocationData):
    def __init__(self, type: _LocationType, name: str, level: int, speedrun: bool = False):
        region = SplasherUtils.level(level, speedrun)
        super().__init__(type, name, lambda opt: region, None)

class _Checkpoint(_BaseLocationData):
    def __init__(self, lvl: int, id: int|None):
        (area_id, _) = SplasherArea.get_area(lvl, id)
        super().__init__(
            _LocationType.CLEAR if id is None else _LocationType.CHECKPOINT,
            SplasherLocationOnEachLevel.CLEAR.fullname(lvl) if id is None else SplasherCheckpoint.name(lvl, id),
            lambda opt: splasher_area_name(SplasherUtils.level(lvl, False), area_id),
            None
        )

class _PowerCheckpoint(_BaseLocationData):
    @staticmethod
    def __region(power: SplasherPowerLocation) -> tuple[int, int|None]:
        match(power):
            case SplasherPowerLocation.WATER: return (0, None)
            case SplasherPowerLocation.STICKINK: return (5, 0)
            case SplasherPowerLocation.BOUNCINK: return (13, 1)

    def __init__(self, power: SplasherPowerLocation):
        (lvl, area) = _PowerCheckpoint.__region(power)
        super().__init__(
            _LocationType.POWER, power.fullname(), 
            lambda opt: splasher_area_name(SplasherUtils.level(lvl, False), area), None
        )

class _Splasher(_BaseLocationData):
    @staticmethod
    def __get_region(level: int, checkpoint: int|None) -> Callable[[SplasherOptions], str]:
        level_name = SplasherUtils.level(level, False)
        (area_id, is_exit_area) = SplasherArea.get_area(level, checkpoint)
        area_region = splasher_area_name(level_name, area_id)

        if is_exit_area or checkpoint is None:
            return lambda opt: area_region

        ckp_region = splasher_ckp_region_name(level_name, checkpoint)
        return lambda opt: ckp_region if opt.checkpoint_sanity == CheckpointSanity.option_progression else area_region
    
    def __init__(self, level: int, checkpoint: int|None, id: int|None, rule: Optional[SplasherPowerRules]=None) -> None:
        type = _LocationType.SPLASHER_GOLD if id is None else _LocationType.SPLASHER
        super().__init__(
            type, SplashersLocation.fullname(level, id),  
            _Splasher.__get_region(level, checkpoint),
            None if rule is None else lambda opt: rule.get(opt.randomize_powers, opt.progressive_water == 1)
        )

    @classmethod
    def many(cls, level: int, checkpoint: int|None, *ids: int|None):
        return [_Splasher(level, checkpoint, id, None) for id in ids]

    @classmethod
    def many_with_rule(cls, level: int, checkpoint: int|None, rule: SplasherPowerRules, *ids: int|None):
        return [_Splasher(level, checkpoint, id, rule) for id in ids]

class _Vortex(_BaseLocationData):
    def __init__(self, level: int, area: int|None, id: int, rule: Optional[SplasherPowerRules]=None) -> None:
        super().__init__(
            _LocationType.SPLASHER, 
            SplashersLocation.fullname(level, id), 
            lambda opt: splasher_area_name(SplasherUtils.level(level, False), area),
            None if rule is None else lambda opt: rule.get(opt.randomize_powers, opt.progressive_water == 1)
        )

    @classmethod
    def many(cls, level: int, area: int, *ids: int):
        return [_Vortex(level, area, id, None) for id in ids]

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