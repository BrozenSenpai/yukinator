import datetime

import pytest

from yukinator.objects import to_date, to_time, RaceDTO
from .resources.examples import (
    example_race_1,
    example_racedto_dict,
    example_racedto_tuple,
    example_racedto_flatdict,
    example_racedto_json,
)


def test_to_date():
    date_string = "2022-04-02"
    date_obj = datetime.date(2022, 4, 2)
    assert to_date(date_string) == date_obj


def test_to_time():
    time_string = "21:42:15Z"
    time_obj = datetime.time(
        hour=21, minute=42, second=15, tzinfo=datetime.timezone.utc
    )
    assert to_time(time_string) == time_obj


@pytest.fixture
def race_dto():
    return RaceDTO(**example_race_1)


def test_to_dict(race_dto):
    assert race_dto.to_dict() == example_racedto_dict


def test_to_tuple(race_dto):
    assert race_dto.to_tuple() == example_racedto_tuple


def test_to_flatdict(race_dto):
    assert race_dto.to_flat_dict() == example_racedto_flatdict


def test_to_json(race_dto):
    assert race_dto.to_json() == example_racedto_json
