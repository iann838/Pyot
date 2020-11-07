from .__core__ import PyotCore, PyotStatic
from pyot.utils import tft_url, cdragon_sanitize
from pyot.core.exceptions import NotFound
from typing import List, Iterator, Mapping, Dict


# PYOT STATIC OBJECT

class TraitEffectData(PyotStatic):
    max_units: int
    min_units: int
    style: int
    variables: Dict[str, int]

    class Meta(PyotStatic.Meta):
        raws = ["variables"]


# PYOT CORE OBJECT

class Trait(PyotCore):
    set: int
    key: str
    name: str
    effects: List[TraitEffectData]
    icon_path: str
    description: str
    cleaned_description: str

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": ["set","key"]}
        renamed = {"api_name": "key", "desc": "description"}

    def __init__(self, key: str = None, set: int = None, locale: str = None):
        a = locals()
        if key and not set:
            try:
                a["set"] = int(self.key.split("_")[0][-1])
            except Exception:
                raise RuntimeError("Could not parse 'set' value from key")
        self._lazy_set(a)

    def _filter(self, data_):
        try:
            data = data_["sets"][str(self.set)]["traits"]
        except KeyError:
            raise NotFound
        for item in data:
            if item["apiName"] == self.key:
                return item
        raise NotFound

    def _refactor(self):
        if self.locale.lower() == "default":
            self._meta.server = "en_us"
        load = getattr(self._meta, "load")
        load.pop("key")

    def _transform(self, data):
        data["iconPath"] = tft_url(data.pop("icon"))
        data["cleanedDescription"] = cdragon_sanitize(data["desc"])
        return data


class Traits(PyotCore):
    set: int
    traits: List[Trait]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": ["set"]}

    def __init__(self, set: int = None, locale: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.traits[item]

    def __iter__(self) -> Iterator[Trait]:
        return iter(self.traits)

    def __len__(self):
        return len(self.traits)

    def _refactor(self):
        if self.locale.lower() == "default":
            self._meta.server = "en_us"

    def _filter(self, data_):
        try:
            data = data_["sets"][str(self.set)]["traits"]
        except KeyError:
            raise NotFound
        return data

    def _transform(self, data):
        return {"traits": data}
