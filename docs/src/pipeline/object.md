# Store Object

This is the object that all Pyot stores subclasses.

```python
class StoreObject:

    def _log_template(self, token):
        return f"<{token.server.upper()} {token.method}: {' '.join([str(token.params[k]) for k in token.params])}>"

    async def get(self, token, *args):
        raise NotImplementedError

    async def set(self, token, response):
        raise NotImplementedError

    async def clear(self):
        raise NotImplementedError

    async def expire(self):
        raise NotImplementedError
    
    async def delete(self, token):
        raise NotImplementedError

    async def contains(self, token):
        raise NotImplementedError
```

## `get(self, token, *args)`
> Get the object from the store.

## `set(self, token, response)`
> Set the object to the store.

## `clear(self)`
> Clear the store.

## `expire(self)`
> Expire the store.

## `delete(self, token)`
> Delete an object from the store.

## `contains(self, token)`
> Check if object exist on the store.
