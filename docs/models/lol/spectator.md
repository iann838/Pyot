# Spectator 

Module: `pyot.models.lol.spectator` 

### _class_ `CurrentGame`

Type: `PyotCore` 

Extends: 
* `pyot.models.lol.spectator.FeaturedGameData` 

Definitions: 
* `__init__` -> `None` 
  * `summoner_id`: `str = empty` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 

Endpoints: 
* `spectator_v4_current_game`: `['summoner_id']` 

Attributes: 
* `id` -> `int` 
* `type` -> `str` 
* `mode` -> `str` 
* `start_time_millis` -> `int` 
* `length_secs` -> `int` 
* `map_id` -> `int` 
* `platform` -> `str` 
* `queue_id` -> `int` 
* `observers_key` -> `str` 
* `teams` -> `List[pyot.models.lol.spectator.CurrentGameTeamData]` 
* `summoner_id` -> `str` 

Properties: 
* _property_ `banned_champions` -> `List[pyot.models.lol.spectator.CurrentGameBansData]` 
* _property_ `blue_team` -> `pyot.models.lol.spectator.CurrentGameTeamData` 
* _property_ `participants` -> `List[pyot.models.lol.spectator.CurrentGameParticipantData]` 
* _property_ `red_team` -> `pyot.models.lol.spectator.CurrentGameTeamData` 
* _property_ `summoner` -> `Summoner` 


### _class_ `FeaturedGames`

Type: `PyotCore` 

Definitions: 
* `__init__` -> `None` 
  * `platform`: `str = models.lol.DEFAULT_PLATFORM` 
* `__iter__` -> `Iterator[pyot.models.lol.spectator.FeaturedGameData]` 
* `__len__` -> `int` 

Endpoints: 
* `spectator_v4_featured_games`: `[]` 

Attributes: 
* `games` -> `List[pyot.models.lol.spectator.FeaturedGameData]` 
* `refresh_interval_secs` -> `int` 

Properties: 
* _property_ `refresh_interval` -> `datetime.timedelta` 


### _class_ `CurrentGameBansData`

Type: `PyotStatic` 

Attributes: 
* `pick_turn` -> `int` 
* `champion_id` -> `int` 
* `team_id` -> `int` 

Properties: 
* _property_ `champion` -> `Champion` 
* _property_ `meraki_champion` -> `MerakiChampion` 


### _class_ `CurrentGameParticipantCustomizationData`

Type: `PyotStatic` 

Attributes: 
* `category` -> `str` 
* `content` -> `str` 


### _class_ `CurrentGameParticipantData`

Type: `PyotStatic` 

Attributes: 
* `team_id` -> `int` 
* `champion_id` -> `int` 
* `profile_icon_id` -> `int` 
* `is_bot` -> `bool` 
* `summoner_name` -> `str` 
* `summoner_id` -> `str` 
* `spell_ids` -> `List[int]` 
* `rune_ids` -> `List[int]` 
* `rune_main_style` -> `int` 
* `rune_sub_style` -> `int` 
* `game_customization_objects` -> `List[pyot.models.lol.spectator.CurrentGameParticipantCustomizationData]` 
* `position` -> `str` 

Properties: 
* _property_ `champion` -> `Champion` 
* _property_ `meraki_champion` -> `MerakiChampion` 
* _property_ `profile_icon` -> `ProfileIcon` 
* _property_ `runes` -> `List[ForwardRef(Rune)]` 
* _property_ `spells` -> `List[ForwardRef(Spell)]` 
* _property_ `summoner` -> `Summoner` 


### _class_ `CurrentGameTeamData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `bans` -> `List[pyot.models.lol.spectator.CurrentGameBansData]` 
* `participants` -> `List[pyot.models.lol.spectator.CurrentGameParticipantData]` 


### _class_ `FeaturedGameData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `type` -> `str` 
* `mode` -> `str` 
* `start_time_millis` -> `int` 
* `length_secs` -> `int` 
* `map_id` -> `int` 
* `platform` -> `str` 
* `queue_id` -> `int` 
* `observers_key` -> `str` 
* `teams` -> `List[pyot.models.lol.spectator.FeaturedGameTeamData]` 

Properties: 
* _property_ `banned_champions` -> `List[pyot.models.lol.spectator.CurrentGameBansData]` 
* _property_ `blue_team` -> `pyot.models.lol.spectator.FeaturedGameTeamData` 
* _property_ `length` -> `datetime.timedelta` 
* _property_ `participants` -> `List[pyot.models.lol.spectator.FeaturedGameParticipantData]` 
* _property_ `red_team` -> `pyot.models.lol.spectator.FeaturedGameTeamData` 
* _property_ `start_time` -> `datetime.datetime` 


### _class_ `FeaturedGameParticipantData`

Type: `PyotStatic` 

Attributes: 
* `team_id` -> `int` 
* `champion_id` -> `int` 
* `profile_icon_id` -> `int` 
* `is_bot` -> `bool` 
* `summoner_name` -> `str` 
* `spell_ids` -> `List[int]` 
* `position` -> `str` 

Properties: 
* _property_ `champion` -> `Champion` 
* _property_ `meraki_champion` -> `MerakiChampion` 
* _property_ `profile_icon` -> `ProfileIcon` 
* _property_ `spells` -> `List[ForwardRef(Spell)]` 
* _property_ `summoner` -> `Summoner` 


### _class_ `FeaturedGameTeamData`

Type: `PyotStatic` 

Attributes: 
* `id` -> `int` 
* `bans` -> `List[pyot.models.lol.spectator.CurrentGameBansData]` 
* `participants` -> `List[pyot.models.lol.spectator.FeaturedGameParticipantData]` 


