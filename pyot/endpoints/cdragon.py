
from typing import Dict
from pyot.pipeline.token import PipelineToken
from .base import BaseEndpoint


class CDragonEndpoint(BaseEndpoint):

    base_url = "https://raw.communitydragon.org"

    all = {
        "lol": {
            "cdragon_champion_by_id": "/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/champions/{id}.json",
            "cdragon_champion_summary": "/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/champion-summary.json",
            "cdragon_item_full": "/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/items.json",
            "cdragon_rune_full": "/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/perks.json",
            "cdragon_spells_full": "/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/summoner-spells.json",
            "cdragon_profile_icon_full": "/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/profile-icons.json",
        },
        "tft": {
            "cdragon_tft_full": "/{version}/cdragon/tft/{locale}.json",
            "cdragon_profile_icon_full": "/{version}/plugins/rcp-be-lol-game-data/global/{locale}/v1/profile-icons.json",
        }
    }

    def clean(self, token: PipelineToken) -> Dict[str, str]:
        if token.model == "lol" and token.params["locale"].lower() == "en_us":
            token.params["locale"] = "default"
        elif token.model == "tft":
            if token.method in self.all["lol"] and token.params["locale"].lower() == "en_us":
                token.params["locale"] = "default"
            elif token.params["locale"].lower() == "default":
                token.params["locale"] = "en_us"
        return token.params
