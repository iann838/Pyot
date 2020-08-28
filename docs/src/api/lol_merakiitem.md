# Meraki Item
Model: League of Legends

## `MerakiItem` <Badge text="Pyot Core" vertical="middle"/>
>`id: int = None` <Badge text="param" type="warning" vertical="middle"/>

>`"meraki_item_by_id": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`name: str`
>
>`id: int`
>
>`tier: int`
>
>`builds_from_ids: List[int]`
>
>`builds_into_ids: List[int]`
>
>`no_effects: bool`
>
>`removed: bool`
>
>`required_champion_key: str`
>
>`required_ally: str`
>
>`icon: str`
>
>`simple_description: str`
>
>`nicknames: List[str]`
>
>`passives: List[MerakiItemPassiveData]`
>
>`active: List[MerakiItemActiveData]`
>
>`stats: MerakiItemStatData`
>
>`shop: MerakiItemShopData`

>`item -> "Item"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`meraki_builds_from -> List["MerakiItem"]` <Badge text="bridge" type="error" vertical="middle"/>
>
>`meraki_builds_into -> List["MerakiItem"]` <Badge text="bridge" type="error" vertical="middle"/>
>
>`builds_from -> List["Item"]` <Badge text="bridge" type="error" vertical="middle"/>
>
>`builds_into -> List["Item"]` <Badge text="bridge" type="error" vertical="middle"/>
>
>`required_champion -> "Champion"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`meraki_required_champion -> "MerakiChampion"` <Badge text="bridge" type="error" vertical="middle"/>

## `MerakiItemPassiveData` <Badge text="Pyot Static" vertical="middle"/>
>`unique: bool`
>
>`name: str`
>
>`effects: str`
>
>`range: int`
>
>`stats: MerakiItemStatData`

## `MerakiItemStatData` <Badge text="Pyot Static" vertical="middle"/>
>`ability_power: MerakiItemStatDetailData`
>
>`armor: MerakiItemStatDetailData`
>
>`armor_penetration: MerakiItemStatDetailData`
>
>`attack_damage: MerakiItemStatDetailData`
>
>`attack_speed: MerakiItemStatDetailData`
>
>`cooldown_reduction: MerakiItemStatDetailData`
>
>`critical_strike_chance: MerakiItemStatDetailData`
>
>`gold_per_10: MerakiItemStatDetailData`
>
>`heal_and_shield_power: MerakiItemStatDetailData`
>
>`health: MerakiItemStatDetailData`
>
>`health_regen: MerakiItemStatDetailData`
>
>`lethality: MerakiItemStatDetailData`
>
>`lifesteal: MerakiItemStatDetailData`
>
>`magic_penetration: MerakiItemStatDetailData`
>
>`magic_resistance: MerakiItemStatDetailData`
>
>`mana: MerakiItemStatDetailData`
>
>`mana_regen: MerakiItemStatDetailData`
>
>`movespeed: MerakiItemStatDetailData`

## `MerakiItemStatDetailData` <Badge text="Pyot Static" vertical="middle"/>
>`flat: int`
>
>`percent: int`
>
>`per_level: int`
>
>`percent_per_level: int`
>
>`percent_base: int`
>
>`percent_bonus: int`

## `MerakiItemActiveData` <Badge text="Pyot Static" vertical="middle"/>
>`unique: bool`
>
>`name: str`
>
>`effects: str`
>
>`range: int`
>
>`cooldown: int`

## `MerakiItemShopData` <Badge text="Pyot Static" vertical="middle"/>
>`prices: MerakiItemShopPriceData`
>
>`purchasable: bool`
>
>`tags: List[str]`

## `MerakiItemShopPriceData` <Badge text="Pyot Static" vertical="middle"/>
>`total: int`
>
>`combined: int`
>
>`sell: int`



