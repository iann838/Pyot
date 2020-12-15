# Store Object

This is the object that all Pyot stores subclasses.

```python
class StoreObject:

    def _log_template(self, token):
        return f"<{token.server.upper()} {token.method}: {' '.join([str(token.params[k]) for k in token.params])}>"

    async def get(self, token, *args, **kwargs):
        raise NotImplementedError

    async def set(self, token, response, *args, **kwargs):
        raise NotImplementedError

    async def post(self, token, body, *args, **kwargs):
        raise NotImplementedError

    async def put(self, token, body, *args, **kwargs):
        raise NotImplementedError

    async def clear(self, *args, **kwargs):
        raise NotImplementedError

    async def expire(self, *args, **kwargs):
        raise NotImplementedError
    
    async def delete(self, token, *args, **kwargs):
        raise NotImplementedError

    async def contains(self, token, *args, **kwargs):
        raise NotImplementedError
```

## `get(self, token, *args, **kwargs)` <Badge text="Pyot Cache" vertical="middle" /> <Badge text="Pyot Service" vertical="middle" />
> Make a Get request to the store.

## `set(self, token, response, *args, **kwargs)` <Badge text="Pyot Cache" vertical="middle" />
> Make a Set request to the store.

## `post(self, token, body, *args, **kwargs)` <Badge text="Pyot Service" vertical="middle" />
> Make a Post request to the store.

## `put(self, token, body, *args, **kwargs)` <Badge text="Pyot Service" vertical="middle" />
> Make a Put request to the store.

## `delete(self, token, *args, **kwargs)` <Badge text="Pyot Cache" vertical="middle" /> <Badge text="Pyot Service" vertical="middle" />
> Make a Delete request to the store.

## `clear(self, *args, **kwargs)` <Badge text="Pyot Cache" vertical="middle" />
> Clear the store.

## `expire(self, *args, **kwargs)` <Badge text="Pyot Cache" vertical="middle" />
> Expire the store.

## `contains(self, token, *args, **kwargs)` <Badge text="Pyot Cache" vertical="middle" />
> Check if object exist on the store.
