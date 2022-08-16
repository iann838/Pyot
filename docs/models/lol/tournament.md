# Tournament 

Module: `pyot.models.lol.tournament` 

### _class_ `Tournament`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = empty` 

Endpoints: 
* `tournament_v4_tournaments`: `[]` 

Body Params: 
* `name`: `str` 
* `provider_id`: `int` 

Attributes: 
* `id` -> `int` 
* `region` -> `str` 


### _class_ `TournamentCode`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `code`: `str = empty` 
  * `region`: `str = empty` 

Endpoints: 
* `tournament_v4_codes_by_code`: `['code']` 

Body Params: 
* `map_type`: `str` 
* `pick_type`: `str` 
* `spectator_type`: `str` 
* `allowed_summoner_ids`: `List[str] = empty` 

Attributes: 
* `code` -> `str` 
* `spectators` -> `str` 
* `lobby_name` -> `str` 
* `meta_data` -> `str` 
* `password` -> `str` 
* `team_size` -> `int` 
* `provider_id` -> `int` 
* `pick_type` -> `str` 
* `tournament_id` -> `int` 
* `id` -> `int` 
* `map` -> `str` 
* `hosted_region` -> `str` 
* `summoner_ids` -> `List[str]` 

Properties: 
* _property_ `summoners` -> `Summoner` 


### _class_ `TournamentCodes`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = empty` 

Endpoints: 
* `tournament_v4_codes`: `[]` 

Query Params: 
* `tournament_id`: `int` 
* `count`: `int = empty` 

Body Params: 
* `map_type`: `str` 
* `pick_type`: `str` 
* `team_size`: `int` 
* `spectator_type`: `str` 
* `allowed_summoner_ids`: `List[str] = empty` 
* `metadata`: `str = empty` 

Attributes: 
* `codes` -> `List[str]` 
* `region` -> `str` 

Properties: 
* _property_ `tournament_codes` -> `List[pyot.models.lol.tournament.TournamentCode]` 


### _class_ `TournamentLobbyEvents`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `code`: `int = empty` 
  * `region`: `str = empty` 
* `__iter__` -> `Iterator[pyot.models.lol.tournament.TournamentLobbyEventData]` 
* `__len__` -> `int` 

Endpoints: 
* `tournament_v4_lobby_events`: `['code']` 

Attributes: 
* `events` -> `List[pyot.models.lol.tournament.TournamentLobbyEventData]` 
* `region` -> `str` 


### _class_ `TournamentProvider`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = empty` 

Endpoints: 
* `tournament_v4_providers`: `[]` 

Body Params: 
* `region`: `str` 
* `url`: `str` 

Attributes: 
* `id` -> `int` 
* `region` -> `str` 


### _class_ `TournamentStub`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.tournament.Tournament` 

Definitions: 

Endpoints: 
* `tournament_stub_v4_tournaments`: `[]` 

Body Params: 
* `name`: `str` 
* `provider_id`: `int` 

Attributes: 
* `id` -> `int` 
* `region` -> `str` 


### _class_ `TournamentStubCodes`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.tournament.TournamentCodes` 

Definitions: 

Endpoints: 
* `tournament_stub_v4_codes`: `[]` 

Query Params: 
* `tournament_id`: `int` 
* `count`: `int = empty` 

Body Params: 
* `map_type`: `str` 
* `pick_type`: `str` 
* `team_size`: `int` 
* `spectator_type`: `str` 
* `allowed_summoner_ids`: `List[str] = empty` 
* `metadata`: `str = empty` 

Attributes: 
* `codes` -> `List[str]` 
* `region` -> `str` 


### _class_ `TournamentStubLobbyEvents`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.tournament.TournamentLobbyEvents` 

Definitions: 

Endpoints: 
* `tournament_stub_v4_lobby_events`: `['code']` 

Attributes: 
* `events` -> `List[pyot.models.lol.tournament.TournamentLobbyEventData]` 
* `region` -> `str` 


### _class_ `TournamentStubProvider`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.tournament.TournamentProvider` 

Definitions: 

Endpoints: 
* `tournament_stub_v4_providers`: `[]` 

Body Params: 
* `region`: `str` 
* `url`: `str` 

Attributes: 
* `id` -> `int` 
* `region` -> `str` 


### _class_ `TournamentLobbyEventData`

Type: `PyotStatic` 

Attributes: 
* `summoner_id` -> `str` 
* `event_type` -> `str` 
* `timestamp` -> `str` 


