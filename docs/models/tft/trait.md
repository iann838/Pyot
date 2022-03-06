# Trait 

Module: `pyot.models.tft.trait` 

### _class_ Trait

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `key`: `str = None` 
  * `set`: `int = None` 
  * `version`: `str = models.tft.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 

Endpoints: 
* `cdragon_tft_full`: `['?set', '?key', 'version', 'locale']` 

Methods: 
* _method_ `find_set` -> `None` 

Attributes: 
* `set` -> `int` 
* `key` -> `str` 
* `name` -> `str` 
* `effects` -> `List[pyot.models.tft.trait.TraitEffectData]` 
* `icon_path` -> `str` 
* `description` -> `str` 

Properties: 
* _lazy_property_ `cleaned_description` -> `str` 
* _lazy_property_ `icon_abspath` -> `str` 


### _class_ Traits

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `set`: `int = -1` 
  * `version`: `str = models.tft.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 
* `__iter__` -> `Iterator[pyot.models.tft.trait.Trait]` 
* `__len__` -> `int` 

Endpoints: 
* `cdragon_tft_full`: `['?set', 'version', 'locale']` 

Attributes: 
* `set` -> `int` 
* `traits` -> `List[pyot.models.tft.trait.Trait]` 


### _class_ TraitEffectData

Type: `PyotStatic` 

Attributes: 
* `max_units` -> `int` 
* `min_units` -> `int` 
* `style` -> `int` 
* `variables` -> `Dict[str, Union[float, str]]` 


