# Rune 

Module: `pyot.models.lol.rune` 

### _class_ `Rune`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `int = None` 
  * `version`: `str = models.lol.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 

Endpoints: 
* `cdragon_rune_full`: `['version', 'locale', '?id']` 

Attributes: 
* `id` -> `int` 
* `name` -> `str` 
* `major_patch` -> `str` 
* `description` -> `str` 
* `tooltip` -> `str` 
* `long_description` -> `str` 
* `icon_path` -> `str` 
* `end_of_game_stat_descs` -> `List[str]` 


### _class_ `Runes`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `version`: `str = models.lol.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 
* `__iter__` -> `Iterator[pyot.models.lol.rune.Rune]` 
* `__len__` -> `int` 

Endpoints: 
* `cdragon_rune_full`: `['version', 'locale']` 

Attributes: 
* `runes` -> `List[pyot.models.lol.rune.Rune]` 


