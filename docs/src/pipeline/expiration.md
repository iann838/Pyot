# Expiration

This argument is available for all the Pyot Stores of type <Badge text="Pyot Cache" vertical="middle" />

## Basics
Accepts a dictionary of endpoints to a timedelta object or int of seconds.

By passing this argument, you **_override_** the default endpoints expirations specified in the dictionary. For example:

```python{2,3}
"EXPIRATIONS": {
    "summoner_v4_by_name": 120,
    "league_v4_challenger_league": 600, # or timedelta(minutes=10)
}
```
This will override the `summoner_v4_by_name` endpoint to cache 2 minutes, and `league_v4_challenger_league` to cache for only 10 minutes, and leaving the rest of the default expirations untouched.

## Default Expiration
Supposing the following import
```python
from datetime import timedelta as td
```
::: tip REMAINDER
**_Changed in v1.1.0:_** Now all expirations default to 0 (not cached) except the endpoints for static data. Developers should choose to cache what they want to. Pyot shouldn't have a default to that assuming the developer know what he/she is doing.

Models with <Badge text="Global" type="error" vertical="middle" /> badge will be available to all objects, meaning that can you still modify the `"account_v1_by_puuid"` in the `LOL` model and such object called from the `LOL` pipeline will use that pipeline expirations.
:::
::: tip INFO
Only data returned by the `get()` method is sinked through the pipeline, and thus the only ones to have expirations in place.
:::

> ### `RIOT` <Badge text="Model" type="warning" vertical="middle" /> <Badge text="Global" type="error" vertical="middle" />
>`"account_v1_by_puuid": 0`
>
>`"account_v1_by_riot_id": 0`
>
>`"account_v1_active_shard": 0`

> ### `LOL` <Badge text="Model" type="warning" vertical="middle" />
>`"champion_v3_rotation": 0`
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
>`"clash_v1_tournaments_all": 0`
>
>`"league_v4_summoner_entries": 0`
>
>`"league_v4_challenger_league": 0`
>
>`"league_v4_grandmaster_league": 0`
>
>`"league_v4_master_league": 0`
>
>`"league_v4_entries_by_division": 0`
>
>`"league_v4_league_by_league_id": 0`
>
>`"status_v4_platform_data": 0`
>
>`"match_v4_match": 0`
>
>`"match_v4_timeline": 0`
>
>`"match_v4_matchlist": 0`
>
>`"match_v4_tournament_match": 0`
>
>`"match_v4_tournament_matches": 0`
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
> `"tournament_v4_codes_by_code": 0`
>
> `"tournament_v4_lobby_events": 0`
>
> `"tournament_stub_v4_lobby_events": 0`
>
>`"cdragon_champion_by_id": td(hours=3)`
>
>`"cdragon_item_full": td(hours=3)`
>
>`"cdragon_rune_full": td(hours=3)`
>
>`"cdragon_profile_icon_full": td(hours=3)`
>
>`"cdragon_spells_full": td(hours=3)`
>
>`"meraki_champion_by_key": td(hours=3)`
>
>`"meraki_item_by_id": td(hours=3)`


> ### `TFT` <Badge text="Model" type="warning" vertical="middle" />
>`"league_v1_summoner_entries": 0`
>
>`"league_v1_challenger_league": 0`
>
>`"league_v1_grandmaster_league": 0`
>
>`"league_v1_master_league": 0`
>
>`"league_v1_entries_by_division": 0`
>
>`"league_v1_league_by_league_id": 0`
>
>`"match_v1_match": 0`
>
>`"match_v1_matchlist": 0`
>
>`"summoner_v1_by_name": 0`
>
>`"summoner_v1_by_id": 0`
>
>`"summoner_v1_by_account_id": 0`
>
>`"summoner_v1_by_puuid": 0`
>
>`"cdragon_tft_full": td(hours=3)`
>
>`"cdragon_profile_icon_full": td(hours=3)`

> ### `LOR` <Badge text="Model" type="warning" vertical="middle" />
>`"ranked_v1_leaderboards": 0`
>
>`"match_v1_matchlist": 0`
>
>`"match_v1_match": 0`
>
>`"status_v1_platform_data": 0`
>
>`"ddragon_lor_set_data": td(hours=3)`


> ### `VAL` <Badge text="Model" type="warning" vertical="middle" />
>`"match_v1_match": 0`
>
>`"match_v1_matchlist": 0`
>
>`"match_v1_recent": 0`
>
>`"ranked_v1_leaderboards": 0`
>
>`"status_v1_platform_data": 0`
>
>`"content_v1_contents": td(hours=3)`
