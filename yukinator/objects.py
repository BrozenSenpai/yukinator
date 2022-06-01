import json
import datetime
from typing import Optional

from attrs import define, field, asdict, astuple, converters

from .utils import flat_dict


class JSONEncoder(json.JSONEncoder):
    """Custom json encoder to deal with dates, times and DTOs"""

    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, DTO):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)


# Helpers for types converting


def to_date(f: str) -> datetime.date:
    return datetime.datetime.strptime(f, "%Y-%m-%d").date()


def to_time(f: str) -> datetime.time:
    return (
        datetime.datetime.strptime(f[:-1], "%H:%M:%S")
        .time()
        .replace(tzinfo=datetime.timezone.utc)
    )


def to_driver_dto(d: dict):
    return DriverDTO(**d)


def to_constructor_dto(d: dict):
    return ConstructorDTO(**d)


def to_location_dto(d: dict):
    return LocationDTO(**d)


def to_circuit_dto(d: dict):
    return CircuitDTO(**d)


def to_race_dto(d: dict):
    return RaceDTO(**d)


def to_time_dto(d: dict):
    return TimeDTO(**d)


def to_fastestlap_dto(d: dict):
    return FastestLapDTO(**d)


def to_timings_dto_list(ll: list):
    return [TimingDTO(**x) for x in ll]


def to_constructors_dto_list(ll: list):
    return [ConstructorDTO(**x) for x in ll]


def to_averagespeed_dto(d: dict):
    return AverageSpeedDTO(**d)


# Data transfer objects


@define
class DTO:
    """Parent class for all DTOs"""

    def to_dict(self) -> dict:
        """Convert object to a dictionary"""
        return asdict(self)

    def to_flat_dict(self) -> dict:
        """Convert object to a flat dictionary"""
        d = asdict(self)
        return flat_dict(d)

    def to_tuple(self) -> tuple:
        """Convert object to a tuple"""
        return astuple(self)

    def to_json(self) -> str:
        """Convert object to a json string"""
        return JSONEncoder().encode(self)


@define
class DriverDTO(DTO):
    driverId: str
    url: str
    givenName: str
    familyName: str
    dateOfBirth: datetime.date = field(converter=to_date)
    nationality: str
    permanentNumber: Optional[int] = field(
        default=None, converter=converters.optional(int)
    )
    code: Optional[str] = None


@define
class ConstructorDTO(DTO):
    constructorId: str
    url: str
    name: str
    nationality: str


@define
class LocationDTO(DTO):
    lat: float = field(converter=float)
    long: float = field(converter=float)
    locality: str
    country: str


@define
class CircuitDTO(DTO):
    circuitId: str
    url: str
    circuitName: str
    Location: LocationDTO = field(converter=to_location_dto)


@define
class RaceDTO(DTO):
    season: int = field(converter=int)
    round: int = field(converter=int)
    url: str
    raceName: str
    Circuit: CircuitDTO = field(converter=to_circuit_dto)
    date: datetime.date = field(converter=to_date)
    time: Optional[datetime.time] = field(
        default=None, converter=converters.optional(to_time)
    )
    firstpracticeDate: Optional[datetime.date] = field(
        default=None, converter=converters.optional(to_date)
    )
    firstpracticeTime: Optional[datetime.time] = field(
        default=None, converter=converters.optional(to_time)
    )
    secondpracticeDate: Optional[datetime.date] = field(
        default=None, converter=converters.optional(to_date)
    )
    secondpracticeTime: Optional[datetime.time] = field(
        default=None, converter=converters.optional(to_time)
    )
    thirdpracticeDate: Optional[datetime.date] = field(
        default=None, converter=converters.optional(to_date)
    )
    thirdpracticeTime: Optional[datetime.time] = field(
        default=None, converter=converters.optional(to_time)
    )
    qualifyingDate: Optional[datetime.date] = field(
        default=None, converter=converters.optional(to_date)
    )
    qualifyingTime: Optional[datetime.time] = field(
        default=None, converter=converters.optional(to_time)
    )
    sprintDate: Optional[datetime.date] = field(
        default=None, converter=converters.optional(to_date)
    )
    sprintTime: Optional[datetime.time] = field(
        default=None, converter=converters.optional(to_time)
    )


@define
class TimeDTO(DTO):
    millis: Optional[int] = field(default=None, converter=converters.optional(int))
    time: Optional[str] = None


@define
class AverageSpeedDTO(DTO):
    units: Optional[str] = None
    speed: Optional[int] = field(default=None, converter=converters.optional(float))


@define
class FastestLapDTO(DTO):
    rank: Optional[int] = field(default=None, converter=converters.optional(int))
    lap: Optional[int] = field(default=None, converter=converters.optional(int))
    Time: Optional[TimeDTO] = field(
        default=None, converter=converters.optional(to_time_dto)
    )
    AverageSpeed: Optional[AverageSpeedDTO] = field(
        default=None, converter=converters.optional(to_averagespeed_dto)
    )


@define
class TimingDTO(DTO):
    driverId: str
    position: int = field(converter=int)
    time: str


@define
class RaceResultDTO(DTO):
    Driver: DriverDTO = field(converter=to_driver_dto)
    number: int = field(converter=int)
    Constructor: ConstructorDTO = field(converter=to_constructor_dto)
    position: int = field(converter=int)
    positionText: str
    points: float = field(converter=float)
    grid: int = field(converter=int)
    laps: int = field(converter=int)
    status: str
    Time: Optional[TimeDTO] = field(
        default=None, converter=converters.optional(to_time_dto)
    )
    FastestLap: Optional[FastestLapDTO] = field(
        default=None, converter=converters.optional(to_fastestlap_dto)
    )


@define
class QualifyingResultDTO(DTO):
    Driver: DriverDTO = field(converter=to_driver_dto)
    number: int = field(converter=int)
    position: int = field(converter=int)
    Constructor: ConstructorDTO = field(converter=to_constructor_dto)
    Q1: Optional[str] = None
    Q2: Optional[str] = None
    Q3: Optional[str] = None


@define
class SprintResultDTO(DTO):
    number: int = field(converter=int)
    Driver: DriverDTO = field(converter=to_driver_dto)
    Constructor: ConstructorDTO = field(converter=to_constructor_dto)
    position: int = field(converter=int)
    positionText: str
    points: float = field(converter=float)
    grid: int = field(converter=int)
    laps: int = field(converter=int)
    status: str
    Time: Optional[TimeDTO] = field(
        default=None, converter=converters.optional(to_time_dto)
    )
    FastestLap: Optional[FastestLapDTO] = field(
        default=None, converter=converters.optional(to_fastestlap_dto)
    )


@define
class DriverStandingDTO(DTO):
    Driver: DriverDTO = field(converter=to_driver_dto)
    position: int = field(converter=int)
    positionText: str
    points: float = field(converter=float)
    wins: int = field(converter=float)
    Constructors: ConstructorDTO = field(converter=to_constructors_dto_list)


@define
class ConstructorStandingDTO(DTO):
    Constructor: ConstructorDTO = field(converter=to_constructor_dto)
    position: int = field(converter=int)
    positionText: str
    points: float = field(converter=float)
    wins: int = field(converter=int)


@define
class StatusDTO(DTO):
    statusId: int = field(converter=int)
    status: str
    count: int = field(converter=int)


@define
class LapDTO(DTO):
    number: int = field(converter=int)
    Timings: list[TimingDTO] = field(converter=to_timings_dto_list)


@define
class PitStopDTO(DTO):
    driverId: str
    lap: int = field(converter=int)
    stop: int = field(converter=int)
    time: str
    duration: float = field(converter=float)


@define
class SeasonDTO(DTO):
    season: int = field(converter=int)
    url: str
