from functools import partial
from typing import List, Iterator, Union
from lor_deckcodes.encode import encode_deck
from lor_deckcodes.decode import decode_deck
from .__core__ import PyotCore, PyotStatic, PyotContainer
from pyot.core.exceptions import NotFound
from pyot.utils import PtrCache, batch_to_ccac

indexer = PtrCache()

# PYOT STATIC OBJECTS

class CardAssetData(PyotStatic):
    game_absolute_path: str
    full_absolute_path: str


# PYOT CORE OBJECTS

class Card(PyotCore):
    associated_card_codes: List[str]
    assets: List[CardAssetData]
    region: str
    region_ref: str
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

    class Meta(PyotCore.Meta):
        raws = ["keywords", "keyword_refs", "subtypes", "associated_card_codes"]
        removed = ["associated_cards"]
        renamed = {"card_code": "code", "associated_card_refs": "associated_card_codes"}
        rules = {"ddragon_lor_set_data": ["set", "locale"]}

    def __init__(self, code: str = None, locale: str = None):
        if code:
            self.set = int(code[:2])
            self.faction = code[2:4]
            self.number = int(code[4:])
        self._lazy_set(locals())

    def filter_func(self, data):
        for ind, card in enumerate(data):
            if card["cardCode"] == self.code:
                return ind
        raise NotFound

    def _filter(self, data): # BE VERY CAREFUL
        ind = indexer.get(self.code, partial(self.filter_func, data))
        if data[ind]["cardCode"] == self.code: # RETURN ONLY IF CODE MATCHES
            return data[ind]
        ind = self.filter_func(data)
        indexer.set(self.code, ind)
        return data[ind]

    def _transform(self, data):
        data["set"] = int(data["set"][3:])
        data["faction"] = data["cardCode"][2:4]
        data["number"] = int(data["cardCode"][4:7])
        data["subcode"] = data["cardCode"][7:] if len(data["cardCode"]) > 7 else ""
        return data

    def __str__(self):
        return self.code

    @property
    def associated_cards(self) -> List["Card"]:
        return [Card(code=code, locale=self.locale) for code in self.associated_card_codes]


class Cards(PyotCore):
    cards: List[Card]

    class Meta(PyotCore.Meta):
        rules = {"ddragon_lor_set_data": ["set", "locale"]}

    def __init__(self, set: int = None, locale: str = None):
        self._lazy_set(locals())

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.cards[item]

    def __iter__(self) -> Iterator[Card]:
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def _transform(self, data):
        return {"cards": data}


## PYOT CONTAINERS

class Batch(PyotContainer):
    code: str
    count: int
    locale: str
    faction: str
    set: int
    number: int

    def __init__(self, code: str = None, count: int = 1, raw: str = None, locale: str = None):
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
        super().__init__(locals())

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

    @property
    def card(self) -> Card:
        return Card(code=self.code, locale=self.locale)


class Deck(PyotContainer):
    batches: List[Batch]
    locale: str
    code: str

    def __init__(self, batches: Union[List[str], List[Batch]] = None, code: str = None, locale: str = None):
        self.batches = []
        if batches:
            for batch in batches:
                self.append(batch)
        if code:
            self.code = code
        super().__init__(locals())

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
        self.batches.append(Batch(code=card_code_and_count[1], count=card_code_and_count[0], locale=self.locale))

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

    def decode(self) -> "Deck":
        '''Decode the string in `self.code`, rebuild the batches and return self.'''
        lor_deck = decode_deck(self.code)
        self.batches = []
        for lor_card in lor_deck:
            self.append(lor_card)
        return self

    @property
    def raw(self) -> List[str]:
        return [str(batch) for batch in self.batches]
