# Championrotation 

Module: `pyot.models.lol.championrotation` 

### _class_ ChampionRotation

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 

Endpoints: 
* `champion_v3_rotation`: `[]` 

Attributes: 
* `free_champion_ids` -> `List[int]` 
* `free_newie_champion_ids` -> `List[int]` 
* `newie_max_level` -> `int` 

Properties: 
* _property_ `free_champions` -> `List[ForwardRef(Champion)]` 
* _property_ `free_newie_champions` -> `List[ForwardRef(Champion)]` 
* _property_ `meraki_free_champions` -> `List[ForwardRef(MerakiChampion)]` 
* _property_ `meraki_free_newie_champions` -> `List[ForwardRef(MerakiChampion)]` 
* _property_ `platform` -> `str` 


