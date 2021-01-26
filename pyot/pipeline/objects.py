

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

    @property
    def classname(self):
        return self.__class__.__name__
