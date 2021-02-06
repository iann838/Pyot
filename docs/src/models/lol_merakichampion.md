# Meraki Champion
Model: League of Legends

## `MerakiChampion` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`id: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`key: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`name: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"meraki_champion_by_key": ["key"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`id: int`
>
>`key: str`
>
>`name: str`
>
>`title: str`
>
>`full_name: str`
>
>`icon: str`
>
>`resource: str`
>
>`attack_type: str`
>
>`adaptive_type: str`
>
>`stats: MerakiChampionStatData`
>
>`roles: List[str]`
>
>`attribute_ratings: MerakiChampionAttributeRatingData`
>
>`abilities: MerakiChampionAbilityData`
>
>`release_date: str`
>
>`release_patch: str`
>
>`patch_last_changed: str`
>
>`price: MerakiChampionPriceData`
>
>`lore: str`
>
>`skins: List[MerakiChampionSkinData]`

>`champion -> "Champion"` <Badge text="bridge" type="error" vertical="middle"/>

## `MerakiChampionStatData` <Badge text="Pyot Static" vertical="middle"/>
>`health: MerakiChampionStatDetailData`
>
>`health_regen: MerakiChampionStatDetailData`
>
>`mana: MerakiChampionStatDetailData`
>
>`mana_regen: MerakiChampionStatDetailData`
>
>`armor: MerakiChampionStatDetailData`
>
>`magic_resistance: MerakiChampionStatDetailData`
>
>`attack_damage: MerakiChampionStatDetailData`
>
>`movespeed: MerakiChampionStatDetailData`
>
>`acquisition_radius: MerakiChampionStatDetailData`
>
>`selection_radius: MerakiChampionStatDetailData`
>
>`pathing_radius: MerakiChampionStatDetailData`
>
>`gameplay_radius: MerakiChampionStatDetailData`
>
>`critical_strike_damage: MerakiChampionStatDetailData`
>
>`critical_strike_damage_modifier: MerakiChampionStatDetailData`
>
>`attack_speed: MerakiChampionStatDetailData`
>
>`attack_speed_ratio: MerakiChampionStatDetailData`
>
>`attack_cast_time: MerakiChampionStatDetailData`
>
>`attack_total_time: MerakiChampionStatDetailData`
>
>`attack_delay_offset: MerakiChampionStatDetailData`
>
>`attack_range: MerakiChampionStatDetailData`
>
>`aram_damage_taken: MerakiChampionStatDetailData`
>
>`aram_damage_dealt: MerakiChampionStatDetailData`
>
>`aram_healing: MerakiChampionStatDetailData`
>
>`aram_shielding: MerakiChampionStatDetailData`
>
>`urf_damage_taken: MerakiChampionStatDetailData`
>
>`urf_damage_dealt: MerakiChampionStatDetailData`
>
>`urf_healing: MerakiChampionStatDetailData`
>
>`urf_shielding: MerakiChampionStatDetailData`

## `MerakiChampionStatDetailData` <Badge text="Pyot Static" vertical="middle"/>
>`flat: int`
>
>`percent: int`
>
>`per_level: int`
>
>`percent_per_level: int`

## `MerakiChampionAbilityData` <Badge text="Pyot Static" vertical="middle"/>
>`p: List[MerakiChampionSpellData]`
>
>`q: List[MerakiChampionSpellData]`
>
>`w: List[MerakiChampionSpellData]`
>
>`e: List[MerakiChampionSpellData]`
>
>`r: List[MerakiChampionSpellData]`

## `MerakiChampionSpellData` <Badge text="Pyot Static" vertical="middle"/>
>`name: str`
>
>`icon: str`
>
>`effects: List[MerakiChampionSpellEffectData]`
>
>`cost: MerakiChampionSpellAttrData`
>
>`cooldown: MerakiChampionSpellAttrData`
>
>`targeting: str`
>
>`affects: str`
>
>`spellshieldable: str`
>
>`resource: str`
>
>`damage_type: str`
>
>`spell_effects: str`
>
>`projectile: str`
>
>`on_hit_effects: str`
>
>`occurrence: int`
>
>`notes: str`
>
>`blurb: str`
>
>`missile_speed: str`
>
>`recharge_rate: str`
>
>`collision_radius: str`
>
>`tether_radius: str`
>
>`on_target_cd_static: str`
>
>`inner_radius: str`
>
>`speed: str`
>
>`width: str`
>
>`angle: str`
>
>`cast_time: str`
>
>`effect_radius: str`
>
>`target_range: str`

## `MerakiChampionSpellEffectData` <Badge text="Pyot Static" vertical="middle"/>
>`description: str`
>
>`leveling: List[MerakiChampionSpellAttrData]`

## `MerakiChampionSpellAttrData` <Badge text="Pyot Static" vertical="middle"/>
>`attribute: str`
>
>`modifiers: List[MerakiChampionSpellModifierData]`
>
>`affected_by_cdr: bool`

## `MerakiChampionSpellModifierData` <Badge text="Pyot Static" vertical="middle"/>
>`values: List[int]`
>
>`units: List[str]`

## `MerakiChampionAttributeRatingData` <Badge text="Pyot Static" vertical="middle"/>
>`damage: int`
>
>`toughness: int`
>
>`control: int`
>
>`mobility: int`
>
>`utility: int`
>
>`ability_reliance: int`
>
>`attack: int`
>
>`defense: int`
>
>`magic: int`
>
>`difficulty: int`

## `MerakiChampionPriceData` <Badge text="Pyot Static" vertical="middle"/>
>`blue_essence: int`
>
>`rp: int`
>
>`sale_rp: int`

## `MerakiChampionSkinData` <Badge text="Pyot Static" vertical="middle"/>
> `name: str`
>
> `id: int`
>
> `is_base: bool`
>
> `availability: str`
>
> `format_name: str`
>
> `loot_eligible: bool`
>
> `cost: int`
>
> `sale: int`
>
> `distribution: str`
>
> `rarity: str`
>
> `chromas: List[MerakiChampionSkinChromaData]`
>
> `lore: str`
>
> `release: str`
>
> `set: List[str]`
>
> `splash_path: str`
>
> `splash_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
> `uncentered_splash_path: str`
>
> `uncentered_splash_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
> `tile_path: str`
>
> `tile_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
> `load_screen_path: str`
>
> `load_screen_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
> `load_screen_vintage_path: str`
>
> `load_screen_vintage_abspath: str` <Badge text="lazy" type="error" vertical="middle"/>
>
> `new_effects: bool`
>
> `new_animations: bool`
>
> `new_recall: bool`
>
> `new_voice: bool`
>
> `new_quotes: bool`
>
> `voice_actor: List[str]`
>
> `splash_artist: List[str]`

## `MerakiChampionSkinChromaData` <Badge text="Pyot Static" vertical="middle"/>
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
> `descriptions: List[MerakiChampionChromaDescriptionsData]`
>
> `rarities: List[MerakiChampionChromaRaritiesData]`
>

## `MerakiChampionChromaDescriptionsData` <Badge text="Pyot Static" vertical="middle"/>
> `region: str`
>
> `description: str`
>

## `MerakiChampionChromaRaritiesData` <Badge text="Pyot Static" vertical="middle"/>
> `region: str`
>
> `description: str`
>
