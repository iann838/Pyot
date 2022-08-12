# DDragon

- Type: Service
- Models: `lor`
- Description: Store that provides data from the Official Data Dragon.

DDragon only supports Legends of Runeterra endpoints (the only one well maintained), DDragon for LoL and TFT are not supported because they are badly maintained and considered low priority by the game team.

## _class_ `DDragon`

Backend: `pyot.stores.ddragon.DDragon`

Definitions:

* `__init__`
  * `error_handler`: `Dict[int, Tuple] = None`
  * `log_level`: `int = 0`

## Endpoints

* `lor`
  * `ddragon_lor_set_data`: `/{version}/set{set}/{locale}/data/set{set}-{locale}.json`
