# Clash
Model: League of Legends

## `ClashTournament` <Badge text="Pyot Core" vertical="middle"/>
>`id: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`team_id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"clash_v1_tournaments_by_team_id": ["team_id"]` <Badge text="endpoint" type="error" vertical="middle"/>
>
>`"clash_v1_toutnaments_by_tournament_id": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`team_id: str`
>
>`id: int`
>
>`theme_id: int`
>
>`name_key: str`
>
>`name_key_secondary: str`
>
>`schedule: List[ClashTournamentPhaseData]`

>`team -> "ClashTeam"` <Badge text="bridge" type="error" vertical="middle"/>

## `ClashTournaments` <Badge text="Pyot Core" vertical="middle"/> <Badge text="Iterable" type="warning" vertical="middle"/>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"clash_v1_tournaments_all": []` <Badge text="endpoint" type="error" vertical="middle"/>

>`tournaments: List[ClashTournamentData]` <Badge text="Iterator" type="warning" vertical="middle"/>

## `ClashTeam` <Badge text="Pyot Core" vertical="middle"/>
>`id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"clash_v1_teams": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`id: str`
>
>`tournament_id: int`
>
>`name: str`
>
>`icon_id: int`
>
>`tier: int`
>
>`captain_summoner_id: str`
>
>`abbreviation: str`
>
>`players: List[ClashPlayerData]`

>`captain -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`tournament -> "ClashTournament"` <Badge text="bridge" type="error" vertical="middle"/>

## `ClashPlayers` <Badge text="Pyot Core" vertical="middle"/>
>`summoner_id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"clash_v1_players": ["summoner_id"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`summoner_id: str`
>
>`players: List[ClashPlayerData]`

>`summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>

## `ClashTournamentData` <Badge text="Pyot Static" vertical="middle"/>
>`id: int`
>
>`theme_id: int`
>
>`name_key: str`
>
>`name_key_secondary: str`
>
>`schedule: List[ClashTournamentPhaseData]`

## `ClashTournamentPhaseData` <Badge text="Pyot Static" vertical="middle"/>
>`id: int`
>
>`registration_time: datetime`
>
>`start_time: datetime`
>
>`cancelled: bool`

## `ClashPlayerData` <Badge text="Pyot Static" vertical="middle"/>
>`summoner_id: str`
>
>`team_id: str`
>
>`position: str`
>
>`role: str`

>`summoner -> "Summoner"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`team -> "ClashTeam"` <Badge text="bridge" type="error" vertical="middle"/>
