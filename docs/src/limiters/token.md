# Token

Token used for Rate Limiting.

## `LimitToken`

Limit Token on limiting.

> ### `__init__(_token: List[int] = field(default_factory=list), flag_app: bool = False, flag_method: bool = False)`
> Creates a limit token.
> - `_token` <Badge text="param" type="warning" vertical="middle"/> -> List[int]: List of limits sub tokens.
> - `flag_app` <Badge text="param" type="warning" vertical="middle"/> -> bool: Flag for the app limit.
> - `flag_method` <Badge text="param" type="warning" vertical="middle"/> -> bool: Flag for the method limit.

> ### `append(val: int)` <Badge text="function" type="error" vertical="middle"/>
> Append a subtoken.
> - `val` <Badge text="param" type="warning" vertical="middle"/> -> int: Subtoken to append

> ### `run_or_wait()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Decides to wait or allow the request.

> ### `max` <Badge text="property" type="error" vertical="middle"/>
> Return the highest subtoken
