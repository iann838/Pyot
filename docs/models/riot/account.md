# Account 

Module: `pyot.models.riot.account` 

### _class_ `Account`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `puuid`: `str = empty` 
  * `game_name`: `str = empty` 
  * `tag_line`: `str = empty` 
  * `region`: `str = models.riot.DEFAULT_REGION` 

Endpoints: 
* `account_v1_by_puuid`: `['puuid']` 
* `account_v1_by_riot_id`: `['game_name', 'tag_line']` 

Methods: 
* _method_ `active_shard` -> `None` 
  * `game`: `str` 

Attributes: 
* `puuid` -> `str` 
* `game_name` -> `str` 
* `tag_line` -> `str` 


### _class_ `ActiveShard`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `puuid`: `str = empty` 
  * `game`: `str = empty` 
  * `region`: `str = models.riot.DEFAULT_REGION` 

Endpoints: 
* `account_v1_active_shard`: `['puuid', 'game']` 

Attributes: 
* `puuid` -> `str` 
* `game` -> `str` 
* `active_shard` -> `str` 

Properties: 
* _property_ `account` -> `None` 


