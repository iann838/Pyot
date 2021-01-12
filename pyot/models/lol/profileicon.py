from typing import List, Iterator

from pyot.utils.cdragon import cdragon_url
from pyot.core.functional import cache_indexes, lazy_property
from .__core__ import PyotCore


class ProfileIcon(PyotCore):
    id: int
    icon_path: str

    class Meta(PyotCore.Meta):
        rules = {"cdragon_profile_icon_full": ["id"]}

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


class ProfileIcons(PyotCore):
    icons: List[ProfileIcon]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_profile_icon_full": []}

    def __init__(self, locale: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.icons[item]

    def __iter__(self) -> Iterator[ProfileIcon]:
        return iter(self.icons)

    def __len__(self):
        return len(self.icons)

    def _clean(self):
        if self.locale.lower() == "en_us":
            self._meta.server = "default"

    def _transform(self, data):
        return {"icons": data}
