from pyot.utils import run
from pyot.models import val
from syot.models import riot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .match import Match, MatchHistory

class Match(SyotBase, val.Match):
    def get(self):
        return run(super().get())

class MatchHistory(SyotBase, val.MatchHistory):
    def get(self):
        return run(super().get())

# from .content import Content

class Content(SyotBase, val.Content):
    def get(self):
        return run(super().get())

SyotBase._bridges = {
    "Match": Match,
    "MatchHistory": MatchHistory,
    "Content": Content,
}
SyotBase._bridges.update(riot.SyotBase._bridges)
