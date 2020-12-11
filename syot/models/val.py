import asyncio
from pyot.models import val
from syot.models import riot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .match import Match, MatchHistory

class Match(SyotBase, val.Match):
    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class MatchHistory(SyotBase, val.MatchHistory):
    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .content import Content

class Content(SyotBase, val.Content):
    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .status import Status

class Status(SyotBase, val.Status):
    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

SyotBase._bridges = {
    "Match": Match,
    "MatchHistory": MatchHistory,
    "Content": Content,
    "Status": Status,
}

SyotBase._bridges.update(riot.SyotBase._bridges)
