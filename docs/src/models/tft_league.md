# League
Model: Teamfight Tactics

## `League` <Badge text="Pyot Core" vertical="middle"/>
>`id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"league_v1_league_by_league_id": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`tier: str`
>
>`id: str`
>
>`queue: str`
>
>`name: str`
>
>`entries: List[LeagueEntryData]`

## `ChallengerLeague` <Badge text="Pyot Core" vertical="middle"/>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"league_v1_challenger_league": []` <Badge text="endpoint" type="error" vertical="middle"/>

>`queue: str`
>
>`id: str`
>
>`tier: str`
>
>`id: str`
>
>`queue: str`
>
>`name: str`
>
>`entries: List[LeagueEntryData]`

>`league -> "League"` <Badge text="bridge" type="error" vertical="middle"/>

## `GrandmasterLeague` <Badge text="Pyot Core" vertical="middle"/>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"league_v1_grandmaster_league": []` <Badge text="endpoint" type="error" vertical="middle"/>

>`queue: str`
>
>`id: str`
>
>`tier: str`
>
>`id: str`
>
>`queue: str`
>
>`name: str`
>
>`entries: List[LeagueEntryData]`

>`league -> "League"` <Badge text="bridge" type="error" vertical="middle"/>

## `MasterLeague` <Badge text="Pyot Core" vertical="middle"/>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"league_v1_master_league": []` <Badge text="endpoint" type="error" vertical="middle"/>

>`queue: str`
>
>`id: str`
>
>`tier: str`
>
>`id: str`
>
>`queue: str`
>
>`name: str`
>
>`entries: List[LeagueEntryData]`

>`league -> "League"` <Badge text="bridge" type="error" vertical="middle"/>

## `DivisionLeague` <Badge text="Pyot Core" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`division: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`tier: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`page: int = None` <Badge text="query" type="error" vertical="middle"/>

>`"league_v1_entries_by_division": ["tier", "division"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`queue: str`
>
>`division: str`
>
>`tier: str`
>
>`entries: List[SummonerLeagueEntryData]` <Badge text="Iterator" type="warning" vertical="middle"/>


## `SummonerLeague` <Badge text="Pyot Core" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`summoner_id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"league_v1_summoner_entries": ["summoner_id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`summoner_id: str`
>
>`entries: List[SummonerLeagueEntryData]` <Badge text="Iterator" type="warning" vertical="middle"/>

>`summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>

## `SummonerLeagueEntryData` <Badge text="Pyot Static" vertical="middle"/>
>`league_id: str`
>
>`queue: str`
>
>`tier: str`

>`league -> "League"` <Badge text="bridge" type="error" vertical="middle"/>

## `LeagueEntryData` <Badge text="Pyot Static" vertical="middle"/>
>`summoner_id: str`
>
>`summoner_name: str`
>
>`league_points: int`
>
>`rank: str`
>
>`wins: int`
>
>`losses: int`
>
>`veteran: bool`
>
>`inactive: bool`
>
>`fresh_blood: bool`
>
>`hot_streak: bool`
>
>`mini_series: MiniSeriesData`

>`summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>

## `MiniSeriesData` <Badge text="Pyot Static" vertical="middle"/>
>`target: int`
>
>`wins: int`
>
>`losses: int`
>
>`progress: str`
