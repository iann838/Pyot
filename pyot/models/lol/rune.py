from .__core__ import PyotCore
from ...stores.cdragon import CDragon, CDragonTransformers
from ...core.exceptions import NotFound
from typing import List, Iterator



# PYOT CORE OBJECTS

class Rune(PyotCore):
    id: int
    name: str
    major_patch: str
    description: str
    long_description: str
    cleaned_description: str
    icon_path: str

    class Meta(PyotCore.Meta):
        removed = ["tooltip", "end_of_game_stat_descs"]
        rules = {"cdragon_rune_full": ["id"]}
        renamed = {"major_change_patch_version": "major_patch", "long_desc": "long_description", "short_desc": "description"}

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
        data["cleanedDescription"] = tr.sanitize(data["longDesc"])
        return data


class Runes(PyotCore):
    runes: List[Rune]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_rune_full": []}

    def __init__(self, locale: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        return self.runes[item]

    def __iter__(self) -> Iterator[Rune]:
        return iter(self.runes)

    async def _refactor(self):
        if self.locale.lower() == "en_us":
            self.Meta.server = "default"

    async def _transform(self, data_):
        tr = CDragonTransformers(self.locale)
        runes = []
        for data in data_:
            data["iconPath"] = tr.url_assets(data["iconPath"])
            data["cleanedDescription"] = tr.sanitize(data["longDesc"])
            runes.append({"data": data})
        return {"runes": runes}