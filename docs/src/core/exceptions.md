# Exceptions

A list of catchable exceptions used by Pyot. Bases at `pyot.core.exceptions`

## Exceptions List

### `NotFindable` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 600: Pipeline token matching pair not found"`


### `SessionNotFound` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 601: Session Not Found."`


### `DecodeError` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 602: AioHttp took too long to decode the response."`


### `NoContent` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 204: No Content."`


### `NotFound` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 404: Data Not Found"`


### `MethodNotAllowed` <Badge type="error" text="Exception" vertical="middle" />
> `"[Trace: Pyot Pipeline] 405: Method Not Allowed"`

        
### `ServerError` <Badge type="error" text="Exception" vertical="middle" />
> `500: "Internal Server Error"`
> `502: "Bad Gateway"`
> `503: "Service Unavailable"`
> `504: "Gateway Timeout"`
>
> `"[Trace: Pyot Pipeline] {code}: {self.messages[code]}"`
        

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