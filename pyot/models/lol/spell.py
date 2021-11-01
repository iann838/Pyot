from typing import List, Iterator

from pyot.conf.model import models
from pyot.core.functional import cache_indexes, lazy_property
from pyot.utils.lol.cdragon import abs_url
from .base import PyotCore


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
        raws = {"modes"}
        renamed = {"game_modes": "modes"}
        rules = {"cdragon_spells_full": ["version", "locale", "?id"]}

    def __init__(self, id: int = None, version: str = models.lol.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    @cache_indexes
    def filter(self, indexer, data):
        return indexer.get(self.id, data, "id")

    @lazy_property
    def icon_abspath(self) -> str:
        return abs_url(self.icon_path, self.metaroot.version)


class Spells(PyotCore):
    spells: List[Spell]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_spells_full": ["version", "locale"]}

    def __init__(self, version: str = models.lol.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.spells[item]

    def __iter__(self) -> Iterator[Spell]:
        return iter(self.spells)

    def __len__(self):
        return len(self.spells)

    def transform(self, data):
        return {"spells": data}
