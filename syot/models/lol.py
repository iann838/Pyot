from pyot.utils import loop_run
from pyot.models import lol
from syot.models import riot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .championmastery import ChampionMasteries, ChampionMastery

class ChampionMasteries(SyotBase, lol.ChampionMasteries):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class ChampionMastery(SyotBase, lol.ChampionMastery):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .league import League, ChallengerLeague, GrandmasterLeague, MasterLeague, SummonerLeague, DivisionLeague

class League(SyotBase, lol.League):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class ChallengerLeague(SyotBase, lol.ChallengerLeague):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class GrandmasterLeague(SyotBase, lol.GrandmasterLeague):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class MasterLeague(SyotBase, lol.MasterLeague):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class SummonerLeague(SyotBase, lol.SummonerLeague):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class DivisionLeague(SyotBase, lol.DivisionLeague):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .clash import ClashPlayers, ClashTeam, ClashTournaments, ClashTournament

class ClashPlayers(SyotBase, lol.ClashPlayers):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class ClashTeam(SyotBase, lol.ClashTeam):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class ClashTournaments(SyotBase, lol.ClashTournaments):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class ClashTournament(SyotBase, lol.ClashTournament):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .match import Match, MatchTimeline, Timeline, MatchHistory

class Match(SyotBase, lol.Match):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class MatchTimeline(SyotBase, lol.MatchTimeline):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class Timeline(SyotBase, lol.Timeline):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class MatchHistory(SyotBase, lol.MatchHistory):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .profileicon import ProfileIcon, ProfileIcons

class ProfileIcon(SyotBase, lol.ProfileIcon):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class ProfileIcons(SyotBase, lol.ProfileIcons):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .spectator import FeaturedGames, CurrentGame

class FeaturedGames(SyotBase, lol.FeaturedGames):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class CurrentGame(SyotBase, lol.CurrentGame):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .championrotation import ChampionRotation

class ChampionRotation(SyotBase, lol.ChampionRotation):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .thirdpartycode import ThirdPartyCode

class ThirdPartyCode(SyotBase, lol.ThirdPartyCode):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .merakichampion import MerakiChampion

class MerakiChampion(SyotBase, lol.MerakiChampion):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .merakiitem import MerakiItem

class MerakiItem(SyotBase, lol.MerakiItem):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .spell import Spell, Spells

class Spell(SyotBase, lol.Spell):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class Spells(SyotBase, lol.Spells):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .champion import Champion

class Champion(SyotBase, lol.Champion):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .status import Status

class Status(SyotBase, lol.Status):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .summoner import Summoner

class Summoner(SyotBase, lol.Summoner):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .item import Item, Items

class Item(SyotBase, lol.Item):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class Items(SyotBase, lol.Items):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .rune import Rune, Runes

class Rune(SyotBase, lol.Rune):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class Runes(SyotBase, lol.Runes):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

# from .tournament import Tournament, TournamentProvider, TournamentCodes, TournamentCode, TournamentLobbyEvents, TournamentStub, TournamentStubCodes, TournamentStubLobbyEvents, TournamentStubProvider

class Tournament(SyotBase, lol.Tournament):
    def post(self, **kwargs):
        return loop_run(super().post(**kwargs))

class TournamentProvider(SyotBase, lol.TournamentProvider):
    def post(self, **kwargs):
        return loop_run(super().post(**kwargs))

class TournamentCodes(SyotBase, lol.TournamentCodes):
    def post(self, **kwargs):
        return loop_run(super().post(**kwargs))

class TournamentCode(SyotBase, lol.TournamentCode):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

    def put(self, **kwargs):
        return loop_run(super().put(**kwargs))

class TournamentLobbyEvents(SyotBase, lol.TournamentLobbyEvents):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class TournamentStub(SyotBase, lol.TournamentStub):
    def post(self, **kwargs):
        return loop_run(super().post(**kwargs))

class TournamentStubCodes(SyotBase, lol.TournamentStubCodes):
    def post(self, **kwargs):
        return loop_run(super().post(**kwargs))

class TournamentStubLobbyEvents(SyotBase, lol.TournamentStubLobbyEvents):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class TournamentStubProvider(SyotBase, lol.TournamentStubProvider):
    def post(self, **kwargs):
        return loop_run(super().post(**kwargs))


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
    "Tournament": Tournament,
    "TournamentProvider": TournamentProvider,
    "TournamentCodes": TournamentCodes,
    "TournamentCode": TournamentCode,
    "TournamentLobbyEvents": TournamentLobbyEvents,
    "TournamentStub": TournamentStub,
    "TournamentStubCodes": TournamentStubCodes,
    "TournamentStubLobbyEvents": TournamentStubLobbyEvents,
    "TournamentStubProvider": TournamentStubProvider,
}

SyotBase._bridges.update(riot.SyotBase._bridges)
