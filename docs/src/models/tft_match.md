# Match
Model: Teamfight Tactics

## `MatchHistory` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`puuid: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`region: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`count: int = 100000` <Badge text="query" type="error" vertical="middle"/>

>`"match_v1_matchlist": ["puuid"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`matches: List[Match]` <Badge text="Iterator" type="warning" vertical="middle"/>
>
>`ids: List[str]`
>
>`puuid: str`

>`summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>

## `Match` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`region: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"match_v1_match": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`id: str`
>
>`info: MatchInfoData`
>
>`metadata: MatchMetadataData`

## `MatchInfoData` <Badge text="Pyot Static" vertical="middle"/>
>`date_millis: int`
>
>`length_secs: int`
>
>`creation: datetime`
>
>`duration: timedelta`
>
>`variation: str`
>
>`version: str`
>
>`participants: List[MatchInfoParticipantData]`
>
>`queue_id: int`
>
>`tft_set_number: int`

## `MatchMetadataData` <Badge text="Pyot Static" vertical="middle"/>
>`id: str`
>
>`data_version: str`
>
>`participant_puuids: List[str]`

>`participants -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>

## `MatchInfoParticipantData` <Badge text="Pyot Static" vertical="middle"/>
>`companion: MatchInfoCompanionData`
>
>`gold_left: int`
>
>`last_round: int`
>
>`level: int`
>
>`placement: int`
>
>`players_eliminated: int`
>
>`puuid: str`
>
>`time_eliminated_secs: int`
>
>`time_eliminated: timedelta`
>
>`total_damage_to_players: int`
>
>`traits: List[MatchInfoTraitData]`
>
>`units: List[MatchInfoUnitData]`
>
>`_pyot_calculated_platform: str`
>:::warning
>The `_pyot_calculated_platform: str` is created for adding the `platform` value for the `summoner` bridge, it is calculated base on the match id, it _might_ be innacurate, please override the `platform` value after assigning the bridge if this variable yields inacurate data.
>:::

>`summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>

## `MatchInfoUnitData` <Badge text="Pyot Static" vertical="middle"/>
>`item_ids: List[int]`
>
>`champion_key: str`
>
>`name: str`
>
>`chosen: str`
>
>`rarity: int`
>
>`tier: int`

>`items -> List["Item"]` <Badge text="bridge" type="error" vertical="middle"/>
>
>`champion -> "Champion"` <Badge text="bridge" type="error" vertical="middle"/>

## `MatchInfoTraitData` <Badge text="Pyot Static" vertical="middle"/>
>`name: str`
>
>`num_units: int`
>
>`style: int`
>
>`tier_current: int`
>
>`tier_total: int`

>`trait -> "Trait"` <Badge text="bridge" type="error" vertical="middle"/>

## `MatchInfoCompanionData` <Badge text="Pyot Static" vertical="middle"/>
>`content_id: str`
>
>`skin_id: int`
>
>`species: str`
