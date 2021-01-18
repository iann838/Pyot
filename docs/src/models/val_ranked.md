# Ranked

Model: VALORANT

## `Leaderboard` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`act_id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`size: int = None` <Badge text="query" type="error" vertical="middle"/>
>
>`start_index: int = None` <Badge text="query" type="error" vertical="middle"/>

>`"ranked_v1_leaderboards": ["act_id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`act_id: str`
>
>`total_players: int`
>
>`shard: str`
>
> `players: List[LeaderboardPlayerData]` <Badge text="Iterator" type="warning" vertical="middle"/>

## `LeaderboardPlayerData` <Badge text="Pyot Static" vertical="middle"/>

>`puuid: str`
>
>`game_name: str`
>
>`tag_line: str`
>
>`leaderboard_rank: int`
>
>`ranked_rating: int`
>
>`number_of_wins: int`

>`account -> "Account"` <Badge text="bridge" type="error" vertical="middle"/>
