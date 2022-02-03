# MerakiCDN

- Type: Service
- Models: `lol`
- Description: Provides data from the Meraki CDN.

Until now, champion abilities in particular were unavailable because ddragon's data is inaccurate and cdragon's data is unparsable, instead the data provided are collected from wiki and served by the meraki cdn.

## _class_ MerakiCDN

Backend: `pyot.stores.merakicdn.MerakiCDN`

Definitions:

* `__init__`
  * `error_handler`: `Dict[int, Tuple] = None`
  * `log_level`: `int = 0`

## Endpoints

* `lol`
  * `meraki_champion_by_key`: ``/lol/resources/latest/en-US/champions/{key}.json`
  * `meraki_item_by_id`: ``/lol/resources/latest/en-US/items/{id}.json`
