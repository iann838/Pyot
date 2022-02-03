# Champion 

Module: `pyot.models.tft.champion` 

### _class_ Champion

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `key`: `str = None` 
  * `set`: `int = None` 
  * `version`: `str = models.tft.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 

Endpoints: 
* `cdragon_tft_full`: `['?key', '?set', 'version', 'locale']` 

Methods: 
* _method_ `find_set` -> `None` 

Attributes: 
* `set` -> `str` 
* `key` -> `str` 
* `name` -> `str` 
* `cost` -> `int` 
* `stats` -> `pyot.models.tft.champion.ChampionStatData` 
* `trait_keys` -> `List[str]` 
* `ability` -> `pyot.models.tft.champion.ChampionAbilityData` 
* `lol_id` -> `int` 
* `icon_path` -> `str` 

Properties: 
* _lazy_property_ `icon_abspath` -> `str` 
* _property_ `traits` -> `List[ForwardRef(Trait)]` 


### _class_ Champions

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `set`: `int = -1` 
  * `version`: `str = models.tft.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 
* `__iter__` -> `Iterator[pyot.models.tft.champion.Champion]` 
* `__len__` -> `int` 

Endpoints: 
* `cdragon_tft_full`: `['?set', 'version', 'locale']` 

Attributes: 
* `set` -> `int` 
* `champions` -> `List[pyot.models.tft.champion.Champion]` 


### _class_ ChampionAbilityData

Type: `PyotStatic` 

Attributes: 
* `name` -> `str` 
* `description` -> `str` 
* `icon_path` -> `str` 
* `variables` -> `List[pyot.models.tft.champion.ChampionAbilityVariableData]` 

Properties: 
* _lazy_property_ `cleaned_description` -> `str` 
* _lazy_property_ `icon_abspath` -> `str` 


### _class_ ChampionAbilityVariableData

Type: `PyotStatic` 

Attributes: 
* `name` -> `str` 
* `value` -> `List[int]` 


### _class_ ChampionStatData

Type: `PyotStatic` 

Attributes: 
* `armor` -> `int` 
* `attack_speed` -> `float` 
* `crit_chance` -> `float` 
* `crit_multiplier` -> `float` 
* `damage` -> `int` 
* `hp` -> `int` 
* `initial_mana` -> `int` 
* `magic_resist` -> `int` 
* `mana` -> `int` 
* `range` -> `int` 


