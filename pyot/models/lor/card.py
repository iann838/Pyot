from typing import Dict, List, Iterator, Union

from lor_deckcodes.encode import encode_deck
from lor_deckcodes.decode import decode_deck
from pyot.conf.model import models
from pyot.core.objects import PyotUtilBase
from pyot.core.functional import cache_indexes
from pyot.utils.lor.cards import batch_to_ccac
from .base import PyotCore, PyotStatic


# PYOT STATIC OBJECTS

class CardAssetData(PyotStatic):
    game_absolute_path: str
    full_absolute_path: str


# PYOT CORE OBJECTS

class Card(PyotCore):
    associated_card_codes: List[str]
    associated_card_refs: List[str]
    assets: List[CardAssetData]
    region: str = None
    region_ref: str
    regions: List[str]
    region_refs: List[str]
    attack: int
    cost: int
    health: int
    description: str
    description_raw: str
    levelup_description: str
    levelup_description_raw: str
    flavor_text: str
    artist_name: str
    name: str
    code: str
    keywords: List[str]
    keyword_refs: List[str]
    spell_speed: str
    spell_speed_ref: str
    rarity: str
    rarity_ref: str
    subtype: str
    subtypes: List[str]
    supertype: str
    type: str
    collectible: bool
    set: int
    faction: str
    number: int
    subcode: str

    class Meta(PyotCore.Meta):
        raws = {"keywords", "keyword_refs", "subtypes", "associated_card_codes", "associated_card_refs", "regions", "region_refs"}
        renamed = {"card_code": "code", "associated_cards": "associated_card_codes"}
        rules = {"ddragon_lor_set_data": ["set", "?code", "version", "locale"]}

    def __init__(self, code: str = None, version: str = models.lor.DEFAULT_VERSION, locale: str = models.lor.DEFAULT_LOCALE):
        self.initialize(locals())
        if code:
            self.set = int(code[:2])
            self.faction = code[2:4]
            self.number = int(code[4:])

    @cache_indexes
    def filter(self, indexer, data):
        return indexer.get(self.code, data, "cardCode")

    def transform(self, data):
        data["set"] = int(data["set"][3:])
        data["faction"] = data["cardCode"][2:4]
        data["number"] = int(data["cardCode"][4:7])
        data["subcode"] = data["cardCode"][7:] if len(data["cardCode"]) > 7 else ""
        return data

    def __str__(self):
        return self.code

    @property
    def associated_cards(self) -> List["Card"]:
        return [Card(code=code, version=self.version, locale=self.locale) for code in self.associated_card_codes]


class Cards(PyotCore):
    cards: List[Card]

    class Meta(PyotCore.Meta):
        rules = {"ddragon_lor_set_data": ["set", "version", "locale"]}

    def __init__(self, set: int = None, version: str = models.lor.DEFAULT_VERSION, locale: str = models.lor.DEFAULT_LOCALE):
        self.initialize(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.cards[item]

    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def transform(self, data):
        return {"cards": data}


## PYOT CONTAINERS

class Batch(PyotUtilBase):
    code: str
    count: int
    faction: str
    set: int
    number: int

    def __init__(self, code: str = None, count: int = 1, raw: str = None):
        if code:
            self.code = code
            self.count = int(count)
        elif raw:
            card_code_and_count = raw.split(":")
            self.code = card_code_and_count[1]
            self.count = card_code_and_count[0]
        else:
            raise RuntimeError("Batch takes at least 'code' or 'raw' string, prioritizing 'code'")
        self.set = int(self.code[:2])
        self.faction = self.code[2:4]
        self.number = int(self.code[4:])

    def __str__(self):
        return f"{self.count}:{self.code}"

    def add(self, amount: int = 1):
        '''Add a copy to the batch, `amount` may be passed to add more than 1 copy.'''
        if self.count + amount <= 3:
            self.count += amount
        else:
            raise RuntimeError("The batch cannot contain more than 3 copies in the current version")

    def remove(self, amount: int = 1):
        '''Remove a copy from the batch, `amount` may be passed to remove more than 1 copy.'''
        if self.count > amount:
            self.count -= 1
        else:
            raise RuntimeError("The batch needs to have at least 1 copy, delete it instead")

    def dict(self):
        return {
            "code": self.code,
            "count": self.count,
            "faction": self.faction,
            "set": self.set,
            "number": self.number,
        }

    @property
    def card(self) -> Card:
        return Card(code=self.code)


class Deck(PyotUtilBase):
    batches: List[Batch]
    code: str

    def __init__(self, batches: Union[List[str], List[Batch]] = None, code: str = None):
        self.batches = []
        if batches:
            for batch in batches:
                self.append(batch)
        if code:
            self.code = code

    def __getitem__(self, item):
        if not isinstance(item, int):
            return getattr(self, item)
        return self.batches[item]

    def __iter__(self):
        return iter(self.batches)

    def __len__(self) -> List[Batch]:
        return len(self.batches)

    def append(self, batch: Union[Batch, str]):
        '''Appends a Batch object or CardCodeAndCount string to the Deck.'''
        if isinstance(batch, Batch):
            self.batches.append(batch)
            return
        card_code_and_count = batch.split(":")
        self.batches.append(Batch(code=card_code_and_count[1], count=card_code_and_count[0]))

    def pop(self, ind: int = -1) -> Batch:
        '''Remove and return a Batch object by index.'''
        return self.batches.pop(ind)

    def pull(self, card_code: str):
        '''Remove and return a Batch object by code.'''
        for ind, batch in enumerate(self.batches):
            if batch.code == card_code:
                return self.batches.pop(ind)

    def encode(self) -> str:
        '''Encode the content in `self.batches`, set the code and return it.'''
        self.code = encode_deck([batch_to_ccac(batch) for batch in self.batches])
        return self.code

    def decode(self):
        '''Decode the string in `self.code`, rebuild the batches and return self.'''
        lor_deck = decode_deck(self.code)
        self.batches = []
        for lor_card in lor_deck:
            self.append(lor_card)
        return self

    def dict(self) -> List[Dict]:
        return [batch.dict() for batch in self.batches]

    @property
    def raw(self) -> List[str]:
        return [str(batch) for batch in self.batches]
