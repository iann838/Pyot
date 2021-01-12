from typing import List, Iterator, Dict

from pyot.utils import tft_url, cdragon_sanitize
from pyot.core.functional import cache_indexes, lazy_property
from pyot.core.exceptions import NotFound
from .__core__ import PyotCore, PyotStatic


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

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": ["set", "key"]}
        renamed = {"api_name": "key", "desc": "description", "icon": "icon_path"}

    def __init__(self, key: str = None, set: int = None, locale: str = None):
        a = locals()
        if key and not set:
            try:
                a["set"] = int(self.key.split("_")[0][-1])
            except Exception:
                raise RuntimeError("Could not parse 'set' value from key")
        self._lazy_set(a)

    @cache_indexes
    def _filter(self, indexer, data):
        return indexer.get(self.key, data["sets"][str(self.set)]["traits"], "apiName")

    def _clean(self):
        if self.locale.lower() == "default":
            self._meta.server = "en_us"
        self._hide_load_value("key")

    @lazy_property
    def icon_abspath(self) -> str:
        return tft_url(self.icon_path)

    @lazy_property
    def cleaned_description(self) -> str:
        return cdragon_sanitize(self.description)


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

    def _clean(self):
        if self.locale.lower() == "default":
            self._meta.server = "en_us"

    def _filter(self, data):
        try:
            return data["sets"][str(self.set)]["traits"]
        except KeyError:
            raise NotFound("Request was successful but filtering gave no matching item")

    def _transform(self, data):
        return {"traits": data}
