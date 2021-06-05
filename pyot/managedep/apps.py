import os

from aiohttp import web

from .views import CloudLineView


class Application:

    def __init__(self):
        self.tasks = {}
        self.routes = web.RouteTableDef()
        self.modules = {}
        self.consume_settings()

    def __call__(self, host: str = None, port: int = None):
        '''
        Run the application server on host:port.

        If host:port is not provided, an instance of web.Application will be returned,
        ready to be consumed by wsgi servers (e.g. Gunicorn).
        '''
        app = web.Application()
        app.add_routes(self.routes)
        if not host and not port:
            return app
        return web.run_app(app, host=host, port=port)

    def task(self, name):
        def wrapper(func):
            self.tasks[name] = func
            return func
        return wrapper

    def consume_settings(self):
        self.routes.post(os.environ.get("PYOT_CLOUDLINE_URL"))(CloudLineView)
