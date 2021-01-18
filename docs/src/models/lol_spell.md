# Spell
Model: League of Legends

## `Spells` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"cdragon_spells_full": []` <Badge text="endpoint" type="error" vertical="middle"/>

>`spells: List[Spell]` <Badge text="Iterator" type="warning" vertical="middle"/>

## `Spell` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`id: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"cdragon_spells_full": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`id: int`
>
>`name: str`
>
>`description: str`
>
>`summoner_level: int`
>
>`cooldown: int`
>
>`modes: List[str]`
>
>`icon_path: str`
>
>`icon_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
