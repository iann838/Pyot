# Default startup tasks declaration file for pyot projects.
# Callables declared in this file will be accessible by the task manager.

from pyot.models import lol
from pyot.core.exceptions import NotFound


async def summoner_level(name, platform):
    '''Get summoner level by name and platform'''

    # Pyot Model: lol
    # Pyot Core Object: Summoner
    # Refer: https://paaksing.github.io/Pyot/models/lol_summoner.html

    try:
        summoner = await lol.Summoner(name=name, platform=platform).get()
        print(summoner.name, 'in', summoner.platform.upper(), 'is level', summoner.level)
    except NotFound:
        print('Summoner not found')
