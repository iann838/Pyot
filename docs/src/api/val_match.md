# Match
Model: Valorant

## `Match` <Badge text="Pyot Core" vertical="middle"/>
>`id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"match_v1_match": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`id: str`
>
>`info: MatchInfoData`
>
>`players: List[MatchPlayerData]`
>
>`teams: List[MatchTeamData]`
>
>`round_results: List[MatchRoundResultData]`

## `MatchHistory` <Badge text="Pyot Core" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`puuid: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"match_v1_matchlist": ["puuid"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`puuid: str`
>
>`history: List[MatchHistoryData]`

>`account -> "Account"` <Badge text="bridge" type="error" vertical="middle"/>

## `MatchHistoryData` <Badge text="Pyot Static" vertical="middle"/>
>`id: str`
>
>`creation: datetime`
>
>`team_id: str`

>`match -> "Match"` <Badge text="bridge" type="error" vertical="middle"/>

## `MatchInfoData` <Badge text="Pyot Static" vertical="middle"/>
>`id: str`
>
>`map_id: str`
>
>`duration: timedelta`
>
>`creation: datetime`
>
>`provisioning_flow_id: str`
>
>`is_completed: bool`
>
>`custom_game_name: str`
>
>`queue_id: str`
>
>`game_mode: str`
>
>`is_ranked: bool`
>
>`season_id: str`

## `MatchRoundResultData` <Badge text="Pyot Static" vertical="middle"/>
>`round_num: int`
>
>`round_result: str`
>
>`round_ceremony: str`
>
>`winning_team: str`
>
>`bomb_planter_puuid: str`
>
>`bomb_defuser_puuid: str`
>
>`plant_round_time: timedelta`
>
>`plant_player_locations: List[MatchPlayerLocationData]`
>
>`plant_location: MatchLocationData`
>
>`plant_site: str`
>
>`defuse_round_time: timedelta`
>
>`defuse_player_locations: List[MatchPlayerLocationData]`
>
>`defuse_location: MatchLocationData`
>
>`player_stats: List[MatchPlayerRoundStatData]`
>
>`round_result_code: str`

>`bomb_planter -> "Account"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`bomb_defuser -> "Account"` <Badge text="bridge" type="error" vertical="middle"/>

## `MatchPlayerRoundStatData` <Badge text="Pyot Static" vertical="middle"/>
>`puuid: str`
>
>`kills: List[MatchPlayerKillData]`
>
>`damage: List[MatchPlayerDamageData]`
>
>`score: int`
>
>`economy: MatchPlayerEconomyData`
>
>`ability: MatchPlayerAbilityData`

## `MatchPlayerAbilityData` <Badge text="Pyot Static" vertical="middle"/>
>`grenade_effects: int`
>
>`ability1_effects: int`
>
>`ability2_effects: int`
>
>`ultimate_effects: int`

## `MatchPlayerDamageData` <Badge text="Pyot Static" vertical="middle"/>
>`receiver: str`
>
>`damage: int`
>
>`legshots: int`
>
>`bodyshots: int`
>
>`headshots: int`

## `MatchPlayerEconomyData` <Badge text="Pyot Static" vertical="middle"/>
>`loadout_value: int`
>
>`weapon: str`
>
>`armor: str`
>
>`remaining: int`
>
>`spent: int`

## `MatchPlayerKillData` <Badge text="Pyot Static" vertical="middle"/>
>`game_duration: timedelta`
>
>`round_duration: timedelta`
>
>`killer_puuid: str`
>
>`victim_puuid: str`
>
>`victim_location: MatchLocationData	`
>
>`assistant_puuids: List[str]`
>
>`player_locations: List[MatchPlayerLocationData]`
>
>`finishing_damage: MatchPlayerFinishingDamageData`

>`killer -> "Account"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`victim -> "Account"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`assistants -> List["Account"]` <Badge text="bridge" type="error" vertical="middle"/>

## `MatchPlayerFinishingDamageData` <Badge text="Pyot Static" vertical="middle"/>
>`damage_type: str`
>
>`damage_item: str`
>
>`is_secondary_fire_mode: bool`

## `MatchPlayerLocationData` <Badge text="Pyot Static" vertical="middle"/>
>`puuid: str`
>
>`view_radians: float`
>
>`location: MatchLocationData`

## `MatchLocationData` <Badge text="Pyot Static" vertical="middle"/>
>`x: int`
>
>`y: int`

## `MatchTeamData` <Badge text="Pyot Static" vertical="middle"/>
>`id: str`
>
>`won: bool`
>
>`rounds_played: int`
>
>`rounds_won: int`

## `MatchPlayerData` <Badge text="Pyot Static" vertical="middle"/>
>`puuid: str`
>
>`team_id: str`
>
>`party_id: str`
>
>`character_id: str`
>
>`stats: MatchPlayerStatData`
>
>`competitive_tier: int`
>
>`player_card: str`
>
>`player_title: str`

>`account -> "Account"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`active_platform -> "ActivePlatform"` <Badge text="bridge" type="error" vertical="middle"/>

## `MatchPlayerStatData` <Badge text="Pyot Static" vertical="middle"/>
>`score: int`
>
>`rounds_played: int`
>
>`kills: int`
>
>`deaths: int`
>
>`assists: int`
>
>`playtime: timedelta`
>
>`ability_casts: MatchPlayerAbilityCastData`

## `MatchPlayerAbilityCastData` <Badge text="Pyot Static" vertical="middle"/>
>`grenade_casts: int`
>
>`ability1_casts: int`
>
>`ability2_casts: int`
>
>`ultimate_casts: int`





