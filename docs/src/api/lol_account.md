# Account
Model: League of Legends

## `Account` <Badge text="Pyot Core" vertical="middle"/>
>`puuid: str = None`<Badge text="param" type="warning" vertical="middle"/>
>
>`name: str = None`<Badge text="param" type="warning" vertical="middle"/>
>
>`tag: str = None`<Badge text="param" type="warning" vertical="middle"/>
>
>`region: str = None`<Badge text="param" type="warning" vertical="middle"/>

>`"account_v1_by_puuid": ["puuid"]`<Badge text="endpoint" type="error" vertical="middle"/>
>
>`"account_v1_by_riot_id": ["name", "tag"]`<Badge text="endpoint" type="error" vertical="middle"/>
>

> `puuid`: `str`
>
> `name`: `str`
>
> `tag`: `str`
>

## `ActivePlatform` <Badge text="Pyot Core" vertical="middle"/>
> `puuid: str = None` <Badge text="param" type="warning" vertical="middle"/>
> 
> `game: str = None` <Badge text="param" type="warning" vertical="middle"/>
> 
> `region: str = None` <Badge text="param" type="warning" vertical="middle"/>

> `"account_v1_active_shard": ["game", "puuid"]` <Badge text="endpoint" type="error" vertical="middle"/>

>`puuid: str`
>
>`game: str`
>
>`platform_id: str`
>