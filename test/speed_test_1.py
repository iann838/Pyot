from pyot.models import lol
from pyot.utils import PtrCache

async def iterate_match_events():
    # pylint: disable=unused-variable
    cache = PtrCache()
    match = await lol.Match(id=3442099474, include_timeline=True, platform="NA1").get()
    for team in match.teams:
        for p in team.participants:
            # for event in p.timeline["events"]:
            for event in p.timeline.events:
                # try:
                #     event.position.x
                # except Exception: pass
                pass
