# Error Handler

This argument is available for all the Pyot Store of type <Badge text="Pyot Source" vertical="middle" />

## Basics
Accepts a dictionary of status code to tuple of strategy and strategy arguments.

>#### Syntax: `Mapping[int, Tuple[str, List[int]]]`
> the key is an integer indentifying the status code, the value is a Tuple that has 2 items, the first item is the strategy token and the second item is a list of arguments passed to the strategy. List of token and accepted arguments:
>
> `"T"` (throw on error): `[]` No arguments
>
> `"R"` (retry a set time): `[times: int]` The number of times to retry
>
> `"E"` (exponential backoff): `[initial: int, times: int]` The number of seconds for initial backoff and the max number of times to backoff. Each backoff will raise the backoff time to the power of 2.

The functionality of this argument is to define the strategy to use when a non 200 status code is returned for the request made out to other sources. By passing this will override the default strategy specified in the dictionary. For example:

```python{2,3,4}
"ERROR_HANDLING": {
    404: ("T", []),
    502: ("R", [3]),
    429: ("E", [3, 3]),
}
```
This will override the strategy used for 404 to throw inmediately, 502 to retry 3 times before throwing and 429 to exponentially backoff with a initial backoff of 3 seconds and a max tries of 3 times.

:::tip WARNING
The Riot Games API can give 3 types of 429: `service`, `application` and `method`, the one that can be overridden is the `service` 429, the other 2 types of 429 is handled by the RiotAPI Ratelimiter.
:::

## Default Handler

:::tip INFO
The status code 888 is for identifying unexpected status codes that are not in the list, for example: a 510 will result in a Pyot side 888 for simplicity.
:::

>`400 : ("T", [])`
>
>`401 : ("T", [])`
>
>`404 : ("T", [])`
>
>`403 : ("T", [])`
>
>`408 : ("E", [2, 3])`
>
>`429 : ("E", [2, 3])`
>
>`500 : ("E", [2, 3])`
>
>`502 : ("E", [2, 3])`
>
>`503 : ("E", [2, 3])`
>
>`504 : ("E", [2, 3])`
>
>`888 : ("T", [])`
