# Summoner
Model: Teamfight Tactics

## `Summoner` <Badge text="Pyot Core" vertical="middle"/> <Badge text="GET" vertical="middle"/>
>`id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`account_id: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`name: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`puuid: str = None` <Badge text="param" type="warning" vertical="middle"/>
>
>`platform: str = None` <Badge text="param" type="warning" vertical="middle"/>

>`"summoner_v1_by_name": ["name"]` <Badge text="endpoint" type="error" vertical="middle"/>
>
>`"summoner_v1_by_id": ["id"]` <Badge text="endpoint" type="error" vertical="middle"/>
>
>`"summoner_v1_by_account_id": ["account_id"]` <Badge text="endpoint" type="error" vertical="middle"/>
>
>`"summoner_v1_by_puuid": ["puuid"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`name: str`
>
>`id: str`
>
>`account_id: str`
>
>`level: int`
>
>`puuid: str`
>
>`profile_icon_id: int`
>
>`revision_date_millis: int`
>
>`revision_date: datetime`

>`league_entries -> "SummonerLeague"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`third_party_code -> "ThirdPartyCode"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`profile_icon -> "ProfileIcon"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`account -> "Account"` <Badge text="bridge" type="error" vertical="middle"/>
>
>`match_history -> "MatchHistory"` <Badge text="bridge" type="error" vertical="middle"/>