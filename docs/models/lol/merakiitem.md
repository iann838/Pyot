# Merakiitem 

Module: `pyot.models.lol.merakiitem` 

### _class_ `MerakiItem`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `int = empty` 

Endpoints: 
* `meraki_item_by_id`: `['id']` 

Attributes: 
* `name` -> `str` 
* `id` -> `int` 
* `tier` -> `int` 
* `rank` -> `List[str]` 
* `builds_from_ids` -> `List[int]` 
* `builds_into_ids` -> `List[int]` 
* `no_effects` -> `bool` 
* `removed` -> `bool` 
* `required_champion_key` -> `str` 
* `required_ally` -> `str` 
* `icon` -> `str` 
* `simple_description` -> `str` 
* `icon_overlay` -> `bool` 
* `special_recipe_id` -> `int` 
* `nicknames` -> `List[str]` 
* `passives` -> `List[pyot.models.lol.merakiitem.MerakiItemPassiveData]` 
* `active` -> `List[pyot.models.lol.merakiitem.MerakiItemActiveData]` 
* `stats` -> `pyot.models.lol.merakiitem.MerakiItemStatData` 
* `shop` -> `pyot.models.lol.merakiitem.MerakiItemShopData` 

Properties: 
* _property_ `builds_from` -> `List[ForwardRef(MerakiItem)]` 
* _property_ `builds_into` -> `List[ForwardRef(MerakiItem)]` 
* _property_ `item` -> `Item` 
* _property_ `required_champion` -> `MerakiChampion` 
* _property_ `special_recipe` -> `MerakiItem` 


### _class_ `MerakiItemActiveData`

Type: `PyotStatic` 

Attributes: 
* `unique` -> `bool` 
* `name` -> `str` 
* `effects` -> `str` 
* `range` -> `int` 
* `cooldown` -> `int` 


### _class_ `MerakiItemPassiveData`

Type: `PyotStatic` 

Attributes: 
* `unique` -> `bool` 
* `name` -> `str` 
* `effects` -> `str` 
* `range` -> `int` 
* `stats` -> `pyot.models.lol.merakiitem.MerakiItemStatData` 


### _class_ `MerakiItemShopData`

Type: `PyotStatic` 

Attributes: 
* `prices` -> `pyot.models.lol.merakiitem.MerakiItemShopPriceData` 
* `purchasable` -> `bool` 
* `tags` -> `List[str]` 


### _class_ `MerakiItemShopPriceData`

Type: `PyotStatic` 

Attributes: 
* `total` -> `int` 
* `combined` -> `int` 
* `sell` -> `int` 


### _class_ `MerakiItemStatData`

Type: `PyotStatic` 

Attributes: 
* `ability_power` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `armor` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `armor_penetration` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `attack_damage` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `attack_speed` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `cooldown_reduction` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `critical_strike_chance` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `gold_per_10` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `heal_and_shield_power` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `health` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `health_regen` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `lethality` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `lifesteal` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `tenacity` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `magic_penetration` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `magic_resistance` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `mana` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `mana_regen` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `movespeed` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `ability_haste` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 
* `omnivamp` -> `pyot.models.lol.merakiitem.MerakiItemStatDetailData` 


### _class_ `MerakiItemStatDetailData`

Type: `PyotStatic` 

Attributes: 
* `flat` -> `float` 
* `percent` -> `float` 
* `per_level` -> `float` 
* `percent_per_level` -> `float` 
* `percent_base` -> `float` 
* `percent_bonus` -> `float` 


