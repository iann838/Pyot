import pyot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .championmastery import ChampionMasteries, ChampionMastery

class ChampionMasteries(SyotBase, pyot.lol.ChampionMasteries):
    def get(self):
        return pyot.run(super().get())

class ChampionMastery(SyotBase, pyot.lol.ChampionMastery):
    def get(self):
        return pyot.run(super().get())

# from .league import League, ChallengerLeague, GrandmasterLeague, MasterLeague, SummonerLeague, DivisionLeague

class League(SyotBase, pyot.lol.League):
    def get(self):
        return pyot.run(super().get())

class ChallengerLeague(SyotBase, pyot.lol.ChallengerLeague):
    def get(self):
        return pyot.run(super().get())

class GrandmasterLeague(SyotBase, pyot.lol.GrandmasterLeague):
    def get(self):
        return pyot.run(super().get())

class MasterLeague(SyotBase, pyot.lol.MasterLeague):
    def get(self):
        return pyot.run(super().get())

class SummonerLeague(SyotBase, pyot.lol.SummonerLeague):
    def get(self):
        return pyot.run(super().get())

class DivisionLeague(SyotBase, pyot.lol.DivisionLeague):
    def get(self):
        return pyot.run(super().get())

# from .clash import ClashPlayers, ClashTeam, ClashTournaments, ClashTournament

class ClashPlayers(SyotBase, pyot.lol.ClashPlayers):
    def get(self):
        return pyot.run(super().get())

class ClashTeam(SyotBase, pyot.lol.ClashTeam):
    def get(self):
        return pyot.run(super().get())

class ClashTournaments(SyotBase, pyot.lol.ClashTournaments):
    def get(self):
        return pyot.run(super().get())

class ClashTournament(SyotBase, pyot.lol.ClashTournament):
    def get(self):
        return pyot.run(super().get())

# from .match import Match, MatchTimeline, Timeline, MatchHistory

class Match(SyotBase, pyot.lol.Match):
    def get(self):
        return pyot.run(super().get())

class MatchTimeline(SyotBase, pyot.lol.MatchTimeline):
    def get(self):
        return pyot.run(super().get())

class Timeline(SyotBase, pyot.lol.Timeline):
    def get(self):
        return pyot.run(super().get())

class MatchHistory(SyotBase, pyot.lol.MatchHistory):
    def get(self):
        return pyot.run(super().get())

# from .profileicon import ProfileIcon, ProfileIcons

class ProfileIcon(SyotBase, pyot.lol.ProfileIcon):
    def get(self):
        return pyot.run(super().get())

class ProfileIcons(SyotBase, pyot.lol.ProfileIcons):
    def get(self):
        return pyot.run(super().get())

# from .spectator import FeaturedGames, CurrentGame

class FeaturedGames(SyotBase, pyot.lol.FeaturedGames):
    def get(self):
        return pyot.run(super().get())

class CurrentGame(SyotBase, pyot.lol.CurrentGame):
    def get(self):
        return pyot.run(super().get())

# from .championrotation import ChampionRotation

class ChampionRotation(SyotBase, pyot.lol.ChampionRotation):
    def get(self):
        return pyot.run(super().get())

# from .account import Account, ActivePlatform

class Account(SyotBase, pyot.lol.Account):
    def get(self):
        return pyot.run(super().get())

class ActivePlatform(SyotBase, pyot.lol.ActivePlatform):
    def get(self):
        return pyot.run(super().get())

# from .thirdpartycode import ThirdPartyCode

class ThirdPartyCode(SyotBase, pyot.lol.ThirdPartyCode):
    def get(self):
        return pyot.run(super().get())

# from .merakichampion import MerakiChampion

class MerakiChampion(SyotBase, pyot.lol.MerakiChampion):
    def get(self):
        return pyot.run(super().get())

# from .merakiitem import MerakiItem

class MerakiItem(SyotBase, pyot.lol.MerakiItem):
    def get(self):
        return pyot.run(super().get())

# from .spell import Spell, Spells

class Spell(SyotBase, pyot.lol.Spell):
    def get(self):
        return pyot.run(super().get())

class Spells(SyotBase, pyot.lol.Spells):
    def get(self):
        return pyot.run(super().get())

# from .champion import Champion

class Champion(SyotBase, pyot.lol.Champion):
    def get(self):
        return pyot.run(super().get())

# from .status import Status

class Status(SyotBase, pyot.lol.Status):
    def get(self):
        return pyot.run(super().get())

# from .summoner import Summoner

class Summoner(SyotBase, pyot.lol.Summoner):
    def get(self):
        return pyot.run(super().get())

# from .item import Item, Items

class Item(SyotBase, pyot.lol.Item):
    def get(self):
        return pyot.run(super().get())

class Items(SyotBase, pyot.lol.Items):
    def get(self):
        return pyot.run(super().get())

# from .rune import Rune, Runes

class Rune(SyotBase, pyot.lol.Rune):
    def get(self):
        return pyot.run(super().get())

class Runes(SyotBase, pyot.lol.Runes):
    def get(self):
        return pyot.run(super().get())

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
    "Account": Account,
    "ActivePlatform": ActivePlatform,
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