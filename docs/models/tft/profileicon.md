# Profileicon 

Module: `pyot.models.tft.profileicon` 

### _class_ ProfileIcon

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `int = None` 
  * `version`: `str = models.tft.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 

Endpoints: 
* `cdragon_profile_icon_full`: `['?id', 'version', 'locale']` 

Attributes: 
* `id` -> `int` 
* `icon_path` -> `str` 

Properties: 
* _lazy_property_ `icon_abspath` -> `str` 


### _class_ ProfileIcons

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `version`: `str = models.tft.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 
* `__iter__` -> `Iterator[pyot.models.tft.profileicon.ProfileIcon]` 
* `__len__` -> `int` 

Endpoints: 
* `cdragon_profile_icon_full`: `['version', 'locale']` 

Attributes: 
* `icons` -> `List[pyot.models.tft.profileicon.ProfileIcon]` 


