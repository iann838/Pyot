# Item 

Module: `pyot.models.lol.item` 

### _class_ `Item`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `int = None` 
  * `version`: `str = models.lol.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 

Endpoints: 
* `cdragon_item_full`: `['version', 'locale', '?id']` 

Attributes: 
* `id` -> `int` 
* `name` -> `str` 
* `description` -> `str` 
* `active` -> `bool` 
* `in_store` -> `bool` 
* `from_ids` -> `List[int]` 
* `to_ids` -> `List[int]` 
* `categories` -> `List[str]` 
* `maps` -> `List[str]` 
* `max_stacks` -> `int` 
* `modes` -> `List[str]` 
* `required_champion_key` -> `str` 
* `required_ally` -> `str` 
* `required_currency` -> `str` 
* `required_currency_cost` -> `int` 
* `is_enchantment` -> `bool` 
* `special_recipe_id` -> `int` 
* `self_cost` -> `int` 
* `total_cost` -> `int` 
* `icon_path` -> `str` 

Properties: 
* _property_ `from_items` -> `List[ForwardRef(Item)]` 
* _property_ `meraki_item` -> `MerakiItem` 
* _property_ `required_champion` -> `Champion` 
* _property_ `special_recipe` -> `Item` 
* _property_ `to_items` -> `List[ForwardRef(Item)]` 


### _class_ `Items`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `version`: `str = models.lol.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 
* `__iter__` -> `Iterator[pyot.models.lol.item.Item]` 
* `__len__` -> `int` 

Endpoints: 
* `cdragon_item_full`: `['version', 'locale']` 

Attributes: 
* `items` -> `List[pyot.models.lol.item.Item]` 


