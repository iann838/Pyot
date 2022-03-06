# Ranked 

Module: `pyot.models.lor.ranked` 

### _class_ Leaderboard

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = models.lor.DEFAULT_REGION` 
* `__iter__` -> `Iterator[pyot.models.lor.ranked.LeaderboardPlayerData]` 
* `__len__` -> `int` 

Endpoints: 
* `ranked_v1_leaderboards`: `[]` 

Attributes: 
* `players` -> `List[pyot.models.lor.ranked.LeaderboardPlayerData]` 

Properties: 
* _property_ `region` -> `str` 


### _class_ LeaderboardPlayerData

Type: `PyotStatic` 

Attributes: 
* `name` -> `str` 
* `rank` -> `int` 
* `lp` -> `float` 


