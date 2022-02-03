# Tournament 

Module: `pyot.models.lol.tournament` 

### _class_ Tournament

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = None` 

Endpoints: 
* `tournament_v4_tournaments`: `[]` 

Attributes: 
* `id` -> `int` 
* `region` -> `str` 


### _class_ TournamentCode

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `code`: `str = None` 
  * `region`: `str = None` 

Endpoints: 
* `tournament_v4_codes_by_code`: `['code']` 

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
* _property_ `region` -> `str` 
* _property_ `summoners` -> `Summoner` 


### _class_ TournamentCodes

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = None` 

Endpoints: 
* `tournament_v4_codes`: `[]` 

Queries: 
* `tournament_id`: `int` 
* `count`: `int = None` 

Attributes: 
* `codes` -> `List[str]` 
* `region` -> `str` 

Properties: 
* _property_ `tournament_codes` -> `List[pyot.models.lol.tournament.TournamentCode]` 


### _class_ TournamentLobbyEvents

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `code`: `int = None` 
  * `region`: `str = None` 
* `__iter__` -> `Iterator[pyot.models.lol.tournament.TournamentLobbyEventData]` 
* `__len__` -> `int` 

Endpoints: 
* `tournament_v4_lobby_events`: `['code']` 

Attributes: 
* `events` -> `List[pyot.models.lol.tournament.TournamentLobbyEventData]` 
* `region` -> `str` 


### _class_ TournamentProvider

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = None` 

Endpoints: 
* `tournament_v4_providers`: `[]` 

Attributes: 
* `id` -> `int` 
* `region` -> `str` 


### _class_ TournamentStub

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.tournament.Tournament` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = None` 

Endpoints: 
* `tournament_stub_v4_tournaments`: `[]` 

Attributes: 
* `id` -> `int` 
* `region` -> `str` 


### _class_ TournamentStubCodes

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.tournament.TournamentCodes` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = None` 

Endpoints: 
* `tournament_stub_v4_codes`: `[]` 

Queries: 
* `tournament_id`: `int` 
* `count`: `int = None` 

Attributes: 
* `codes` -> `List[str]` 
* `region` -> `str` 

Properties: 
* _property_ `tournament_codes` -> `List[pyot.models.lol.tournament.TournamentCode]` 


### _class_ TournamentStubLobbyEvents

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.tournament.TournamentLobbyEvents` 

Definitions: 
* `__init__` -> `None` 
  * `code`: `int = None` 
  * `region`: `str = None` 
* `__iter__` -> `Iterator[pyot.models.lol.tournament.TournamentLobbyEventData]` 
* `__len__` -> `int` 

Endpoints: 
* `tournament_stub_v4_lobby_events`: `['code']` 

Attributes: 
* `events` -> `List[pyot.models.lol.tournament.TournamentLobbyEventData]` 
* `region` -> `str` 


### _class_ TournamentStubProvider

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.tournament.TournamentProvider` 

Definitions: 
* `__init__` -> `None` 
  * `region`: `str = None` 

Endpoints: 
* `tournament_stub_v4_providers`: `[]` 

Attributes: 
* `id` -> `int` 
* `region` -> `str` 


### _class_ TournamentLobbyEventData

Type: `PyotStatic` 

Attributes: 
* `summoner_id` -> `str` 
* `event_type` -> `str` 
* `timestamp` -> `str` 


