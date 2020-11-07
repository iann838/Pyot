# Item
Model: Teamfight Tactics

## `Items` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"cdragon_tft_full": []` <Badge text="endpoint" type="error" vertical="middle"/>

>`items: List[Item]` <Badge text="Iterator" type="warning" vertical="middle"/>

## `Item` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`id: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"cdragon_tft_full": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`description: str`
>
>`cleaned_description: str`
>
>`effects: Mapping[str, int]`
>
>`from_ids: List[int]`
>
>`icon_path: str`
>
>`id: int`
>
>`name: str`

>`from_items -> List["Item"]` <Badge text="bridge" type="error" vertical="middle"/>