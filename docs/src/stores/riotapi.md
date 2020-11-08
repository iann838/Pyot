# Riot API

- Type: <Badge text="Pyot Service" vertical="middle" />
- Models: <Badge text="LOL" type="error" vertical="middle" /> <Badge text="TFT" type="error" vertical="middle" /> <Badge text="LOR" type="error" vertical="middle" /> <Badge text="VAL" type="error" vertical="middle" /> <Badge text="RIOT" type="error" vertical="middle" />
- Description: Store that provides data from the Riot Games API, this contains 70 % of all the endpoints for all the Pyot Core Objects, a list of the endpoints is found below. 

:::tip INFO ABOUT THIS STORE
Service Store integrated from the official Riot Games API. Official endpoints are found at the [Riot Developer Portal](https://developer.riotgames.com/). 

Some endpoints may return 403 due to api key policies restrictions. During late night PST the riot API will experience 5xx due to daily maintainance.
:::

## Pipeline Settings Reference
### Backend: `pyot.stores.RiotAPI`
### Arguments:
> #### `key: str`
> The Riot API key to be used for this model/pipeline.
>
> #### `limiting_share: float = 1`
> ::: danger DEPRECATED
> Since v1.1.0: The `limiting_share` param, now is a sub setting of the new `rate_limiter` param.
> :::
> #### `rate_limiter: Mapping[str, str] = None`
> Accepts a Dict containing the settings for the rate limiter. Please refer to Limiters tab section.
>
> #### `error_handling: Mapping[int, Tuple[str, List[int]]] = None`
> Define how this store should handle request errors, please refer to the General -> Error Handler section on the sidebar.
>
> #### `log_level: int = 10`
> Set the log level for the store. Defaults to 10 (DEBUG level).

## Initialization

> ### initialize() <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
>::: danger DEPRECATED
>Removed since v1.1.0, due to adding unnecessary delays on imports.
>:::

## Endpoints

> ### `RIOT` <Badge text="Model" type="warning" vertical="middle" /> <Badge text="Global" type="error" vertical="middle" />
>`"account_v1_by_puuid"`
>
>`"account_v1_by_riot_id"`
>
>`"account_v1_active_shard"`

> ### `LOL` <Badge text="Model" type="warning" vertical="middle" />
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
>
>`"tournament_v4_codes"`
>
>`"tournament_v4_codes_by_code"`
>
>`"tournament_v4_lobby_events"`
>
>`"tournament_v4_providers"`
>
>`"tournament_v4_tournaments"`
>
>`"tournament_stub_v4_codes"`
>
>`"tournament_stub_v4_lobby_events"`
>
>`"tournament_stub_v4_providers"`
>
>`"tournament_stub_v4_tournaments"`


> ### `TFT` <Badge text="Model" type="warning" vertical="middle" />
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

> ### `LOR` <Badge text="Model" type="warning" vertical="middle" />
>`"ranked_v1_leaderboards"`
>
>`"match_v1_matchlist"`
>
>`"match_v1_match"`

> ### `VAL` <Badge text="Model" type="warning" vertical="middle" />
>`"match_v1_match"`
>
>`"match_v1_matchlist"`
>
>`"match_v1_recent"`
>
>`"content_v1_contents"`

## Example Usage

```python
{
    "BACKEND": "pyot.stores.RiotAPI",
    "API_KEY": os.environ["RIOT_API_KEY"],
    "RATE_LIMITER": {
        "BACKEND": "pyot.limiters.MemoryLimiter",
        "LIMITING_SHARE": 1,
    },
    "ERROR_HANDLING": {
        400: ("T", []),
        503: ("E", [3,3])
    }
}
```