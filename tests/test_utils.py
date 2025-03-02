import requests

import pytest
import requests_cache

from yukinator.utils import Cache, flat_dict
from yukinator.exceptions import WrongDirectory


def test_path_create():
    import os
    # Normalize the expected path so it matches OS-specific path separators
    expected_output = os.path.normpath("tests/resources/yuki_cache")
    assert Cache.path_create("tests/resources") == expected_output
    assert Cache.path_create("tests/resources/") == expected_output


def test_path_create_wrong_dir():
    with pytest.raises(WrongDirectory):
        Cache.path_create("tests/wrongdir")


def test_cache_get():
    Cache.cache_enable(
        "tests/resources", {"User-Agent": "Yukinator testing"}, 3600, True
    )

    assert (
        type(
            Cache.cache_get("https://api.jolpi.ca/ergast/f1/1995/4/drivers.json?limit=1000")
        )
        == requests.models.Response
    )
    assert (
        type(
            Cache.cache_get("https://api.jolpi.ca/ergast/f1/1995/4/drivers.json?limit=1000")
        )
        == requests_cache.models.response.CachedResponse
    )


flat_dict_data = [
    (
        [
            {
                "key_1": "value_1",
                "key_2": {
                    "nested_key_1": "nested_value_1",
                    "nested_key_2": "nested_value_2",
                },
                "key_3": {"nested_key_3": "nested_value_3"},
            },
            ["key_2"],
        ],
        {
            "key_1": "value_1",
            "key_2Nested_key_1": "nested_value_1",
            "key_2Nested_key_2": "nested_value_2",
            "key_3": {"nested_key_3": "nested_value_3"},
        },
    ),
    (
        [
            {
                "key_1": "value_1",
                "key_2": {
                    "nested_key_1": "nested_value_1",
                    "nested_key_2": "nested_value_2",
                },
                "key_3": {"nested_key_3": "nested_value_3"},
            },
        ],
        {
            "key_1": "value_1",
            "key_2Nested_key_1": "nested_value_1",
            "key_2Nested_key_2": "nested_value_2",
            "key_3Nested_key_3": "nested_value_3",
        },
    ),
]


@pytest.mark.parametrize("args, result", flat_dict_data)
def test_flat_dict(args, result):
    assert flat_dict(*args) == result
