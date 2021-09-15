from typing import TYPE_CHECKING

from pyot.conf.model import models

from .base import PyotCore

if TYPE_CHECKING:
    from .summoner import Summoner


class ThirdPartyCode(PyotCore):
    code: str
    summoner_id: str

    class Meta(PyotCore.Meta):
        rules = {"third_party_code_v4_code": ["summoner_id"]}

    def __init__(self, summoner_id: str = None, platform: str = models.tft.DEFAULT_PLATFORM):
        self.initialize(locals())

    def transform(self, data):
        new_data = {}
        new_data["code"] = data
        return new_data

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)
