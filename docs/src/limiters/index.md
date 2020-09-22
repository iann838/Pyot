# Base Limiter

This is the class that all Rate Limiters subclasses.

> ### `get_limit_token(self, server: str, method: str) -> LimitToken` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Process to get limit tokens.

> ### `stream(self, response: Any, server: str, method: str, token: LimitToken)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Stream states to the limiter.

> ### `put_stream(self, fetched: dict, server: str, method: str, token: LimitToken)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Put updated states to backend limiter.

> ### `inmediate_backoff(self, seconds: int, type_: str, server: str, method: str = None)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Inmediate backoff of the limits.

> ### `get_limits(self, server: str, method: str)` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Get limits from backend limiter.

> ### `set_limits(self, server: str, method: str, limits: List[Any])` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Set limits to backend limiter

> ### `validate_bucket(self, server, method, token: LimitToken)` <Badge text="function" type="error" vertical="middle"/>
> Validate token to modify bucket.
