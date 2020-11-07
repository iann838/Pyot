from pyot.utils import loop_run
from pyot.models import lor
from syot.models import riot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .card import Card, Cards, Batch, Deck

class Card(SyotBase, lor.Card):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class Cards(SyotBase, lor.Cards):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class Batch(SyotBase, lor.Batch):
    pass

class Deck(SyotBase, lor.Deck):
    pass

# from .match import Match, MatchHistory

class Match(SyotBase, lor.Match):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class MatchHistory(SyotBase, lor.MatchHistory):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .ranked import Leaderboard

class Leaderboard(SyotBase, lor.Leaderboard):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))


SyotBase._bridges = {
    "Card": Card,
    "Cards": Cards,
    "Batch": Batch,
    "Deck": Deck,
    "Match": Match,
    "MatchHistory": MatchHistory,
    "Leaderboard": Leaderboard,
}

SyotBase._bridges.update(riot.SyotBase._bridges)
