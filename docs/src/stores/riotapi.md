# Riot API

- Type: <Badge text="Pyot Source" vertical="middle" />
- Models: <Badge text="LOL" type="error" vertical="middle" /> <Badge text="TFT" type="error" vertical="middle" /> <Badge text="VAL" type="error" vertical="middle" />
- Description: Store that provides data from the Riot Games API, this contains 70 % of all the endpoints for all the Pyot Core Objects, a list of the endpoints is found below. 

:::tip INFO ABOUT THIS STORE
Some endpoints can return 403 due to api key policies restrictions. Official endpoints are found at the [Riot Developer Portal](https://developer.riotgames.com/). 
:::

## Pipeline Settings Reference
### Backend: `pyot.stores.RiotAPI`
### Arguments:
> #### `key: str`
> The Riot API key to be used for this model/pipeline.
>
> #### `limiting_share: float = 1`
> How much of limit of you API key you want to consume in case you have multiple servers with the same key.
>
> #### `error_handling: Mapping[int, Tuple[str, List[int]]] = None`
> Define how this store should handle request errors, please refer to the General -> Error Handler section on the sidebar.
>
> #### `logs_enabled: bool = True`
> Indicates if this stores is allowed to make logs.

## Initialization

> ### initialize() <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> RiotAPI will check if the key is valid by doing a preflight call to `status_v3_shard_data` endpoint.

## Endpoints

> ### `LOL` <Badge text="Model" type="warning" vertical="middle" />
>`"account_v1_by_puuid"`
>
>`"account_v1_active_shard"`
>
>`"champion_v3_rotation"`
>
>`"champion_mastery_v4_by_champion_id"`
>
>`"champion_mastery_v4_all_mastery"`
>
>`"clash_v1_players"`
>
>`"clash_v1_teams"`
>
>`"clash_v1_tournaments_by_team_id"`
>
>`"clash_v1_toutnaments_by_tournament_id"`
>
>`"clash_v1_tournaments_all"`
>
>`"league_v4_summoner_entries"`
>
>`"league_v4_challenger_league"`
>
>`"league_v4_grandmaster_league"`
>
>`"league_v4_master_league"`
>
>`"league_v4_entries_by_division"`
>
>`"league_v4_league_by_league_id"`
>
>`"status_v3_shard_data"`
>
>`"match_v4_match"`
>
>`"match_v4_timeline"`
>
>`"match_v4_matchlist"`
>
>`"spectator_v4_current_game"`
>
>`"spectator_v4_featured_games"`
>
>`"summoner_v4_by_name"`
>
>`"summoner_v4_by_id"`
>
>`"summoner_v4_by_account_id"`
>
>`"summoner_v4_by_puuid"`
>
>`"third_party_code_v4_code"`

> ### `TFT` <Badge text="Model" type="warning" vertical="middle" />
>`"account_v1_by_puuid"`
>
>`"account_v1_active_shard"`
>
>`"league_v1_summoner_entries"`
>
>`"league_v1_challenger_league"`
>
>`"league_v1_grandmaster_league"`
>
>`"league_v1_master_league"`
>
>`"league_v1_entries_by_division"`
>
>`"league_v1_league_by_league_id"`
>
>`"match_v1_matchlist"`
>
>`"match_v1_match"`
>
>`"summoner_v1_by_name"`
>
>`"summoner_v1_by_id"`
>
>`"summoner_v1_by_account_id"`
>
>`"summoner_v1_by_puuid"`

> ### `VAL` <Badge text="Model" type="warning" vertical="middle" />
>`"account_v1_by_puuid"`
>
>`"account_v1_by_riot_id"`
>
>`"account_v1_active_shard"`
>
>`"match_v1_match"`
>
>`"match_v1_matchlist"`
>
>`"content_v1_contents"`