from typing import Dict
from datetime import timedelta as td
import copy

from pyot.utils.logging import Logger


LOGGER = Logger(__name__)


class ExpirationManager:

    shared: Dict[str, int] = {
        "account_v1_by_puuid": 0,
        "account_v1_by_riot_id": 0,
        "account_v1_active_shard": 0,
    }

    all: Dict[str, Dict] = {
        "lol": {
            "champion_v3_rotation": 0,
            "champion_mastery_v4_all_mastery": 0,
            "champion_mastery_v4_by_champion_id": 0,
            "clash_v1_players": 0,
            "clash_v1_teams": 0,
            "clash_v1_tournaments_by_team_id": 0,
            "clash_v1_toutnaments_by_tournament_id": 0,
            "clash_v1_tournaments_all": 0,
            "league_v4_summoner_entries": 0,
            "league_v4_challenger_league": 0,
            "league_v4_grandmaster_league": 0,
            "league_v4_master_league": 0,
            "league_v4_entries_by_division": 0,
            "league_v4_league_by_league_id": 0,
            "status_v4_platform_data": 0,
            "match_v4_match": 0,
            "match_v4_timeline": 0,
            "match_v4_matchlist": 0,
            "match_v4_tournament_match": 0,
            "match_v4_tournament_matches": 0,
            "match_v5_match": 0,
            "match_v5_timeline": 0,
            "match_v5_matches": 0,
            "spectator_v4_current_game": 0,
            "spectator_v4_featured_games": 0,
            "summoner_v4_by_name": 0,
            "summoner_v4_by_id": 0,
            "summoner_v4_by_account_id": 0,
            "summoner_v4_by_puuid": 0,
            "third_party_code_v4_code": 0,
            "tournament_v4_codes_by_code": 0,
            "tournament_v4_lobby_events": 0,
            "tournament_stub_v4_lobby_events": 0,

            "cdragon_champion_by_id": td(minutes=20),
            "cdragon_champion_summary": td(minutes=20),
            "cdragon_item_full": td(minutes=20),
            "cdragon_rune_full": td(minutes=20),
            "cdragon_profile_icon_full": td(minutes=20),
            "cdragon_spells_full": td(minutes=20),

            "meraki_champion_by_key": td(minutes=20),
            "meraki_item_by_id": td(minutes=20),
        },
        "lor": {
            "ranked_v1_leaderboards": 0,
            "match_v1_matchlist": 0,
            "match_v1_match": 0,
            "ddragon_lor_set_data": td(minutes=20),
            "status_v1_platform_data": 0,
        },
        "tft": {
            "league_v1_summoner_entries": 0,
            "league_v1_challenger_league": 0,
            "league_v1_grandmaster_league": 0,
            "league_v1_master_league": 0,
            "league_v1_entries_by_division": 0,
            "league_v1_league_by_league_id": 0,
            "match_v1_match": 0,
            "match_v1_matchlist": 0,
            "summoner_v1_by_name": 0,
            "summoner_v1_by_id": 0,
            "summoner_v1_by_account_id": 0,
            "summoner_v1_by_puuid": 0,

            "cdragon_tft_full": td(minutes=20),
            "cdragon_profile_icon_full": td(minutes=20),
        },
        "val": {
            "match_v1_match": 0,
            "match_v1_matchlist": 0,
            "match_v1_recent": 0,
            "content_v1_contents": 0,
            "ranked_v1_leaderboards": 0,
            "status_v1_platform_data": 0,
        }
    }

    def __init__(self, game: str, custom_expirations: Dict):
        self.expirations = copy.deepcopy(self.all[game])
        self.expirations.update(copy.deepcopy(self.shared))
        if custom_expirations is not None:
            for key in custom_expirations:
                if key not in self.expirations:
                    raise RuntimeError(f"'{key}' is not a valid expiration token")
            self.expirations.update(custom_expirations)
        self.expirations = self.create_expiration(self.expirations)

    def create_expiration(self, expirations):
        expirations_ = {}
        for key, time in expirations.items():
            if isinstance(time, td):
                expirations_[key] = int(time.total_seconds())
            else:
                try:
                    expirations_[key] = int(time)
                except Exception as e:
                    raise AttributeError(f"Expiration value type error, {type(expirations_[key])} was given") from e
        return expirations_

    def get_timeout(self, key):
        try:
            return self.expirations[key]
        except KeyError:
            LOGGER.warning("[Trace: Pyot Pipeline] WARN: A non defined expiration token was passed, returned 0 by default")
            return 0

    def __iter__(self):
        return iter(self.expirations)

    def __len__(self):
        return len(self.expirations)
