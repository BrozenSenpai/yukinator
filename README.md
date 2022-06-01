# yukinator
![actions](https://github.com/BrozenSenpai/yukinator/actions/workflows/python-package.yml/badge.svg)[![Documentation Status](https://readthedocs.org/projects/yukinator/badge/?version=latest)](https://yukinator.readthedocs.io/en/latest/?badge=latest)

Unofficial API wrapper for [Ergast API](http://ergast.com/mrd/). 

Created mainly for learning purposes. There are already at least two other wrappers worth checking: [fastF1](https://github.com/theOehrly/Fast-F1) -  a swiss army knife for F1-related analyses, [pyErgast](https://github.com/weiranyu/pyErgast) - a neat pandas wrapper.

The name of the wrapper is Yukinator, in honor of the Japanese Formula 1 driver - Yuki Tsunoda.

## Features
- **Extensive**: covers all Ergast API endpoints
- **Responsible**: minimize the load on the API server
    - implemented caching
- **Simple**: easy to use and customize:
    - object-oriented design
    - use of data transfer objects
    - converts adequate fields from strings to the more suitable types
- **Lightweight**: minimal usage of the third-party packages

## Installation
```
pip install yukinator
 ```

## Getting started
Obtaining data for an Ergast API endpoint is very simple. For example, you can get a list of race objects from the 2020 season like this:
```python
import yukinator

y = yukinator.Yuki()
races_2020 = y.get_races(year=2020)
```
Check the docs to get acquainted with the methods for the rest of the endpoints.

The wrapper is initiated with the caching enabled by default. You can manually set the caching-related attributes like a directory for cache file, time after cached items expire, or clear the whole cache before the first request as follows:
```python
y = yukinator.Yuki(cache_dir='f1project/races', expires_after=9000, force_clear=True)
```
The caching can be also disabled (strongly not recommended):
```python
y = yukinator.Yuki(cache_enabled=False)
```
Chosen fields of the object can be accessed easily:
```python
race_1 = races_2020[0]

# print name of the race
print(race_1.raceName)

# print name from every nested Circuit object
for race in races_2020:
    print(race.Circuit.circuitName)
```
Every object from the obtained list can be converted to the simpler structures:
```python
# convert object to the dictionary
race_1_dict = race_1.to_dict()

# convert object to the tuple
race_1_tuple = race_1.to_tuple()

# convert object to the flat dict - useful for creating pandas dataframes
race_1_flat_dict = race_1.to_flat_dict() 

# convert object to a json string
race_1_json = race_1.to_json()
```

**WARNING**

The Ergast API has a limit of four calls per second and 200 per hour. Please take care while calling the methods within a loop.

## Documentation
The documentation is hosted on [ReadTheDocs.io](https://yukinator.readthedocs.io/en/latest/)

## Help, questions, and contributing
All contributors are very welcome. If you have any questions or a bug to report feel free to open an issue.

## External packages
Yukinator depends on these third-party packages:
* [attrs](https://www.attrs.org/en/stable/)
* [requests-cache](https://requests-cache.readthedocs.io/en/stable/)