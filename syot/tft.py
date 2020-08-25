import pyot

# from .league import ChallengerLeague, MasterLeague, GrandmasterLeague, DivisionLeague, SummonerLeague, League

class League(pyot.tft.League):
    def get(self):
        return pyot.run(super().get())

class ChallengerLeague(pyot.tft.ChallengerLeague):
    def get(self):
        return pyot.run(super().get())

class GrandmasterLeague(pyot.tft.GrandmasterLeague):
    def get(self):
        return pyot.run(super().get())

class MasterLeague(pyot.tft.MasterLeague):
    def get(self):
        return pyot.run(super().get())

class SummonerLeague(pyot.tft.SummonerLeague):
    def get(self):
        return pyot.run(super().get())

class DivisionLeague(pyot.tft.DivisionLeague):
    def get(self):
        return pyot.run(super().get())

# from .profileicon import ProfileIcon, ProfileIcons

class ProfileIcon(pyot.tft.ProfileIcon):
    def get(self):
        return pyot.run(super().get())

class ProfileIcons(pyot.tft.ProfileIcons):
    def get(self):
        return pyot.run(super().get())

# from .account import Account, ActivePlatform

class Account(pyot.tft.Account):
    def get(self):
        return pyot.run(super().get())

class ActivePlatform(pyot.tft.ActivePlatform):
    def get(self):
        return pyot.run(super().get())

# from .thirdpartycode import ThirdPartyCode

class ThirdPartyCode(pyot.tft.ThirdPartyCode):
    def get(self):
        return pyot.run(super().get())

# from .champion import Champion, Champions

class Champion(pyot.tft.Champion):
    def get(self):
        return pyot.run(super().get())

class Champions(pyot.tft.Champions):
    def get(self):
        return pyot.run(super().get())

# from .match import MatchHistory, Match

class Match(pyot.tft.Match):
    def get(self):
        return pyot.run(super().get())

class MatchHistory(pyot.tft.MatchHistory):
    def get(self):
        return pyot.run(super().get())

# from .trait import Trait, Traits

class Trait(pyot.tft.Trait):
    def get(self):
        return pyot.run(super().get())

class Traits(pyot.tft.Traits):
    def get(self):
        return pyot.run(super().get())

# from .summoner import Summoner

class Summoner(pyot.tft.Summoner):
    def get(self):
        return pyot.run(super().get())

# from .item import Item, Items

class Item(pyot.tft.Item):
    def get(self):
        return pyot.run(super().get())

class Items(pyot.tft.Items):
    def get(self):
        return pyot.run(super().get())
