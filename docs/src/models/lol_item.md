# Item
Model: League of Legends

## `Items` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"cdragon_item_full": []` <Badge text="endpoint" type="error" vertical="middle"/>

>`items: List[Item]` <Badge text="Iterator" type="warning" vertical="middle"/>

## `Item` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`id: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"cdragon_item_full": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`id: int`
>
>`name: str`
>
>`description: str`
>
>`cleaned_description: str`
>
>`active: bool`
>
>`in_store: bool`
>
>`from_ids: List[int]`
>
>`to_ids: List[int]`
>
>`categories: List[str]`
>
>`maps: List[str]`
>
>`max_stacks: int`
>
>`modes: List[str]`
>
>`required_champion_key: str`
>
>`required_currency: str`
>
>`required_currency_cost: int`
>
>`special_recipe: int`
>
>`self_cost: int`
>
>`total_cost: int`
>
>`icon_path: str`

>`from_items -> List["Item"]` <Badge text="bridge" type="error" vertical="middle"/>
>
>`to_items -> List["Item"]` <Badge text="bridge" type="error" vertical="middle"/>
>
>`meraki_item -> "MerakiItem"` <Badge text="bridge" type="error" vertical="middle"/>
