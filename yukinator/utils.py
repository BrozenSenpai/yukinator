import os
from collections.abc import MutableMapping
from typing import Union

import requests_cache

from .exceptions import WrongDirectory


class Cache:
    _session = None
    _path = ""

    @staticmethod
    def path_create(path: str) -> str:
        """Create a cache path.

        Args:
            path (str): Directory for a cache file.

        Returns:
            str: Concatenated path.

        Raises:
            WrongDirectory: The provider directory for a cache does not exist.
        """
        if not os.path.exists(path):
            raise WrongDirectory()
        return os.path.normpath(os.path.join(path, "yuki_cache"))

    @classmethod
    def cache_enable(
        cls,
        path: str,
        headers: dict,
        expires_after: Union[None, int, float, str],
        clear: bool,
    ):
        """Enable caching.

        Args:
            path (str): Directory for a cache file.
            headers (dict): Dictionary of headers to be sent on each request.
            expires_after (None, int, float, str): Time after cached items will expire.
            clear (bool): If True clear cache. Defaults to False.

        Raises:
            WrongDirectory: The provider directory for a cache does not exist.
        """

        cls._path = path
        cls._session = requests_cache.CachedSession(
            cache_name=Cache.path_create(path),
            backend="sqlite",
            allowable_methods=("GET"),
            expire_after=expires_after,
            stale_if_error=True,
            headers=headers,
        )
        if clear:
            cls._session.cache.clear()

    @classmethod
    def cache_get(cls, url):
        """Make a get request with caching

        Args:
            url (str): API endpoint URL.

        Returns:
            requests.models.Response: Response for the request.

        HTTPError: If the response's status code is not less than 400.
        """

        return cls._session.get(url)


def flat_dict(d: dict, keys: list = None) -> dict:
    """Flat nested dict"""

    def _flatten_dict_gen(d, parent_key):
        for k, v in d.items():
            new_key = parent_key.lower() + k.capitalize() if parent_key else k
            if keys:
                if isinstance(v, MutableMapping) and k in keys:
                    yield from flatten_dict(v, new_key).items()
                else:
                    yield new_key, v
            else:
                if isinstance(v, MutableMapping):
                    yield from flatten_dict(v, new_key).items()
                else:
                    yield new_key, v

    def flatten_dict(d: MutableMapping, parent_key: str = ""):
        return dict(_flatten_dict_gen(d, parent_key))

    return flatten_dict(d)
