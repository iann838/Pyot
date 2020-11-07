from pyot.utils import loop_run
from pyot.models import val
from syot.models import riot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .match import Match, MatchHistory

class Match(SyotBase, val.Match):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class MatchHistory(SyotBase, val.MatchHistory):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .content import Content

class Content(SyotBase, val.Content):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

SyotBase._bridges = {
    "Match": Match,
    "MatchHistory": MatchHistory,
    "Content": Content,
}

SyotBase._bridges.update(riot.SyotBase._bridges)
