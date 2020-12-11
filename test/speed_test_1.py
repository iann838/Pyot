from pyot.models import lol
from pyot.utils import PtrCache

async def iterate_match_events():
    cache = PtrCache()
    match = await lol.MatchTimeline(id=3442099474).get()
    for team in match.teams:
        for p in team.participants:
            for event in p.timeline["events"]:
                pass
