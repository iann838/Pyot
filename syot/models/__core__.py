from pyot.core.objects import PyotCoreObject
from inspect import signature

class SyotBaseObject:
    _bridges = {}

    def __getattribute__(self, name):
        obj = super().__getattribute__(name)
        if isinstance(obj, PyotCoreObject):
            cls_name = obj.__class__.__name__
            load = {attr: getattr(obj, attr, None) for attr in signature(obj.__init__).parameters}
            return self._bridges[cls_name](**load)
        return obj