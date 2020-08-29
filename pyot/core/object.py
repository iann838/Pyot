from functools import wraps
from typing import Dict, List, Mapping, Any, get_type_hints
from .pipeline import PyotPipeline, PyotPipelineToken
import copy
import re
import json


class PyotLazyObject:
    obj: Any
    clas: Any

    def __init__(self, clas, obj, platform, region, locale):
        try:
            if clas.__origin__ is list:
                self.clas = clas.__args__[0]
        except Exception:
            self.clas = clas
        server_map = {"platform": platform, "region": region, "locale": locale}
        for key, val in server_map.items():
            if val is not None:
                if isinstance(obj, list):
                    for l in obj:
                        l.update({key: val})
                else:
                    obj.update({key: val})
        self.obj = obj

    def __call__(self):
        if issubclass(self.clas, PyotCoreObject):
            if isinstance(self.obj, list):
                l = []
                for obj in self.obj:
                    data = obj["data"]
                    shallow = {k:v for (k,v) in obj.items() if k != "data"}
                    instance = self.clas(**shallow)
                    instance.Meta.data = data
                    instance._fill()
                    l.append(instance)
                return l
            else:
                data = self.obj["data"]
                shallow = {k:v for (k,v) in self.obj.items() if k != "data"}
                instance = self.clas(**shallow)
                instance.Meta.data = data
                instance._fill()
                return instance
        elif issubclass(self.clas, PyotStaticObject):
            if isinstance(self.obj, list):
                l = []
                for obj in self.obj:
                    l.append(self.clas(obj)._fill())
                return l
            else:
                return self.clas(self.obj)._fill()
        raise RuntimeError(f"Unable to lazy load '{self.clas}'")

    @staticmethod
    def need_lazy(obj):
        if isinstance(obj, list) or isinstance(obj, dict):
            return True
        return False


class PyotStaticObject:

    class Meta:
        raws: List[str] = []
        removed: List[str] = []
        types: Dict[str, Any] = {}
        data: Dict[str, Any] = {}
        renamed: Dict[str, str] = {}

    region: str = ""
    platform: str = ""
    locale: str = ""

    def __init__(self, data):
        self.Meta = self.Meta()
        self.Meta.types = get_type_hints(self.__class__)
        self.Meta.data = data

    def __getattribute__(self, name):
        try:
            if type(super().__getattribute__(name)) is PyotLazyObject:
                obj = super().__getattribute__(name)()
                setattr(self, name, obj)
                return obj
            else:
                return super().__getattribute__(name)
        except (KeyError, AttributeError):
            raise
            # raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def _normalize(self, data):
        new_data = {}
        for attr, val in data.items():
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', attr)
            snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
            new_data[snake_case] = val
        return new_data
    
    def _fill(self):
        data_ = self._normalize(self.Meta.data)
        for server in ["platform", "region", "locale"]:
            if server in data_:
                setattr(self, server, data_[server])
        for attr, val in data_.items():   # RENAME > REMOVE > RAW > LAZY
            attr = attr if attr not in self.Meta.renamed else self.Meta.renamed[attr]
            if attr in self.Meta.removed:
                continue
            elif attr in self.Meta.raws:
                setattr(self, attr, val)
            elif PyotLazyObject.need_lazy(val):
                servers = []
                for server in ["platform", "region", "locale"]:
                    try:
                        servers.append(getattr(self, server))
                    except AttributeError:
                        servers.append(None)
                setattr(self, attr, PyotLazyObject(self.Meta.types[attr], val, servers[0], servers[1], servers[2]))
            elif attr not in ["platform", "region", "locale"]:
                setattr(self, attr, val)
        return self

    def dict(self, pyotify: bool = False, remove_server: bool = True):
        if not pyotify:
            return copy.deepcopy(self.Meta.data)
        def recursive(obj):
            dic = copy.deepcopy(obj.__dict__)
            if "Meta" in dic:
                del dic["Meta"]
            if remove_server:
                for server in ["platform", "region", "locale"]:
                    if server in dic:
                        dic.pop(server)
            for key, val in dic.items():
                if type(val) is PyotLazyObject:
                    obj = val()
                    if isinstance(obj, list):
                        dic[key] = []
                        for i in range(len(obj)):
                            inner = recursive(obj[i])
                            dic[key].append(inner)
                    else:
                        inner = recursive(obj)
                        dic[key] = inner
            return dic
        return recursive(self)


    def json(self, pyotify: bool = False, remove_server: bool = True):
        if not pyotify:
            return json.dumps(self.Meta.data)
        return json.dumps(self.dict(pyotify=pyotify, remove_server=remove_server))


class PyotCoreObject(PyotStaticObject):

    class Meta(PyotStaticObject.Meta):
        pipeline: PyotPipeline
        key: str
        server: str
        session_id: str = None
        load: Mapping[str, Any]
        query: Mapping[str, Any] = {}
        types: Dict[str, Any] = None
        rules: Mapping[str, List[str]] = {}
        server_type: str = "platform"
        allow_query: bool = False
        region_list = []
        platform_list = []
        locale_list = []

    def __getattribute__(self, name):
        if name in ["region", "platform", "locale"] and name != self.Meta.server_type:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return super().__getattribute__(name)

    def query(self, **kwargs):
        if not self.Meta.allow_query:
            raise RuntimeError("This Pyot object does not accept queries")
        self.Meta.query = self._parse_query(locals())
        return self

    async def get(self):
        token = await self.create_token()
        data = await self.Meta.pipeline.get(token, self.filter, self.Meta.session_id)
        self.Meta.data = await self._transform(data)
        self._fill()
        return self

    def _lazy_set(self, kwargs):
        self.Meta = self.Meta()
        for server in ["platform", "region", "locale"]:
            if server in kwargs:
                self.Meta.server_type = server
                break
            if server == "locale":  # if server is last and still not found, raise
                raise RuntimeError("Invalid or missing server type was passed as subclass")
        self.Meta.types = get_type_hints(self.__class__)
        self.Meta.data = {}
        for name, val in kwargs.items():
            if name in ["platform", "region", "locale"] and val is not None:
                self.Meta.data[name] = val.lower()
                setattr(self, name, val.lower())
            elif val is not None and name != "self":
                self.Meta.data[name] = val
                setattr(self, name, val)
        return self

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def _parse_query(self, kwargs) -> Dict:
        return {self.to_camel_case(key): val for (key,val) in kwargs.items() if key != "self" and val is not None}

    def set_session_id(self, id: str):
        self.Meta.session_id = id
        return self

    async def create_token(self) -> PyotPipelineToken:
        if not hasattr(self.Meta, "pipeline"): raise RuntimeError("Pyot for this variant wasn't activated")
        await self._clean()
        await self._get_rule()
        await self._get_server()
        await self._refactor()
        return PyotPipelineToken(self.Meta.server, self.Meta.key, self.Meta.load, self.Meta.query)

    async def _get_rule(self):
        if len(self.Meta.rules) == 0:
            raise RuntimeError("This Pyot object is not get-able")
        repeated = False
        for key, attr in self.Meta.rules.items():
            load = {}
            for a in attr:
                try:
                    load[a] = getattr(self, a)
                except AttributeError:
                    break
            if len(load) != len(attr):
                continue
            if hasattr(self.Meta, "key") and key == self.Meta.key and load == self.Meta.load:
                repeated = True
                continue
            self.Meta.key = key
            self.Meta.load = load
            return self
        if not repeated:
            raise ValueError("Incomplete values to create request token")
        self.Meta.key = None
        self.Meta.load = {}
        return await self._get_rule()

    async def _get_server(self):
        for server_type in ["platform", "region", "locale"]:
            if self.Meta.server_type == server_type:
                server = getattr(self, server_type)
                list_ = getattr(self.Meta, server_type+"_list")
                if server.lower() not in list_:
                    raise ValueError(f"Invalid '{server_type}' value, '{server}' was given")
                self.Meta.server = server.lower()
                break
            if server_type == "locale": # if server is last and still not found, raise
                raise RuntimeError("Invalid or missing server type was passed as subclass")
        return self

    async def _transform(self, data) -> Dict:
        return data

    async def _clean(self):
        pass

    async def _refactor(self):
        pass

    def filter(self, data):
        return data
