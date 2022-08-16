# Spell 

Module: `pyot.models.lol.spell` 

### _class_ `Spell`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `int = empty` 
  * `version`: `str = models.lol.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 

Endpoints: 
* `cdragon_spells_full`: `['version', 'locale', '?id']` 

Attributes: 
* `id` -> `int` 
* `name` -> `str` 
* `description` -> `str` 
* `summoner_level` -> `int` 
* `cooldown` -> `int` 
* `modes` -> `List[str]` 
* `icon_path` -> `str` 


### _class_ `Spells`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `version`: `str = models.lol.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 
* `__iter__` -> `Iterator[pyot.models.lol.spell.Spell]` 
* `__len__` -> `int` 

Endpoints: 
* `cdragon_spells_full`: `['version', 'locale']` 

Attributes: 
* `spells` -> `List[pyot.models.lol.spell.Spell]` 


