from .__core__ import PyotCore
from pyot.utils import tft_url
from pyot.core.exceptions import NotFound
from typing import List, Iterator


class ProfileIcon(PyotCore):
    id: int
    icon_path: str

    class Meta(PyotCore.Meta):
        rules = {"cdragon_profile_icon_full": ["id"]}

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
        data["iconPath"] = tft_url(data["iconPath"])
        return data


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

    def _refactor(self):
        if self.locale.lower() == "en_us":
            self._meta.server = "default"

    def _transform(self, data):
        return {"icons": data}
