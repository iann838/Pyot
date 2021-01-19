# Version 2 → 3

This guide **covers only backward imcompatible changes** and the necessary steps for migrating Pyot 2 to Pyot 3. For Pyot 3 release notes please head to releases.

## Major changes

List of major changes in Pyot 3.

### `lol.MatchTimeline` has been removed.
> `lol.Match` constructor will have an extra param `include_timeline` that calls `lol.Timeline.get` and inject the events and frames to each of the participants.
> ```python
> match = lol.Match(id=match_id, include_timeline=True)
> ```

### `lol.Timeline` reworked.
> Core `lol.Timeline` will not longer transform the data into `{frames: [[],], events: []}` format, it now instead uses a closer formatting to the one returned by the Riot API: `{frames: [{participantFrames: [], events: [], interval: x}],}` (Transformation of the 1~10 index participantFrames into a list remains).

### `ptr_cache` param of `get` method of `PyotCore` objects removed.
> Removed due to low benefit and the need of extra handling on filtered result. The use leaves 2 problems that is not solved: 1) Unnecessary instantiation of classes; 2) Generation of pipeline token does not account filtered params. Please use `PtrCache` in its standard way and its new `lazy` param for delaying instantiation of classes.

### `keep_raw` param of `get` method of `PyotCore` objects replaced.
> Since Pyot 3, raw response is always saved, the transformer that mutates the dict will do **smart copying** achieve non-destructive mutations, however slight differences might exist compared to original response, to save the actual original response please set the new `deepcopy` param to `True`.

### `json` method of `PyotCore` objects removed.
> Since the new method `raw()` is now always accessible, this method feels out, developer should json encode the data they choose.

### `dict` method of `PyotCore` objects reworked.
> `pyotify` param has renamed to `recursive`. Two new optional params are addded.

### Static objects absolute urls are now lazy.
> All urls of CDragon objects were already modified, this adds extra serialization when it is not needed. They are now migrated to `lazy_property` in a syntax of `*_abspath`, object `dict` method will not return these properties by default, to return it, pass `lazy_props=True` param to `dict()` method.

### Pyot Queue will NO longer handle non-Pyot exceptions.
> The supressing was originally designed to avoid log overload, but turned out to brutantly affect the debug process. Shrinking the fench down to Pyot Specific exceptions. Note: This will only let the python interpreter raise the exception and log the traceback, the Queue WILL NOT STOP running.

## Minor changes

List of minor changes in Pyot 3.

### `Match` object dict will no longer return `blue_team` nor `red_team`.
> This adds extra repeated serialization and outbound data transfer, migrated to property and thus, `dict()` will not return it.

### `lol.match.MatchTeamData.team_id` renamed.
> Attribute `team_id` from `lol.match.MatchTeamData` (Core Parent: `lol.Match`) has been renamed to `id`

### `lol.match.MatchEventData.timestamp` no longer returns timedelta.
> This object is serialized by mass, old version retuns timedelta by modifying `__getattribute__` dunder method which adds extra overhead and its one of the cause of slow serialization, a new property `time` will return what `timestamp` use to return, please use that instead.

### `lol.match.MatchParticipantStatData.rune_style` renamed.
> A more suited attribute name is `rune_main_style`.

### All deltas in `lol.match.MatchParticipantTimelineData` will not be parsed anymore.
> All deltas returned is dependant of the `role` and `lane` returned by the Riot API, and we all know how ~~inaccurate~~ massive is the spaghetti algorithm that Riot uses to calculate them. Makes no sense to spend CPU time to parse unreliable data. They are now returned as dict.

### Timeline now also injects events related to victim in `lol.Match`.
> Now also injects to participants timelines where the `victimId` of the event matches. To avoid taking account of wrong data, always validate `killerId` or `killer_id`.

### `lol.FeaturedGame.queue` renamed.
> A more suited attribute name is `queue_id`. This also affects to the inherited object `lol.CurrentGame`

### `val.match.MatchPlayerKillData.game_duration` and `val.match.MatchPlayerKillData.round_duration` renamed.
> A more suited attribute name is `game_time`.
> A more suited attribute name is `round_time`.

### region, platform, locale will no longer be lowercase forever.
> For scenario where you need to validate against a database in choices (e.g. Django's ORM `choices` param), just `.lower()` instead.
