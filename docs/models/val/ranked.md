# Ranked 

Module: `pyot.models.val.ranked` 

### _class_ Leaderboard

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `act_id`: `str = None` 
  * `platform`: `str = models.val.DEFAULT_PLATFORM` 
* `__iter__` -> `Iterator[pyot.models.val.ranked.LeaderboardPlayerData]` 
* `__len__` -> `int` 

Endpoints: 
* `ranked_v1_leaderboards`: `['act_id']` 

Queries: 
* `size`: `int = None` 
* `start_index`: `int = None` 

Attributes: 
* `act_id` -> `str` 
* `total_players` -> `int` 
* `players` -> `List[pyot.models.val.ranked.LeaderboardPlayerData]` 
* `shard` -> `str` 

Properties: 
* _property_ `platform` -> `str` 


### _class_ LeaderboardPlayerData

Type: `PyotStatic` 

Attributes: 
* `puuid` -> `str` 
* `game_name` -> `str` 
* `tag_line` -> `str` 
* `leaderboard_rank` -> `int` 
* `ranked_rating` -> `int` 
* `number_of_wins` -> `int` 

Properties: 
* _property_ `account` -> `Account` 


