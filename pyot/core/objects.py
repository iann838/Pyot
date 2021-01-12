from typing import Dict, List, Mapping, Any, get_type_hints
import inspect
import re
import json

from pyot.pipeline.core import Pipeline
from pyot.pipeline.token import PipelineToken
from pyot.utils import PtrCache, camelcase, fast_copy
from pyot.pipeline import pipelines

from .functional import lazy_property, save_raw_response, laziable


class PyotLazyObject:
    obj: Any
    clas: Any

    def __init__(self, clas, obj, server_type, server):
        self.clas = clas
        self.server_map = [server_type, server]
        self.obj = obj

    def __call__(self):
        try:
            if issubclass(self.clas, PyotCoreObject):
                if isinstance(self.obj, list):
                    return [self._load_core(obj) for obj in self.obj]
                return self._load_core(self.obj)
            if isinstance(self.obj, list):
                return [self._load_static(obj) for obj in self.obj]
            return self._load_static(self.obj)
        except Exception as e:
            raise RuntimeError(f"Failed to lazy load '{self.clas.__name__}' object") from e

    def _load_static(self, obj):
        instance = self.clas(obj)
        instance._meta.server_map = self.server_map
        return instance._fill()

    def _load_core(self, obj):
        instance = self.clas()
        # SERVER MAP WILL GO FIRST THAN OBJECT
        instance._meta.server_map = self.server_map
        instance._meta.data = instance._transform(obj)
        return instance._fill()


class PyotMetaClass(type):

    def __new__(cls, name, bases, attrs):
        if 'Meta' not in attrs and cls.is_static_core(bases):
            attrs['Meta'] = type('Meta', (cls.get_static_core(bases).Meta,), {'__module__': attrs['__module__'] + f".{name}"})
        clas = super().__new__(cls, name, bases, attrs)
        clas.Meta.types = cls.get_types(clas)
        clas.Meta.nomcltrs = {}
        if cls.is_static_core(bases):
            clas.Meta.lazy_props = cls.get_lazy_props(clas, [])
            # if cls.get_static_core(bases).__name__ == "PyotCore" and clas.Meta.turbo_level > 0:
            #     clas._transform = save_raw_response(clas._transform)
        return clas

    @staticmethod
    def is_static_core(bases):
        base_names = set()
        for base in bases:
            base_names |= {cl.__name__ for cl in inspect.getmro(base)}
        return 'PyotStatic' in base_names or 'PyotCore' in base_names

    @staticmethod
    def get_static_core(bases):
        deep_bases = set()
        for base in bases:
            deep_bases |= set(inspect.getmro(base))
        return next(base for base in deep_bases if base.__name__ == 'PyotStatic' or base.__name__ == 'PyotCore')

    @staticmethod
    def get_types(clas):
        types = get_type_hints(clas)
        for typ, clas in types.items():
            try:
                if clas.__origin__ is list:
                    types[typ] = clas.__args__[0]
            except Exception:
                pass
        return types

    @staticmethod
    def get_lazy_props(clas, props, prefix=""):
        props += [prefix + p for p in dir(clas) if isinstance(getattr(clas, p), lazy_property)]
        types = {attr:cl for attr, cl in clas.Meta.types.items() if inspect.isclass(cl) and issubclass(cl, PyotStaticObject)}
        for typ, cl in types.items():
            PyotMetaClass.get_lazy_props(cl, props, prefix + typ + ".")
        return props


class PyotStaticObject(metaclass=PyotMetaClass):

    class Meta:
        # Mutable objects should be overriden on inheritance
        server_type: str
        server_map: List[str]
        nomcltrs: Dict[str, Any]
        types: Dict[str, Any]
        data: Dict[str, Any]
        raws: List[str] = []
        renamed: Dict[str, str] = {}

    region: str = ""
    platform: str = ""
    locale: str = ""

    def __init__(self, data):
        # Instantiate Meta class, isolating data dict
        self._meta = self.Meta()
        self._meta.data = data

    def __getattr__(self, name):
        try:
            lazy = self.__dict__['_lazy__' + name]
            obj = lazy()
            setattr(self, name, obj)
            return obj
        except (KeyError, AttributeError) as e:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'") from e

    def __getitem__(self, item):
        return self._meta.data[item]

    def _rename(self, key):
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
        newkey = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        if newkey in self._meta.renamed:
            newkey = self._meta.renamed[newkey]
        return newkey

    def _fill(self):
        try:
            server_type = self._meta.server_map
            self._meta.server_type = server_type[0]
            setattr(self, server_type[0], server_type[1])
        except AttributeError: pass

        mapping = self._meta.nomcltrs

        for key, val in self._meta.data.items():
            try:
                attr = mapping[key]
            except KeyError:
                attr = self._rename(key)
                mapping[key] = attr

            if laziable(val):
                if attr in self._meta.raws:
                    setattr(self, attr, val)
                else:
                    server = getattr(self, self._meta.server_type)
                    setattr(self, '_lazy__' + attr, PyotLazyObject(self._meta.types[attr], val, self._meta.server_type, server))
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
            return fast_copy(self._meta.data)
        def recursive(obj):
            dic = obj.__dict__
            del dic["_meta"]
            if remove_server:
                dic.pop(self._meta.server_type, None)
            for key, val in dic.items():
                if isinstance(val, PyotLazyObject):
                    obj = val()
                    if isinstance(obj, list):
                        dic[key] = []
                        for ob in obj:
                            inner = recursive(ob)
                            dic[key].append(inner)
                    else:
                        inner = recursive(obj)
                        dic[key] = inner
            return dic
        obj = fast_copy(self)
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
        server: str
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
                    raise ValueError(
                        f"Invalid '{server_type}' value, '{server}' was given "
                        f"{'. Did you activate the settings and set a default value ?' if not server else ''}"
                    )
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
        filter_key: str = ""
        server_type: str = "platform"
        allow_query: bool = False
        rules: Mapping[str, List[str]] = {}
        region_list = []
        platform_list = []
        locale_list = []
        turbo_level: int = 0
        raw_data: Any

    async def get(self, sid: str = None, pipeline: str = None, keep_raw: bool = False, ptr_cache: PtrCache = None):
        '''Awaitable. Get this object from the pipeline.\n
        `sid` id identifying the session on the pipeline to reuse.\n
        `pipeline` key identifying the pipeline to execute against.\n
        `keep_raw` flag for storing raw data of the request as a dictionary.\n
        `ptr_cache` intercepts a PtrCache, usage details please refer to documentations.\n
        '''
        self.set_pipeline(pipeline)
        token = await self.create_token()

        if ptr_cache:
            if not isinstance(ptr_cache, PtrCache):
                raise TypeError(f"'ptr_cache' receives object of type 'PtrCache', got '{ptr_cache.__class__.__name__}'")
            item = ptr_cache.get(token.stringify + self._meta.filter_key)
            if item:
                return item

        data = await self._meta.pipeline.get(token, sid)
        data = self._filter(data)
        if keep_raw:
            self._meta.raw_data = fast_copy(data)
        self._meta.data = self._transform(data)
        self._fill()

        if ptr_cache:
            ptr_cache.set(token.stringify + self._meta.filter_key, self)

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
        self._meta.body = {}

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
        except KeyError as e:
            raise RuntimeError(f"Pipeline '{pipeline}' does not exist, inactive or dead") from e
        return self

    @staticmethod
    def _parse_camel(kwargs) -> Dict:
        '''Parse locals to json compatible camelcased keys'''
        return {camelcase(key): val for (key, val) in kwargs.items() if key != "self" and val is not None}

    async def create_token(self, search: str = None) -> PipelineToken:
        '''Awaitable. Create a pipeline token that identifies this object (its parameters).'''
        await self._clean()
        self._get_rule(search)
        self._get_server()
        self._refactor()
        self._validate()
        if not hasattr(self._meta, "pipeline"): raise RuntimeError("Pyot pipeline for this model is not activated or lost")
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

    def raw(self):
        """Return the raw response of the request, only available for Core objects"""
        return self._meta.raw_data

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
