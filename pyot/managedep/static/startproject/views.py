
from aiohttp import web

from pyot.models import lol
from pyot.core.exceptions import NotFound

from .wsgi import app


# Create your views here ...

@app.routes.get('/summoner_level/{name}/{platform}')
async def summoner_level(request: web.Request):
    '''Get summoner level by name and platform'''

    # Sample Function based View
    # Pyot Model: lol
    # Pyot Core Object: Summoner

    try:
        summoner = await lol.Summoner(name=request.match_info["name"], platform=request.match_info["platform"]).get()
        return web.json_response(summoner.level)
    except NotFound:
        return web.json_response({"message": "Summoner Not Found"}, status=404)


@app.routes.view('/summoner_winrate/{name}/{platform}')
class SummonerWinrate(web.View):
    '''Get summoner winrate by name and platform for this season'''

    # Sample Class based View
    # Pyot Model: lol
    # Pyot Core Object: Summoner, SummonerLeague

    def get_winrate(self, league: lol.SummonerLeague):
        wr = []
        for entry in league.entries:
            wr.append(entry.wins / (entry.wins + entry.losses))
        return sum(wr) / len(wr)

    async def get(self):
        summoner = await lol.Summoner(name=self.request.match_info["name"], platform=self.request.match_info["platform"]).get()
        league = await summoner.league_entries.get()
        return web.json_response(self.get_winrate(league) * 100)
