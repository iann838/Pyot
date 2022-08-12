# Item 

Module: `pyot.models.tft.item` 

### _class_ `Item`

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
* `effects` -> `Dict[str, Union[float, str]]` 
* `from_ids` -> `List[int]` 
* `icon_path` -> `str` 
* `id` -> `int` 
* `name` -> `str` 
* `unique` -> `bool` 

Properties: 
* _property_ `from_items` -> `List[ForwardRef(Item)]` 


### _class_ `Items`

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


