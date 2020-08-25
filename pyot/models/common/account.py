from .__core__ import PyotCoreObject


class AccountObject(PyotCoreObject):
    puuid: str
    name: str
    tag: str

    class Meta:
        rules = {
            "account_v1_by_puuid": ["puuid"],
            "account_v1_by_riot_id": ["name", "tag"],
        }
        renamed = {"game_name": "name", "tag_line": "tag"}

    def __init__(self, puuid: str = None, name: str = None, tag: str = None, region: str = None):
        self._lazy_set(locals())


class ActivePlatformObject(PyotCoreObject):
    puuid: str
    game: str
    platform_id: str

    class Meta:
        renamed = {"active_shard": "platform_id"}
        rules = {"account_v1_active_shard": ["game", "puuid"]}

    def __init__(self, puuid: str = None, game: str = None, region: str = None):
        self._lazy_set(locals())
