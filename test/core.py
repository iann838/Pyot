from typing import get_type_hints
import inspect

from typeguard import check_type

from pyot.core.functional import lazy_property
from pyot.core.objects import PyotStaticBase

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
