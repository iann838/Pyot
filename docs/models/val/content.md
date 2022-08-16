# Content 

Module: `pyot.models.val.content` 

### _class_ `Content`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `platform`: `str = models.val.DEFAULT_PLATFORM` 

Endpoints: 
* `content_v1_contents`: `[]` 

Query Params: 
* `locale`: `str = empty` 

Attributes: 
* `version` -> `str` 
* `characters` -> `List[pyot.models.val.content.ContentItemData]` 
* `maps` -> `List[pyot.models.val.content.ContentItemData]` 
* `chromas` -> `List[pyot.models.val.content.ContentItemData]` 
* `skins` -> `List[pyot.models.val.content.ContentItemData]` 
* `skin_levels` -> `List[pyot.models.val.content.ContentItemData]` 
* `equips` -> `List[pyot.models.val.content.ContentItemData]` 
* `game_modes` -> `List[pyot.models.val.content.ContentItemData]` 
* `sprays` -> `List[pyot.models.val.content.ContentItemData]` 
* `spray_levels` -> `List[pyot.models.val.content.ContentItemData]` 
* `charms` -> `List[pyot.models.val.content.ContentItemData]` 
* `charm_levels` -> `List[pyot.models.val.content.ContentItemData]` 
* `player_cards` -> `List[pyot.models.val.content.ContentItemData]` 
* `player_titles` -> `List[pyot.models.val.content.ContentItemData]` 
* `ceremonies` -> `List[pyot.models.val.content.ContentItemData]` 
* `acts` -> `List[pyot.models.val.content.ContentActData]` 


### _class_ `ContentActData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `str` 
* `name` -> `str` 
* `type` -> `str` 
* `parent_id` -> `str` 
* `localized_names` -> `pyot.models.val.content.ContentLocalizedNamesData` 
* `is_active` -> `bool` 

Properties: 
* _property_ `leaderboard` -> `Leaderboard` 


### _class_ `ContentItemData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `str` 
* `name` -> `str` 
* `asset_name` -> `str` 
* `asset_path` -> `str` 
* `localized_names` -> `pyot.models.val.content.ContentLocalizedNamesData` 


### _class_ `ContentLocalizedNamesData`

Type: `PyotStatic` 

Attributes: 
* `ar_ae` -> `str` 
* `de_de` -> `str` 
* `en_gb` -> `str` 
* `en_us` -> `str` 
* `es_es` -> `str` 
* `es_mx` -> `str` 
* `fr_fr` -> `str` 
* `id_id` -> `str` 
* `it_it` -> `str` 
* `ja_jp` -> `str` 
* `ko_kr` -> `str` 
* `pl_pl` -> `str` 
* `pt_br` -> `str` 
* `ru_ru` -> `str` 
* `th_th` -> `str` 
* `tr_tr` -> `str` 
* `vi_vn` -> `str` 
* `zh_cn` -> `str` 
* `zh_tw` -> `str` 


