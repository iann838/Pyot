from .__core__ import PyotCore
from pyot.pipeline import pipelines


class Account(PyotCore):
    puuid: str
    name: str
    tag: str

    class Meta(PyotCore.Meta):
        rules = {
            "account_v1_by_puuid": ["puuid"],
            "account_v1_by_riot_id": ["name", "tag"],
        }
        renamed = {"game_name": "name", "tag_line": "tag"}

    def __init__(self, puuid: str = None, name: str = None, tag: str = None, region: str = None):
        self._lazy_set(locals())


class ActiveShard(PyotCore):
    puuid: str
    game: str
    shard: str

    class Meta(PyotCore.Meta):
        renamed = {"active_shard": "shard"}
        rules = {"account_v1_active_shard": ["puuid", "game"]}

    def __init__(self, puuid: str = None, game: str = None, region: str = None):
        self._lazy_set(locals())
