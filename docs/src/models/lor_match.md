# Match

Model: Legends of Runeterra


## `Match` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
> `id: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
> `region: str = None` <Badge text="param" type="warning" vertical="middle"/>

> `"match_v1_match": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

> `id: int`
>
> `metadata: MatchMetaData`
>
> `info: MatchInfoData`

## `MatchHistory` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`puuid: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`region: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"match_v1_matchlist": ["puuid"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`ids: List[str]`
>
>`puuid: str`
>
>`matches: List[Match]` <Badge text="Iterator" type="warning" vertical="middle"/>

>`account -> "Account"` <Badge text="bridge" type="error" vertical="middle"/>


## `MatchInfoData` <Badge text="Pyot Static" vertical="middle"/>
> `mode: str` (Legal values: Constructed, Expeditions, Tutorial)
>
> `type: str` (Legal values: Ranked, Normal, AI, Tutorial, VanillaTrial, Singleton, StandardGauntlet)
>
> `start_strftime: str`
>
> `creation: datetime`
>
> `version: str`
>
> `players: List[MatchPlayerData]`
>
> `total_turn_count: int`


## `MatchMetaData` <Badge text="Pyot Static" vertical="middle"/>
>`data_version: str`
>
>`match_id: str`
>
>`participant_puuids: List[str]`

> `participants -> List["Account"]` <Badge text="bridge" type="error" vertical="middle"/>

## `MatchPlayerData` <Badge text="Pyot Static" vertical="middle"/>
>`puuid: str`
>
>`deck_id: str`
>
>`deck_code: str`
>
>`factions: List[str]`
>
>`game_outcome: str`
>
>`order_of_play: int`
>
>`win: bool`

>`account -> "Account"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`deck -> "Deck"` <Badge text="bridge" type="error" vertical="middle"/>
