# Spectator
Model: League of Legends


## `CurrentGame` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`summoner_id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"spectator_v4_current_game": ["summoner_id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`id: int`
>
>`type: str`
>
>`mode: str`
>
>`start_millis: int`
>
>`length_secs: int`
>
>`duration: timedelta`
>
>`map_id: int`
>
>`platform: str`
>
>`queue: int`
>
>`observers_key: str`
>
>`summoner_id: str`
>
>`teams: List[CurrentGameTeamData]`
>
>`banned_champions: List[CurrentGameBansData]` <Badge text="property" type="error" vertical="middle"/>
>
>`participants: List[CurrentGameParticipantData]` <Badge text="property" type="error" vertical="middle"/>
>
>`blue_team: CurrentGameTeamData` <Badge text="property" type="error" vertical="middle"/>
>
>`red_team: CurrentGameTeamData` <Badge text="property" type="error" vertical="middle"/>

> #### `roleidentification()` <Badge text="extension" type="error" vertical="middle"/>
> Executes `roleidentification.getroles()` using raw match and the returned champion roles from `roleidentification.pull_data()` (This data is rotated every 3 hours if task is long lived, missing keys from data will be handled aswell), injects the returned position to `teams[].participants[].timeline.position` attribute and return the original response in a dict based on team ids.

>`summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>

## `FeaturedGames` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"spectator_v4_featured_games": []` <Badge text="endpoint" type="error" vertical="middle"/>

>`games: List[FeaturedGameData]` <Badge text="Iterator" type="warning" vertical="middle"/>
>
>`refresh_interval_secs: int`
>
>`refresh_interval: timedelta`

## `FeaturedGameData` <Badge text="Pyot Static" vertical="middle"/>
>`id: int`
>
>`type: str`
>
>`mode: str`
>
>`start_millis: int`
>
>`length_secs: int`
>
>`creation: datetime`
>
>`duration: timedelta`
>
>`map_id: int`
>
>`platform: str`
>
>`queue: int`
>
>`observers_key: str`
>
>`teams: List[FeaturedGameTeamData]`
>
>`banned_champions: List[CurrentGameBansData]` <Badge text="property" type="error" vertical="middle"/>
>
>`participants: List[FeaturedGameParticipantData]` <Badge text="property" type="error" vertical="middle"/>
>
>`blue_team: FeaturedGameTeamData` <Badge text="property" type="error" vertical="middle"/>
>
>`red_team: FeaturedGameTeamData` <Badge text="property" type="error" vertical="middle"/>

> #### `roleidentification()` <Badge text="extension" type="error" vertical="middle"/>
> Executes `roleidentification.getroles()` using raw match and the returned champion roles from `roleidentification.pull_data()` (This data is rotated every 3 hours if task is long lived, missing keys from data will be handled aswell), injects the returned position to `teams[].participants[].timeline.position` attribute and return the original response in a dict based on team ids.

## `CurrentGameTeamData` <Badge text="Pyot Static" vertical="middle"/>
>`id: int`
>
>`bans: List[CurrentGameBansData]`
>
>`participants: List[CurrentGameParticipantData]`

## `FeaturedGameTeamData` <Badge text="Pyot Static" vertical="middle"/>
>`id: int`
>
>`bans: List[CurrentGameBansData]`
>
>`participants: List[FeaturedGameParticipantData]`

## `CurrentGameParticipantData` <Badge text="Pyot Static" vertical="middle"/>
>`team_id: int`
>
>`champion_id: int`
>
>`profile_icon_id: int`
>
>`is_bot: bool`
>
>`summoner_name: str`
>
>`summoner_id: str`
>
>`spell_ids: List[int]`
>
>`rune_ids: List[int]`
>
>`rune_main_style: int`
>
>`rune_sub_style: int`
>
>`game_customization_objects: List[CurrentGameParticipantCustomizationData]`

>`summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`champion -> "Champion"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`meraki_champion -> "MerakiChampion"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`profile_icon -> "ProfileIcon"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`runes -> List["Rune"]` <Badge text="bridge" type="error" vertical="middle"/>
>
>`spells -> List["Spell"]` <Badge text="bridge" type="error" vertical="middle"/>

## `CurrentGameParticipantCustomizationData` <Badge text="Pyot Static" vertical="middle"/>
>`category: str`
>
>`content: str`

## `FeaturedGameParticipantData` <Badge text="Pyot Static" vertical="middle"/>
>`team_id: int`
>
>`champion_id: int`
>
>`profile_icon_id: int`
>
>`is_bot: bool`
>
>`summoner_name: str`
>
>`spell_ids: List[int]`

>`summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`champion -> "Champion"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`meraki_champion -> "MerakiChampion"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`profile_icon -> "ProfileIcon"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`spells -> List["Spell"]` <Badge text="bridge" type="error" vertical="middle"/>

## `CurrentGameBansData` <Badge text="Pyot Static" vertical="middle"/>
>`pick_turn: int`
>
>`champion_id: int`
>
>`team_id: int`

>`champion -> "Champion"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`meraki_champion -> "MerakiChampion"` <Badge text="bridge" type="error" vertical="middle"/>
