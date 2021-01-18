# Champion
Model: League of Legends

## `Champion` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
> `id: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
> `key: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
> `name: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
> `locale: str = None` <Badge text="param" type="warning" vertical="middle"/>

> `"cdragon_champion_by_id": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`id: int`
>
>`key: str`
>
>`name: str`
>
>`lore: str`
>
>`tactical_info: ChampionTacticalData`
>
>`play_style: ChampionPlayerStyleData`
>
>`square_path: str`
>
>`square_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`roles: List[str]`
>
>`skins: List[ChampionSkinData]`
>
>`abilities: ChampionAbilityData `
>
>`recommended_item_defaults: List[str]`

> `meraki_champion -> "MerakiChampion"` <Badge text="bridge" type="error" vertical="middle"/>

## `ChampionAbilityData` <Badge text="Pyot Static" vertical="middle"/>
>`p: ChampionPassiveData`
>
>`q: ChampionSpellData`
>
>`w: ChampionSpellData`
>
>`e: ChampionSpellData`
>
>`r: ChampionSpellData`

## `ChampionSpellData` <Badge text="Pyot Static" vertical="middle"/>
>`key: str`
>
>`name: str`
>
>`icon_path: str`
>
>`icon_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`cost: List[int]`
>
>`cooldown: List[int]`
>
>`range: List[int]`
>
>`description: str`
>
>`long_description: str`
>
>`cleaned_description: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`ability_video_path: str`
>
>`ability_video_image_path: str`
>
>`max_level: int`
>
>`formulas: Dict`
>
>`coefficients: Dict[str, int]`
>
>`effect_amounts: Dict[str, List[int]]`
>
>`ammo: Dict[str, List[int]]`

## `ChampionPassiveData` <Badge text="Pyot Static" vertical="middle"/>
>`name: str`
>
>`icon_path: str`
>
>`icon_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`description: str`

## `ChampionSkinData` <Badge text="Pyot Static" vertical="middle"/>
>`id: int`
>
>`is_base: bool`
>
>`name: str`
>
>`splash_path: str`
>
>`splash_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`uncentered_splash_path: str`
>
>`uncentered_splash_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`tile_path: str`
>
>`tile_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`load_screen_path: str`
>
>`load_screen_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`skin_type: str`
>
>`rarity: str`
>
>`is_legacy: bool`
>
>`chroma_path: str`
>
>`chroma_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
>`chromas: List[ChampionSkinChromaData]`
>
>`skin_line: int`
>
>`description: str`

## `ChampionSkinChromaData` <Badge text="Pyot Static" vertical="middle"/>
> `id: int`
>
> `name: str`
>
> `chroma_path: str`
>
> `chroma_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
> `colors: List[str]`
>
> `descriptions: List[ChampionChromaDescriptionsData]`
>
> `rarities: List[ChampionChromaRaritiesData]`

## `ChampionChromaRaritiesData` <Badge text="Pyot Static" vertical="middle"/>
>`region: str`
>
>`description: str`

## `ChampionChromaDescriptionsData` <Badge text="Pyot Static" vertical="middle"/>
>`region: str`
>
>`description: str`

## `ChampionPlayerStyleData` <Badge text="Pyot Static" vertical="middle"/>
>`damage: int`
>
>`durability: int`
>
>`crowd_control: int`
>
>`mobility: int`
>
>`utility: int`

## `ChampionTacticalData` <Badge text="Pyot Static" vertical="middle"/>
>`style: int`
>
>`difficulty: int`
>
>`damage_type: str`

