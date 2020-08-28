import pyot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .account import Account, ActivePlatform

class Account(SyotBase, pyot.val.Account):
    def get(self):
        return pyot.run(super().get())

class ActivePlatform(SyotBase, pyot.val.ActivePlatform):
    def get(self):
        return pyot.run(super().get())

# from .match import Match, MatchHistory

class Match(SyotBase, pyot.val.Match):
    def get(self):
        return pyot.run(super().get())

class MatchHistory(SyotBase, pyot.val.MatchHistory):
    def get(self):
        return pyot.run(super().get())

# from .content import Content

class Content(SyotBase, pyot.val.Content):
    def get(self):
        return pyot.run(super().get())

SyotBase._bridges = {
    "Account": Account,
    "ActivePlatform": ActivePlatform,
    "Match": Match,
    "MatchHistory": MatchHistory,
    "Content": Content,
}