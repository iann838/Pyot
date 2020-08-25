from .__core__ import PyotCore
from ...stores.cdragon import CDragonTransformers
from ...core.exceptions import NotFound
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
    
    async def _refactor(self):
        if self.locale.lower() == "en_us":
            self.Meta.server = "default"
        load = getattr(self.Meta, "load")
        load.pop("id")

    async def _transform(self, data):
        tr = CDragonTransformers(self.locale)
        data["iconPath"] = tr.url_assets(data["iconPath"])
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

    async def _refactor(self):
        if self.locale.lower() == "en_us":
            self.Meta.server = "default"

    async def _transform(self, data_):
        tr = CDragonTransformers(self.locale)
        icons = []
        for data in data_:
            data["iconPath"] = tr.url_assets(data["iconPath"])
            icons.append({"data": data})
        return {"icons": icons}