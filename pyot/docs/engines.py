from abc import ABC, abstractmethod
from typing import Callable, Iterable, TypeVar, get_type_hints
from pathlib import Path
import shutil
import pkgutil
import inspect

from pyot.core.objects import PyotCoreBase, PyotRoutingBase, PyotStaticBase, PyotUtilBase, lazy_property
from pyot.utils.importlib import import_class, import_module
from pyot.utils.nullsafe import nullsafe as _

from .serializers import PyotDocTypeSerializer
from .utils import get_method_properties, get_method_property_names, newline_join


class DocEngine(ABC):

    BASE_PATH = Path.cwd() / 'docs'

    def __init__(self, path: Path = None) -> None:
        if path:
            self.BASE_PATH = path

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def build(self):
        pass

    def run(self):
        self.prepare()
        self.build()


class ModelsDocEngine(DocEngine):

    BASE_PATH = Path.cwd() / 'docs' / 'models'
    MODELS = ['riot', 'lol', 'tft', 'lor', 'val']

    def prepare(self):
        '''Activate all models and remove existing docs'''
        from pyot import models
        from pyot.conf.model import activate_model, ModelConf

        for module in pkgutil.iter_modules(models.__path__):
            activate_model(module.name)(type(module.name.upper() + "Model", (ModelConf,), {
                "default_region": f"models.{module.name}.DEFAULT_REGION",
                "default_locale": f"models.{module.name}.DEFAULT_LOCALE",
                "default_platform": f"models.{module.name}.DEFAULT_PLATFORM",
                "default_version": f"models.{module.name}.DEFAULT_VERSION",
            }))
        shutil.rmtree(self.BASE_PATH, ignore_errors=True)
        self.BASE_PATH.mkdir(parents=True, exist_ok=True)
        with open(self.BASE_PATH / 'README.md', 'w+') as f:
            f.writelines(["# Models"])

    def build(self):
        for model in self.MODELS:
            model_detail, model_classes = self.get_model_classes(model)
            (self.BASE_PATH / model).mkdir(parents=True, exist_ok=True)
            with open(self.BASE_PATH / model / 'README.md', 'w+') as f:
                lines = [
                    f"# {model_detail['repr']} \n\n",
                ]
                if model_detail['regions']:
                    lines.extend([
                        '## Routing Regions \n\n',
                        newline_join(['* `' + i + '`' for i in sorted(model_detail['regions'])]) + '\n\n',
                    ])
                if model_detail['platforms']:
                    lines.extend([
                        '## Routing Platforms \n\n',
                        newline_join(['* `' + i + '`' for i in sorted(model_detail['platforms'])]) + '\n\n',
                    ])
                f.writelines(lines)
            for submodule, classcontent in model_classes.items():
                with open(self.BASE_PATH / model / (submodule + '.md'), 'w+') as f:
                    lines = [
                        f'# {submodule.capitalize()} \n\n',
                        f'Module: `pyot.models.{model}.{submodule}` \n\n',
                    ]
                    for classtype, classes in classcontent.items():
                        for clas in classes:
                            clas_detail = self.get_model_class_details(model, submodule, clas)
                            lines.append(f'### _class_ {clas}' + '\n')
                            lines.append(f'\nType: `Pyot{classtype.capitalize()}` \n')
                            if clas_detail['extends']:
                                lines.append(f'\nExtends: \n')
                                lines.extend([f'* `{ext}` \n' for ext in clas_detail['extends']])
                            if classtype in ('core', 'util'):
                                lines.append(f'\nDefinitions: \n')
                                for def_name, definition in clas_detail['definitions'].items():
                                    lines.extend([
                                        f"* `{def_name}` -> `{definition['returns']}` \n",
                                        *[f"  * `{arg_name}`: `{arg_type}` \n" for arg_name, arg_type in definition['args'].items()]
                                    ])
                            if clas_detail['endpoints']:
                                lines.append(f'\nEndpoints: \n')
                                for end_name, end_args in clas_detail['endpoints'].items():
                                    lines.append(f"* `{end_name}`: `{end_args}` \n")
                            if clas_detail['queries']:
                                lines.append(f'\nQueries: \n')
                                for q_name, q_type in clas_detail['queries'].items():
                                    lines.append(f"* `{q_name}`: `{q_type}` \n")
                            if clas_detail['methods']:
                                lines.append(f'\nMethods: \n')
                                for att_name, att_content in clas_detail['methods'].items():
                                    lines.append(f"* _{att_content['type']}_ `{att_name}` -> `{att_content['returns']}` \n")
                                    if att_content['args']:
                                        lines.extend([f"  * `{arg_name}`: `{arg_type}` \n" for arg_name, arg_type in att_content['args'].items()])
                                    if att_content['docs']:
                                        doc_str = '\n  > '.join(inspect.cleandoc(att_content['docs']).split('\n'))
                                        lines.append(f"  > {doc_str} \n")
                            if clas_detail['attributes']:
                                lines.append(f'\nAttributes: \n')
                                for att_name, att_content in clas_detail['attributes'].items():
                                    lines.append(f"* `{att_name}` -> `{att_content['returns']}` \n")
                            if clas_detail['properties']:
                                lines.append(f'\nProperties: \n')
                                for att_name, att_content in clas_detail['properties'].items():
                                    lines.append(f"* _{att_content['type']}_ `{att_name}` -> `{att_content['returns']}` \n")
                            lines.append('\n\n')
                            # lines.append(str(clas_detail) + '\n\n')
                    f.writelines(lines)

    def get_model_classes(self, name: str):
        model = import_module(f"pyot.models.{name}")
        modules = pkgutil.iter_modules(model.__path__)
        module_classes = {}
        module_detail = {}

        for module in modules:
            if module.name == "base":
                submodule = import_module(f"pyot.models.{name}.{module.name}")
                module_detail['regions'] = list(_(submodule.PyotRouting)._regions or [])
                module_detail['platforms'] = list(_(submodule.PyotRouting)._platforms or [])
                module_detail['repr'] = submodule.MODULE_REPR
                continue
            submodule = import_module(f"pyot.models.{name}.{module.name}")
            module_classes[module.name] = {"core": [], "static": [], "utils": []}
            for key, obj in inspect.getmembers(submodule):
                obj: object
                if inspect.isclass(obj) and key[0].upper() + key[1:] == key and not key.startswith("Pyot"):
                    if issubclass(obj, PyotCoreBase):
                        module_classes[module.name]["core"].append(key)
                    elif issubclass(obj, PyotStaticBase):
                        module_classes[module.name]["static"].append(key)
                    elif issubclass(obj, PyotUtilBase):
                        module_classes[module.name]["utils"].append(key)
        return module_detail, module_classes


    def get_model_class_details(self, name: str, submodule: str, clasname: str):
        clas: PyotStaticBase = import_class(f"pyot.models.{name}.{submodule}.{clasname}")
        o = {}
        for key, typ in get_type_hints(clas).items():
            if key[0] == "_" and key[-1] != "_":
                continue
            o[key] = {
                "args": None,
                "returns": PyotDocTypeSerializer(typ, []).data,
                "type": "attribute",
                "docs": None,
            }
        queries = {}
        if issubclass(clas, PyotCoreBase):
            for paramname, typ in inspect.signature(clas.query).parameters.items():
                if paramname in ("self", "kwargs"):
                    continue
                typ_anno = typ.annotation
                if typ.annotation == inspect._empty:
                    if typ.default != inspect._empty and typ.default is not None:
                        typ_anno = typ.default.__class__
                    else:
                        typ_anno = None
                queries[paramname] = PyotDocTypeSerializer(typ_anno, []).data
                if typ.default != inspect._empty:
                    queries[paramname] += " = " + str(typ.default)
        base_class_method_props = get_method_property_names(PyotCoreBase) + get_method_property_names(PyotRoutingBase)
        for key, func in get_method_properties(clas):
            if (key not in base_class_method_props or key in [_(clas).Meta.server_type, "__init__", "__iter__"]) and key not in o:
                member_type = "method"
                args = None
                docs_string = None
                if key.startswith("__") and key.endswith("__"):
                    member_type = "definition"
                    if key == "__init__":
                        docs_string = clas.__doc__
                elif key.startswith("_"):
                    continue
                if isinstance(func, lazy_property):
                    member_type = "lazy_property"
                    return_type = inspect.signature(func.real_func).return_annotation
                    docs_string = func.real_func.__doc__
                elif isinstance(func, property):
                    member_type = "property"
                    return_type = inspect.signature(func.fget).return_annotation
                    docs_string = func.fget.__doc__
                else:
                    return_type = inspect.signature(func).return_annotation
                    docs_string = func.__doc__
                    args = {}
                    for paramname, typ in inspect.signature(func).parameters.items():
                        if paramname == "self":
                            continue
                        typ_anno = typ.annotation
                        if typ.annotation == inspect._empty:
                            if typ.default != inspect._empty and typ.default is not None:
                                typ_anno = typ.default.__class__
                            else:
                                typ_anno = None
                        args[paramname] = PyotDocTypeSerializer(typ_anno, []).data
                        if typ.default != inspect._empty:
                            args[paramname] += " = " + str(typ.default)
                if return_type is inspect._empty:
                    return_type = None
                if key == "__str__":
                    return_type = "str"
                if key == "__len__":
                    return_type = "int"
                if inspect.iscoroutinefunction(func):
                    member_type = "async" + member_type
                o[key] = {
                    "args": args,
                    "returns": PyotDocTypeSerializer(return_type, []).data,
                    "type": member_type,
                    "docs": docs_string,
                }
        endpoints = {}
        if issubclass(clas, PyotCoreBase):
            endpoints = clas.Meta.rules
        extends = []
        for cl in clas.__mro__[1:]:
            cl_name = PyotDocTypeSerializer(cl, []).data
            if cl_name.endswith(("base.PyotCore", "base.PyotStatic", "PyotUtilBase")):
                break
            extends.append(cl_name)
        return {
            "extends": extends,
            "endpoints": endpoints,
            "queries": queries,
            "definitions": dict(filter(lambda item: item[1]["type"].endswith("definition"), o.items())),
            "attributes": dict(filter(lambda item: item[1]["type"].endswith("attribute"), o.items())),
            "properties": dict(filter(lambda item: item[1]["type"].endswith(("property", "lazy_property")), o.items())),
            "methods": dict(filter(lambda item: item[1]["type"].endswith("method"), o.items())),
        }


class UtilsDocEngine(DocEngine):

    BASE_PATH = Path.cwd() / 'docs' / 'utils'

    def prepare(self):
        '''Activate all models and remove existing docs'''
        shutil.rmtree(self.BASE_PATH, ignore_errors=True)

    def build(self):
        from pyot import utils
        (self.BASE_PATH).mkdir(parents=True, exist_ok=True)
        with open(self.BASE_PATH / 'README.md', 'w+') as f:
            f.writelines(["# Utils"])
        self.build_by_path(utils.__path__)

    def build_by_path(self, path: Iterable[str], nested_levels=tuple()):
        for module in pkgutil.iter_modules(path):
            module = import_module(f"pyot.utils{'.' if nested_levels else ''}{'.'.join(nested_levels)}.{module.name}")
            members = {}
            jump_next_module = False
            for key, obj in inspect.getmembers(module):
                if inspect.ismodule(obj) and obj.__name__.startswith("pyot.utils"):
                    middle_module = obj.__name__.split(".")[-2]
                    (self.BASE_PATH / middle_module).mkdir(parents=True, exist_ok=True)
                    with open(self.BASE_PATH / middle_module / 'README.md', 'w+') as f:
                        f.writelines([f"# {middle_module.capitalize()}"])
                    self.build_by_path([path[0] + '\\' + middle_module], (*nested_levels, middle_module))
                    jump_next_module = True
                    break
                if key.startswith("__") or inspect.ismodule(obj) or isinstance(obj, TypeVar) or (not isinstance(obj, (str, bool, int, float, list)) and obj.__module__ != module.__name__):
                    continue
                if inspect.isclass(obj):
                    is_alias = obj.__name__ != key
                    if not is_alias:
                        members[key] = {"type": "class", "docs": obj.__doc__, **self.get_class_details(obj)}
                    else:
                        members[key] = {"type": "alias", "to": obj.__name__}
                elif inspect.isfunction(obj):
                    is_alias = obj.__name__ != key
                    if not is_alias:
                        members[key] = {"type": "function", "docs": obj.__doc__, **self.get_func_details(obj)}
                    else:
                        members[key] = {"type": "alias", "to": obj.__name__}
                else:
                    members[key] = {"type": "constant", "value": str(obj)}
            
            if jump_next_module:
                continue

            module_lastname = module.__name__.split(".")[-1]
            open_path = self.BASE_PATH
            for nested_level in nested_levels:
                open_path /= nested_level
            with open(open_path / (module_lastname + '.md'), 'w+') as f:
                lines = [
                    f'# {module_lastname.capitalize()} \n\n',
                    f'Module: `{module.__name__}` \n\n',
                ]
                for key, member_info in members.items():
                    if member_info["type"] == "class":
                        lines.append(f'### _class_ {key}' + '\n')
                        if member_info['docs']:
                            doc_str = '\n> '.join(inspect.cleandoc(member_info['docs']).split('\n'))
                            lines.append(f"\n> {doc_str}\n")
                        if member_info['extends']:
                            lines.append(f'\nExtends: \n')
                            lines.extend([f'* `{ext}` \n' for ext in member_info['extends']])
                        if member_info["definitions"]:
                            lines.append(f'\nDefinitions: \n')
                            for def_name, definition in member_info['definitions'].items():
                                lines.extend([
                                    f"* `{def_name}` -> `{definition['returns']}` \n",
                                    *[f"  * `{arg_name}`: `{arg_type}` \n" for arg_name, arg_type in definition['args'].items()]
                                ])
                        if member_info['methods']:
                            lines.append(f'\nMethods: \n')
                            for att_name, att_content in member_info['methods'].items():
                                lines.append(f"* _{att_content['type']}_ `{att_name}` -> `{att_content['returns']}` \n")
                                if att_content['args']:
                                    lines.extend([f"  * `{arg_name}`: `{arg_type}` \n" for arg_name, arg_type in att_content['args'].items()])
                                if att_content['docs']:
                                    doc_str = '\n  > '.join(inspect.cleandoc(att_content['docs']).split('\n'))
                                    lines.append(f"  > {doc_str} \n")
                        if member_info['attributes']:
                            lines.append(f'\nAttributes: \n')
                            for att_name, att_content in member_info['attributes'].items():
                                lines.append(f"* `{att_name}` -> `{att_content['returns']}` \n")
                        if member_info['properties']:
                            lines.append(f'\nProperties: \n')
                            for att_name, att_content in member_info['properties'].items():
                                lines.append(f"* `{att_name}` -> `{att_content['returns']}` \n")
                    elif member_info["type"].endswith("function"):
                        lines.append(f"### _{member_info['type']}_ `{key}` -> `{member_info['returns']}` \n")
                        if member_info['args']:
                            lines.extend([f"* `{arg_name}`: `{arg_type}` \n" for arg_name, arg_type in member_info['args'].items()])
                        if member_info['docs']:
                            doc_str = '\n> '.join(inspect.cleandoc(member_info['docs']).split('\n'))
                            lines.append(f"> {doc_str} \n")
                    elif member_info["type"] == "alias":
                        lines.append(f"### _{member_info['type']}_ `{key}` ~ `{member_info['to']}` \n")
                    elif member_info["type"] == "constant":
                        lines.append(f"### _{member_info['type']}_ `{key}`: `{member_info['value']}` \n")
                    lines.append('\n\n')
                f.writelines(lines)

    def get_func_details(self, func: Callable, is_method=False, member_class=None):
        key = func.__name__.split(".")[-1]
        member_type = "method" if is_method else "function"
        args = None
        docs_string = None
        if key.startswith("__") and key.endswith("__"):
            member_type = "definition"
        elif key.startswith("_"):
            return
        if isinstance(func, property):
            member_type = "property"
            return_type = inspect.signature(func.fget).return_annotation
            docs_string = func.fget.__doc__
        else:
            if member_type == "method" and member_class and func.__name__ in member_class.__dict__:
                if isinstance(member_class.__dict__[func.__name__], classmethod):
                    member_type = "classmethod"
                elif isinstance(member_class.__dict__[func.__name__], staticmethod):
                    member_type = "staticmethod"
            return_type = inspect.signature(func).return_annotation
            docs_string = func.__doc__
            args = {}
            for paramname, typ in inspect.signature(func).parameters.items():
                if paramname == "self":
                    continue
                typ_anno = typ.annotation
                if typ.annotation == inspect._empty:
                    if typ.default != inspect._empty and typ.default is not None:
                        typ_anno = typ.default.__class__
                    else:
                        typ_anno = None
                args[paramname] = PyotDocTypeSerializer(typ_anno, []).data
                if args[paramname] is not None and typ.default != inspect._empty:
                    args[paramname] += " = " + str(typ.default)
        if return_type is inspect._empty:
            return_type = None
        if key == "__str__":
            return_type = "str"
        if key == "__len__":
            return_type = "int"
        if inspect.iscoroutinefunction(func):
            member_type = "async" + member_type
        return {
            "args": args,
            "returns": PyotDocTypeSerializer(return_type, []).data,
            "type": member_type,
            "docs": docs_string,
        }

    def get_class_details(self, clas):
        o = {}
        for key, typ in get_type_hints(clas).items():
            if key[0] == "_" and key[-1] != "_":
                continue
            o[key] = {
                "args": None,
                "returns": PyotDocTypeSerializer(typ, []).data,
                "type": "attribute",
                "docs": None,
            }
        for key, func in get_method_properties(clas):
            if key not in o:
                func_details = self.get_func_details(func, True, clas)
                if func_details:
                    o[key] = func_details
        extends = []
        for cl in clas.__mro__[1:]:
            cl_name = PyotDocTypeSerializer(cl, []).data
            if cl_name.endswith(("object")):
                break
            extends.append(cl_name)
        return {
            "extends": extends,
            "definitions": dict(filter(lambda item: item[1]["type"].endswith("definition"), o.items())),
            "attributes": dict(filter(lambda item: item[1]["type"].endswith("attribute"), o.items())),
            "properties": dict(filter(lambda item: item[1]["type"].endswith(("property", "lazy_property")), o.items())),
            "methods": dict(filter(lambda item: item[1]["type"].endswith("method"), o.items())),
        }
