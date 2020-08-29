# Exceptions

A list of catchable exceptions used by Pyot. Bases at `pyot.core.exceptions`

## Exceptions List

### `GathererCancelled` <Badge type="error" text="Exception" vertical="middle" />
> `f"[Trace: PyotGatherer] All statements of session '{session_id}' are cancelled due to exception: {e}"`


### `SessionNotFound` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 661: Session Not Found, use 'pyot.run' to your coroutines"`


### `NotFound` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 404: Data Not Found"`
        
        
### `ServerError` <Badge type="error" text="Exception" vertical="middle" />
> `500: "Internal Server Error"`
> `502: "Bad Gateway"`
> `503: "Service Unavailable"`
> `504: "Gateway Timeout"`
>
> `f"[Trace: Pyot Pipeline] {code}: {self.messages[code]}"`
        

### `RateLimited` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 429: Rate limit Exceeded"`


### `Forbidden` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 403: Access Forbidden"`


### `Unauthorized` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 401: Access Unauthorized"`


### `BadRequest` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 400: Bad Request"`


### `Timeout` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 408: Timeout Connection"`


### `UnidentifiedResponse` <Badge type="error" text="Exception" vertical="middle" />
> `f"[Trace: Pyot Pipeline] {code}: Unidentified Response {code}"`


## Example Usage
```python
from pyot.core.exceptions import NotFound

try:
    # ...
except (NotFound):
    # do something
```