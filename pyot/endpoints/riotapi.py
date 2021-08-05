
from typing import Dict
from pyot.pipeline.token import PipelineToken
from .base import BaseEndpoint


class RiotAPIEndpoint(BaseEndpoint):

    base_url = "https://{server}.api.riotgames.com"

    shared = {
        "account_v1_by_puuid": "/riot/account/v1/accounts/by-puuid/{puuid}",
        "account_v1_by_riot_id": "/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}",
        "account_v1_active_shard": "/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}",
    }

    all = {
        "lol": {
            "champion_v3_rotation": "/lol/platform/v3/champion-rotations",
            "champion_mastery_v4_by_champion_id": "/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}/by-champion/{champion_id}",
            "champion_mastery_v4_all_mastery": "/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}",
            "clash_v1_players": "/lol/clash/v1/players/by-summoner/{summoner_id}",
            "clash_v1_teams": "/lol/clash/v1/teams/{id}",
            "clash_v1_tournaments_by_team_id": "/lol/clash/v1/tournaments/by-team/{team_id}",
            "clash_v1_toutnaments_by_tournament_id": "/lol/clash/v1/tournaments/{id}",
            "clash_v1_tournaments_all": "/lol/clash/v1/tournaments",
            "league_v4_summoner_entries": "/lol/league/v4/entries/by-summoner/{summoner_id}",
            "league_v4_challenger_league": "/lol/league/v4/challengerleagues/by-queue/{queue}",
            "league_v4_grandmaster_league": "/lol/league/v4/grandmasterleagues/by-queue/{queue}",
            "league_v4_master_league": "/lol/league/v4/masterleagues/by-queue/{queue}",
            "league_v4_entries_by_division": "/lol/league/v4/entries/{queue}/{tier}/{division}",
            "league_v4_league_by_league_id": "/lol/league/v4/leagues/{id}",
            "status_v4_platform_data": "/lol/status/v4/platform-data",
            "match_v4_match": "/lol/match/v4/matches/{id}",
            "match_v4_timeline": "/lol/match/v4/timelines/by-match/{id}",
            "match_v4_matchlist": "/lol/match/v4/matchlists/by-account/{account_id}",
            "match_v4_tournament_match": "/lol/match/v4/matches/{id}/by-tournament-code/{tournament_code}",
            "match_v4_tournament_matches": "/lol/match/v4/matches/by-tournament-code/{tournament_code}/ids",
            "match_v5_match": "/lol/match/v5/matches/{id}",
            "match_v5_timeline": "/lol/match/v5/matches/{id}/timeline",
            "match_v5_matches": "/lol/match/v5/matches/by-puuid/{puuid}/ids",
            "spectator_v4_current_game": "/lol/spectator/v4/active-games/by-summoner/{summoner_id}",
            "spectator_v4_featured_games": "/lol/spectator/v4/featured-games",
            "summoner_v4_by_name": "/lol/summoner/v4/summoners/by-name/{name}",
            "summoner_v4_by_id": "/lol/summoner/v4/summoners/{id}",
            "summoner_v4_by_account_id": "/lol/summoner/v4/summoners/by-account/{account_id}",
            "summoner_v4_by_puuid": "/lol/summoner/v4/summoners/by-puuid/{puuid}",
            "third_party_code_v4_code": "/lol/platform/v4/third-party-code/by-summoner/{summoner_id}",
            "tournament_v4_codes": "/lol/tournament/v4/codes",
            "tournament_v4_codes_by_code": "/lol/tournament/v4/codes/{code}",
            "tournament_v4_lobby_events": "/lol/tournament/v4/lobby-events/by-code/{code}",
            "tournament_v4_providers": "/lol/tournament/v4/providers",
            "tournament_v4_tournaments": "/lol/tournament/v4/tournaments",
            "tournament_stub_v4_codes": "/lol/tournament-stub/v4/codes",
            "tournament_stub_v4_lobby_events": "/lol/tournament-stub/v4/lobby-events/by-code/{code}",
            "tournament_stub_v4_providers": "/lol/tournament-stub/v4/providers",
            "tournament_stub_v4_tournaments": "/lol/tournament-stub/v4/tournaments",
        },
        "tft": {
            "league_v1_summoner_entries": "/tft/league/v1/entries/by-summoner/{summoner_id}",
            "league_v1_challenger_league": "/tft/league/v1/challenger",
            "league_v1_grandmaster_league": "/tft/league/v1/grandmaster",
            "league_v1_master_league": "/tft/league/v1/master",
            "league_v1_entries_by_division": "/tft/league/v1/entries/{tier}/{division}",
            "league_v1_league_by_league_id": "/tft/league/v1/leagues/{id}",
            "match_v1_matchlist": "/tft/match/v1/matches/by-puuid/{puuid}/ids",
            "match_v1_match": "/tft/match/v1/matches/{id}",
            "summoner_v1_by_name": "/tft/summoner/v1/summoners/by-name/{name}",
            "summoner_v1_by_id": "/tft/summoner/v1/summoners/{id}",
            "summoner_v1_by_account_id": "/tft/summoner/v1/summoners/by-account/{account_id}",
            "summoner_v1_by_puuid": "/tft/summoner/v1/summoners/by-puuid/{puuid}",
        },
        "lor": {
            "ranked_v1_leaderboards": "/lor/ranked/v1/leaderboards",
            "match_v1_matchlist": "/lor/match/v1/matches/by-puuid/{puuid}/ids",
            "match_v1_match": "/lor/match/v1/matches/{id}",
            "status_v1_platform_data": "/lor/status/v1/platform-data",
        },
        "val": {
            "match_v1_match": "/val/match/v1/matches/{id}",
            "match_v1_matchlist": "/val/match/v1/matchlists/by-puuid/{puuid}",
            "match_v1_recent": "/val/match/v1/recent-matches/by-queue/{queue}",
            "content_v1_contents": "/val/content/v1/contents",
            "ranked_v1_leaderboards": "/val/ranked/v1/leaderboards/by-act/{act_id}",
            "status_v1_platform_data": "/val/status/v1/platform-data",
        }
    }

    def clean(self, token: PipelineToken) -> Dict[str, str]:
        return {
            "server": token.server,
            **token.params,
        }
