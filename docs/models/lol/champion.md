# Champion 

Module: `pyot.models.lol.champion` 

### _class_ Champion

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `int = None` 
  * `key`: `str = None` 
  * `name`: `str = None` 
  * `version`: `str = models.lol.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 

Endpoints: 
* `cdragon_champion_by_id`: `['version', 'locale', 'id']` 

Attributes: 
* `id` -> `int` 
* `key` -> `str` 
* `name` -> `str` 
* `lore` -> `str` 
* `tactical_info` -> `pyot.models.lol.champion.ChampionTacticalData` 
* `play_style` -> `pyot.models.lol.champion.ChampionPlayerStyleData` 
* `square_path` -> `str` 
* `stinger_sfx_path` -> `str` 
* `choose_vo_path` -> `str` 
* `ban_vo_path` -> `str` 
* `roles` -> `List[str]` 
* `skins` -> `List[pyot.models.lol.champion.ChampionSkinData]` 
* `abilities` -> `pyot.models.lol.champion.ChampionAbilityData` 
* `passive` -> `pyot.models.lol.champion.ChampionPassiveData` 
* `title` -> `str` 
* `recommended_item_defaults` -> `List[str]` 

Properties: 
* _lazy_property_ `ban_vo_abspath` -> `str` 
* _lazy_property_ `choose_vo_abspath` -> `str` 
* _property_ `meraki_champion` -> `MerakiChampion` 
* _lazy_property_ `square_abspath` -> `str` 
* _lazy_property_ `stinger_sfx_abspath` -> `str` 


### _class_ Champions

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `version`: `str = models.lol.DEFAULT_VERSION` 
  * `locale`: `str = models.lol.DEFAULT_LOCALE` 
* `__iter__` -> `Iterator[pyot.models.lol.champion.Champion]` 
* `__len__` -> `int` 

Endpoints: 
* `cdragon_champion_summary`: `['version', 'locale']` 

Attributes: 
* `champions` -> `List[pyot.models.lol.champion.Champion]` 


### _class_ ChampionAbilityData

Type: `PyotStatic` 

Attributes: 
* `p` -> `pyot.models.lol.champion.ChampionPassiveData` 
* `q` -> `pyot.models.lol.champion.ChampionSpellData` 
* `w` -> `pyot.models.lol.champion.ChampionSpellData` 
* `e` -> `pyot.models.lol.champion.ChampionSpellData` 
* `r` -> `pyot.models.lol.champion.ChampionSpellData` 


### _class_ ChampionChromaDescriptionsData

Type: `PyotStatic` 

Attributes: 
* `region` -> `str` 
* `description` -> `str` 


### _class_ ChampionChromaRaritiesData

Type: `PyotStatic` 

Attributes: 
* `region` -> `str` 
* `description` -> `str` 
* `rarity` -> `int` 


### _class_ ChampionPassiveData

Type: `PyotStatic` 

Attributes: 
* `name` -> `str` 
* `icon_path` -> `str` 
* `description` -> `str` 
* `ability_video_path` -> `str` 
* `ability_video_image_path` -> `str` 

Properties: 
* _lazy_property_ `icon_abspath` -> `str` 


### _class_ ChampionPlayerStyleData

Type: `PyotStatic` 

Attributes: 
* `damage` -> `int` 
* `durability` -> `int` 
* `crowd_control` -> `int` 
* `mobility` -> `int` 
* `utility` -> `int` 


### _class_ ChampionSkinChromaData

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `name` -> `str` 
* `chroma_path` -> `str` 
* `colors` -> `List[str]` 
* `descriptions` -> `List[pyot.models.lol.champion.ChampionChromaDescriptionsData]` 
* `rarities` -> `List[pyot.models.lol.champion.ChampionChromaRaritiesData]` 

Properties: 
* _lazy_property_ `chroma_abspath` -> `str` 


### _class_ ChampionSkinData

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `is_base` -> `bool` 
* `name` -> `str` 
* `splash_path` -> `str` 
* `uncentered_splash_path` -> `str` 
* `tile_path` -> `str` 
* `load_screen_path` -> `str` 
* `load_screen_vintage_path` -> `str` 
* `skin_type` -> `str` 
* `rarity` -> `str` 
* `is_legacy` -> `bool` 
* `chroma_path` -> `str` 
* `chromas` -> `List[pyot.models.lol.champion.ChampionSkinChromaData]` 
* `emblems` -> `List[str]` 
* `skin_line` -> `int` 
* `description` -> `str` 
* `splash_video_path` -> `str` 
* `collection_splash_video_path` -> `str` 
* `features_text` -> `str` 
* `region_rarity_id` -> `int` 
* `rarity_gem_path` -> `str` 

Properties: 
* _lazy_property_ `chroma_abspath` -> `str` 
* _lazy_property_ `collection_splash_video_abspath` -> `str` 
* _lazy_property_ `load_screen_abspath` -> `str` 
* _lazy_property_ `load_screen_vintage_abspath` -> `str` 
* _lazy_property_ `splash_abspath` -> `str` 
* _lazy_property_ `splash_video_abspath` -> `str` 
* _lazy_property_ `tile_abspath` -> `str` 
* _lazy_property_ `uncentered_splash_abspath` -> `str` 


### _class_ ChampionSpellData

Type: `PyotStatic` 

Attributes: 
* `key` -> `str` 
* `name` -> `str` 
* `icon_path` -> `str` 
* `cost` -> `List[float]` 
* `cooldown` -> `List[float]` 
* `range` -> `List[float]` 
* `description` -> `str` 
* `long_description` -> `str` 
* `ability_video_path` -> `str` 
* `ability_video_image_path` -> `str` 
* `max_level` -> `int` 
* `formulas` -> `Dict` 
* `coefficients` -> `Dict[str, float]` 
* `effect_amounts` -> `Dict[str, List[float]]` 
* `ammo` -> `Dict[str, List[float]]` 

Properties: 
* _lazy_property_ `cleaned_description` -> `str` 
* _lazy_property_ `icon_abspath` -> `str` 


### _class_ ChampionTacticalData

Type: `PyotStatic` 

Attributes: 
* `style` -> `int` 
* `difficulty` -> `int` 
* `damage_type` -> `str` 


