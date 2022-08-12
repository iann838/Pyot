# Match 

Module: `pyot.models.tft.match` 

### _class_ `Match`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `str = None` 
  * `region`: `str = models.tft.DEFAULT_REGION` 

Endpoints: 
* `match_v1_match`: `['id']` 

Attributes: 
* `id` -> `str` 
* `info` -> `pyot.models.tft.match.MatchInfoData` 
* `metadata` -> `pyot.models.tft.match.MatchMetadataData` 


### _class_ `MatchHistory`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `puuid`: `str = None` 
  * `region`: `str = models.tft.DEFAULT_REGION` 
* `__iter__` -> `Iterator[pyot.models.tft.match.Match]` 
* `__len__` -> `int` 

Endpoints: 
* `match_v1_matchlist`: `['puuid']` 

Query Params: 
* `count`: `int = 20` 

Attributes: 
* `ids` -> `List[str]` 
* `puuid` -> `str` 

Properties: 
* _property_ `matches` -> `List[pyot.models.tft.match.Match]` 
* _property_ `summoner` -> `Summoner` 


### _class_ `MatchInfoCompanionData`

Type: `PyotStatic` 

Attributes: 
* `content_id` -> `str` 
* `skin_id` -> `int` 
* `species` -> `str` 


### _class_ `MatchInfoData`

Type: `PyotStatic` 

Attributes: 
* `datetime_millis` -> `int` 
* `length_secs` -> `float` 
* `variation` -> `str` 
* `version` -> `str` 
* `participants` -> `List[pyot.models.tft.match.MatchInfoParticipantData]` 
* `queue_id` -> `int` 
* `tft_mode` -> `str` 
* `tft_set_number` -> `int` 

Properties: 
* _property_ `datetime` -> `datetime.datetime` 
* _property_ `length` -> `datetime.timedelta` 


### _class_ `MatchInfoParticipantData`

Type: `PyotStatic` 

Attributes: 
* `companion` -> `pyot.models.tft.match.MatchInfoCompanionData` 
* `gold_left` -> `int` 
* `last_round` -> `int` 
* `level` -> `int` 
* `placement` -> `int` 
* `players_eliminated` -> `int` 
* `puuid` -> `str` 
* `time_eliminated_secs` -> `float` 
* `total_damage_to_players` -> `int` 
* `traits` -> `List[pyot.models.tft.match.MatchInfoTraitData]` 
* `units` -> `List[pyot.models.tft.match.MatchInfoUnitData]` 

Properties: 
* _property_ `summoner` -> `Summoner` 
* _property_ `time_eliminated` -> `datetime.timedelta` 


### _class_ `MatchInfoTraitData`

Type: `PyotStatic` 

Attributes: 
* `name` -> `str` 
* `num_units` -> `int` 
* `style` -> `int` 
* `tier_current` -> `int` 
* `tier_total` -> `int` 

Properties: 
* _property_ `trait` -> `Trait` 


### _class_ `MatchInfoUnitData`

Type: `PyotStatic` 

Attributes: 
* `item_ids` -> `List[int]` 
* `champion_key` -> `str` 
* `chosen` -> `str` 
* `name` -> `str` 
* `rarity` -> `int` 
* `tier` -> `int` 

Properties: 
* _property_ `champion` -> `Champion` 
* _property_ `items` -> `List[ForwardRef(Item)]` 


### _class_ `MatchMetadataData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `str` 
* `data_version` -> `str` 
* `participant_puuids` -> `List[str]` 

Properties: 
* _property_ `participants` -> `List[ForwardRef(Summoner)]` 


