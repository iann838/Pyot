from typing import get_type_hints
import inspect

from typeguard import check_type

from pyot.core.functional import laziable, lazy_property
from pyot.core.objects import PyotCoreBase, PyotLazy, PyotStaticBase

from .exceptions import UntypedAttribute
from .utils import get_module_locals, get_properties, get_forward_refs


def assert_walkable(o: PyotStaticBase):
    o.dict(recursive=True, lazy_props=True)


def assert_types(o: PyotStaticBase):
    if isinstance(o, (list, tuple, set)):
        for o_item in o:
            assert_types(o_item)
        return
    if isinstance(o, dict):
        for o_item in o.values():
            assert_types(o_item)
        return
    forward_refs = {"riot": get_forward_refs("riot")}
    if isinstance(o, PyotStaticBase):
        model = o._meta.pipeline.model
        if model not in forward_refs:
            forward_refs[model] = forward_refs["riot"].copy()
            forward_refs[model].update(get_forward_refs(model))
        for key, typ in get_type_hints(o.__class__).items():
            if key[0] == "_" and key[-1] != "_":
                continue
            attr = getattr(o, key, None)
            if attr is None:
                continue
            check_type(f"{o.__class__.__name__}.{key}", attr, typ)
            assert_types(attr)
        for key, func in get_properties(o):
            attr = getattr(o, key, None)
            if attr is None:
                continue
            return_anno = None
            if isinstance(func, lazy_property):
                return_anno = inspect.signature(func.real_func).return_annotation
            elif isinstance(func, property):
                return_anno = inspect.signature(func.fget).return_annotation
            check_type(f"{o.__class__.__name__}.{key}", attr, return_anno, globals=forward_refs[model], locals=get_module_locals(o.__class__))


def inject_guards():
    
    def PyotStaticBasefill(self: PyotStaticBase):
        mapping = self._meta.nomcltrs

        for key, val in self._meta.data.items():
            try:
                attr = mapping[key]
            except KeyError:
                attr = self.qualkey(key)
                mapping[key] = attr

            if attr not in self._meta.types:
                raise UntypedAttribute(self.__class__, attr, val)

            if laziable(val):
                if attr in self._meta.raws:
                    setattr(self, attr, val)
                    continue
                try:
                    attr_type = self._meta.types[attr]
                    setattr(self, '_lazy__' + attr, PyotLazy(attr_type[1], attr_type[0], val, self._meta.root))
                except KeyError:
                    setattr(self, attr, val)
            else:
                setattr(self, attr, val)

        return self
    
    PyotStaticBase.fill = PyotStaticBasefill

    def PyotLazy__call__(self: PyotLazy):
        try:
            if issubclass(self.clas, PyotCoreBase):
                if self.container is None:
                    return self.load_core(self.obj)
                if issubclass(self.container, list):
                    return [self.load_core(obj) for obj in self.obj]
                if issubclass(self.container, dict):
                    return {okey: self.load_core(obj) for okey, obj in self.obj.items()}
                raise TypeError(f"Invalid container type '{self.container.__name__}'")
            if self.container is None:
                return self.load_static(self.obj)
            if issubclass(self.container, list):
                return [self.load_static(obj) for obj in self.obj]
            if issubclass(self.container, dict):
                return {okey: self.load_static(obj) for okey, obj in self.obj.items()}
            raise TypeError(f"Invalid container type '{self.container.__name__}'")
        except UntypedAttribute as e:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to lazy load '{self.clas.__name__}' object due to: ({type(e)}) {e}") from e

    PyotLazy.__call__ = PyotLazy__call__
