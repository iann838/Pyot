# Match 

Module: `pyot.models.lor.match` 

### _class_ Match

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `str = None` 
  * `region`: `str = models.lor.DEFAULT_REGION` 

Endpoints: 
* `match_v1_match`: `['id']` 

Attributes: 
* `id` -> `str` 
* `metadata` -> `pyot.models.lor.match.MatchMetaData` 
* `info` -> `pyot.models.lor.match.MatchInfoData` 

Properties: 
* _property_ `region` -> `str` 


### _class_ MatchHistory

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `puuid`: `str = None` 
  * `region`: `str = models.lor.DEFAULT_REGION` 
* `__iter__` -> `Iterator[pyot.models.lor.match.Match]` 
* `__len__` -> `int` 

Endpoints: 
* `match_v1_matchlist`: `['puuid']` 

Attributes: 
* `ids` -> `List[str]` 
* `puuid` -> `str` 

Properties: 
* _property_ `account` -> `Account` 
* _property_ `matches` -> `List[pyot.models.lor.match.Match]` 
* _property_ `region` -> `str` 


### _class_ MatchInfoData

Type: `PyotStatic` 

Attributes: 
* `mode` -> `str` 
* `type` -> `str` 
* `start_time_strftime` -> `str` 
* `version` -> `str` 
* `players` -> `List[pyot.models.lor.match.MatchPlayerData]` 
* `total_turn_count` -> `int` 

Properties: 
* _property_ `start_time` -> `datetime.datetime` 


### _class_ MatchMetaData

Type: `PyotStatic` 

Attributes: 
* `data_version` -> `str` 
* `match_id` -> `str` 
* `participant_puuids` -> `List[str]` 

Properties: 
* _property_ `participants` -> `List[ForwardRef(Account)]` 


### _class_ MatchPlayerData

Type: `PyotStatic` 

Attributes: 
* `puuid` -> `str` 
* `deck_id` -> `str` 
* `deck_code` -> `str` 
* `factions` -> `List[str]` 
* `game_outcome` -> `str` 
* `order_of_play` -> `int` 
* `win` -> `bool` 

Properties: 
* _property_ `account` -> `Account` 
* _property_ `deck` -> `Deck` 


