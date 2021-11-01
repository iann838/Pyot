from typing import List, Iterator

from pyot.conf.model import models
from pyot.core.functional import cache_indexes, lazy_property
from pyot.utils.lol.cdragon import abs_url, sanitize
from .base import PyotCore


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
        raws = {"end_of_game_stat_descs"}
        rules = {"cdragon_rune_full": ["version", "locale", "?id"]}
        renamed = {"major_change_patch_version": "major_patch", "long_desc": "long_description", "short_desc": "description"}

    def __init__(self, id: int = None, version: str = models.lol.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    @cache_indexes
    def filter(self, indexer, data):
        return indexer.get(self.id, data, "id")

    @lazy_property
    def icon_abspath(self) -> str:
        return abs_url(self.icon_path, self.metaroot.version)

    @lazy_property
    def cleaned_description(self) -> str:
        return sanitize(self.long_description)


class Runes(PyotCore):
    runes: List[Rune]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_rune_full": ["version", "locale"]}

    def __init__(self, version: str = models.lol.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.runes[item]

    def __iter__(self) -> Iterator[Rune]:
        return iter(self.runes)

    def __len__(self):
        return len(self.runes)

    def transform(self, data):
        return {"runes": data}
