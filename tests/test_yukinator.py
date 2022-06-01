import json
from http import HTTPStatus

import pytest

from yukinator.yukinator import Yuki
from yukinator.exceptions import WrongQueryParameters

build_urls_data = [
    (
        [2022, 4, "qualifying"],
        "https://ergast.com/api/f1/2022/4/qualifying.json?limit=1000",
    ),
    ([2001, None, "drivers"], "https://ergast.com/api/f1/2001/drivers.json?limit=1000"),
]


@pytest.mark.parametrize("args, result", build_urls_data)
def test_build_url(args, result):
    assert Yuki._build_url(*args) == result


@pytest.fixture
def fake_response():
    with open("tests/resources/drivers.json") as f:
        return json.load(f)


def test_make_request_witout_caching(mocker, fake_response):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=fake_response)
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("yukinator.yukinator.requests.get", return_value=fake_resp)

    resp = Yuki(cache_enabled=False)._make_request(
        "https://ergast.com/api/f1/2022/4/drivers.json?limit=1000"
    )
    assert resp == fake_response


@pytest.fixture
def fake_wrong_response():
    with open("tests/resources/wrong_request.json") as f:
        return json.load(f)


def test_make_request_with_wrong_query(mocker, fake_wrong_response):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=fake_wrong_response)
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("yukinator.yukinator.requests.get", return_value=fake_resp)

    with pytest.raises(WrongQueryParameters):
        Yuki(cache_enabled=False)._make_request(
            "https://ergast.com/api/f1/1949/drivers.json?limit=1000"
        )


@pytest.fixture
def races_response():
    with open("tests/resources/races.json") as f:
        return json.load(f)


def test_get_races(mocker, races_response):
    fake_resp = mocker.Mock()
    fake_resp.json = mocker.Mock(return_value=races_response)
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("yukinator.yukinator.requests.get", return_vakue=fake_resp)

    resp = Yuki(cache_enabled=False).get_races(2022, 4)
    assert type(resp) == list
