from typing import List, Iterator, Dict, Union

from pyot.conf.model import models
from pyot.core.functional import cache_indexes, lazy_property
from pyot.core.exceptions import NotFound
from pyot.utils.tft.cdragon import abs_url, join_set_data
from pyot.utils.lol.cdragon import sanitize
from .base import PyotCore, PyotStatic


# PYOT STATIC OBJECT

class TraitEffectData(PyotStatic):
    max_units: int
    min_units: int
    style: int
    variables: Dict[str, Union[float, str]]

    class Meta(PyotStatic.Meta):
        raws = {"variables"}


# PYOT CORE OBJECT

class Trait(PyotCore):
    set: int
    key: str
    name: str
    effects: List[TraitEffectData]
    icon_path: str
    description: str

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": ["?set", "?key", "version", "locale"]}
        renamed = {"api_name": "key", "desc": "description", "icon": "icon_path"}

    def __init__(self, key: str = None, set: int = None, version: str = models.tft.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())
        if key and set is None:
            self.find_set()

    def find_set(self):
        try:
            self.set = int(self.key.split("_")[0][3:])
        except Exception:
            self.set = -1

    @cache_indexes
    def filter(self, indexer, data):
        return indexer.get(self.key, join_set_data(data, self.set, "traits"), "apiName")

    @lazy_property
    def icon_abspath(self) -> str:
        return abs_url(self.icon_path, self.metaroot.version)

    @lazy_property
    def cleaned_description(self) -> str:
        return sanitize(self.description)


class Traits(PyotCore):
    set: int
    traits: List[Trait]

    class Meta(PyotCore.Meta):
        rules = {"cdragon_tft_full": ["?set", "version", "locale"]}

    def __init__(self, set: int = -1, version: str = models.tft.DEFAULT_VERSION, locale: str = models.lol.DEFAULT_LOCALE):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.traits[item]

    def __iter__(self) -> Iterator[Trait]:
        return iter(self.traits)

    def __len__(self):
        return len(self.traits)

    def filter(self, data):
        try:
            return join_set_data(data, self.set, "traits")
        except KeyError as e:
            raise NotFound("Request was successful but filtering gave no matching item") from e

    def transform(self, data):
        return {"traits": data}
