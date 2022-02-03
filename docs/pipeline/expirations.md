# Expirations

Expirations are used across all cache stores for managing expiration of cached objects. The configuration accepts a dictionary of endpoint key mapping to a timedelta object or number of seconds.

By configuring this argument, it overrides the default endpoints expirations. For example:

```python{2,3}
"expirations": {
    "summoner_v4_by_name": 120,
    "league_v4_challenger_league": 600, # or timedelta(minutes=10)
}
```

This will override the `summoner_v4_by_name` endpoint to cache 2 minutes, and `league_v4_challenger_league` to cache for 10 minutes, and leaving the rest of the default expirations untouched.

## Default Expiration

Global models (e.g. `riot`) will be available to all pipelines, meaning that it is allowed modify endpoints of those models in any pipeline, for example the `"account_v1_by_puuid"` in a pipeline bound to the `val` model and such object called using the `val` pipeline will use such expirations.

{% hint style='info' %}
Only data returned by the `get()` method is sinked through the pipeline, and thus the only ones that can be cached and use expirations.
{% endhint %}

All expirations defaults to `0` (No-Cache). Except for static data sources (e.g. cdragon, meraki, ddragon, etc.) which defaults to `timedelta(minutes=20)` (20 minutes) due to its frequency of data changes and helping to decrease traffic load.
