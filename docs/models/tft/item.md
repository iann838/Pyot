# Item 

Module: `pyot.models.tft.item` 

### _class_ Item

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `int = None` 
  * `version`: `str = models.tft.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 

Endpoints: 
* `cdragon_tft_full`: `['?id', 'version', 'locale']` 

Attributes: 
* `description` -> `str` 
* `effects` -> `Mapping[str, int]` 
* `from_ids` -> `List[int]` 
* `icon_path` -> `str` 
* `id` -> `int` 
* `name` -> `str` 

Properties: 
* _lazy_property_ `cleaned_description` -> `str` 
* _property_ `from_items` -> `List[ForwardRef(Item)]` 
* _lazy_property_ `icon_abspath` -> `str` 


### _class_ Items

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `version`: `str = models.tft.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 
* `__iter__` -> `Iterator[pyot.models.tft.item.Item]` 
* `__len__` -> `int` 

Endpoints: 
* `cdragon_tft_full`: `['version', 'locale']` 

Attributes: 
* `items` -> `List[pyot.models.tft.item.Item]` 


