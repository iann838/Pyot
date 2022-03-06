# Merakichampion 

Module: `pyot.models.lol.merakichampion` 

### _class_ MerakiChampion

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `int = None` 
  * `key`: `str = None` 
  * `name`: `str = None` 

Endpoints: 
* `meraki_champion_by_key`: `['key']` 

Attributes: 
* `id` -> `int` 
* `key` -> `str` 
* `name` -> `str` 
* `title` -> `str` 
* `full_name` -> `str` 
* `icon` -> `str` 
* `resource` -> `str` 
* `attack_type` -> `str` 
* `adaptive_type` -> `str` 
* `stats` -> `pyot.models.lol.merakichampion.MerakiChampionStatData` 
* `roles` -> `List[str]` 
* `attribute_ratings` -> `pyot.models.lol.merakichampion.MerakiChampionAttributeRatingData` 
* `abilities` -> `pyot.models.lol.merakichampion.MerakiChampionAbilityData` 
* `release_date` -> `str` 
* `release_patch` -> `str` 
* `patch_last_changed` -> `str` 
* `price` -> `pyot.models.lol.merakichampion.MerakiChampionPriceData` 
* `skins` -> `List[pyot.models.lol.merakichampion.MerakiChampionSkinData]` 
* `lore` -> `str` 

Properties: 
* _property_ `champion` -> `Champion` 
* _property_ `locale` -> `str` 


### _class_ MerakiChampionAbilityData

Type: `PyotStatic` 

Attributes: 
* `p` -> `List[pyot.models.lol.merakichampion.MerakiChampionSpellData]` 
* `q` -> `List[pyot.models.lol.merakichampion.MerakiChampionSpellData]` 
* `w` -> `List[pyot.models.lol.merakichampion.MerakiChampionSpellData]` 
* `e` -> `List[pyot.models.lol.merakichampion.MerakiChampionSpellData]` 
* `r` -> `List[pyot.models.lol.merakichampion.MerakiChampionSpellData]` 


### _class_ MerakiChampionAttributeRatingData

Type: `PyotStatic` 

Attributes: 
* `damage` -> `int` 
* `toughness` -> `int` 
* `control` -> `int` 
* `mobility` -> `int` 
* `utility` -> `int` 
* `ability_reliance` -> `int` 
* `attack` -> `int` 
* `defense` -> `int` 
* `magic` -> `int` 
* `difficulty` -> `int` 


### _class_ MerakiChampionChromaDescriptionsData

Type: `PyotStatic` 

Attributes: 
* `region` -> `str` 
* `description` -> `str` 


### _class_ MerakiChampionChromaRaritiesData

Type: `PyotStatic` 

Attributes: 
* `region` -> `str` 
* `description` -> `str` 
* `rarity` -> `int` 


### _class_ MerakiChampionPriceData

Type: `PyotStatic` 

Attributes: 
* `blue_essence` -> `int` 
* `rp` -> `int` 
* `sale_rp` -> `int` 


### _class_ MerakiChampionSkinChromaData

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `name` -> `str` 
* `chroma_path` -> `str` 
* `colors` -> `List[str]` 
* `descriptions` -> `List[pyot.models.lol.merakichampion.MerakiChampionChromaDescriptionsData]` 
* `rarities` -> `List[pyot.models.lol.merakichampion.MerakiChampionChromaRaritiesData]` 


### _class_ MerakiChampionSkinData

Type: `PyotStatic` 

Attributes: 
* `name` -> `str` 
* `id` -> `int` 
* `is_base` -> `bool` 
* `availability` -> `str` 
* `format_name` -> `str` 
* `loot_eligible` -> `bool` 
* `cost` -> `Union[str, int]` 
* `sale` -> `int` 
* `distribution` -> `str` 
* `rarity` -> `str` 
* `chromas` -> `List[pyot.models.lol.merakichampion.MerakiChampionSkinChromaData]` 
* `lore` -> `str` 
* `release` -> `str` 
* `set` -> `List[str]` 
* `splash_path` -> `str` 
* `uncentered_splash_path` -> `str` 
* `tile_path` -> `str` 
* `load_screen_path` -> `str` 
* `load_screen_vintage_path` -> `str` 
* `new_effects` -> `bool` 
* `new_animations` -> `bool` 
* `new_recall` -> `bool` 
* `new_voice` -> `bool` 
* `new_quotes` -> `bool` 
* `voice_actor` -> `List[str]` 
* `splash_artist` -> `List[str]` 


### _class_ MerakiChampionSpellAttrData

Type: `PyotStatic` 

Attributes: 
* `attribute` -> `str` 
* `modifiers` -> `List[pyot.models.lol.merakichampion.MerakiChampionSpellModifierData]` 
* `affected_by_cdr` -> `bool` 


### _class_ MerakiChampionSpellData

Type: `PyotStatic` 

Attributes: 
* `name` -> `str` 
* `icon` -> `str` 
* `effects` -> `List[pyot.models.lol.merakichampion.MerakiChampionSpellEffectData]` 
* `cost` -> `pyot.models.lol.merakichampion.MerakiChampionSpellAttrData` 
* `cooldown` -> `pyot.models.lol.merakichampion.MerakiChampionSpellAttrData` 
* `targeting` -> `str` 
* `affects` -> `str` 
* `spellshieldable` -> `str` 
* `resource` -> `str` 
* `damage_type` -> `str` 
* `spell_effects` -> `str` 
* `projectile` -> `str` 
* `on_hit_effects` -> `str` 
* `occurrence` -> `int` 
* `notes` -> `str` 
* `blurb` -> `str` 
* `missile_speed` -> `str` 
* `recharge_rate` -> `str` 
* `collision_radius` -> `str` 
* `tether_radius` -> `str` 
* `on_target_cd_static` -> `str` 
* `inner_radius` -> `str` 
* `speed` -> `str` 
* `width` -> `str` 
* `angle` -> `str` 
* `cast_time` -> `str` 
* `effect_radius` -> `str` 
* `target_range` -> `str` 


### _class_ MerakiChampionSpellEffectData

Type: `PyotStatic` 

Attributes: 
* `description` -> `str` 
* `leveling` -> `List[pyot.models.lol.merakichampion.MerakiChampionSpellAttrData]` 


### _class_ MerakiChampionSpellModifierData

Type: `PyotStatic` 

Attributes: 
* `values` -> `List[float]` 
* `units` -> `List[str]` 


### _class_ MerakiChampionStatData

Type: `PyotStatic` 

Attributes: 
* `health` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `health_regen` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `mana` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `mana_regen` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `armor` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `magic_resistance` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `attack_damage` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `movespeed` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `acquisition_radius` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `selection_radius` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `pathing_radius` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `gameplay_radius` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `critical_strike_damage` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `critical_strike_damage_modifier` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `attack_speed` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `attack_speed_ratio` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `attack_cast_time` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `attack_total_time` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `attack_delay_offset` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `attack_range` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `aram_damage_taken` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `aram_damage_dealt` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `aram_healing` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `aram_shielding` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `urf_damage_taken` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `urf_damage_dealt` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `urf_healing` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 
* `urf_shielding` -> `pyot.models.lol.merakichampion.MerakiChampionStatDetailData` 


### _class_ MerakiChampionStatDetailData

Type: `PyotStatic` 

Attributes: 
* `flat` -> `float` 
* `percent` -> `float` 
* `per_level` -> `float` 
* `percent_per_level` -> `float` 


