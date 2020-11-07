from .__core__ import PyotCore
from pyot.utils import cdragon_url, cdragon_sanitize
from pyot.core.exceptions import NotFound
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

    def _filter(self, data):
        for item in data:
            if item["id"] == self.id:
                return item
        raise NotFound

    def _refactor(self):
        if self.locale.lower() == "en_us":
            self._meta.server = "default"
        load = getattr(self._meta, "load")
        load.pop("id")

    def _transform(self, data):
        data["iconPath"] = cdragon_url(data["iconPath"])
        data["cleanedDescription"] = cdragon_sanitize(data["longDesc"])
        return data


class Runes(PyotCore):
    runes: List[Rune]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_rune_full": []}

    def __init__(self, locale: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.runes[item]

    def __iter__(self) -> Iterator[Rune]:
        return iter(self.runes)

    def __len__(self):
        return len(self.runes)

    def _refactor(self):
        if self.locale.lower() == "en_us":
            self._meta.server = "default"

    def _transform(self, data):
        return {"runes": data}
