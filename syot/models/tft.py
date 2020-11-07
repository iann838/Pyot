from pyot.utils import loop_run
from pyot.models import tft
from syot.models import riot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .league import ChallengerLeague, MasterLeague, GrandmasterLeague, DivisionLeague, SummonerLeague, League

class League(SyotBase, tft.League):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class ChallengerLeague(SyotBase, tft.ChallengerLeague):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class GrandmasterLeague(SyotBase, tft.GrandmasterLeague):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class MasterLeague(SyotBase, tft.MasterLeague):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class SummonerLeague(SyotBase, tft.SummonerLeague):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class DivisionLeague(SyotBase, tft.DivisionLeague):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .profileicon import ProfileIcon, ProfileIcons

class ProfileIcon(SyotBase, tft.ProfileIcon):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class ProfileIcons(SyotBase, tft.ProfileIcons):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .thirdpartycode import ThirdPartyCode

class ThirdPartyCode(SyotBase, tft.ThirdPartyCode):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .champion import Champion, Champions

class Champion(SyotBase, tft.Champion):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class Champions(SyotBase, tft.Champions):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .match import MatchHistory, Match

class Match(SyotBase, tft.Match):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class MatchHistory(SyotBase, tft.MatchHistory):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .trait import Trait, Traits

class Trait(SyotBase, tft.Trait):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class Traits(SyotBase, tft.Traits):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .summoner import Summoner

class Summoner(SyotBase, tft.Summoner):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .item import Item, Items

class Item(SyotBase, tft.Item):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class Items(SyotBase, tft.Items):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

SyotBase._bridges = {
    "League": League,
    "ChallengerLeague": ChallengerLeague,
    "GrandmasterLeague": GrandmasterLeague,
    "MasterLeague": MasterLeague,
    "SummonerLeague": SummonerLeague,
    "DivisionLeague": DivisionLeague,
    "ProfileIcon": ProfileIcon,
    "ProfileIcons": ProfileIcons,
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
SyotBase._bridges.update(riot.SyotBase._bridges)
