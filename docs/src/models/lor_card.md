# Card

Model: Legends of Runeterra

## `Cards` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`set: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"ddragon_lor_set_data": ["set", "locale"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`cards: List[Card]` <Badge text="Iterator" type="warning" vertical="middle"/>


## `Card` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`code: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"ddragon_lor_set_data": ["set", "locale"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`associated_card_codes: List[str]`
>
>`assets: List[CardAssetData]`
>
>`region: str`
>
>`region_ref: str`
>
>`attack: int`
>
>`cost: int`
>
>`health: int`
>
>`description: str`
>
>`description_raw: str`
>
>`levelup_description: str`
>
>`levelup_description_raw: str`
>
>`flavor_text: str`
>
>`artist_name: str`
>
>`name: str`
>
>`code: str`
>
>`keywords: List[str]`
>
>`keyword_refs: List[str]`
>
>`spell_speed: str`
>
>`spell_speed_ref: str`
>
>`rarity: str`
>
>`rarity_ref: str`
>
>`subtype: str`
>
>`subtypes: List[str]`
>
>`supertype: str`
>
>`type: str`
>
>`collectible: bool`
>
>`set: int`
>
>`faction: str`
>
>`number: int`

>`associated_cards -> List["Card"]` <Badge text="bridge" type="error" vertical="middle"/>

## `CardAssetData` <Badge text="Pyot Static" vertical="middle"/>
>`game_absolute_path: str`
>
>`full_absolute_path: str`

## `Deck` <Badge text="Pyot Container" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`batches: Union[List[str], List[Batch]] = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`code: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`batches: List[Batch]` <Badge text="Iterator" type="warning" vertical="middle"/>
>
>`locale: str`
>
>`code: str`
>
>`raw: List[str]`

> #### `append(batch: Union[Batch, str])` <Badge text="method" type="error" vertical="middle"/>
> Appends a Batch object or CardCodeAndCount string to the Deck.
>
> #### `pop(ind: int = -1) -> Batch` <Badge text="method" type="error" vertical="middle"/>
> Remove and return a Batch object by index.
>
> #### `pull(card_code: str)` <Badge text="method" type="error" vertical="middle"/>
> Remove and return a Batch object by code.
>
> #### `encode() -> str` <Badge text="method" type="error" vertical="middle"/>
> Encode the content in `self.batches`, set the code and return it.
>
> #### `decode() -> "Deck"` <Badge text="method" type="error" vertical="middle"/>
> Decode the string in `self.code`, rebuild the batches and return self.

## `Batch` <Badge text="Pyot Container" vertical="middle"/>
>`code: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`count: int = 1` <Badge text="param" type="warning" vertical="middle"/>
>
>`raw: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`code: str`
>
>`count: int`
>
>`locale: str`
>
>`faction: str`
>
>`set: int`
>
>`number: int`

>`card -> Card` <Badge text="bridge" type="error" vertical="middle"/>

> #### `add(amount: int = 1)` <Badge text="method" type="error" vertical="middle"/>
> Add a copy to the batch, `amount` may be passed to add more than 1 copy.
>
> #### `remove(amount: int = 1)` <Badge text="method" type="error" vertical="middle"/>
> Remove a copy from the batch, `amount` may be passed to remove more than 1 copy.

:::tip INFO
Deck encoding and decoding is done using the third party library `lor-deckcodes`, python implementation of the official C# library, details in [repository](https://github.com/Rafalonso/LoRDeckCodesPython).

There are utils methods on the `pyot.utils` module that can help you transform between `lor-deckcodes` type objects and `PyotContainer` type objects.
:::
