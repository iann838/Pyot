from pyot.utils import loop_run
from pyot.models import riot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .account import Account, ActivePlatform

class Account(SyotBase, riot.Account):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

class ActiveShard(SyotBase, riot.ActiveShard):
    def get(self, **kwargs):
        return loop_run(super().get(**kwargs))

SyotBase._bridges = {
    "Account": Account,
    "ActiveShard": ActiveShard,
}