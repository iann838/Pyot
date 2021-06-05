# THIS IS ONLY A CONCEPT, NOT IMPLEMENTED YET

from typing import Dict
import copy

from pyot.utils.logging import Logger

LOGGER = Logger(__name__)


def pass_all(_):
    return True


class Filterer:

    shared = {
        "account_v1_by_puuid": pass_all,
        "account_v1_by_riot_id": pass_all,
        "account_v1_active_shard": pass_all,
    }

    all = {
        "lol": {
            "champion_v3_rotation": pass_all,
            "champion_mastery_v4_all_mastery": pass_all,
            "champion_mastery_v4_by_champion_id": pass_all,
            "clash_v1_players": pass_all,
            "clash_v1_teams": pass_all,
            "clash_v1_tournaments_by_team_id": pass_all,
            "clash_v1_toutnaments_by_tournament_id": pass_all,
            "clash_v1_tournaments_all": pass_all,
            "league_v4_summoner_entries": pass_all,
            "league_v4_challenger_league": pass_all,
            "league_v4_grandmaster_league": pass_all,
            "league_v4_master_league": pass_all,
            "league_v4_entries_by_division": pass_all,
            "league_v4_league_by_league_id": pass_all,
            "status_v3_shard_data": pass_all,
            "match_v4_match": pass_all,
            "match_v4_timeline": pass_all,
            "match_v4_matchlist": pass_all,
            "spectator_v4_current_game": pass_all,
            "spectator_v4_featured_games": pass_all,
            "summoner_v4_by_name": pass_all,
            "summoner_v4_by_id": pass_all,
            "summoner_v4_by_account_id": pass_all,
            "summoner_v4_by_puuid": pass_all,
            "third_party_code_v4_code": pass_all,

            "cdragon_champion_by_id": pass_all,
            "cdragon_item_full": pass_all,
            "cdragon_rune_full": pass_all,
            "cdragon_profile_icon_full": pass_all,
            "cdragon_spells_full": pass_all,

            "meraki_champion_by_key": pass_all,
            "meraki_item_by_id": pass_all,
        },
        "tft": {
            "league_v1_summoner_entries": pass_all,
            "league_v1_challenger_league": pass_all,
            "league_v1_grandmaster_league": pass_all,
            "league_v1_master_league": pass_all,
            "league_v1_entries_by_division": pass_all,
            "league_v1_league_by_league_id": pass_all,
            "match_v1_match": pass_all,
            "match_v1_matchlist": pass_all,
            "summoner_v1_by_name": pass_all,
            "summoner_v1_by_id": pass_all,
            "summoner_v1_by_account_id": pass_all,
            "summoner_v1_by_puuid": pass_all,

            "cdragon_tft_full": pass_all,
            "cdragon_profile_icon_full": pass_all,
        },
        "val": {
            "match_v1_match": pass_all,
            "match_v1_matchlist": pass_all,
            "match_v1_recent": pass_all,
            "content_v1_contents": pass_all,
        }
    }

    def __init__(self, game, custom_filters: Dict):
        self.filters = copy.deepcopy(self.all[game])
        self.filters.update(copy.deepcopy(self.shared))
        if custom_filters is not None:
            for key in custom_filters:
                if key not in self.filters:
                    raise RuntimeError(f"'{key}' is not a valid expiration token")
            self.filters.update(custom_filters)
        self.filters = self.create_filters(self.filters)

    def create_filters(self, filters):
        filters_ = {}
        for key, func in filters.items():
            if not callable(func):
                raise RuntimeError(f"Value for '{key}' is not callable")
        return filters_

    def get_filter(self, key):
        try:
            return self.filters[key]
        except KeyError:
            LOGGER.warning("[Trace: Pyot Pipeline] WARN: A non defined key was passed, returned True by default")
            return pass_all
