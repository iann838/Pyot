# Profileicon 

Module: `pyot.models.lol.profileicon` 

### _class_ `ProfileIcon`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `int = empty` 
  * `version`: `str = models.lol.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 

Endpoints: 
* `cdragon_profile_icon_full`: `['version', 'locale', '?id']` 

Attributes: 
* `id` -> `int` 
* `icon_path` -> `str` 


### _class_ `ProfileIcons`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `version`: `str = models.lol.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 
* `__iter__` -> `Iterator[pyot.models.lol.profileicon.ProfileIcon]` 
* `__len__` -> `int` 

Endpoints: 
* `cdragon_profile_icon_full`: `['version', 'locale']` 

Attributes: 
* `icons` -> `List[pyot.models.lol.profileicon.ProfileIcon]` 


