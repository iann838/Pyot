import pyot

# from .account import Account, ActivePlatform

class Account(pyot.val.Account):
    def get(self):
        return pyot.run(super().get())

class ActivePlatform(pyot.val.ActivePlatform):
    def get(self):
        return pyot.run(super().get())

# from .match import Match, MatchHistory

class Match(pyot.val.Match):
    def get(self):
        return pyot.run(super().get())

class MatchHistory(pyot.val.MatchHistory):
    def get(self):
        return pyot.run(super().get())

# from .content import Content

class Content(pyot.val.Content):
    def get(self):
        return pyot.run(super().get())
