import pyot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .league import ChallengerLeague, MasterLeague, GrandmasterLeague, DivisionLeague, SummonerLeague, League

class League(SyotBase, pyot.tft.League):
    def get(self):
        return pyot.run(super().get())

class ChallengerLeague(SyotBase, pyot.tft.ChallengerLeague):
    def get(self):
        return pyot.run(super().get())

class GrandmasterLeague(SyotBase, pyot.tft.GrandmasterLeague):
    def get(self):
        return pyot.run(super().get())

class MasterLeague(SyotBase, pyot.tft.MasterLeague):
    def get(self):
        return pyot.run(super().get())

class SummonerLeague(SyotBase, pyot.tft.SummonerLeague):
    def get(self):
        return pyot.run(super().get())

class DivisionLeague(SyotBase, pyot.tft.DivisionLeague):
    def get(self):
        return pyot.run(super().get())

# from .profileicon import ProfileIcon, ProfileIcons

class ProfileIcon(SyotBase, pyot.tft.ProfileIcon):
    def get(self):
        return pyot.run(super().get())

class ProfileIcons(SyotBase, pyot.tft.ProfileIcons):
    def get(self):
        return pyot.run(super().get())

# from .account import Account, ActivePlatform

class Account(SyotBase, pyot.tft.Account):
    def get(self):
        return pyot.run(super().get())

class ActivePlatform(SyotBase, pyot.tft.ActivePlatform):
    def get(self):
        return pyot.run(super().get())

# from .thirdpartycode import ThirdPartyCode

class ThirdPartyCode(SyotBase, pyot.tft.ThirdPartyCode):
    def get(self):
        return pyot.run(super().get())

# from .champion import Champion, Champions

class Champion(SyotBase, pyot.tft.Champion):
    def get(self):
        return pyot.run(super().get())

class Champions(SyotBase, pyot.tft.Champions):
    def get(self):
        return pyot.run(super().get())

# from .match import MatchHistory, Match

class Match(SyotBase, pyot.tft.Match):
    def get(self):
        return pyot.run(super().get())

class MatchHistory(SyotBase, pyot.tft.MatchHistory):
    def get(self):
        return pyot.run(super().get())

# from .trait import Trait, Traits

class Trait(SyotBase, pyot.tft.Trait):
    def get(self):
        return pyot.run(super().get())

class Traits(SyotBase, pyot.tft.Traits):
    def get(self):
        return pyot.run(super().get())

# from .summoner import Summoner

class Summoner(SyotBase, pyot.tft.Summoner):
    def get(self):
        return pyot.run(super().get())

# from .item import Item, Items

class Item(SyotBase, pyot.tft.Item):
    def get(self):
        return pyot.run(super().get())

class Items(SyotBase, pyot.tft.Items):
    def get(self):
        return pyot.run(super().get())

SyotBase._bridges = {
    "League": League,
    "ChallengerLeague": ChallengerLeague,
    "GrandmasterLeague": GrandmasterLeague,
    "MasterLeague": MasterLeague,
    "SummonerLeague": SummonerLeague,
    "DivisionLeague": DivisionLeague,
    "ProfileIcon": ProfileIcon,
    "ProfileIcons": ProfileIcons,
    "Account": Account,
    "ActivePlatform": ActivePlatform,
    "ThirdPartyCode": ThirdPartyCode,
    "Champion": Champion,
    "Champions": Champions,
    "Match": Match,
    "MatchHistory": MatchHistory,
    "Trait": Trait,
    "Traits": Traits,
    "Summoner": Summoner,
    "Item": Item,
    "Items": Items,
}