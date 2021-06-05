
from .base import BaseEndpoint


class MerakiCDNEndpoint(BaseEndpoint):

    base_url = "https://cdn.merakianalytics.com/riot"

    all = {
        "lol": {
            "meraki_champion_by_key": "/lol/resources/latest/en-US/champions/{key}.json",
            "meraki_item_by_id": "/lol/resources/latest/en-US/items/{id}.json"
        }
    }
