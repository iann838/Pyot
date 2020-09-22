from pyot.utils import run
from pyot.models import lol
from syot.models import riot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .championmastery import ChampionMasteries, ChampionMastery

class ChampionMasteries(SyotBase, lol.ChampionMasteries):
    def get(self):
        return run(super().get())

class ChampionMastery(SyotBase, lol.ChampionMastery):
    def get(self):
        return run(super().get())

# from .league import League, ChallengerLeague, GrandmasterLeague, MasterLeague, SummonerLeague, DivisionLeague

class League(SyotBase, lol.League):
    def get(self):
        return run(super().get())

class ChallengerLeague(SyotBase, lol.ChallengerLeague):
    def get(self):
        return run(super().get())

class GrandmasterLeague(SyotBase, lol.GrandmasterLeague):
    def get(self):
        return run(super().get())

class MasterLeague(SyotBase, lol.MasterLeague):
    def get(self):
        return run(super().get())

class SummonerLeague(SyotBase, lol.SummonerLeague):
    def get(self):
        return run(super().get())

class DivisionLeague(SyotBase, lol.DivisionLeague):
    def get(self):
        return run(super().get())

# from .clash import ClashPlayers, ClashTeam, ClashTournaments, ClashTournament

class ClashPlayers(SyotBase, lol.ClashPlayers):
    def get(self):
        return run(super().get())

class ClashTeam(SyotBase, lol.ClashTeam):
    def get(self):
        return run(super().get())

class ClashTournaments(SyotBase, lol.ClashTournaments):
    def get(self):
        return run(super().get())

class ClashTournament(SyotBase, lol.ClashTournament):
    def get(self):
        return run(super().get())

# from .match import Match, MatchTimeline, Timeline, MatchHistory

class Match(SyotBase, lol.Match):
    def get(self):
        return run(super().get())

class MatchTimeline(SyotBase, lol.MatchTimeline):
    def get(self):
        return run(super().get())

class Timeline(SyotBase, lol.Timeline):
    def get(self):
        return run(super().get())

class MatchHistory(SyotBase, lol.MatchHistory):
    def get(self):
        return run(super().get())

# from .profileicon import ProfileIcon, ProfileIcons

class ProfileIcon(SyotBase, lol.ProfileIcon):
    def get(self):
        return run(super().get())

class ProfileIcons(SyotBase, lol.ProfileIcons):
    def get(self):
        return run(super().get())

# from .spectator import FeaturedGames, CurrentGame

class FeaturedGames(SyotBase, lol.FeaturedGames):
    def get(self):
        return run(super().get())

class CurrentGame(SyotBase, lol.CurrentGame):
    def get(self):
        return run(super().get())

# from .championrotation import ChampionRotation

class ChampionRotation(SyotBase, lol.ChampionRotation):
    def get(self):
        return run(super().get())

# from .thirdpartycode import ThirdPartyCode

class ThirdPartyCode(SyotBase, lol.ThirdPartyCode):
    def get(self):
        return run(super().get())

# from .merakichampion import MerakiChampion

class MerakiChampion(SyotBase, lol.MerakiChampion):
    def get(self):
        return run(super().get())

# from .merakiitem import MerakiItem

class MerakiItem(SyotBase, lol.MerakiItem):
    def get(self):
        return run(super().get())

# from .spell import Spell, Spells

class Spell(SyotBase, lol.Spell):
    def get(self):
        return run(super().get())

class Spells(SyotBase, lol.Spells):
    def get(self):
        return run(super().get())

# from .champion import Champion

class Champion(SyotBase, lol.Champion):
    def get(self):
        return run(super().get())

# from .status import Status

class Status(SyotBase, lol.Status):
    def get(self):
        return run(super().get())

# from .summoner import Summoner

class Summoner(SyotBase, lol.Summoner):
    def get(self):
        return run(super().get())

# from .item import Item, Items

class Item(SyotBase, lol.Item):
    def get(self):
        return run(super().get())

class Items(SyotBase, lol.Items):
    def get(self):
        return run(super().get())

# from .rune import Rune, Runes

class Rune(SyotBase, lol.Rune):
    def get(self):
        return run(super().get())

class Runes(SyotBase, lol.Runes):
    def get(self):
        return run(super().get())

SyotBase._bridges = {
    "ChampionMasteries": ChampionMasteries,
    "ChampionMastery": ChampionMastery,
    "League": League,
    "ChallengerLeague": ChallengerLeague,
    "GrandmasterLeague": GrandmasterLeague,
    "MasterLeague": MasterLeague,
    "SummonerLeague": SummonerLeague,
    "DivisionLeague": DivisionLeague,
    "ClashPlayers": ClashPlayers,
    "ClashTeam": ClashTeam,
    "ClashTournaments": ClashTournaments,
    "ClashTournament": ClashTournament,
    "Match": Match,
    "MatchTimeline": MatchTimeline,
    "Timeline": Timeline,
    "MatchHistory": MatchHistory,
    "ProfileIcon": ProfileIcon,
    "ProfileIcons": ProfileIcons,
    "FeaturedGames": FeaturedGames,
    "CurrentGame": CurrentGame,
    "ChampionRotation": ChampionRotation,
    "ThirdPartyCode": ThirdPartyCode,
    "MerakiChampion": MerakiChampion,
    "MerakiItem": MerakiItem,
    "Spell": Spell,
    "Spells": Spells,
    "Champion": Champion,
    "Summoner": Summoner,
    "Item": Item,
    "Items": Items,
    "Rune": Rune,
    "Runes": Runes,
    "Status": Status,
}
SyotBase._bridges.update(riot.SyotBase._bridges)
