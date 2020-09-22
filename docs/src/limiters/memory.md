# Memory Limiter

Rate limiter based on runtime Python Objects. This Rate Limiter is async safe, thread safe and the fastest available rate limiter. For cross-process safe Rate Limiter please refer to other Limiters.

## Rate Limiter Settings Reference
### Backend: `pyot.limiters.MemoryLimiter`
### Arguments:
> #### `limiting_share: float = 1`
> The amount of rate limits * `limiting_share` to use at most, receives a float between 0 and 1. Defaults to 1.

## Example Usage

```python
{
    "BACKEND": "pyot.stores.RiotAPI",
    "RATE_LIMITER": {
        "BACKEND": "pyot.limiters.MemoryLimiter",
        "LIMITING_SHARE": 1,
    }
}
```
