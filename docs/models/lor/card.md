# Card 

Module: `pyot.models.lor.card` 

### _class_ `Card`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `code`: `str = empty` 
  * `version`: `str = models.lor.DEFAULT_VERSION` 
  * `locale`: `str = models.lor.DEFAULT_LOCALE` 
* `__str__` -> `str` 

Endpoints: 
* `ddragon_lor_set_data`: `['set', '?code', 'version', 'locale']` 

Attributes: 
* `associated_card_codes` -> `List[str]` 
* `associated_card_refs` -> `List[str]` 
* `assets` -> `List[pyot.models.lor.card.CardAssetData]` 
* `region` -> `str` 
* `region_ref` -> `str` 
* `regions` -> `List[str]` 
* `region_refs` -> `List[str]` 
* `attack` -> `int` 
* `cost` -> `int` 
* `health` -> `int` 
* `description` -> `str` 
* `description_raw` -> `str` 
* `levelup_description` -> `str` 
* `levelup_description_raw` -> `str` 
* `flavor_text` -> `str` 
* `artist_name` -> `str` 
* `name` -> `str` 
* `code` -> `str` 
* `keywords` -> `List[str]` 
* `keyword_refs` -> `List[str]` 
* `spell_speed` -> `str` 
* `spell_speed_ref` -> `str` 
* `rarity` -> `str` 
* `rarity_ref` -> `str` 
* `subtype` -> `str` 
* `subtypes` -> `List[str]` 
* `supertype` -> `str` 
* `type` -> `str` 
* `collectible` -> `bool` 
* `set` -> `int` 
* `faction` -> `str` 
* `number` -> `int` 
* `subcode` -> `str` 

Properties: 
* _property_ `associated_cards` -> `List[ForwardRef(Card)]` 


### _class_ `Cards`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `set`: `int = empty` 
  * `version`: `str = models.lor.DEFAULT_VERSION` 
  * `locale`: `str = models.lor.DEFAULT_LOCALE` 
* `__iter__` -> `Iterator[pyot.models.lor.card.Card]` 
* `__len__` -> `int` 

Endpoints: 
* `ddragon_lor_set_data`: `['set', 'version', 'locale']` 

Attributes: 
* `cards` -> `List[pyot.models.lor.card.Card]` 


### _class_ `CardAssetData`

Type: `PyotStatic` 

Attributes: 
* `game_absolute_path` -> `str` 
* `full_absolute_path` -> `str` 


### _class_ `Batch`

Type: `PyotUtils` 

Methods: 
* _method_ `add` -> `None` 
  * `amount`: `int = 1` 
  > Add a copy to the batch, `amount` may be passed to add more than 1 copy. 
* _method_ `remove` -> `None` 
  * `amount`: `int = 1` 
  > Remove a copy from the batch, `amount` may be passed to remove more than 1 copy. 

Attributes: 
* `code` -> `str` 
* `count` -> `int` 
* `faction` -> `str` 
* `set` -> `int` 
* `number` -> `int` 

Properties: 
* _property_ `card` -> `pyot.models.lor.card.Card` 


### _class_ `Deck`

Type: `PyotUtils` 

Methods: 
* _method_ `append` -> `None` 
  * `batch`: `Union[pyot.models.lor.card.Batch, str]` 
  > Appends a Batch object or CardCodeAndCount string to the Deck. 
* _method_ `decode` -> `None` 
  > Decode the string in `self.code`, rebuild the batches and return self. 
* _method_ `encode` -> `str` 
  > Encode the content in `self.batches`, set the code and return it. 
* _method_ `pop` -> `pyot.models.lor.card.Batch` 
  * `ind`: `int = -1` 
  > Remove and return a Batch object by index. 
* _method_ `pull` -> `None` 
  * `card_code`: `str` 
  > Remove and return a Batch object by code. 

Attributes: 
* `batches` -> `List[pyot.models.lor.card.Batch]` 
* `code` -> `str` 


