from inspect import signature
from pyot.core.objects import PyotCoreObject

class SyotBaseObject:
    _bridges = {} # riot.py will modify this

    def __getattribute__(self, name):
        obj = super().__getattribute__(name)
        if isinstance(obj, list):
            return [self.syot_bridge_proxy(item) for item in obj]
        return self.syot_bridge_proxy(obj)

    def syot_bridge_proxy(self, obj):
        if isinstance(obj, PyotCoreObject):
            cls_name = obj.__class__.__name__
            load = {attr: getattr(obj, attr, None) for attr in signature(obj.__init__).parameters}
            return self._bridges[cls_name](**load)
        return obj
