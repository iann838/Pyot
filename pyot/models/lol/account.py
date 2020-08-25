from ..common.account import AccountObject, ActivePlatformObject
from .__core__ import PyotCore


class Account(AccountObject, PyotCore):

    class Meta(AccountObject.Meta, PyotCore.Meta):
        pass

    @property
    def account_platform(self) -> "ActivePlatform":
        return ActivePlatform(puuid=self.puuid, region=self.region)


class ActivePlatform(ActivePlatformObject, PyotCore):

    class Meta(ActivePlatformObject.Meta, PyotCore.Meta):
        pass

    def __init__(self, puuid: str = None, game: str = None, region: str = None):
        if game is None: raise RuntimeError("Parameter 'game' is needed as this model doesn't support 'active-shard-v1' endpoint")
        self._lazy_set(locals())

    @property
    def account(self) -> "Account":
        return Account(puuid=self.puuid, region=self.region)