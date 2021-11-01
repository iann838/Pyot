from typing import List, Iterator

from pyot.conf.model import models
from pyot.core.functional import cache_indexes, lazy_property
from pyot.utils.tft.cdragon import abs_url
from .base import PyotCore


class ProfileIcon(PyotCore):
    id: int
    icon_path: str

    class Meta(PyotCore.Meta):
        rules = {"cdragon_profile_icon_full": ["?id", "version", "locale"]}

    def __init__(self, id: int = None, version: str = models.tft.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    @cache_indexes
    def filter(self, indexer, data):
        return indexer.get(self.id, data, "id")

    @lazy_property
    def icon_abspath(self) -> str:
        return abs_url(self.icon_path, self.metaroot.version)


class ProfileIcons(PyotCore):
    icons: List[ProfileIcon]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_profile_icon_full": ["version", "locale"]}

    def __init__(self, version: str = models.tft.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.icons[item]

    def __iter__(self) -> Iterator[ProfileIcon]:
        return iter(self.icons)

    def __len__(self):
        return len(self.icons)

    def transform(self, data):
        return {"icons": data}
