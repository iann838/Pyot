
from .base import BaseEndpoint


class DDragonEndpoint(BaseEndpoint):

    base_url = "https://dd.b.pvp.net"

    all = {
        "lor": {
            "ddragon_lor_set_data": "/{version}/set{set}/{locale}/data/set{set}-{locale}.json"
        }
    }
