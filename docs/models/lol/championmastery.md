# Championmastery 

Module: `pyot.models.lol.championmastery` 

### _class_ ChampionMasteries

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `summoner_id`: `str = None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 
* `__iter__` -> `Iterator[pyot.models.lol.championmastery.ChampionMastery]` 
* `__len__` -> `int` 

Endpoints: 
* `champion_mastery_v4_all_mastery`: `['summoner_id']` 

Attributes: 
* `summoner_id` -> `str` 
* `masteries` -> `List[pyot.models.lol.championmastery.ChampionMastery]` 
* `total_score` -> `int` 

Properties: 
* _property_ `platform` -> `str` 
* _property_ `summoner` -> `Summoner` 


### _class_ ChampionMastery

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `summoner_id`: `str = None` 
  * `champion_id`: `int = None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 

Endpoints: 
* `champion_mastery_v4_by_champion_id`: `['summoner_id', 'champion_id']` 

Attributes: 
* `champion_id` -> `int` 
* `champion_level` -> `int` 
* `champion_points` -> `int` 
* `last_play_timestamp` -> `int` 
* `champion_points_since_last_level` -> `int` 
* `champion_points_until_next_level` -> `int` 
* `chest_granted` -> `bool` 
* `tokens_earned` -> `int` 
* `summoner_id` -> `str` 

Properties: 
* _property_ `champion` -> `Champion` 
* _property_ `last_play_time` -> `datetime.datetime` 
* _property_ `meraki_champion` -> `MerakiChampion` 
* _property_ `platform` -> `str` 
* _property_ `summoner` -> `Summoner` 


