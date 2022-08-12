# Match 

Module: `pyot.models.val.match` 

### _class_ `Match`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `str = None` 
  * `platform`: `str = models.val.DEFAULT_PLATFORM` 

Endpoints: 
* `match_v1_match`: `['id']` 

Attributes: 
* `id` -> `str` 
* `info` -> `pyot.models.val.match.MatchInfoData` 
* `players` -> `List[pyot.models.val.match.MatchPlayerData]` 
* `teams` -> `List[pyot.models.val.match.MatchTeamData]` 
* `coaches` -> `List[pyot.models.val.match.MatchCoachData]` 
* `round_results` -> `List[pyot.models.val.match.MatchRoundResultData]` 
* `start_time_millis` -> `int` 
* `team_id` -> `str` 
* `queue_id` -> `str` 

Properties: 
* _property_ `start_time` -> `datetime.datetime` 


### _class_ `MatchHistory`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `puuid`: `str = None` 
  * `platform`: `str = models.val.DEFAULT_PLATFORM` 
* `__iter__` -> `Iterator[pyot.models.val.match.Match]` 
* `__len__` -> `int` 

Endpoints: 
* `match_v1_matchlist`: `['puuid']` 

Attributes: 
* `puuid` -> `str` 
* `history` -> `List[pyot.models.val.match.Match]` 

Properties: 
* _property_ `account` -> `Account` 


### _class_ `RecentMatches`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `queue`: `str = None` 
  * `platform`: `str = models.val.DEFAULT_PLATFORM` 
* `__iter__` -> `Iterator[pyot.models.val.match.Match]` 
* `__len__` -> `int` 

Endpoints: 
* `match_v1_recent`: `['queue']` 

Attributes: 
* `current_timestamp` -> `int` 
* `match_ids` -> `List[str]` 

Properties: 
* _property_ `current_time` -> `datetime.datetime` 
* _property_ `matches` -> `List[pyot.models.val.match.Match]` 


### _class_ `MatchCoachData`

Type: `PyotStatic` 

Attributes: 
* `puuid` -> `str` 
* `team_id` -> `str` 


### _class_ `MatchInfoData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `str` 
* `map_url` -> `str` 
* `start_millis` -> `int` 
* `length_millis` -> `int` 
* `provisioning_flow_id` -> `str` 
* `is_completed` -> `bool` 
* `custom_game_name` -> `str` 
* `queue_id` -> `str` 
* `game_mode` -> `str` 
* `game_version` -> `str` 
* `is_ranked` -> `bool` 
* `season_id` -> `str` 

Properties: 
* _property_ `length` -> `datetime.timedelta` 
* _property_ `start` -> `datetime.datetime` 


### _class_ `MatchLocationData`

Type: `PyotStatic` 

Attributes: 
* `x` -> `int` 
* `y` -> `int` 


### _class_ `MatchPlayerAbilityCastData`

Type: `PyotStatic` 

Attributes: 
* `grenade_casts` -> `int` 
* `ability1_casts` -> `int` 
* `ability2_casts` -> `int` 
* `ultimate_casts` -> `int` 


### _class_ `MatchPlayerAbilityData`

Type: `PyotStatic` 

Attributes: 
* `grenade_effects` -> `int` 
* `ability1_effects` -> `int` 
* `ability2_effects` -> `int` 
* `ultimate_effects` -> `int` 


### _class_ `MatchPlayerDamageData`

Type: `PyotStatic` 

Attributes: 
* `receiver` -> `str` 
* `damage` -> `int` 
* `legshots` -> `int` 
* `bodyshots` -> `int` 
* `headshots` -> `int` 


### _class_ `MatchPlayerData`

Type: `PyotStatic` 

Attributes: 
* `puuid` -> `str` 
* `game_name` -> `str` 
* `tag_line` -> `str` 
* `team_id` -> `str` 
* `party_id` -> `str` 
* `character_id` -> `str` 
* `stats` -> `pyot.models.val.match.MatchPlayerStatData` 
* `competitive_tier` -> `int` 
* `player_card_id` -> `str` 
* `player_title_id` -> `str` 

Properties: 
* _property_ `account` -> `Account` 


### _class_ `MatchPlayerEconomyData`

Type: `PyotStatic` 

Attributes: 
* `loadout_value` -> `int` 
* `weapon_id` -> `str` 
* `armor_id` -> `str` 
* `remaining` -> `int` 
* `spent` -> `int` 


### _class_ `MatchPlayerFinishingDamageData`

Type: `PyotStatic` 

Attributes: 
* `damage_type` -> `str` 
* `damage_item` -> `str` 
* `is_secondary_fire_mode` -> `bool` 


### _class_ `MatchPlayerKillData`

Type: `PyotStatic` 

Attributes: 
* `game_time_millis` -> `int` 
* `round_time_millis` -> `int` 
* `killer_puuid` -> `str` 
* `victim_puuid` -> `str` 
* `victim_location` -> `pyot.models.val.match.MatchLocationData` 
* `assistant_puuids` -> `List[str]` 
* `player_locations` -> `List[pyot.models.val.match.MatchPlayerLocationData]` 
* `finishing_damage` -> `pyot.models.val.match.MatchPlayerFinishingDamageData` 

Properties: 
* _property_ `assistants` -> `List[ForwardRef(Account)]` 
* _property_ `game_time` -> `datetime.timedelta` 
* _property_ `killer` -> `Account` 
* _property_ `round_time` -> `datetime.timedelta` 
* _property_ `victim` -> `Account` 


### _class_ `MatchPlayerLocationData`

Type: `PyotStatic` 

Attributes: 
* `puuid` -> `str` 
* `view_radians` -> `float` 
* `location` -> `pyot.models.val.match.MatchLocationData` 


### _class_ `MatchPlayerRoundStatData`

Type: `PyotStatic` 

Attributes: 
* `puuid` -> `str` 
* `kills` -> `List[pyot.models.val.match.MatchPlayerKillData]` 
* `damage` -> `List[pyot.models.val.match.MatchPlayerDamageData]` 
* `score` -> `int` 
* `economy` -> `pyot.models.val.match.MatchPlayerEconomyData` 
* `ability` -> `pyot.models.val.match.MatchPlayerAbilityData` 


### _class_ `MatchPlayerStatData`

Type: `PyotStatic` 

Attributes: 
* `score` -> `int` 
* `rounds_played` -> `int` 
* `kills` -> `int` 
* `deaths` -> `int` 
* `assists` -> `int` 
* `playtime_millis` -> `int` 
* `ability_casts` -> `pyot.models.val.match.MatchPlayerAbilityCastData` 

Properties: 
* _property_ `playtime` -> `datetime.timedelta` 


### _class_ `MatchRoundResultData`

Type: `PyotStatic` 

Attributes: 
* `round_num` -> `int` 
* `round_result` -> `str` 
* `round_ceremony` -> `str` 
* `winning_team` -> `str` 
* `bomb_planter_puuid` -> `str` 
* `bomb_defuser_puuid` -> `str` 
* `plant_round_millis` -> `int` 
* `plant_player_locations` -> `List[pyot.models.val.match.MatchPlayerLocationData]` 
* `plant_location` -> `pyot.models.val.match.MatchLocationData` 
* `plant_site` -> `str` 
* `defuse_round_millis` -> `int` 
* `defuse_player_locations` -> `List[pyot.models.val.match.MatchPlayerLocationData]` 
* `defuse_location` -> `pyot.models.val.match.MatchLocationData` 
* `player_stats` -> `List[pyot.models.val.match.MatchPlayerRoundStatData]` 
* `round_result_code` -> `str` 

Properties: 
* _property_ `bomb_defuser` -> `Account` 
* _property_ `bomb_planter` -> `Account` 
* _property_ `defuse_round_time` -> `datetime.timedelta` 
* _property_ `plant_round_time` -> `datetime.timedelta` 


### _class_ `MatchTeamData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `str` 
* `won` -> `bool` 
* `rounds_played` -> `int` 
* `rounds_won` -> `int` 
* `num_points` -> `int` 


