from typing import Dict

from aiohttp import web

from pyot.core.exceptions import PyotException
from pyot.pipeline.conf import pipelines
from pyot.pipeline.token import PipelineToken


class CloudLineView(web.View):

    @staticmethod
    def parse_cloudline_body(body: Dict) -> Dict:
        body = {k: v for k, v in body.items() if v is not None}
        body["token"] = PipelineToken.load(body["token"])
        return body

    async def post(self):
        try:
            pipeline = pipelines[self.request.headers["Pyot-CloudLine-Target"]]
        except KeyError:
            return web.json_response({"message": "Pipeline Not Found"}, status=404)

        body = await self.request.json()
        caller = getattr(pipeline, self.request.headers["Pyot-CloudLine-Method"])
        try:
            response = await caller(**self.parse_cloudline_body(body))
        except PyotException as e:
            return web.json_response(str(e), status=e.code)
        return web.json_response(response)
