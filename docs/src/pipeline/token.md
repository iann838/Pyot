# Token

## `PipelineToken`

Token class used among all the stores in the pipeline. Typically generated from `create_token()` from `PyotCore` objects.

> ### `__init__(model: str, server: str, method: str, params: Dict[str, Any], queries: Dict[str, Any])`
> - `model` <Badge text="param" type="warning" vertical="middle"/> -> `str`: Name of the pipeline.
> - `server` <Badge text="param" type="warning" vertical="middle"/> -> `str`: Name of the server (region/platform/locale).
> - `method` <Badge text="param" type="warning" vertical="middle"/> -> `str`: Name of the method endpoint.
> - `params` <Badge text="param" type="warning" vertical="middle"/> -> `Dict[str, Any]`: Dict containing the params.
> - `queries` <Badge text="param" type="warning" vertical="middle"/> -> `Dict[str, Any]`: Dict containing the queries params.

> ### `__hash__(self)`
> Returns the hash of the token.

> ### `stringify` <Badge text="property" type="error" vertical="middle"/>
> Returns the string version of the token.

## `RequestToken`

Token class used to handle request based on configured error handler.

> ### `__init__(tries: int = 0, _raise_at: int = 1, _exception: Any = None, _code: int = 0)`
> - `tries` <Badge text="param" type="warning" vertical="middle"/> -> int: Number of tries attempted.
> - `_raise_at` <Badge text="param" type="warning" vertical="middle"/> -> int: Number of try to raise exception.
> - `_exception` <Badge text="param" type="warning" vertical="middle"/> -> Any: Exception to raise.
> - `_code` <Badge text="param" type="warning" vertical="middle"/> -> int: Status code of the request.

> ### `stream(code: int, how: Tuple, origin: str)`
> Streams the new state to the token.
> - `code` <Badge text="param" type="warning" vertical="middle"/> -> int: Status code of the request.
> - `how` <Badge text="param" type="warning" vertical="middle"/> -> Tuple: Tuple containing the handler configs.
> - `origin` <Badge text="param" type="warning" vertical="middle"/> -> str: Attempted request's pipeline token string.

> ### `run_or_raise()` <Badge text="function" type="error" vertical="middle"/> <Badge text="awaitable" type="error" vertical="middle"/>
> Decide if the the request should be made or raise exception.
