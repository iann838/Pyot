import asyncio
from pyot.models import lol
from syot.models import riot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .championmastery import ChampionMasteries, ChampionMastery

class ChampionMasteries(SyotBase, lol.ChampionMasteries):
    class Meta(lol.ChampionMasteries.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class ChampionMastery(SyotBase, lol.ChampionMastery):
    class Meta(lol.ChampionMastery.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .league import League, ChallengerLeague, GrandmasterLeague, MasterLeague, SummonerLeague, DivisionLeague

class League(SyotBase, lol.League):
    class Meta(lol.League.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class ChallengerLeague(SyotBase, lol.ChallengerLeague):
    class Meta(lol.ChallengerLeague.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class GrandmasterLeague(SyotBase, lol.GrandmasterLeague):
    class Meta(lol.GrandmasterLeague.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class MasterLeague(SyotBase, lol.MasterLeague):
    class Meta(lol.MasterLeague.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class SummonerLeague(SyotBase, lol.SummonerLeague):
    class Meta(lol.SummonerLeague.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class DivisionLeague(SyotBase, lol.DivisionLeague):
    class Meta(lol.DivisionLeague.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .clash import ClashPlayers, ClashTeam, ClashTournaments, ClashTournament

class ClashPlayers(SyotBase, lol.ClashPlayers):
    class Meta(lol.ClashPlayers.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class ClashTeam(SyotBase, lol.ClashTeam):
    class Meta(lol.ClashTeam.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class ClashTournaments(SyotBase, lol.ClashTournaments):
    class Meta(lol.ClashTournaments.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class ClashTournament(SyotBase, lol.ClashTournament):
    class Meta(lol.ClashTournament.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .match import Match, MatchTimeline, Timeline, MatchHistory

class Match(SyotBase, lol.Match):
    class Meta(lol.Match.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class Matches(SyotBase, lol.Matches):
    class Meta(lol.Matches.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class Timeline(SyotBase, lol.Timeline):
    class Meta(lol.Timeline.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class MatchHistory(SyotBase, lol.MatchHistory):
    class Meta(lol.MatchHistory.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class Matches(SyotBase, lol.Matches):
    class Meta(lol.Matches.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .profileicon import ProfileIcon, ProfileIcons

class ProfileIcon(SyotBase, lol.ProfileIcon):
    class Meta(lol.ProfileIcon.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class ProfileIcons(SyotBase, lol.ProfileIcons):
    class Meta(lol.ProfileIcons.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .spectator import FeaturedGames, CurrentGame

class FeaturedGames(SyotBase, lol.FeaturedGames):
    class Meta(lol.FeaturedGames.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class CurrentGame(SyotBase, lol.CurrentGame):
    class Meta(lol.CurrentGame.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .championrotation import ChampionRotation

class ChampionRotation(SyotBase, lol.ChampionRotation):
    class Meta(lol.ChampionRotation.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .thirdpartycode import ThirdPartyCode

class ThirdPartyCode(SyotBase, lol.ThirdPartyCode):
    class Meta(lol.ThirdPartyCode.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .merakichampion import MerakiChampion

class MerakiChampion(SyotBase, lol.MerakiChampion):
    class Meta(lol.MerakiChampion.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .merakiitem import MerakiItem

class MerakiItem(SyotBase, lol.MerakiItem):
    class Meta(lol.MerakiItem.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .spell import Spell, Spells

class Spell(SyotBase, lol.Spell):
    class Meta(lol.Spell.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class Spells(SyotBase, lol.Spells):
    class Meta(lol.Spells.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .champion import Champion

class Champion(SyotBase, lol.Champion):
    class Meta(lol.Champion.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .status import Status

class Status(SyotBase, lol.Status):
    class Meta(lol.Status.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .summoner import Summoner

class Summoner(SyotBase, lol.Summoner):
    class Meta(lol.Summoner.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .item import Item, Items

class Item(SyotBase, lol.Item):
    class Meta(lol.Item.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class Items(SyotBase, lol.Items):
    class Meta(lol.Items.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .rune import Rune, Runes

class Rune(SyotBase, lol.Rune):
    class Meta(lol.Rune.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class Runes(SyotBase, lol.Runes):
    class Meta(lol.Runes.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

# from .tournament import Tournament, TournamentProvider, TournamentCodes, TournamentCode, TournamentLobbyEvents, TournamentStub, TournamentStubCodes, TournamentStubLobbyEvents, TournamentStubProvider

class Tournament(SyotBase, lol.Tournament):
    class Meta(lol.Tournament.Meta): pass

    def post(self, **kwargs):
        return asyncio.run(super().post(**kwargs))

class TournamentProvider(SyotBase, lol.TournamentProvider):
    class Meta(lol.TournamentProvider.Meta): pass

    def post(self, **kwargs):
        return asyncio.run(super().post(**kwargs))

class TournamentCodes(SyotBase, lol.TournamentCodes):
    class Meta(lol.TournamentCodes.Meta): pass

    def post(self, **kwargs):
        return asyncio.run(super().post(**kwargs))

class TournamentCode(SyotBase, lol.TournamentCode):
    class Meta(lol.TournamentCode.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

    def put(self, **kwargs):
        return asyncio.run(super().put(**kwargs))

class TournamentLobbyEvents(SyotBase, lol.TournamentLobbyEvents):
    class Meta(lol.TournamentLobbyEvents.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class TournamentStub(SyotBase, lol.TournamentStub):
    class Meta(lol.TournamentStub.Meta): pass

    def post(self, **kwargs):
        return asyncio.run(super().post(**kwargs))

class TournamentStubCodes(SyotBase, lol.TournamentStubCodes):
    class Meta(lol.TournamentStubCodes.Meta): pass

    def post(self, **kwargs):
        return asyncio.run(super().post(**kwargs))

class TournamentStubLobbyEvents(SyotBase, lol.TournamentStubLobbyEvents):
    class Meta(lol.TournamentStubLobbyEvents.Meta): pass

    def get(self, **kwargs):
        return asyncio.run(super().get(**kwargs))

class TournamentStubProvider(SyotBase, lol.TournamentStubProvider):
    class Meta(lol.TournamentStubProvider.Meta): pass

    def post(self, **kwargs):
        return asyncio.run(super().post(**kwargs))


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
