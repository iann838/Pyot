# THIS IS ONLY A CONCEPT, NOT IMPLEMENTED

from functools import wraps, partial
from typing import Dict, List, Mapping, Any, get_type_hints
import pickle
import re
import json

from pyot.pipeline.core import Pipeline
from pyot.pipeline.token import PipelineToken
from pyot.utils import PtrCache

normalizer_cache = PtrCache()
typing_cache = PtrCache()


class PyotLazyObject:
    obj: Any
    clas: Any

    def __init__(self, clas, obj, server_type, server):
        try:
            if clas.__origin__ is list:
                self.clas = clas.__args__[0]
        except Exception:
            self.clas = clas
        self.server_map = [server_type, server]
        self.obj = obj

    def __call__(self):
        if issubclass(self.clas, PyotCoreObject):
            if isinstance(self.obj, list):
                l = []
                for obj in self.obj:
                    data = obj.pop("data")
                    instance = self.clas(**obj)
                    instance.meta.data = data
                    instance.meta.server_map = self.server_map
                    instance._fill()
                    l.append(instance)
                return l
            else:
                # pop the data
                data = self.obj.pop("data")
                # obj are the arguments
                instance = self.clas(**self.obj)
                # insert the data and fill
                instance.meta.data = data
                instance.meta.server_map = self.server_map
                instance._fill()
                return instance
        elif issubclass(self.clas, PyotStaticObject):
            if isinstance(self.obj, list):
                l = []
                for obj in self.obj:
                    instance = self.clas(obj)
                    instance.meta.server_map = self.server_map
                    l.append(instance._fill())
                return l
            else:
                instance = self.clas(self.obj)
                instance.meta.server_map = self.server_map
                return instance._fill()
        raise RuntimeError(f"Unable to lazy load '{self.clas}'")


class PyotStaticObject:

    class Meta:
        # BE CAREFUL WHEN MANIPULATING MUTABLE OBJECTS
        # ALL MUTABLE OBJECTS SHOULD BE OVERRIDDEN ON ITS SUBCLASS !
        server_map: List[str]
        types: Dict[str, Any]
        data: Dict[str, Any]
        ata: Dict[str, Any]
        raws: List[str] = []
        removed: List[str] = []
        renamed: Dict[str, str] = {}

    region: str = ""
    platform: str = ""
    locale: str = ""

    def __init__(self, data):
        # META CLASS UNIQUE MUTABLE OBJECTS
        self.meta = self.Meta()
        self.meta.data = data
        self.meta.ata = {}
        self.meta.types = typing_cache.get(self.__class__, partial(get_type_hints, self.__class__))

    def __getattribute__(self, name):
        if name == "meta":
            return super().__getattribute__(name)
        try:
            val = self.meta.ata[name]
            if isinstance(val, list) or isinstance(val, dict):
                if name in self.meta.raws:
                    return val
                server = self.meta.ata[self.meta.server_type]
                self.meta.ata[name] = PyotLazyObject(self.meta.types[name], val, self.meta.server_type, server)()
                return self.meta.ata[name]
            return val
        except (KeyError, AttributeError):
            return super().__getattribute__(name)

    def _rename(self, data):
        # SNAKECASE > RENAME > REMOVE
        new_data = {}
        mapping = {}
        for attr, val in data.items():
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', attr)
            newkey = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
            if newkey in self.meta.removed:
                continue
            if newkey in self.meta.renamed:
                newkey = self.meta.renamed[newkey]
            mapping[attr] = newkey
            new_data[newkey] = val

        return new_data, mapping

    def _normalize(self, data):
        mapping = normalizer_cache.get(self.__class__, dict)
        new_data = {}
        for attr, val in data.items():
            try:
                new_data[mapping[attr]] = val
            except KeyError:
                new_data, new_mapping = self._rename(data)
                mapping.update(new_mapping)
                return new_data
        for key in self.meta.removed:
            new_data.pop(key, None)
        return new_data

    def _fill(self):
        # BIND SERVER > NORMALIZE > RAW > LAZY
        try:
            server_type = self.meta.server_map
            self.meta.server_type = server_type[0]
            setattr(self, server_type[0], server_type[1].lower())
        except AttributeError: pass

        data_ = self._normalize(self.meta.data)

        if self.meta.server_type in data_:
            data_[self.meta.server_type] = data_[self.meta.server_type].lower()
            setattr(self, self.meta.server_type, data_[self.meta.server_type].lower())

        self.meta.ata = data_
        self.meta.ata.update(self.__dict__)
        # for attr, val in data_.items():
        #     if attr in self.meta.raws:
        #         setattr(self, attr, val)
        #     elif PyotLazyObject.need_lazy(val):
        #         if has_server:
        #             server = data_[self.meta.server_type]
        #         else:
        #             server = getattr(self, self.meta.server_type)
        #         setattr(self, attr, PyotLazyObject(self.meta.types[attr], val, self.meta.server_type, server))
        #     elif attr == self.meta.server_type:
        #         setattr(self, attr, val.lower())
        #     else:
        #         setattr(self, attr, val)
        return self

    def dict(self, pyotify: bool = False, remove_server: bool = True):
        '''
        Convert this pyot object to a python dictionary.\n
        Set `pyotify` to True to return a dict with the same schema of the pyot object (This is expensive due to recursion).\n
        Set `remove_server` to False to not remove the server values (region/platform/locale).
        '''
        if not pyotify:
            return pickle.loads(pickle.dumps(self.meta.data)) # USING PICKLE FOR FASTER COPY
        def recursive(obj):
            dic = obj.__dict__
            del dic["meta"]
            if remove_server:
                dic.pop(self.meta.server_type, None)
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
        obj = pickle.loads(pickle.dumps(self))
        return recursive(obj)

    def json(self, pyotify: bool = False, remove_server: bool = True):
        '''
        Convert this pyot object to a json string.\n
        Set `pyotify` to True to return a json with the same schema of the pyot object (This is expensive due to recursion).\n
        Set `remove_server` to False to not remove the server values (region/platform/locale).
        '''
        if not pyotify:
            return json.dumps(self.meta.data)
        return json.dumps(self.dict(pyotify=pyotify, remove_server=remove_server))


class PyotCoreObject(PyotStaticObject):

    class Meta(PyotStaticObject.Meta):
        # BE CAREFUL WHEN MANIPULATING MUTABLE OBJECTS
        # ALL MUTABLE OBJECTS SHOULD BE OVERRIDDEN ON ITS SUBCLASS !
        pipeline: Pipeline
        key: str
        server: str
        session_id: str = None
        load: Mapping[str, Any]
        query: Mapping[str, Any]
        server_type: str = "platform"
        allow_query: bool = False
        rules: Mapping[str, List[str]] = {}
        region_list = []
        platform_list = []
        locale_list = []

    async def get(self, sid: str = None):
        '''Awaitable. Get this object from the pipeline.\n
        `sid` may be passed to reuse a session on the pipeline.'''
        token = await self.create_token()
        data = await self.meta.pipeline.get(token, sid)
        data = self.filter(data)
        self.meta.data = self._transform(data)
        self._fill()
        return self

    def _lazy_set(self, kwargs):
        # META CLASS UNIQUE MUTABLE OBJECTS
        self.meta = self.Meta()
        self.meta.query = {}
        self.meta.data = {}
        self.meta.types = typing_cache.get(self.__class__, partial(get_type_hints, self.__class__))

        for server in ["platform", "region", "locale"]:
            if server in kwargs:
                self.meta.server_type = server
                break
            if server == "locale":  # if server is last and still not found, raise
                raise RuntimeError("Invalid or missing server type was passed as subclass")
        for name, val in kwargs.items():
            if name in ["platform", "region", "locale"] and val is not None:
                self.meta.data[name] = val.lower()
                setattr(self, name, val.lower())
            elif val is not None and name != "self":
                self.meta.data[name] = val
                setattr(self, name, val)
        return self

    def query(self, **kwargs):
        '''Add query parameters to the object.'''
        if not self.meta.allow_query:
            raise RuntimeError("This Pyot object does not accept queries")
        self.meta.query = self._parse_query(locals())
        return self

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def _parse_query(self, kwargs) -> Dict:
        return {self.to_camel_case(key): val for (key,val) in kwargs.items() if key != "self" and val is not None}

    async def create_token(self, search: str = None) -> PipelineToken:
        '''Awaitable. Create a pipeline token that identifies this object (its parameters).'''
        await self._clean()
        self._get_rule(search)
        self._get_server()
        self._refactor()
        if not hasattr(self.meta, "pipeline"): raise RuntimeError("Pyot pipeline for this model wasn't activated or lost")
        return PipelineToken(self.meta.pipeline.model, self.meta.server, self.meta.key, self.meta.load, self.meta.query)

    def _get_rule(self, search):
        if len(self.meta.rules) == 0:
            raise RuntimeError("This Pyot object is not getable")
        for key, attr in self.meta.rules.items():
            if search and search not in key: continue
            load = {}
            for a in attr:
                try:
                    load[a] = getattr(self, a)
                except AttributeError:
                    break
            if len(load) != len(attr):
                continue
            self.meta.key = key
            self.meta.load = load
            return self
        raise ValueError("Incomplete values to create request token")

    def _get_server(self):
        for server_type in ["platform", "region", "locale"]:
            if self.meta.server_type == server_type:
                server = getattr(self, server_type)
                list_ = getattr(self.meta, server_type+"_list")
                if server.lower() not in list_:
                    raise ValueError(f"Invalid '{server_type}' value, '{server}' was given")
                self.meta.server = server.lower()
                break
            if server_type == "locale": # if server is last and still not found, raise
                raise RuntimeError("Invalid or missing server type was passed as subclass")
        return self

    async def _clean(self):
        pass

    def _transform(self, data) -> Dict:
        return data

    def _refactor(self):
        pass

    def filter(self, data):
        return data
