from typing import List, Iterator, TYPE_CHECKING

from pyot.core.functional import parse_camelcase
from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from .summoner import Summoner


# PYOT STATIC

class TournamentLobbyEventData(PyotStatic):
    summoner_id: str
    event_type: str
    timestamp: str


# PYOT CORE

class TournamentProvider(PyotCore):
    id: int
    region: str

    class Meta(PyotCore.Meta):
        rules = {"tournament_v4_providers": []}

    def __init__(self, region: str = None):
        self.initialize(locals())

    def body(self, region: str, url: str):
        '''Body parameters setter.'''
        if not url.startswith("https://") and not url.startswith("http://"):
            raise TypeError("url should be well-formed, starting with an http protocol")
        if region not in {"BR", "EUNE", "EUW", "JP", "LAN", "LAS", "NA", "OCE", "PBE", "RU", "TR"}:
            raise TypeError(f"Invalid region '{region}' parameter, region in tournament-v4 uses client keys (NA, EUW, BR, LAN, ...)")
        self._meta.body = parse_camelcase(locals())
        return self

    def clean(self):
        if not hasattr(self._meta, "body"):
            raise TypeError("This object's body parameters is required")

    def transform(self, data):
        return {"id": data}


class TournamentStubProvider(TournamentProvider):

    class Meta(TournamentProvider.Meta):
        rules = {"tournament_stub_v4_providers": []}


class Tournament(PyotCore):
    id: int
    region: str

    class Meta(PyotCore.Meta):
        rules = {"tournament_v4_tournaments": []}

    def __init__(self, region: str = None):
        self.initialize(locals())

    def body(self, name: str, provider_id: int):
        '''Body parameters setter.'''
        if not isinstance(provider_id, int):
            raise TypeError("provider_id must be int type")
        self._meta.body = parse_camelcase(locals())
        return self

    def clean(self):
        if not hasattr(self._meta, "body"):
            raise TypeError("This object's body parameters is required")

    def transform(self, data):
        return {"id": data}


class TournamentStub(Tournament):

    class Meta(Tournament.Meta):
        rules = {"tournament_stub_v4_tournaments": []}


class TournamentLobbyEvents(PyotCore):
    events: List[TournamentLobbyEventData]
    region: str

    class Meta(PyotCore.Meta):
        rules = {"tournament_v4_lobby_events": ["code"]}

    def __init__(self, code: int = None, region: str = None):
        self.initialize(locals())

    def transform(self, data):
        return {"events": data}

    def __getitem__(self, item):
        if not isinstance(item, int):
            return super().__getitem__(item)
        return self.events[item]

    def __iter__(self) -> Iterator[TournamentLobbyEventData]:
        return iter(self.events)

    def __len__(self):
        return len(self.events)


class TournamentStubLobbyEvents(TournamentLobbyEvents):

    class Meta(TournamentLobbyEvents.Meta):
        rules = {"tournament_stub_v4_lobby_events": ["code"]}


class TournamentCode(PyotCore):
    code: str
    spectators: str
    lobby_name: str
    meta_data: str
    password: str
    team_size: int
    provider_id: int
    pick_type: str
    tournament_id: int
    id: int
    map: str
    hosted_region: str
    summoner_ids: List[str]

    class Meta(PyotCore.Meta):
        raws = {"summoner_ids"}
        renamed = {"region": "hosted_region", "participants": "summoner_ids"}
        rules = {"tournament_v4_codes_by_code": ["code"]}

    def __init__(self, code: str = None, region: str = None):
        self.initialize(locals())

    def body(self, map_type: str, pick_type: str, spectator_type: str, allowed_summoner_ids: List[str] = None):
        '''Body parameters setter.'''
        if pick_type not in ["BLIND_PICK", "DRAFT_MODE", "ALL_RANDOM", "TOURNAMENT_DRAFT"]:
            raise TypeError(f"Invalid pick type '{pick_type}' parameter, must be one of BLIND_PICK, DRAFT_MODE, ALL_RANDOM, TOURNAMENT_DRAFT")
        if map_type not in ["SUMMONERS_RIFT", "TWISTED_TREELINE", "HOWLING_ABYSS"]:
            raise TypeError(f"Invalid map type '{map_type}' parameter, must be one of SUMMONERS_RIFT, TWISTED_TREELINE, HOWLING_ABYSS")
        if spectator_type not in ["NONE", "LOBBYONLY", "ALL"]:
            raise TypeError(f"Invalid spectator type '{spectator_type}' parameter, must be one of NONE, LOBBYONLY, ALL")
        self._meta.body = parse_camelcase(locals())
        return self

    @property
    def summoners(self) -> "Summoner":
        from .summoner import Summoner
        return [Summoner(id=id_) for id_ in self.summoner_ids]


class TournamentCodes(PyotCore):
    codes: List[str]
    region: str

    class Meta(PyotCore.Meta):
        raws = {"codes"}
        rules = {"tournament_v4_codes": []}

    def __init__(self, region: str = None):
        self.initialize(locals())

    def query(self, tournament_id: int, count: int = None):
        if not isinstance(count, int) or count > 1000 or count < 1:
            raise TypeError(f"Invalid count '{count}' parameter, must be between 1-5")
        self._meta.query = parse_camelcase(locals())
        return self

    def body(self, map_type: str, pick_type: str, team_size: int, spectator_type: str, allowed_summoner_ids: List[str] = None, metadata: str = None):
        '''Body parameters setter.'''
        if pick_type not in ["BLIND_PICK", "DRAFT_MODE", "ALL_RANDOM", "TOURNAMENT_DRAFT"]:
            raise TypeError(f"Invalid pick type '{pick_type}' parameter, must be one of BLIND_PICK, DRAFT_MODE, ALL_RANDOM, TOURNAMENT_DRAFT")
        if map_type not in ["SUMMONERS_RIFT", "TWISTED_TREELINE", "HOWLING_ABYSS"]:
            raise TypeError(f"Invalid map type '{map_type}' parameter, must be one of SUMMONERS_RIFT, TWISTED_TREELINE, HOWLING_ABYSS")
        if spectator_type not in ["NONE", "LOBBYONLY", "ALL"]:
            raise TypeError(f"Invalid spectator type '{spectator_type}' parameter, must be one of NONE, LOBBYONLY, ALL")
        if not isinstance(team_size, int) or team_size > 5 or team_size < 1:
            raise TypeError(f"Invalid team size '{team_size}' parameter, must be between 1-5")
        self._meta.body = parse_camelcase(locals())
        return self

    def clean(self):
        if not hasattr(self._meta, "body"):
            raise TypeError("This object's body parameters is required")
        if not hasattr(self._meta, "query"):
            raise TypeError("This object is missing query parameters")

    def transform(self, data):
        return {"codes": data}

    @property
    def tournament_codes(self) -> List[TournamentCode]:
        return [TournamentCode(code=code, region=self.region) for code in self.codes]


class TournamentStubCodes(TournamentCodes):

    class Meta(TournamentCodes.Meta):
        rules = {"tournament_stub_v4_codes": []}
