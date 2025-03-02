from typing import Union

import requests
import os

from .exceptions import WrongQueryParameters
from .utils import Cache, flat_dict
from .objects import (
    DriverDTO,
    ConstructorDTO,
    CircuitDTO,
    RaceDTO,
    RaceResultDTO,
    QualifyingResultDTO,
    SprintResultDTO,
    DriverStandingDTO,
    ConstructorStandingDTO,
    StatusDTO,
    LapDTO,
    PitStopDTO,
    SeasonDTO,
)


class Yuki:
    """API wrapper for the Ergast F1 API.

    |  The data for every endpoint is provided in the handy data transfer object.
    |  DTOs have methods for converting them into simpler structures.

    Methods:
        to_dict: convert an object to a dictionary
        to_flat_dict: convert object to a flat dictionary
        to_tuple: convert an object to a tuple
        to_json: convert an object to a JSON string

    |  Disabling the caching is strongly not recommended.
    |  Ergast API has a limit of four calls per second and 200 per hour.
    |  Please take care while calling the methods within a loop.
    """

    _base_url = "https://api.jolpi.ca/ergast/f1/"

    def __init__(
        self,
        headers: dict = {"User-Agent": "Yukinator"},
        cache_enabled: bool = True,
        cache_dir: str = os.getcwd(),
        expires_after: Union[None, int, float, str] = 3600,
        force_clear: bool = False,
    ):
        """Initialize the Yuki class object.

        If caching is disabled, all of the cache related attributes are None.

        Args:
            headers (dict): Dictionary of headers to be sent on each request.
                Defaults to {'User-Agent': 'Yukinator'}
            cache_enabled (bool): Enable caching. Defaults to True.
            cache_dir (str): Directory for the cache sqlite file.
                Defaults to a current working directory.
            expires_after (None, int, float, str): Time after cached items will expire.
                Defaults to 3600 - one hour.
            force_clear (bool): Clear the whole cache before the first request.
                Defaults to False.
        """

        self.headers = headers
        self.cache_enabled = cache_enabled
        self.cache_dir = cache_dir if cache_enabled else None
        self.expires_after = expires_after if cache_enabled else None
        self.force_clear = force_clear if cache_enabled else None

        if self.cache_enabled:
            Cache.cache_enable(
                path=self.cache_dir,
                headers=self.headers,
                expires_after=self.expires_after,
                clear=self.force_clear,
            )

    def __repr__(self):
        return (
            f"Yuki({self.headers},{self.cache_enabled},'{self.cache_dir}',"
            f"{self.expires_after},{self.force_clear})"
        )

    @classmethod
    def _build_url(cls, *endpoints) -> str:
        """Build a full URL for provided API endpoint with a limit set to 1000.

        Args:
            *endpoints: API endpoint suffixes.

        Returns:
            str: URL ready for an API call.
        """

        return (
            cls._base_url
            + "/".join(str(suffix) for suffix in endpoints if suffix)
            + ".json?limit=1000"
        )

    def _make_request(self, url: str) -> dict:
        """Make a successful GET request for a specified URL.

        If a caching is enabled, get the result from the cache if possible,
        else call the API and cache it.
        If a cache is disabled, call the API.

        Args:
            url (str): API endpoint URL.

        Returns:
            dict: Content of response.

        Raises:
            HTTPError: If the response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        if self.cache_enabled:
            response = Cache.cache_get(url)
            if not response.ok:
                response.raise_for_status()
            result = response.json()
        else:
            response = requests.get(url, headers=self.headers)
            if not response.ok:
                response.raise_for_status()
            result = response.json()

        if int(result["MRData"]["total"]) <= 0:
            raise WrongQueryParameters()

        return result

    def get_drivers(
        self, year: Union[int, str, None] = None, race: Union[int, str, None] = None
    ) -> list[DriverDTO]:
        """Obtain a list of data transfer objects with information about the drivers.

        |  By default, return every driver in the F1 history.
        |  If only the year is provided, return a list for that season.
        |  If year and race are provided, return a list for that race and year.
        |  If only the race is provided, raise the WrongQueryParameters error.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str, None): Optional parameter with a year to be queried.
                Defaults to None.
            race (int, str, None): Optional parameter with a number of a race
                to be queried. Defaults to None.

        Returns:
            list[DriverDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        url = Yuki._build_url(year, race, "drivers")
        response = self._make_request(url)

        response = response["MRData"]["DriverTable"]["Drivers"]
        return [DriverDTO(**x) for x in response]

    def get_constructors(
        self, year: Union[int, str, None] = None, race: Union[int, str, None] = None
    ) -> list[ConstructorDTO]:
        """Obtain a list of data transfer objects with information about the constructors.

        |  By default, return every constructor in the F1 history.
        |  If only the year is provided, return a list for that season.
        |  If year and race are provided, return a list for that race and year.
        |  If only the race is provided, raise the WrongQueryParameters error.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str, None): Optional parameter with a year to be queried.
                Defaults to None.
            race (int, str, None): Optional parameter with a number of a race
                to be queried. Defaults to None.

        Returns:
            list[ConstructorDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        url = Yuki._build_url(year, race, "constructors")
        response = self._make_request(url)

        response = response["MRData"]["ConstructorTable"]["Constructors"]
        return [ConstructorDTO(**x) for x in response]

    def get_circuits(
        self, year: Union[int, str, None] = None, race: Union[int, str, None] = None
    ) -> list[CircuitDTO]:
        """Obtain a list of data transfer objects with information about the circuits.

        |  By default, return every circuit in the F1 history.
        |  If only the year is provided, return a list for that season.
        |  If year and race are provided, return a list for that race and year.
        |  If only the race is provided, raise the WrongQueryParameters error.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str, None): Optional parameter with a year to be queried.
                Defaults to None.
            race (int, str, None): Optional parameter with a number of a race
            to be queried. Defaults to None.

        Returns:
            list[CircuitDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        url = Yuki._build_url(year, race, "circuits")
        response = self._make_request(url)

        response = response["MRData"]["CircuitTable"]["Circuits"]

        return [CircuitDTO(**x) for x in response]

    def get_seasons(self) -> list[SeasonDTO]:
        """Obtain a list of data transfer objects with all F1 seasons

        Returns:
            list[SeasonDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
        """

        url = Yuki._build_url("seasons")
        response = self._make_request(url)

        response = response["MRData"]["SeasonTable"]["Seasons"]
        return [SeasonDTO(**x) for x in response]

    def get_races(
        self, year: Union[int, str] = "current", race: Union[int, str, None] = None
    ) -> list[RaceDTO]:
        """Obtain a list of data transfer objects with information about the races.

        |  By default, return the races for a current season.
        |  If only the year is provided, return a list for that season.
        |  If year and race are provided, return a list for that race and year.
        |  If only the race is provided, return a race from a current season.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str): Optional parameter with a year to be queried.
                Defaults to 'current'
            race (int, str, None): Optional parameter with a number of a race
                to be queried. Defaults to None.

        Returns:
            list[RaceDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        url = Yuki._build_url(year, race)
        response = self._make_request(url)
        response = response["MRData"]["RaceTable"]["Races"]

        return [
            RaceDTO(
                **flat_dict(
                    x,
                    [
                        "FirstPractice",
                        "SecondPractice",
                        "ThirdPractice",
                        "Qualifying",
                        "Sprint",
                    ],
                )
            )
            for x in response
        ]

    def get_race_results(
        self, year: Union[int, str] = "current", race: Union[int, str] = "last"
    ) -> list[RaceResultDTO]:
        """Obtain a list of data transfer objects with the race results.

        |  By default, return the results for the last race.
        |  If only year parameter is provided, return the results for the last race of that year.
        |  If year and race are provided, return the results for that race from that season.
        |  If only the race is provided, return the results for that race from current season.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str): Optional parameter with a year to be queried.
                Defaults to 'current'.
            race (int, str): Optional parameter with a number of a race to be queried.
                Defaults to 'last'.

        Returns:
            list[RaceResultDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        url = Yuki._build_url(year, race, "results")
        response = self._make_request(url)

        response = response["MRData"]["RaceTable"]["Races"][0]["Results"]
        return [RaceResultDTO(**x) for x in response]

    def get_qualifying_results(
        self, year: Union[int, str] = "current", race: Union[int, str] = "last"
    ) -> list[QualifyingResultDTO]:
        """Obtain a list of data transfer objects with the qualifying results.

        |  By default, return the results for the last GP.
        |  If only year parameter is provided, return the results for the last GP of that year.
        |  If year and race are provided, return the results for that GP from that season.
        |  If only the race is provided, return the results for that GP from current season.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str): Optional parameter with a year to be queried.
                Defaults to 'current'.
            race (int, str): Optional parameter with a number of a race to be queried.
                Defaults to 'last'.

        Returns:
            list[QualyfingResultDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        url = Yuki._build_url(year, race, "qualifying")
        response = self._make_request(url)

        response = response["MRData"]["RaceTable"]["Races"][0]["QualifyingResults"]
        return [QualifyingResultDTO(**x) for x in response]

    def get_sprint_results(
        self, year: Union[int, str] = "current", race: Union[int, str, None] = None
    ) -> list[SprintResultDTO]:
        """Obtain a list of data transfer objects with the sprint results.

        |  By default, return the results of sprints in the current season.
        |  If only year parameter is provided, return the results for that year.
        |  If year and race are provided, return the results for that GP from that season.
        |  If only the race is provided, return the results for that GP from current season.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str): Optional parameter with a year to be queried.
                Defaults to 'current'.
            race (int, str, None): Optional parameter with a number of a race
                to be queried. Defaults to None.

        Returns:
            list[SprintResultDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        url = Yuki._build_url(year, race, "sprint")
        response = self._make_request(url)

        response = response["MRData"]["RaceTable"]["Races"][0]["SprintResults"]
        return [SprintResultDTO(**x) for x in response]

    def get_drivers_standings(
        self,
        year: Union[int, str] = "current",
        race: Union[int, str, None] = None,
        winners: bool = False,
    ) -> list[DriverStandingDTO]:
        """Obtain a list of data transfer objects with the driver standings.

        |  By default, return the standings for a current seasons.
        |  If only year parameter is provided, return the standings at the end of that season.
        |  If year and race are provided, return the standings after that race in that season.
        |  If only the race is provided, return the standings after that race in the current season.
        |  If winners argument is True, list all winners of the driver championships.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str): Optional parameter with a year to be queried.
                Defaults to 'current'.
            race (int, str, None): Optional parameter with a number of a race
                to be queried. Defaults to 'last'.
            winners (bool): Optional parameter for listing all winners of championship.
                Defaults to False.

        Returns:
            list[RaceResultDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        if winners:
            url = Yuki._build_url("driverStandings", "1")
        url = Yuki._build_url(year, race, "driverStandings")
        response = self._make_request(url)

        response = response["MRData"]["StandingsTable"]["StandingsLists"][0][
            "DriverStandings"
        ]
        return [DriverStandingDTO(**x) for x in response]

    def get_constructors_standings(
        self,
        year: Union[int, str] = "current",
        race: Union[int, str, None] = None,
        winners: bool = False,
    ) -> list[ConstructorStandingDTO]:
        """Obtain a list of data transfer objects with the constructor standings.

        |  By default, return the standings for a current seasons.
        |  If only year parameter is provided, return the standings at the end of that season.
        |  If year and race are provided, return the standings after that race in that season.
        |  If only the race is provided, return the standings after that race in the current season.
        |  If winners argument is True, list all winners of the constructor championships.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str): Optional parameter with a year to be queried.
                Defaults to 'current'.
            race (int, str, None): Optional parameter with a number of a race
                to be queried. Defaults to 'last'.
            winners (bool): Optional parameter for listing all winners of championship.
                Defaults to False.

        Returns:
            list[RaceResultDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        if winners:
            url = Yuki._build_url("constructorStandings", "1")
        url = Yuki._build_url(year, race, "constructorStandings")
        response = self._make_request(url)

        response = response["MRData"]["StandingsTable"]["StandingsLists"][0][
            "ConstructorStandings"
        ]
        return [ConstructorStandingDTO(**x) for x in response]

    def get_finishing_statuses(
        self, year: Union[int, str, None] = None, race: Union[int, str, None] = None
    ) -> list[StatusDTO]:
        """Obtain a list of data transfer objects with finishing statuses.

        |  By default, return all of finishing status codes.
        |  If only the year is provided, return the status codes for that season.
        |  If year and race are provided, return the status codes for that race.
        |  If only the race is provided, raise the WrongQueryParameters error.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str, None): Optional parameter with a year to be queried.
                Defaults to None.
            race (int, str, None): Optional parameter with a number of a race
                to be queried. Defaults to None.

        Returns:
            list[StatusDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        url = Yuki._build_url(year, race, "status")
        response = self._make_request(url)

        response = response["MRData"]["StatusTable"]["Status"]
        return [StatusDTO(**x) for x in response]

    def get_lap_times(
        self,
        year: Union[int, str] = "current",
        race: Union[int, str] = "last",
        lap: Union[int, str] = 1,
    ) -> list[LapDTO]:
        """Obtain a list of data transfer objects with lap times.

        Lap time data is available from the 1996 season onwards.

        |  By default, return the pit stops from the last race.
        |  If only the year is provided, return the pit stops from the last race of that season.
        |  If only the year and race are provided, return the pit stops of that race.
        |  If only the race is provided, return the pit stops of that race in the current season.
        |  If only the lap parameters is provided, return that lap from the last race.
        |  If only the race and lap parameters are provided, return that lap from that race
        |  from a current season.
        |  If only the year and lap parameters are provided, return that lap from the last race
        |  from that season.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str): Optional parameter with a year to be queried.
                Defaults to 'current'.
            race (int, str): Optional parameter with a number of a race
                to be queried. Defaults to 'last'.
            lap (int, str): Optional parameter with a number of a lap to be queried.
                Defaults to 1.

        Returns:
            list[LapDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        url = Yuki._build_url(year, race, "laps", lap)
        response = self._make_request(url)

        response = response["MRData"]["RaceTable"]["Races"][0]["Laps"]
        return [LapDTO(**x) for x in response]

    def get_pit_stops(
        self, year: Union[int, str] = "current", race: Union[int, str] = "last"
    ) -> list[PitStopDTO]:
        """Obtain a list of data transfer objects with information about the pit stops .

        Pit stop data is available from the 2012 season onwards.

        |  By default, return the pit stops from the last race.
        |  If only the year is provided, return the pit stops from the last race of that season.
        |  If only the year and race are provided, return the pit stops from that race.
        |  If only the race is provided, return the pit stops from that race in the current season.
        |  If provided parameters are not real (e.g. year from the future),
        |  raise the WrongQueryParameters error.

        Args:
            year (int, str): Optional parameter with a year to be queried.
                Defaults to 'current'.
            race (int, str): Optional parameter with a number of a race
                to be queried. Defaults to 'last'.

        Returns:
            list[PitStopDTO]: List of data transfer objects.

        Raises:
            HTTPError: The response's status code is not less than 400.
            WrongQueryParameters: The output for provided query parameters is empty.
        """

        url = Yuki._build_url(year, race, "pitstops")
        response = self._make_request(url)

        response = response["MRData"]["RaceTable"]["Races"][0]["PitStops"]
        return [PitStopDTO(**x) for x in response]
