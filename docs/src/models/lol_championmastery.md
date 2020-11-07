# Champion Mastery
Model: League of Legends

## `ChampionMasteries` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`summoner_id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"champion_mastery_v4_all_mastery": ["summoner_id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`summoner_id: str`
>
>`masteries: List[ChampionMastery]` <Badge text="Iterator" type="warning" vertical="middle"/>
>
>`total_score: int`

>` summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>

## `ChampionMastery` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`summoner_id: str = None`<Badge text="param" type="warning" vertical="middle"/>
>
>`champion_id: int = None`<Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None`<Badge text="param" type="warning" vertical="middle"/>

>`"champion_mastery_v4_by_champion_id": ["summoner_id", "champion_id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`champion_id: int`
>
>`champion_level: int`
>
>`champion_points: int`
>
>`last_play_time: datetime`
>
>`champion_points_since_last_level: int`
>
>`champion_points_until_next_level: int`
>
>`chest_granted: bool`
>
>`tokens_earned: int`
>
>`summoner_id: str`

>`summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`champion -> "Champion"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`meraki_champion -> "MerakiChampion"` <Badge text="bridge" type="error" vertical="middle"/>