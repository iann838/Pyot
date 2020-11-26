from typing import Dict, List, Mapping, Any, get_type_hints
import pickle
import re
import json

from pyot.pipeline.core import Pipeline
from pyot.pipeline.token import PipelineToken
from pyot.utils import PtrCache, camelcase, fast_copy
from pyot.pipeline import pipelines

normalizer_cache = PtrCache()
typing_cache = PtrCache()


class PyotLazyObject:
    obj: Any
    clas: Any

    def __init__(self, clas, obj, server_type, server):
        self.clas = clas
        self.server_map = [server_type, server]
        self.obj = obj

    def __call__(self):
        if issubclass(self.clas, PyotCoreObject):
            if isinstance(self.obj, list):
                li = []
                for obj in self.obj:
                    instance = self.clas()
                    instance._meta.server_map = self.server_map
                    instance._meta.data = instance._transform(obj)
                    instance._fill()
                    li.append(instance)
                return li
            else:
                instance = self.clas()
                # SERVER MAP WILL GO FIRST THAN OBJECT
                instance._meta.server_map = self.server_map
                instance._meta.data = instance._transform(self.obj)
                instance._fill()
                return instance
        elif issubclass(self.clas, PyotStaticObject):
            if isinstance(self.obj, list):
                l = []
                for obj in self.obj:
                    instance = self.clas(obj)
                    instance._meta.server_map = self.server_map
                    l.append(instance._fill())
                return l
            else:
                instance = self.clas(self.obj)
                instance._meta.server_map = self.server_map
                return instance._fill()
        raise RuntimeError(f"Unable to lazy load '{self.clas}'")

    @staticmethod
    def need_lazy(obj):
        if isinstance(obj, list) or isinstance(obj, dict):
            return True
        return False


class PyotStaticObject:

    class Meta:
        # BE CAREFUL WHEN MANIPULATING MUTABLE OBJECTS
        # ALL MUTABLE OBJECTS SHOULD BE OVERRIDDEN ON ITS SUBCLASS !
        server_map: List[str]
        types: Dict[str, Any]
        data: Dict[str, Any]
        raws: List[str] = []
        removed: List[str] = []
        renamed: Dict[str, str] = {}

    region: str = ""
    platform: str = ""
    locale: str = ""

    def __init__(self, data):
        # META CLASS UNIQUE MUTABLE OBJECTS
        self._meta = self.Meta()
        self._meta.data = data
        self._meta.types = typing_cache.get(self.__class__, self._get_types)

    def __getattribute__(self, name):
        try:
            attr = super().__getattribute__(name)
            if isinstance(attr, PyotLazyObject):
                obj = attr()
                setattr(self, name, obj)
                return obj
            else:
                return attr
        except (KeyError, AttributeError):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __getitem__(self, item):
        return self._meta.data[item]

    def _rename(self, data):
        # SNAKECASE > RENAME > REMOVE
        new_data = {}
        mapping = {}
        for attr, val in data.items():
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', attr)
            newkey = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
            if newkey in self._meta.removed:
                continue
            if newkey in self._meta.renamed:
                newkey = self._meta.renamed[newkey]
            mapping[attr] = newkey
            new_data[newkey] = val

        return new_data, mapping

    def _get_types(self):
        types = get_type_hints(self.__class__)
        for typ, clas in types.items():
            try:
                if clas.__origin__ is list:
                    types[typ] = clas.__args__[0]
            except Exception:
                pass
        return types

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
        for key in self._meta.removed:
            new_data.pop(key, None)
        return new_data

    def _fill(self):
        # BIND SERVER > NORMALIZE > RAW > LAZY
        try:
            server_type = self._meta.server_map
            self._meta.server_type = server_type[0]
            setattr(self, server_type[0], server_type[1].lower())
        except AttributeError: pass

        data_ = self._normalize(self._meta.data)

        if self._meta.server_type in data_:
            has_server = True
        else:
            has_server = False

        for attr, val in data_.items():
            if attr in self._meta.raws:
                setattr(self, attr, val)
            elif PyotLazyObject.need_lazy(val):
                if has_server:
                    server = data_[self._meta.server_type]
                else:
                    server = getattr(self, self._meta.server_type)
                setattr(self, attr, PyotLazyObject(self._meta.types[attr], val, self._meta.server_type, server))
            elif attr == self._meta.server_type:
                setattr(self, attr, val.lower())
            else:
                setattr(self, attr, val)
        return self

    def dict(self, pyotify: bool = False, remove_server: bool = True):
        '''
        Convert this pyot object to a python dictionary.\n
        Set `pyotify` to True to return a dict with the same schema of the pyot object (This is expensive due to recursion).\n
        Set `remove_server` to False to not remove the server values (region/platform/locale).
        '''
        if not pyotify:
            return fast_copy(self._meta.data) # USING PICKLE FOR FASTER COPY
        def recursive(obj):
            dic = obj.__dict__
            del dic["_meta"]
            if remove_server:
                dic.pop(self._meta.server_type, None)
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
            return json.dumps(self._meta.data)
        return json.dumps(self.dict(pyotify=pyotify, remove_server=remove_server))


class PyotContainerObject:

    class Meta:
        # THIS META CLASS IS NOT INHERITED ON CORE, USED ONLY ON CONTAINER
        server_type: str = "locale"
        region_list = []
        platform_list = []
        locale_list = []

    region: str = ""
    platform: str = ""
    locale: str = ""

    def __init__(self, kwargs):
        # META CLASS UNIQUE MUTABLE OBJECTS
        self._meta = self.Meta()
        self._set_server_type(kwargs)
        for name, val in kwargs.items():
            if name in ["platform", "region", "locale"] and val is not None:
                setattr(self, name, val.lower())

    def _get_server(self):
        for server_type in ["platform", "region", "locale"]:
            if self._meta.server_type == server_type:
                server = getattr(self, server_type)
                list_ = getattr(self._meta, server_type+"_list")
                if server.lower() not in list_:
                    raise ValueError(f"Invalid '{server_type}' value, '{server}' was given \
                        {'. Did you activate the settings and set a default value ?' if not server else ''}")
                self._meta.server = server.lower()
                break
            if server_type == "locale": # if server is last and still not found, raise
                raise TypeError("Invalid or missing server type was passed as subclass")
        return self

    def _set_server_type(self, kwargs):
        for server in ["platform", "region", "locale"]:
            if server in kwargs:
                self._meta.server_type = server
                break
            if server == "locale":  # if server is last and still not found, raise
                raise TypeError("Invalid or missing server type was passed as subclass")


class PyotCoreObject(PyotStaticObject, PyotContainerObject):

    class Meta(PyotStaticObject.Meta):
        # BE CAREFUL WHEN MANIPULATING MUTABLE OBJECTS
        # ALL MUTABLE OBJECTS MUST BE OVERRIDDEN ON ITS SUBCLASS !
        pipeline: Pipeline
        key: str
        server: str
        session_id: str = None
        load: Mapping[str, Any]
        query: Mapping[str, Any]
        body: Mapping[str, Any]
        server_type: str = "platform"
        allow_query: bool = False
        rules: Mapping[str, List[str]] = {}
        region_list = []
        platform_list = []
        locale_list = []

    async def get(self, sid: str = None, pipeline: str = None, ptr_cache: PtrCache = None):
        '''Awaitable. Get this object from the pipeline.\n
        `sid` id identifying the session on the pipeline to reuse.\n
        `pipeline` key identifying the pipeline to execute against.\n
        `ptr_cache` intercepts a PtrCache, usage details please refer to documentations.\n 
        '''
        self.set_pipeline(pipeline)
        token = await self.create_token()

        if ptr_cache:
            if not isinstance(ptr_cache, PtrCache):
                raise TypeError(f"'ptr_cache' receives object of type 'PtrCache', got '{ptr_cache.__class__.__name__}'")
            item = ptr_cache.get(token)
            if item:
                return item

        data = await self._meta.pipeline.get(token, sid)
        data = self._filter(data)
        self._meta.data = self._transform(data)
        self._fill()

        if ptr_cache:
            ptr_cache.set(token, self)

        return self

    async def post(self, sid: str = None, pipeline: str = None):
        '''Awaitable. Post this object to the pipeline.\n
        `sid` id identifying the session on the pipeline to reuse.\n
        `pipeline` key identifying the pipeline to execute against.\n
        '''
        self.set_pipeline(pipeline)
        token = await self.create_token()
        data = await self._meta.pipeline.post(token, self._meta.body, sid)
        data = self._filter(data)
        self._meta.data = self._transform(data)
        self._fill()
        return self

    async def put(self, sid: str = None, pipeline: str = None):
        '''Awaitable. Put this object to the pipeline.\n
        `sid` id identifying the session on the pipeline to reuse.\n
        `pipeline` key identifying the pipeline to execute against.\n
        '''
        self.set_pipeline(pipeline)
        token = await self.create_token()
        data = await self._meta.pipeline.put(token, self._meta.body, sid)
        data = self._filter(data)
        self._meta.data = self._transform(data)
        self._fill()
        return self

    def _lazy_set(self, kwargs):
        # META CLASS UNIQUE MUTABLE OBJECTS
        self._meta = self.Meta()
        self._meta.query = {}
        self._meta.data = {}
        self._meta.types = typing_cache.get(self.__class__, self._get_types)

        self._set_server_type(kwargs)
        for name, val in kwargs.items():
            if name in ["platform", "region", "locale"] and val is not None:
                self._meta.data[name] = val.lower()
                setattr(self, name, val.lower())
            elif val is not None and name != "self":
                self._meta.data[name] = val
                setattr(self, name, val)
        return self

    def query(self, **kwargs):
        '''Add query parameters to the object.'''
        self._meta.query = self._parse_camel(locals())
        return self

    def body(self, **kwargs):
        '''Add body parameters to the object.'''
        self._meta.body = self._parse_camel(locals())
        return self

    def set_pipeline(self, pipeline: str = None):
        '''Set the pipeline to execute against.'''
        if pipeline is None: return self
        try:
            self._meta.pipeline = pipelines[pipeline]
        except KeyError:
            raise RuntimeError(f"Pipeline '{pipeline}' does not exist, inactive or dead")
        return self

    def _parse_camel(self, kwargs) -> Dict:
        '''Parse locals to json compatible camelcased keys'''
        return {camelcase(key): val for (key,val) in kwargs.items() if key != "self" and val is not None}

    async def create_token(self, search: str = None) -> PipelineToken:
        '''Awaitable. Create a pipeline token that identifies this object (its parameters).'''
        await self._clean()
        self._get_rule(search)
        self._get_server()
        self._refactor()
        self._validate()
        if not hasattr(self._meta, "pipeline"): raise RuntimeError("Pyot pipeline for this model wasn't activated or lost")
        return PipelineToken(self._meta.pipeline.model, self._meta.server, self._meta.key, self._meta.load, self._meta.query)

    def _get_rule(self, search):
        if len(self._meta.rules) == 0:
            raise RuntimeError("This Pyot object is not getable")
        for key, attr in self._meta.rules.items():
            if search and search not in key: continue
            load = {}
            for a in attr:
                try:
                    load[a] = getattr(self, a)
                except AttributeError:
                    break
            if len(load) != len(attr):
                continue
            self._meta.key = key
            self._meta.load = load
            return self
        raise TypeError("Incomplete values to create request token")


    async def _clean(self):
        pass

    def _validate(self):
        pass

    def _transform(self, data) -> Dict:
        return data

    def _refactor(self):
        pass

    def _filter(self, data):
        return data
