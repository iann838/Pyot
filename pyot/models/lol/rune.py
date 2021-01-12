from typing import List, Iterator

from pyot.utils import cdragon_url, cdragon_sanitize
from pyot.core.functional import cache_indexes, lazy_property
from .__core__ import PyotCore


# PYOT CORE OBJECTS

class Rune(PyotCore):
    id: int
    name: str
    major_patch: str
    description: str
    tooltip: str
    long_description: str
    icon_path: str
    end_of_game_stat_descs: List[str]

    class Meta(PyotCore.Meta):
        raws = ["end_of_game_stat_descs"]
        rules = {"cdragon_rune_full": ["id"]}
        renamed = {"major_change_patch_version": "major_patch", "long_desc": "long_description", "short_desc": "description"}

    def __init__(self, id: int = None, locale: str = None):
        self._lazy_set(locals())

    @cache_indexes
    def _filter(self, indexer, data):
        return indexer.get(self.id, data, "id")

    def _clean(self):
        if self.locale.lower() == "en_us":
            self._meta.server = "default"
        self._hide_load_value("id")

    @lazy_property
    def icon_abspath(self) -> str:
        return cdragon_url(self.icon_path)

    @lazy_property
    def cleaned_description(self) -> str:
        return cdragon_sanitize(self.long_description)


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

    def _clean(self):
        if self.locale.lower() == "en_us":
            self._meta.server = "default"

    def _transform(self, data):
        return {"runes": data}
