from .__core__ import PyotCore
from ...stores.cdragon import CDragon, CDragonTransformers
from ...core.exceptions import NotFound
from typing import List, Iterator


# PYOT CORE OBJECTS

class Spell(PyotCore):
    id: int
    name: str
    description: str
    summoner_level: int
    cooldown: int
    modes: List[str]
    icon_path: str

    class Meta(PyotCore.Meta):
        raws = ["modes"]
        renamed = {"game_modes": "modes"}
        rules = {"cdragon_spells_full": ["id"]}

    def __init__(self, id: int = None, locale: str = None):
        self._lazy_set(locals())

    def filter(self, data):
        for item in data:
            if item["id"] == self.id:
                return item
        raise NotFound

    async def _refactor(self):
        if self.locale.lower() == "en_us":
            self.Meta.server = "default"
        load = getattr(self.Meta, "load")
        load.pop("id")

    async def _transform(self, data):
        tr = CDragonTransformers(self.locale)
        data["iconPath"] = tr.url_assets(data["iconPath"])
        return data


class Spells(PyotCore):
    spells: List[Spell]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_spells_full": []}

    def __init__(self, locale: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        return self.spells[item]

    def __iter__(self) -> Iterator[Spell]:
        return iter(self.spells)

    async def _refactor(self):
        if self.locale.lower() == "en_us":
            self.Meta.server = "default"

    async def _transform(self, data_):
        tr = CDragonTransformers(self.locale)
        spells = []
        for data in data_:
            data["iconPath"] = tr.url_assets(data["iconPath"])
            spells.append({"data": data})
        return {"spells": spells}