# Clash 

Module: `pyot.models.lol.clash` 

### _class_ `ClashPlayers`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `summoner_id`: `str = None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 

Endpoints: 
* `clash_v1_players`: `['summoner_id']` 

Attributes: 
* `summoner_id` -> `str` 
* `players` -> `List[pyot.models.lol.clash.ClashPlayerData]` 

Properties: 
* _property_ `summoner` -> `Summoner` 


### _class_ `ClashTeam`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `str = None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 

Endpoints: 
* `clash_v1_teams`: `['id']` 

Attributes: 
* `id` -> `str` 
* `tournament_id` -> `int` 
* `name` -> `str` 
* `icon_id` -> `int` 
* `tier` -> `int` 
* `captain_summoner_id` -> `str` 
* `abbreviation` -> `str` 
* `players` -> `List[pyot.models.lol.clash.ClashPlayerData]` 

Properties: 
* _property_ `captain` -> `Summoner` 
* _property_ `tournament` -> `ClashTournament` 


### _class_ `ClashTournament`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.clash.ClashTournamentData` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `int = None` 
  * `team_id`: `str = None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 

Endpoints: 
* `clash_v1_tournaments_by_team_id`: `['team_id']` 
* `clash_v1_toutnaments_by_tournament_id`: `['id']` 

Attributes: 
* `id` -> `int` 
* `theme_id` -> `int` 
* `name_key` -> `str` 
* `name_key_secondary` -> `str` 
* `schedule` -> `List[pyot.models.lol.clash.ClashTournamentPhaseData]` 
* `team_id` -> `str` 

Properties: 
* _property_ `team` -> `pyot.models.lol.clash.ClashTeam` 


### _class_ `ClashTournaments`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 
* `__iter__` -> `List[pyot.models.lol.clash.ClashTournamentData]` 
* `__len__` -> `int` 

Endpoints: 
* `clash_v1_tournaments_all`: `[]` 

Attributes: 
* `tournaments` -> `List[pyot.models.lol.clash.ClashTournamentData]` 


### _class_ `ClashPlayerData`

Type: `PyotStatic` 

Attributes: 
* `summoner_id` -> `str` 
* `team_id` -> `str` 
* `position` -> `str` 
* `role` -> `str` 

Properties: 
* _property_ `summoner` -> `Summoner` 
* _property_ `team` -> `ClashTeam` 


### _class_ `ClashTournamentData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `theme_id` -> `int` 
* `name_key` -> `str` 
* `name_key_secondary` -> `str` 
* `schedule` -> `List[pyot.models.lol.clash.ClashTournamentPhaseData]` 


### _class_ `ClashTournamentPhaseData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `registration_timestamp` -> `int` 
* `start_timestamp` -> `int` 
* `cancelled` -> `bool` 

Properties: 
* _property_ `registration_time` -> `datetime.datetime` 
* _property_ `start_time` -> `datetime.datetime` 


