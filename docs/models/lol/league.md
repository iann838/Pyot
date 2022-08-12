# League 

Module: `pyot.models.lol.league` 

### _class_ `ApexLeague`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.league.League` 

Definitions: 
* `__init__` -> `None` 
  * `queue`: `str = None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 

Endpoints: 
* `league_v4_league_by_league_id`: `['id']` 

Attributes: 
* `tier` -> `str` 
* `id` -> `str` 
* `queue` -> `str` 
* `name` -> `str` 
* `entries` -> `List[pyot.models.lol.league.LeagueEntryData]` 

Properties: 
* _property_ `league` -> `pyot.models.lol.league.League` 


### _class_ `ChallengerLeague`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.league.ApexLeague` 
* `pyot.models.lol.league.League` 

Definitions: 

Endpoints: 
* `league_v4_challenger_league`: `['queue']` 

Attributes: 
* `tier` -> `str` 
* `id` -> `str` 
* `queue` -> `str` 
* `name` -> `str` 
* `entries` -> `List[pyot.models.lol.league.LeagueEntryData]` 


### _class_ `DivisionLeague`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.league.SummonerLeague` 

Definitions: 
* `__init__` -> `None` 
  * `queue`: `str = None` 
  * `division`: `str = None` 
  * `tier`: `str = None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 

Endpoints: 
* `league_v4_entries_by_division`: `['queue', 'tier', 'division']` 

Query Params: 
* `page`: `int = None` 

Attributes: 
* `summoner_id` -> `str` 
* `entries` -> `List[pyot.models.lol.league.SummonerLeagueEntryData]` 
* `queue` -> `str` 
* `division` -> `str` 
* `tier` -> `str` 

Properties: 
* _property_ `summoner` -> `NoReturn` 


### _class_ `GrandmasterLeague`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.league.ApexLeague` 
* `pyot.models.lol.league.League` 

Definitions: 

Endpoints: 
* `league_v4_grandmaster_league`: `['queue']` 

Attributes: 
* `tier` -> `str` 
* `id` -> `str` 
* `queue` -> `str` 
* `name` -> `str` 
* `entries` -> `List[pyot.models.lol.league.LeagueEntryData]` 


### _class_ `League`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `str = None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 

Endpoints: 
* `league_v4_league_by_league_id`: `['id']` 

Attributes: 
* `tier` -> `str` 
* `id` -> `str` 
* `queue` -> `str` 
* `name` -> `str` 
* `entries` -> `List[pyot.models.lol.league.LeagueEntryData]` 


### _class_ `MasterLeague`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.league.ApexLeague` 
* `pyot.models.lol.league.League` 

Definitions: 

Endpoints: 
* `league_v4_master_league`: `['queue']` 

Attributes: 
* `tier` -> `str` 
* `id` -> `str` 
* `queue` -> `str` 
* `name` -> `str` 
* `entries` -> `List[pyot.models.lol.league.LeagueEntryData]` 


### _class_ `SummonerLeague`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `summoner_id`: `str = None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 
* `__iter__` -> `Iterator[pyot.models.lol.league.SummonerLeagueEntryData]` 
* `__len__` -> `int` 

Endpoints: 
* `league_v4_summoner_entries`: `['summoner_id']` 

Attributes: 
* `summoner_id` -> `str` 
* `entries` -> `List[pyot.models.lol.league.SummonerLeagueEntryData]` 

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
* `mini_series` -> `pyot.models.lol.league.MiniSeriesData` 

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
* `pyot.models.lol.league.LeagueEntryData` 

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
* `mini_series` -> `pyot.models.lol.league.MiniSeriesData` 
* `league_id` -> `str` 
* `queue` -> `str` 
* `tier` -> `str` 

Properties: 
* _property_ `league` -> `League` 


