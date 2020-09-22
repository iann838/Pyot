# Trait
Model: Teamfight Tactics

## `Traits` <Badge text="Pyot Core" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`set: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"cdragon_tft_full": ["set"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`set: int`
>
>`traits: List[Trait]` <Badge text="Iterator" type="warning" vertical="middle"/>

## `Trait` <Badge text="Pyot Core" vertical="middle"/>
>`key: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`set: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"cdragon_tft_full": ["set","key"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`set: int`
>
>`key: str`
>
>`name: str`
>
>`effects: List[TraitEffectData]`
>
>`icon_path: str`
>
>`description: str`
>
>`cleaned_description: str`

## `TraitEffectData` <Badge text="Pyot Static" vertical="middle"/>
>`max_units: int`
>
>`min_units: int`
>
>`style: int`
>
>`variables: Dict[str, int]`
