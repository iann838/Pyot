# Match 

Module: `pyot.models.lol.match` 

### _class_ Match

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `str` 
  * `region`: `str = models.lol.DEFAULT_REGION` 

Endpoints: 
* `match_v5_match`: `['id']` 

Methods: 
* _method_ `feed_timeline` -> `None` 
  * `timeline`: `Timeline` 
  * `include_assisted`: `bool = False` 
  * `include_victim`: `bool = False` 
  > Parse the given `Timeline` object's frames and events into this match's participants.
  > - `include_assisted`: Include frames and events where the participants are scoring an assist.
  > - `include_victim`: Include frames and events where the participants are victims. 

Attributes: 
* `metadata` -> `pyot.models.lol.match.MatchMetaData` 
* `info` -> `pyot.models.lol.match.MatchInfoData` 
* `id` -> `str` 

Properties: 
* _property_ `region` -> `str` 


### _class_ MatchHistory

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `puuid`: `str` 
  * `region`: `str = models.lol.DEFAULT_REGION` 
* `__iter__` -> `Iterator[pyot.models.lol.match.Match]` 
* `__len__` -> `int` 

Endpoints: 
* `match_v5_matches`: `['puuid']` 

Queries: 
* `start`: `int = 0` 
* `count`: `int = 20` 
* `queue`: `int = None` 
* `type`: `str = None` 
* `start_time`: `Union[int, datetime.datetime] = None` 
* `end_time`: `Union[int, datetime.datetime] = None` 

Attributes: 
* `ids` -> `List[str]` 
* `puuid` -> `str` 

Properties: 
* _property_ `match_timelines` -> `List[Tuple[pyot.models.lol.match.Match, pyot.models.lol.match.Timeline]]` 
* _property_ `matches` -> `List[pyot.models.lol.match.Match]` 
* _property_ `region` -> `str` 
* _property_ `timelines` -> `List[pyot.models.lol.match.Timeline]` 


### _class_ Timeline

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `id`: `str` 
  * `region`: `str = models.lol.DEFAULT_REGION` 

Endpoints: 
* `match_v5_timeline`: `['id']` 

Attributes: 
* `metadata` -> `pyot.models.lol.match.MatchMetaData` 
* `info` -> `pyot.models.lol.match.TimelineInfoData` 
* `id` -> `str` 

Properties: 
* _property_ `region` -> `str` 


### _class_ MatchBanData

Type: `PyotStatic` 

Attributes: 
* `champion_id` -> `int` 
* `pick_turn` -> `int` 

Properties: 
* _property_ `champion` -> `Champion` 
* _property_ `meraki_champion` -> `MerakiChampion` 


### _class_ MatchInfoData

Type: `PyotStatic` 

Attributes: 
* `game_id` -> `int` 
* `creation_millis` -> `int` 
* `duration_units` -> `int` 
* `start_millis` -> `int` 
* `end_millis` -> `int` 
* `mode` -> `str` 
* `name` -> `str` 
* `type` -> `str` 
* `version` -> `str` 
* `platform` -> `str` 
* `map_id` -> `int` 
* `queue_id` -> `int` 
* `tournament_code` -> `str` 
* `participants` -> `List[pyot.models.lol.match.MatchParticipantData]` 
* `teams` -> `List[pyot.models.lol.match.MatchTeamData]` 

Properties: 
* _property_ `creation` -> `datetime.datetime` 
* _property_ `duration` -> `datetime.timedelta` 
* _property_ `duration_millis` -> `int` 
* _property_ `duration_secs` -> `int` 
* _property_ `end` -> `datetime.datetime` 
* _property_ `start` -> `datetime.datetime` 


### _class_ MatchMetaData

Type: `PyotStatic` 

Attributes: 
* `match_id` -> `str` 
* `data_version` -> `str` 
* `participant_puuids` -> `List[str]` 

Properties: 
* _property_ `participants` -> `Summoner` 


### _class_ MatchObjectiveData

Type: `PyotStatic` 

Attributes: 
* `baron` -> `pyot.models.lol.match.MatchObjectiveDetailData` 
* `champion` -> `pyot.models.lol.match.MatchObjectiveDetailData` 
* `dragon` -> `pyot.models.lol.match.MatchObjectiveDetailData` 
* `inhibitor` -> `pyot.models.lol.match.MatchObjectiveDetailData` 
* `rift_herald` -> `pyot.models.lol.match.MatchObjectiveDetailData` 
* `tower` -> `pyot.models.lol.match.MatchObjectiveDetailData` 


### _class_ MatchObjectiveDetailData

Type: `PyotStatic` 

Attributes: 
* `first` -> `bool` 
* `kills` -> `int` 


### _class_ MatchParticipantData

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `assists` -> `int` 
* `baron_kills` -> `int` 
* `bounty_level` -> `int` 
* `champ_experience` -> `int` 
* `champ_level` -> `int` 
* `champion_id` -> `int` 
* `champion_name` -> `str` 
* `champion_transform` -> `int` 
* `consumables_purchased` -> `int` 
* `damage_dealt_to_buildings` -> `int` 
* `damage_dealt_to_objectives` -> `int` 
* `damage_dealt_to_turrets` -> `int` 
* `damage_self_mitigated` -> `int` 
* `deaths` -> `int` 
* `detector_wards_placed` -> `int` 
* `double_kills` -> `int` 
* `dragon_kills` -> `int` 
* `eligible_for_progression` -> `bool` 
* `first_blood_assist` -> `bool` 
* `first_blood_kill` -> `bool` 
* `first_tower_assist` -> `bool` 
* `first_tower_kill` -> `bool` 
* `game_ended_in_early_surrender` -> `bool` 
* `game_ended_in_surrender` -> `bool` 
* `gold_earned` -> `int` 
* `gold_spent` -> `int` 
* `individual_position` -> `str` 
* `inhibitor_kills` -> `int` 
* `inhibitor_takedowns` -> `int` 
* `inhibitors_lost` -> `int` 
* `item0` -> `int` 
* `item1` -> `int` 
* `item2` -> `int` 
* `item3` -> `int` 
* `item4` -> `int` 
* `item5` -> `int` 
* `item6` -> `int` 
* `items_purchased` -> `int` 
* `killing_sprees` -> `int` 
* `kills` -> `int` 
* `lane` -> `str` 
* `largest_critical_strike` -> `int` 
* `largest_killing_spree` -> `int` 
* `largest_multi_kill` -> `int` 
* `longest_time_spent_living_secs` -> `int` 
* `magic_damage_dealt` -> `int` 
* `magic_damage_dealt_to_champions` -> `int` 
* `magic_damage_taken` -> `int` 
* `neutral_minions_killed` -> `int` 
* `nexus_kills` -> `int` 
* `nexus_takedowns` -> `int` 
* `nexus_lost` -> `int` 
* `objectives_stolen` -> `int` 
* `objectives_stolen_assists` -> `int` 
* `penta_kills` -> `int` 
* `perks` -> `pyot.models.lol.match.MatchPerkData` 
* `physical_damage_dealt` -> `int` 
* `physical_damage_dealt_to_champions` -> `int` 
* `physical_damage_taken` -> `int` 
* `profile_icon_id` -> `int` 
* `puuid` -> `str` 
* `quadra_kills` -> `int` 
* `riot_id_name` -> `str` 
* `riot_id_tagline` -> `str` 
* `role` -> `str` 
* `sight_wards_bought_in_game` -> `int` 
* `spell1_casts` -> `int` 
* `spell2_casts` -> `int` 
* `spell3_casts` -> `int` 
* `spell4_casts` -> `int` 
* `summoner1_casts` -> `int` 
* `summoner1_id` -> `int` 
* `summoner2_casts` -> `int` 
* `summoner2_id` -> `int` 
* `summoner_id` -> `str` 
* `summoner_level` -> `int` 
* `summoner_name` -> `str` 
* `team_early_surrendered` -> `bool` 
* `team_id` -> `int` 
* `team_position` -> `str` 
* `time_ccing_others_secs` -> `int` 
* `time_played_secs` -> `int` 
* `total_damage_dealt` -> `int` 
* `total_damage_dealt_to_champions` -> `int` 
* `total_damage_shielded_on_teammates` -> `int` 
* `total_damage_taken` -> `int` 
* `total_heal` -> `int` 
* `total_heals_on_teammates` -> `int` 
* `total_minions_killed` -> `int` 
* `total_time_cc_dealt_secs` -> `int` 
* `total_time_spent_dead_secs` -> `int` 
* `total_units_healed` -> `int` 
* `triple_kills` -> `int` 
* `true_damage_dealt` -> `int` 
* `true_damage_dealt_to_champions` -> `int` 
* `true_damage_taken` -> `int` 
* `turret_kills` -> `int` 
* `turret_takedowns` -> `int` 
* `turrets_lost` -> `int` 
* `unreal_kills` -> `int` 
* `vision_score` -> `int` 
* `vision_wards_bought_in_game` -> `int` 
* `wards_killed` -> `int` 
* `wards_placed` -> `int` 
* `challenges` -> `Dict[str, float]` 
* `frames` -> `List[pyot.models.lol.match.TimelineParticipantFrameData]` 
* `events` -> `List[pyot.models.lol.match.TimelineEventData]` 
* `win` -> `bool` 

Properties: 
* _lazy_property_ `item_ids` -> `List[int]` 
* _property_ `items` -> `List[ForwardRef(Item)]` 
* _property_ `longest_time_spent_living` -> `datetime.timedelta` 
* _property_ `meraki_items` -> `List[ForwardRef(MerakiItem)]` 
* _lazy_property_ `rune_ids` -> `List[int]` 
* _lazy_property_ `rune_primary_style` -> `int` 
* _lazy_property_ `rune_sub_style` -> `int` 
* _property_ `runes` -> `List[ForwardRef(Rune)]` 
* _lazy_property_ `spell_ids` -> `List[int]` 
* _property_ `spells` -> `List[ForwardRef(Spell)]` 
* _lazy_property_ `stat_rune_ids` -> `List[int]` 
* _property_ `summoner` -> `Summoner` 
* _property_ `time_ccing_others` -> `datetime.timedelta` 
* _property_ `time_played` -> `datetime.timedelta` 
* _property_ `total_time_cc_dealt` -> `datetime.timedelta` 
* _property_ `total_time_spent_dead` -> `datetime.timedelta` 


### _class_ MatchPerkData

Type: `PyotStatic` 

Attributes: 
* `stat_perks` -> `pyot.models.lol.match.MatchStatPerkData` 
* `styles` -> `List[pyot.models.lol.match.MatchPerkStyleData]` 


### _class_ MatchPerkSelectionData

Type: `PyotStatic` 

Attributes: 
* `perk` -> `int` 
* `var1` -> `int` 
* `var2` -> `int` 
* `var3` -> `int` 


### _class_ MatchPerkStyleData

Type: `PyotStatic` 

Attributes: 
* `description` -> `str` 
* `selections` -> `List[pyot.models.lol.match.MatchPerkSelectionData]` 
* `style` -> `int` 


### _class_ MatchStatPerkData

Type: `PyotStatic` 

Attributes: 
* `offense` -> `int` 
* `flex` -> `int` 
* `defense` -> `int` 


### _class_ MatchTeamData

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `win` -> `bool` 
* `bans` -> `List[pyot.models.lol.match.MatchBanData]` 
* `objectives` -> `pyot.models.lol.match.MatchObjectiveData` 

Properties: 
* _property_ `participants` -> `List[ForwardRef(MatchParticipantData)]` 


### _class_ TimelineChampionStatData

Type: `PyotStatic` 

Attributes: 
* `ability_haste` -> `int` 
* `ability_power` -> `int` 
* `armor` -> `int` 
* `armor_pen` -> `int` 
* `armor_pen_percent` -> `int` 
* `attack_damage` -> `int` 
* `attack_speed` -> `int` 
* `bonus_armor_pen_percent` -> `int` 
* `bonus_magic_pen_percent` -> `int` 
* `cc_reduction` -> `int` 
* `cooldown_reduction` -> `int` 
* `health` -> `int` 
* `health_max` -> `int` 
* `health_regen` -> `int` 
* `lifesteal` -> `int` 
* `magic_pen` -> `int` 
* `magic_pen_percent` -> `int` 
* `magic_resist` -> `int` 
* `movement_speed` -> `int` 
* `omnivamp` -> `int` 
* `physical_vamp` -> `int` 
* `power` -> `int` 
* `power_max` -> `int` 
* `power_regen` -> `int` 
* `spell_vamp` -> `int` 


### _class_ TimelineDamageStatData

Type: `PyotStatic` 

Attributes: 
* `magic_damage_done` -> `int` 
* `magic_damage_done_to_champions` -> `int` 
* `magic_damage_taken` -> `int` 
* `physical_damage_done` -> `int` 
* `physical_damage_done_to_champions` -> `int` 
* `physical_damage_taken` -> `int` 
* `total_damage_done` -> `int` 
* `total_damage_done_to_champions` -> `int` 
* `total_damage_taken` -> `int` 
* `true_damage_done` -> `int` 
* `true_damage_done_to_champions` -> `int` 
* `true_damage_taken` -> `int` 


### _class_ TimelineEventData

Type: `PyotStatic` 

Attributes: 
* `actual_start_time_millis` -> `int` 
* `ascended_type` -> `str` 
* `assisting_participant_ids` -> `List[int]` 
* `after_id` -> `int` 
* `before_id` -> `int` 
* `bounty` -> `int` 
* `building_type` -> `str` 
* `creator_id` -> `int` 
* `event_type` -> `str` 
* `game_id` -> `int` 
* `gold_gain` -> `int` 
* `item_id` -> `int` 
* `kill_streak_length` -> `int` 
* `kill_type` -> `str` 
* `killer_id` -> `int` 
* `killer_team_id` -> `int` 
* `lane_type` -> `str` 
* `level` -> `int` 
* `level_up_type` -> `str` 
* `monster_type` -> `str` 
* `monster_sub_type` -> `str` 
* `multi_kill_length` -> `int` 
* `name` -> `str` 
* `participant_id` -> `int` 
* `point_captured` -> `str` 
* `position` -> `pyot.models.lol.match.TimelinePositionData` 
* `real_timestamp` -> `int` 
* `skill_slot` -> `int` 
* `shutdown_bounty` -> `int` 
* `team_id` -> `int` 
* `timestamp` -> `int` 
* `transform_type` -> `str` 
* `type` -> `str` 
* `tower_type` -> `str` 
* `victim_id` -> `int` 
* `victim_damage_dealt` -> `List[pyot.models.lol.match.TimelineVictimDamageData]` 
* `victim_damage_received` -> `List[pyot.models.lol.match.TimelineVictimDamageData]` 
* `ward_type` -> `str` 
* `winning_team` -> `int` 

Properties: 
* _property_ `actual_start_time` -> `datetime.timedelta` 
* _property_ `after_item` -> `Item` 
* _property_ `before_item` -> `Item` 
* _property_ `item` -> `Item` 
* _property_ `meraki_after_item` -> `MerakiItem` 
* _property_ `meraki_before_item` -> `MerakiItem` 
* _property_ `meraki_item` -> `MerakiItem` 
* _property_ `real_time` -> `datetime.datetime` 
* _property_ `time` -> `datetime.timedelta` 


### _class_ TimelineFrameData

Type: `PyotStatic` 

Attributes: 
* `events` -> `List[pyot.models.lol.match.TimelineEventData]` 
* `participant_frames` -> `List[pyot.models.lol.match.TimelineParticipantFrameData]` 
* `timestamp` -> `int` 

Properties: 
* _property_ `time` -> `datetime.timedelta` 


### _class_ TimelineInfoData

Type: `PyotStatic` 

Attributes: 
* `frame_interval_millis` -> `int` 
* `frames` -> `List[pyot.models.lol.match.TimelineFrameData]` 
* `game_id` -> `int` 
* `participants` -> `List[pyot.models.lol.match.TimelineParticipantData]` 

Properties: 
* _property_ `frame_interval` -> `datetime.timedelta` 


### _class_ TimelineParticipantData

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `puuid` -> `str` 

Properties: 
* _property_ `summoner` -> `Summoner` 


### _class_ TimelineParticipantFrameData

Type: `PyotStatic` 

Attributes: 
* `champion_stats` -> `pyot.models.lol.match.TimelineChampionStatData` 
* `current_gold` -> `int` 
* `damage_stats` -> `pyot.models.lol.match.TimelineDamageStatData` 
* `gold_per_second` -> `int` 
* `jungle_minions_killed` -> `int` 
* `level` -> `int` 
* `minions_killed` -> `int` 
* `participant_id` -> `int` 
* `position` -> `pyot.models.lol.match.TimelinePositionData` 
* `time_enemy_spent_controlled_millis` -> `int` 
* `total_gold` -> `int` 
* `xp` -> `int` 

Properties: 
* _property_ `time_enemy_spent_controlled` -> `datetime.timedelta` 


### _class_ TimelinePositionData

Type: `PyotStatic` 

Attributes: 
* `x` -> `int` 
* `y` -> `int` 


### _class_ TimelineVictimDamageData

Type: `PyotStatic` 

Attributes: 
* `basic` -> `bool` 
* `magic_damage` -> `int` 
* `name` -> `str` 
* `participant_id` -> `int` 
* `physical_damage` -> `int` 
* `spell_name` -> `str` 
* `spell_slot` -> `int` 
* `true_damage` -> `int` 
* `type` -> `str` 


