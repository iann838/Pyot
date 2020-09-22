from .__core__ import PyotCore
from pyot.utils.cdragon import cdragon_url
from pyot.core.exceptions import NotFound
from typing import List, Iterator


class ProfileIcon(PyotCore):
    id: int
    icon_path: str

    class Meta(PyotCore.Meta):
        rules = {"cdragon_profile_icon_full": ["id"]}

    def __init__(self, id: int = None, locale: str = None):
        self._lazy_set(locals())

    def filter(self, data):
        for item in data:
            if item["id"] == self.id:
                return item
        raise NotFound
    
    def _refactor(self):
        if self.locale.lower() == "en_us":
            self.meta.server = "default"
        load = getattr(self.meta, "load")
        load.pop("id")

    def _transform(self, data):
        data["iconPath"] = cdragon_url(data["iconPath"])
        return data


class ProfileIcons(PyotCore):
    icons: List[ProfileIcon]
    
    class Meta(PyotCore.Meta):
        rules = {"cdragon_profile_icon_full": []}

    def __init__(self, locale: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        return self.icons[item]

    def __iter__(self) -> Iterator[ProfileIcon]:
        return iter(self.icons)

    def _refactor(self):
        if self.locale.lower() == "en_us":
            self.meta.server = "default"

    def _transform(self, data_):
        icons = []
        for data in data_:
            data["iconPath"] = cdragon_url(data["iconPath"])
            icons.append({"data": data})
        return {"icons": icons}