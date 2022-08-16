# Ranked 

Module: `pyot.models.val.ranked` 

### _class_ `Leaderboard`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `act_id`: `str = empty` 
  * `platform`: `str = models.val.DEFAULT_PLATFORM` 
* `__iter__` -> `Iterator[pyot.models.val.ranked.LeaderboardPlayerData]` 
* `__len__` -> `int` 

Endpoints: 
* `ranked_v1_leaderboards`: `['act_id']` 

Query Params: 
* `size`: `int = 200` 
* `start_index`: `int = 0` 

Attributes: 
* `act_id` -> `str` 
* `total_players` -> `int` 
* `players` -> `List[pyot.models.val.ranked.LeaderboardPlayerData]` 
* `immortal_starting_page` -> `int` 
* `immortal_starting_index` -> `int` 
* `top_tier_rr_threshold` -> `int` 
* `tier_details` -> `Dict[str, pyot.models.val.ranked.LeaderboardTierDetailData]` 
* `start_index` -> `int` 
* `query_str` -> `str` 
* `shard` -> `str` 


### _class_ `LeaderboardPlayerData`

Type: `PyotStatic` 

Attributes: 
* `puuid` -> `str` 
* `game_name` -> `str` 
* `tag_line` -> `str` 
* `leaderboard_rank` -> `int` 
* `ranked_rating` -> `int` 
* `number_of_wins` -> `int` 
* `competitive_tier` -> `int` 

Properties: 
* _property_ `account` -> `Account` 


### _class_ `LeaderboardTierDetailData`

Type: `PyotStatic` 

Attributes: 
* `ranked_rating_threshold` -> `int` 
* `starting_page` -> `int` 
* `starting_index` -> `int` 


