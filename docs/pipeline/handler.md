# Handler

Error handlers are used across all service stores for error handling, backoffs and managing request exceptions. The configuration accepts a dictionary of status code mapping to a tuple of strategy arguments.

* Syntax: `Mapping[int, Tuple[str, List[int]]]`

The key is an integer indentifying the status code, the value is a Tuple that has 2 items, the first item is the strategy token and the second item is a list of arguments passed to the strategy. List of tokens and accepted arguments:

* `"T"` (throw on error): `[]` No arguments
* `"R"` (retry a set time): `[times: int]` The number of times to retry
* `"E"` (exponential backoff): `[initial: int, times: int]` The number of seconds for initial backoff and the max number of times to backoff. Each backoff will raise the backoff time to the power of 2.

The functionality of this argument is to define the strategy to use when a non 200 status code is returned for the request made out to other sources. By passing this will override the default strategy specified in the dictionary. For example:

```python{2,3,4}
    # ... Other Stores
        # ... Stores configurations
        "error_handler": {
            404: ("T", []),
            502: ("R", [3]),
            429: ("E", [3, 3]),
        }
        # ...
```

This will override the strategy used for 404 to throw inmediately, 502 to retry 3 times before throwing and 429 to exponentially backoff with a initial backoff of 3 seconds and a max tries of 3 times.

{% hint style='info' %}
The Riot Games API can give 3 types of 429: `service`, `application` and `method`, the one that can be overridden is only the `service` 429, the other 2 types of 429 is handled by the rate limiters.
{% endhint %}

## Default Handler

{% hint style='info' %}
Code 800 is for unidentified status codes that are not in the list, for example: a 510 will result in a 800 containing the error code.
{% endhint %}

* `204 : ("T", [])`
* `400 : ("T", [])`
* `401 : ("T", [])`
* `403 : ("T", [])`
* `404 : ("T", [])`
* `405 : ("T", [])`
* `408 : ("E", [3, 3])`
* `429 : ("E", [3, 3])`
* `500 : ("E", [3, 3])`
* `502 : ("E", [3, 3])`
* `503 : ("E", [3, 3])`
* `504 : ("E", [3, 3])`
* `602 : ("R", [2])`
* `800 : ("T", [])`
