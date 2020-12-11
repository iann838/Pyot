from pyot.models import lol
from pyot.utils import PtrCache

async def iterate_match_events():
    cache = PtrCache()
    match = await lol.MatchTimeline(id=3442099474).get()
    for team in match.teams:
        for p in team.participants:
            for event in p.timeline["events"]:
                if "itemId" in event:
                    item = await lol.Item(id=event["itemId"]).get(ptr_cache=cache)
                if "beforeId" in event and event["beforeId"]:
                    item = await lol.Item(id=event["beforeId"]).get(ptr_cache=cache)
                if "afterId" in event and event["afterId"]:
                    item = await lol.Item(id=event["afterId"]).get(ptr_cache=cache)
            # for event in p.timeline.events:
            #     pass
