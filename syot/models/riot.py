from pyot.utils import run
from pyot.models import riot
from .__core__ import SyotBaseObject

class SyotBase(SyotBaseObject):
    pass

# from .account import Account, ActivePlatform

class Account(SyotBase, riot.Account):
    def get(self):
        return run(super().get())

class ActivePlatform(SyotBase, riot.ActivePlatform):
    def get(self):
        return run(super().get())

SyotBase._bridges = {
    "Account": Account,
    "ActivePlatform": ActivePlatform,
}