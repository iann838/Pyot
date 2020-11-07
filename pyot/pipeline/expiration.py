from typing import Dict
from datetime import timedelta as td
import copy

from logging import getLogger
LOGGER = getLogger(__name__)


class ExpirationManager:
    _riot_expirations = {
        "account_v1_by_puuid": 0,
        "account_v1_by_riot_id": 0,
        "account_v1_active_shard": 0,
    }

    _expirations = {
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
            "status_v3_shard_data": 0,
            "match_v4_match": 0,
            "match_v4_timeline": 0,
            "match_v4_matchlist": 0,
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

            "cdragon_champion_by_id": td(hours=3),
            "cdragon_item_full": td(hours=3),
            "cdragon_rune_full": td(hours=3),
            "cdragon_profile_icon_full": td(hours=3),
            "cdragon_spells_full": td(hours=3),

            "meraki_champion_by_key": td(hours=3),
            "meraki_item_by_id": td(hours=3),
        },
        "lor": {
            "ranked_v1_leaderboards": 0,
            "match_v1_matchlist": 0,
            "match_v1_match": 0,
            "ddragon_lor_set_data": td(hours=3),
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

            "cdragon_tft_full": td(hours=3),
            "cdragon_profile_icon_full": td(hours=3),
        },
        "val": {
            "match_v1_match": 0,
            "match_v1_matchlist": 0,
            "match_v1_recent": 0,
            "content_v1_contents": 0,
        }
    }

    def __init__(self, game, custom_expirations: Dict):
        self.expirations = copy.deepcopy(self._expirations[game])
        self.expirations.update(copy.deepcopy(self._riot_expirations))
        if custom_expirations is not None:
            for key in custom_expirations:
                if key not in self.expirations:
                    raise RuntimeError(f"'{key}' is not a valid expiration token")
            self.expirations.update(custom_expirations)
        self.expirations = self._create_expiration(self.expirations)

    def _create_expiration(self, expirations):
        expirations_ = {}
        for key, time in expirations.items():
            if type(time) is td:
                expirations_[key] = int(time.total_seconds())
            else:
                try:
                    expirations_[key] = int(time)
                except Exception:
                    raise AttributeError(f"Expiration value not allowed, {type(expirations_[key])} was given")
        return expirations_
        
    def get_timeout(self, key):
        try:
            return self.expirations[key]
        except KeyError:
            LOGGER.warning("[Trace: Pyot Pipeline] WARNING: A non defined expiration token was passed, returned 0 by default")
            return 0

    def __iter__(self):
        return iter(self.expirations)

    def __len__(self):
        return len(self.expirations)
