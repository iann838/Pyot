# League 

Module: `pyot.models.tft.league` 

### _class_ `ApexLeague`

Type: `PyotCore` 

Extends: 
* `pyot.models.tft.league.League` 

Definitions: 
* `__init__` -> `None` 
  * `platform`: `str = models.tft.DEFAULT_PLATFORM` 

Endpoints: 
* `league_v1_league_by_league_id`: `['id']` 

Attributes: 
* `tier` -> `str` 
* `id` -> `str` 
* `queue` -> `str` 
* `name` -> `str` 
* `entries` -> `List[pyot.models.tft.league.LeagueEntryData]` 

Properties: 
* _property_ `league` -> `pyot.models.tft.league.League` 


### _class_ `ChallengerLeague`

Type: `PyotCore` 

Extends: 
* `pyot.models.tft.league.ApexLeague` 
* `pyot.models.tft.league.League` 

Definitions: 

Endpoints: 
* `league_v1_challenger_league`: `[]` 

Attributes: 
* `tier` -> `str` 
* `id` -> `str` 
* `queue` -> `str` 
* `name` -> `str` 
* `entries` -> `List[pyot.models.tft.league.LeagueEntryData]` 


### _class_ `DivisionLeague`

Type: `PyotCore` 

Extends: 
* `pyot.models.tft.league.SummonerLeague` 

Definitions: 
* `__init__` -> `None` 
  * `division`: `str = empty` 
  * `tier`: `str = empty` 
  * `platform`: `str = models.tft.DEFAULT_PLATFORM` 

Endpoints: 
* `league_v1_entries_by_division`: `['tier', 'division']` 

Query Params: 
* `page`: `int = empty` 

Attributes: 
* `summoner_id` -> `str` 
* `entries` -> `List[pyot.models.tft.league.SummonerLeagueEntryData]` 
* `queue` -> `str` 
* `division` -> `str` 
* `tier` -> `str` 

Properties: 
* _property_ `summoner` -> `NoReturn` 


### _class_ `GrandmasterLeague`

Type: `PyotCore` 

Extends: 
* `pyot.models.tft.league.ApexLeague` 
* `pyot.models.tft.league.League` 

Definitions: 

Endpoints: 
* `league_v1_grandmaster_league`: `[]` 

Attributes: 
* `tier` -> `str` 
* `id` -> `str` 
* `queue` -> `str` 
* `name` -> `str` 
* `entries` -> `List[pyot.models.tft.league.LeagueEntryData]` 


### _class_ `League`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `str = empty` 
  * `platform`: `str = models.tft.DEFAULT_PLATFORM` 

Endpoints: 
* `league_v1_league_by_league_id`: `['id']` 

Attributes: 
* `tier` -> `str` 
* `id` -> `str` 
* `queue` -> `str` 
* `name` -> `str` 
* `entries` -> `List[pyot.models.tft.league.LeagueEntryData]` 


### _class_ `MasterLeague`

Type: `PyotCore` 

Extends: 
* `pyot.models.tft.league.ApexLeague` 
* `pyot.models.tft.league.League` 

Definitions: 

Endpoints: 
* `league_v1_master_league`: `[]` 

Attributes: 
* `tier` -> `str` 
* `id` -> `str` 
* `queue` -> `str` 
* `name` -> `str` 
* `entries` -> `List[pyot.models.tft.league.LeagueEntryData]` 


### _class_ `SummonerLeague`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `summoner_id`: `str = empty` 
  * `platform`: `str = models.tft.DEFAULT_PLATFORM` 
* `__iter__` -> `Iterator[pyot.models.tft.league.SummonerLeagueEntryData]` 
* `__len__` -> `int` 

Endpoints: 
* `league_v1_summoner_entries`: `['summoner_id']` 

Attributes: 
* `summoner_id` -> `str` 
* `entries` -> `List[pyot.models.tft.league.SummonerLeagueEntryData]` 

Properties: 
* _property_ `summoner` -> `Summoner` 


### _class_ `LeagueEntryData`

Type: `PyotStatic` 

Attributes: 
* `summoner_id` -> `str` 
* `summoner_name` -> `str` 
* `league_points` -> `int` 
* `rank` -> `str` 
* `wins` -> `int` 
* `losses` -> `int` 
* `veteran` -> `bool` 
* `inactive` -> `bool` 
* `fresh_blood` -> `bool` 
* `hot_streak` -> `bool` 
* `mini_series` -> `pyot.models.tft.league.MiniSeriesData` 

Properties: 
* _property_ `summoner` -> `Summoner` 


### _class_ `MiniSeriesData`

Type: `PyotStatic` 

Attributes: 
* `target` -> `int` 
* `wins` -> `int` 
* `losses` -> `int` 
* `progress` -> `str` 


### _class_ `SummonerLeagueEntryData`

Type: `PyotStatic` 

Extends: 
* `pyot.models.tft.league.LeagueEntryData` 

Attributes: 
* `summoner_id` -> `str` 
* `summoner_name` -> `str` 
* `league_points` -> `int` 
* `rank` -> `str` 
* `wins` -> `int` 
* `losses` -> `int` 
* `veteran` -> `bool` 
* `inactive` -> `bool` 
* `fresh_blood` -> `bool` 
* `hot_streak` -> `bool` 
* `mini_series` -> `pyot.models.tft.league.MiniSeriesData` 
* `league_id` -> `str` 
* `queue` -> `str` 
* `tier` -> `str` 

Properties: 
* _property_ `league` -> `League` 


