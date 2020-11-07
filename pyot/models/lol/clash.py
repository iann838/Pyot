from .__core__ import PyotCore, PyotStatic
from typing import List
from datetime import datetime


# PYOT STATIC OBJECTS

class ClashPlayerData(PyotStatic):
    summoner_id: str
    team_id: str
    position: str
    role: str
    
    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)

    @property
    def team(self) -> "ClashTeam":
        return ClashTeam(id=self.team_id, platform=self.platform)


class ClashTournamentPhaseData(PyotStatic):
    id: int
    registration_time: datetime
    start_time: datetime
    cancelled: bool

    def __getattribute__(self, name):
        if name in ["start_time", "registration_time"]:
            return datetime.fromtimestamp(super().__getattribute__(name)//1000)
        return super().__getattribute__(name)


class ClashTournamentData(PyotStatic):
    id: int
    theme_id: int
    name_key: str
    name_key_secondary: str
    schedule: List[ClashTournamentPhaseData]


# PYOT CORE OBJECTS

class ClashPlayers(PyotCore):
    summoner_id: str
    players: List[ClashPlayerData]

    class Meta(PyotCore.Meta):
        rules = {"clash_v1_players": ["summoner_id"]}

    def __init__(self, summoner_id: str = None, platform: str = None):
        self._lazy_set(locals())

    def _transform(self, data):
        new_data = {}
        new_data["players"] = data
        return new_data

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.summoner_id, platform=self.platform)


class ClashTeam(PyotCore):
    id: str
    tournament_id: int
    name: str
    icon_id: int
    tier: int
    captain_summoner_id: str
    abbreviation: str
    players: List[ClashPlayerData]

    class Meta(PyotCore.Meta):
        renamed = {"captain": "captain_summoner_id"}
        rules = {"clash_v1_teams": ["id"]}

    def __init__(self, id: str = None, platform: str = None):
        self._lazy_set(locals())

    def _transform(self, data):
        for player in data["players"]:
            player["teamId"] = self.id
        return data

    @property
    def captain(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self.captain_summoner_id, platform=self.platform)

    @property
    def tournament(self) -> "ClashTournament":
        return ClashTournament(id=self.tournament_id, platform=self.platform)


class ClashTournaments(PyotCore):
    tournaments: List[ClashTournamentData]

    class Meta(PyotCore.Meta):
        rules = {"clash_v1_tournaments_all": []}

    def __init__(self, platform: str = None):
        self._lazy_set(locals())

    def __getitem__(self, name):
        if not isinstance(name, int):
            return super().__getitem__(name)
        return self.tournaments[name]

    def __iter__(self) -> List[ClashTournamentData]:
        return iter(self.tournaments)

    def __len__(self):
        return len(self.tournaments)

    def _transform(self, data):
        new_data = {}
        new_data["tournaments"] = data
        return new_data


class ClashTournament(ClashTournamentData, PyotCore):
    team_id: str

    class Meta(PyotCore.Meta):
        rules = {
            "clash_v1_tournaments_by_team_id": ["team_id"],
            "clash_v1_toutnaments_by_tournament_id": ["id"]
        }

    def __init__(self, id: int = None, team_id: str = None, platform: str = None):
        self._lazy_set(locals())

    @property
    def team(self) -> "ClashTeam":
        return ClashTeam(id=self.team_id, platform=self.platform)

    