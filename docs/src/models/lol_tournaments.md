# Tournaments

Model: League of Legends

## `TournamentProvider` <Badge text="Pyot Core" vertical="middle"/> <Badge text="POST" vertical="middle"/>
> `region: str = None` <Badge text="param" type="warning" vertical="middle"/>

> `"tournament_v4_providers": []` <Badge text="endpoint" type="error" vertical="middle"/>

> `region: str` <Badge text="body" type="error" vertical="middle"/>
>
> `url: str` <Badge text="body" type="error" vertical="middle"/>

> `id: int`
>
> `region: str`

## `TournamentStubProvider` <Badge text="Pyot Core" vertical="middle"/> <Badge text="POST" vertical="middle"/>
> `"tournament_stub_v4_providers": []` <Badge text="endpoint" type="error" vertical="middle"/>

> **_All variables and parameters inherited from TournamentProvider._**

## `Tournament` <Badge text="Pyot Core" vertical="middle"/> <Badge text="POST" vertical="middle"/>
> `region: str = None` <Badge text="param" type="warning" vertical="middle"/>

> `"tournament_v4_tournaments": []` <Badge text="endpoint" type="error" vertical="middle"/>

> `name: str` <Badge text="body" type="error" vertical="middle"/>
>
> `provider_id: int` <Badge text="body" type="error" vertical="middle"/>

> `id: int`
>
> `region: str`

## `TournamentStub` <Badge text="Pyot Core" vertical="middle"/> <Badge text="POST" vertical="middle"/>
> `"tournament_stub_v4_tournaments": []` <Badge text="endpoint" type="error" vertical="middle"/>

> **_All variables and parameters inherited from Tournament._**

## `TournamentLobbyEvents` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
> `code: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
> `region: str = None` <Badge text="param" type="warning" vertical="middle"/>

> `"tournament_v4_lobby_events": ["code"]` <Badge text="endpoint" type="error" vertical="middle"/>

> `events: List[TournamentLobbyEventData]`
>
> `region: str`

## `TournamentStubLobbyEvents` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
> `"tournament_stub_v4_lobby_events": ["code"]` <Badge text="endpoint" type="error" vertical="middle"/>

> **_All variables and parameters inherited from TournamentLobbyEvents._**

## `TournamentCode` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/> <Badge text="PUT" vertical="middle"/>
> `code: int = None` <Badge text="param" type="warning" vertical="middle"/>
>
> `region: str = None` <Badge text="param" type="warning" vertical="middle"/>

> `"tournament_v4_codes_by_code": ["code"]` <Badge text="endpoint" type="error" vertical="middle"/>

> `map_type: str` <Badge text="body" type="error" vertical="middle"/>
>
> `pick_type: str` <Badge text="body" type="error" vertical="middle"/>
>
> `spectator_type: str` <Badge text="body" type="error" vertical="middle"/>
>
> `allowed_summoner_ids: List[str] = None` <Badge text="body" type="error" vertical="middle"/>

> `code: str`
>
> `spectators: str`
>
> `lobby_name: str`
>
> `meta_data: str`
>
> `password: str`
>
> `team_size: int`
>
> `provider_id: int`
>
> `pick_type: str`
>
> `tournament_id: int`
>
> `id: int`
>
> `map: str`
>
> `hosted_region: str`
>
> `summoner_ids: List[str]`

## `TournamentCodes` <Badge text="Pyot Core" vertical="middle"/> <Badge text="POST" vertical="middle"/>
>`region: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"tournament_v4_codes": []` <Badge text="endpoint" type="error" vertical="middle"/>

>`tournament_id: int` <Badge text="query" type="error" vertical="middle"/>
>
>`count: int = None` <Badge text="query" type="error" vertical="middle"/>

>`map_type: str` <Badge text="body" type="error" vertical="middle"/>
>
>`pick_type: str` <Badge text="body" type="error" vertical="middle"/>
>
>`team_size: int` <Badge text="body" type="error" vertical="middle"/>
>
>`spectator_type: str` <Badge text="body" type="error" vertical="middle"/>
>
>`allowed_summoner_ids: List[str] = None` <Badge text="body" type="error" vertical="middle"/>
>
>`metadata: str = None` <Badge text="body" type="error" vertical="middle"/>

>`codes: List[str]`
>
>`region: str`

>`tournament_codes -> List[TournamentCode]` <Badge text="bridge" type="error" vertical="middle"/>
