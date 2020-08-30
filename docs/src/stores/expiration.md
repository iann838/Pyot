# Expirations

This argument is available for all the Pyot Stores of type <Badge text="Pyot Cache" vertical="middle" />

## Basics
Accepts a dictionary of endpoints to a timedelta object or int of seconds.

By passing this argument, you override the default endpoints expirations specified in the dictionary. For example:

```python{2,3}
"EXPIRATIONS": {
    "summoner_v4_by_name": 0,
    "league_v4_challenger_league": td(minutes=10),
}
```
This will override the `summoner_v4_by_name` endpoint NOT cache (0 seconds), and `league_v4_challenger_league` to cache for only 10 minutes, and leaving the rest of the default expirations untouched.

## Wildcard Endpoint
To override the rest of the settings without the need of specifying each endpoint, you can use the wildcard `"*"`. For example:
```python{3}
"EXPIRATIONS": {
    "summoner_v4_by_id": td(seconds=10),
    "*": 0
}
```
This will override the `summoner_v4_by_id` expiration to 10 seconds, and **_setting the rest of the endpoints to 0, for instance to NOT cache_**.
:::tip
A good manipulation of expirations mapping will result in a better pipeline stack, for example: `Omnistone` takes care of short time caching like `ChallengerLeague`, while `DjangoCache` taking care of longer caching like `Match` and `Timeline`.
:::

## Default Expirations
Supposing the following import
```python
from datetime import timedelta as td
```
> ### `LOL` <Badge text="Model" type="warning" vertical="middle" />
>`"account_v1_by_puuid": 0`
>
>`"account_v1_active_shard": 0`
>
>`"champion_v3_rotation": td(hours=3)`
>
>`"champion_mastery_v4_all_mastery": 0`
>
>`"champion_mastery_v4_by_champion_id": 0`
>
>`"clash_v1_players": 0`
>
>`"clash_v1_teams": 0`
>
>`"clash_v1_tournaments_by_team_id": 0`
>
>`"clash_v1_toutnaments_by_tournament_id": 0`
>
>`"clash_v1_tournaments_all": td(hours=3)`
>
>`"league_v4_summoner_entries": 0`
>
>`"league_v4_challenger_league": td(minutes=10)`
>
>`"league_v4_grandmaster_league": td(minutes=10)`
>
>`"league_v4_master_league": td(minutes=10)`
>
>`"league_v4_entries_by_division": 0`
>
>`"league_v4_league_by_league_id": 0`
>
>`"status_v3_shard_data": 0`
>
>`"match_v4_match": td(days=7)`
>
>`"match_v4_timeline": td(days=3)`
>
>`"match_v4_matchlist": 0`
>
>`"spectator_v4_current_game": 0`
>
>`"spectator_v4_featured_games": 0`
>
>`"summoner_v4_by_name": 0`
>
>`"summoner_v4_by_id": 0`
>
>`"summoner_v4_by_account_id": 0`
>
>`"summoner_v4_by_puuid": 0`
>
>`"third_party_code_v4_code": 0`
>
>`"cdragon_champion_by_id": td(hours=1)`
>
>`"cdragon_item_full": td(hours=1)`
>
>`"cdragon_rune_full": td(hours=1)`
>
>`"cdragon_profile_icon_full": td(hours=1)`
>
>`"cdragon_spells_full": td(hours=1)`
>
>`"meraki_champion_by_key": td(hours=3)`
>
>`"meraki_item_by_id": td(hours=3)`

> ### `TFT` <Badge text="Model" type="warning" vertical="middle" />
>`"account_v1_by_puuid": 0`
>
>`"account_v1_active_shard": 0`
>
>`"league_v1_summoner_entries": 0`
>
>`"league_v1_challenger_league": td(minutes=10)`
>
>`"league_v1_grandmaster_league": td(minutes=10)`
>
>`"league_v1_master_league": td(minutes=10)`
>
>`"league_v1_entries_by_division": 0`
>
>`"league_v1_league_by_league_id": 0`
>
>`"match_v1_match": td(days=7)`
>
>`"match_v1_matchlist": td(minutes=5)`
>
>`"summoner_v1_by_name": 0`
>
>`"summoner_v1_by_id": 0`
>
>`"summoner_v1_by_account_id": 0`
>
>`"summoner_v1_by_puuid": 0`
>
>`"cdragon_tft_full": td(hours=1)`
>
>`"cdragon_profile_icon_full": td(hours=1)`

> ### `VAL` <Badge text="Model" type="warning" vertical="middle" />
>`"account_v1_by_puuid": 0`
>
>`"account_v1_by_riot_id": 0`
>
>`"account_v1_active_shard": 0`
>
>`"match_v1_match": td(days=7)`
>
>`"match_v1_matchlist": 0`
>
>`"content_v1_contents": td(hours=3)`