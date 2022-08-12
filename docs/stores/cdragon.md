# CDragon

- Type: Service
- Models: `lol`, `tft`
- Description: Provides data from CommunityDragon Raw.

The CDragon has data that the game client uses. The data structure in CDragon might change at any time without warning, the Pyot Core objects for this might break aswell. Submit an issue if this happens and it will be fixed asap.

## _class_ `CDragon`

Backend: `pyot.stores.cdragon.CDragon`

Definitions:

* `__init__`
  * `error_handler`: `Dict[int, Tuple] = None`
  * `log_level`: `int = 0`

## Endpoints

* `lol`
  * `cdragon_champion_by_id`: `/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/champions/{id}.json`
  * `cdragon_champion_summary`: `/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/champion-summary.json`
  * `cdragon_item_full`: `/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/items.json`
  * `cdragon_rune_full`: `/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/perks.json`
  * `cdragon_spells_full`: `/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/summoner-spells.json`
  * `cdragon_profile_icon_full`: `/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/profile-icons.json`

* `tft`
  * `cdragon_tft_full`: `/{version}/cdragon/tft/{locale}.json`
  * `cdragon_profile_icon_full`: `/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/profile-icons.json`
