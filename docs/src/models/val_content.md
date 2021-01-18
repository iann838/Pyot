# Content
Model: VALORANT

## `Content` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`locale: str = None` <Badge text="query" type="error" vertical="middle"/>

>`"content_v1_contents": []` <Badge text="endpoint" type="error" vertical="middle"/>

>`version: str`
>
>`characters: List[ContentItemData]`
>
>`maps: List[ContentItemData]`
>
>`chromas: List[ContentItemData]`
>
>`skins: List[ContentItemData]`
>
>`skin_levels: List[ContentItemData]`
>
>`equips: List[ContentItemData]`
>
>`game_modes: List[ContentItemData]`
>
>`sprays: List[ContentItemData]`
>
>`spray_levels: List[ContentItemData]`
>
>`charms: List[ContentItemData]`
>
>`charm_levels: List[ContentItemData]`
>
>`player_cards: List[ContentItemData]`
>
>`player_titles: List[ContentItemData]`
>
>`acts: List[ContentActData]`

## `ContentActData` <Badge text="Pyot Static" vertical="middle"/>
>`id: str`
>
>`name: str`
>
>`localized_names: ContentLocalizedNamesData`
>
>`is_active: bool`

>`leaderboard -> "Leaderboard"` <Badge text="bridge" type="error" vertical="middle"/>

## `ContentItemData` <Badge text="Pyot Static" vertical="middle"/>
>`name: str`
>
>`asset_name: str`
>
>`localized_names: ContentLocalizedNamesData`
> :::warning
> Some values will not yield `localized_names`, iterating over each attr might raise `AttributeError`
> :::

## `ContentLocalizedNamesData` <Badge text="Pyot Static" vertical="middle"/>
>`ar_ae: str`
>
>`de_de: str`
>
>`en_gb: str`
>
>`en_us: str`
>
>`es_es: str`
>
>`es_mx: str`
>
>`fr_fr: str`
>
>`id_id: str`
>
>`it_it: str`
>
>`ja_jp: str`
>
>`ko_kr: str`
>
>`pl_pl: str`
>
>`pt_br: str`
>
>`ru_ru: str`
>
>`th_th: str`
>
>`tr_tr: str`
>
>`vi_vn: str`
>
>`zh_cn: str`
>
>`zh_tw: str`
>
>:::tip
>To get the original keys of the object, please call `dict()` or `json()` with `pyotify=False`(default).
>:::
