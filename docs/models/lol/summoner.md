# Summoner 

Module: `pyot.models.lol.summoner` 

### _class_ Summoner

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `str = None` 
  * `account_id`: `str = None` 
  * `name`: `str = None` 
  * `puuid`: `str = None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 

Endpoints: 
* `summoner_v4_by_puuid`: `['puuid']` 
* `summoner_v4_by_id`: `['id']` 
* `summoner_v4_by_account_id`: `['account_id']` 
* `summoner_v4_by_name`: `['name']` 

Attributes: 
* `name` -> `str` 
* `id` -> `str` 
* `account_id` -> `str` 
* `level` -> `int` 
* `puuid` -> `str` 
* `profile_icon_id` -> `int` 
* `revision_date_millis` -> `int` 

Properties: 
* _property_ `account` -> `Account` 
* _property_ `champion_masteries` -> `ChampionMasteries` 
* _property_ `clash_players` -> `ClashPlayers` 
* _property_ `current_game` -> `CurrentGame` 
* _property_ `league_entries` -> `SummonerLeague` 
* _property_ `match_history` -> `MatchHistory` 
* _property_ `platform` -> `str` 
* _property_ `profile_icon` -> `ProfileIcon` 
* _property_ `revision_date` -> `datetime.datetime` 
* _property_ `third_party_code` -> `ThirdPartyCode` 


