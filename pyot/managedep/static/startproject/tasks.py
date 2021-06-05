
from pyot.models import lol
from pyot.core.exceptions import NotFound

from .wsgi import app


# Create your tasks here ...

@app.task('summoner_level')
async def summoner_level(name, platform):
    '''Get summoner level by name and platform'''

    # Sample Function based Task
    # Pyot Model: lol
    # Pyot Core Object: Summoner

    try:
        summoner = await lol.Summoner(name=name, platform=platform).get()
        print(summoner.name, 'in', summoner.platform.upper(), 'is level', summoner.level)
    except NotFound:
        print('Summoner not found')


@app.task('summoner_winrate')
class SummonerWinrate:
    '''Get summoner winrate by name and platform for this season'''

    # Sample Class based Task
    # Pyot Model: lol
    # Pyot Core Object: Summoner, SummonerLeague

    async def __call__(self, name, platform):
        summoner = await lol.Summoner(name=name, platform=platform).get()
        league = await summoner.league_entries.get()
        print(summoner.name, "has a", self.get_winrate(league) * 100, "% winrate in ranked this season")

    def get_winrate(self, league: lol.SummonerLeague):
        wr = []
        for entry in league.entries:
            wr.append(entry.wins / (entry.wins + entry.losses))
        return sum(wr) / len(wr)
