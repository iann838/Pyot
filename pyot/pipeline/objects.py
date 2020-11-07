

class StoreObject:

    def _log_template(self, token):
        return f"<{token.server.upper()} {token.method}: {' '.join([str(token.params[k]) for k in token.params])}>"

    async def get(self, token, *args):
        raise NotImplementedError

    async def set(self, token, response):
        raise NotImplementedError

    async def post(self, token, body, *args):
        raise NotImplementedError

    async def put(self, token, body, *args):
        raise NotImplementedError

    async def clear(self):
        raise NotImplementedError

    async def expire(self):
        raise NotImplementedError
    
    async def delete(self, token):
        raise NotImplementedError

    async def contains(self, token):
        raise NotImplementedError
