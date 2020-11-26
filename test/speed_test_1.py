from pyot.models import lol

async def iterate_match_events():
    match = await lol.MatchTimeline(id=3442099474).get()
    for team in match.teams:
        for p in team.participants:
            # for event in p.timeline["events"]:
            for event in p.timeline.events:
                pass
