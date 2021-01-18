# Champion
Model: Teamfight Tactics

## `Champions` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`set: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"cdragon_tft_full": ["set"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`set: int`
>
>`champions: List[Champion]` <Badge text="Iterator" type="warning" vertical="middle"/>

## `Champion` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`key: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`set: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`lol_id: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`name: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"cdragon_tft_full": ["key", "set"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`set: str`
>
>`key: str`
>
>`name: str`
>
>`cost: int`
>
>`stats: ChampionStatData`
>
>`trait_keys: List[str]`
>
>`ability: ChampionAbilityData`
>
>`lol_id: int`
>
>`icon_path: str`
>
>`icon_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>

>`traits -> List["Trait"]` <Badge text="bridge" type="error" vertical="middle"/>

## `ChampionStatData` <Badge text="Pyot Static" vertical="middle"/>
>`armor: int`
>
>`attack_speed: float`
>
>`crit_chance: float`
>
>`crit_multiplier: float`
>
>`damage: int`
>
>`hp: int`
>
>`initial_mana: int`
>
>`magic_resist: int`
>
>`mana: int`
>
>`range: int`

## `ChampionAbilityData` <Badge text="Pyot Static" vertical="middle"/>
>`name: str`
>
>`description: str`
>
>`cleaned_description: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`icon_path: str`
>
>`icon_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`variables: List[ChampionAbilityVariableData]`

## `ChampionAbilityVariableData` <Badge text="Pyot Static" vertical="middle"/>
>`name: str`
>
>`value: List[int]`
