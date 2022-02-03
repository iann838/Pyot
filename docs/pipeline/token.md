# Token

### _class_ PipelineToken

Token class is used among all the stores in the pipeline. Typically generated from `token()` on `PyotCore` objects.

Definitions:

* `__init__`
  - `model`: `str`
    > Name of the pipeline.
  - `server`: `str`
    > Name of the server (region/platform/locale).
  - `method`: `str`
    > Name of the method endpoint.
  - `params`: `Dict[str, Any]`
    > Dict containing the params.
  - `queries`: `Dict[str, Any]`
    > Dict containing the queries params.

* `__hash__` -> `str`
  > Returns the hash of the token.

Attributes:

* `value`: `str`
* `hashval`: `str`
* `model`: `str`
* `server`: `str`
* `method`: `str`
* `params`: `Dict[str, str]`
* `queries`: `Dict[str, Any]`

Methods:

* _staticmethod_ `parse_params` -> `str`
  * `dic`: `Dict`
* _staticmethod_ `parse_queries` -> `str`
  * `dic`: `Dict`
* _classmethod_ `load` -> `PipelineToken`
  * `dic`: `Dict`
* _method_ `dict` -> `Dict`
