from typing import Dict, List, Mapping, Any, get_type_hints
import inspect
import re

from pyot.pipeline.core import Pipeline
from pyot.pipeline.token import PipelineToken
from pyot.utils import camelcase, fast_copy
from pyot.pipeline import pipelines

from .functional import lazy_property, laziable


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
            if issubclass(clas, PyotCoreObject):
                try:
                    cls.set_server_type(clas, inspect.getfullargspec(clas.__init__).args)
                except TypeError:
                    pass
            clas.Meta.lazy_props = [prop.split(".") for prop in cls.get_lazy_props(clas, [])]
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
        try:
            return next(base for base in deep_bases if base.__name__ == 'PyotCore')
        except StopIteration:
            return next(base for base in deep_bases if base.__name__ == 'PyotStatic')

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

    @staticmethod
    def set_server_type(clas, args):
        for server in clas.Meta.server_type_names:
            if server in args:
                clas.Meta.server_type = server
                return
        raise TypeError("Invalid or missing server type was passed as subclass")


class PyotStaticObject(metaclass=PyotMetaClass):

    class Meta:
        # Mutable objects should be overriden on inheritance
        server_type: str
        server_map: List[str]
        lazy_props: List[str]
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
            lazy = self.__dict__.pop('_lazy__' + name)
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

    def _load_lazy_prop(self, instance, prop, ind=0):
        if ind == len(prop):
            return
        try:
            attr = getattr(instance, prop[ind])
        except AttributeError:
            return
        if isinstance(attr, list):
            for val in attr:
                self._load_lazy_prop(val, prop, ind + 1)
        else:
            self._load_lazy_prop(attr, prop, ind + 1)

    def _recursive_dict(self):
        dic = {}
        for key, val in self._meta.types.items():
            try:
                obj = getattr(self, key)
            except AttributeError:
                continue
            try:
                if issubclass(val, PyotStaticObject):
                    try:
                        if isinstance(obj, list):
                            dic[key] = [ob._recursive_dict() for ob in obj]
                        else:
                            dic[key] = obj._recursive_dict()
                    except AttributeError:
                        pass
                else:
                    dic[key] = obj
            except TypeError:
                pass
        return dic

    def dict(self, deepcopy=False, lazy_props=False, recursive=False):
        if lazy_props:
            for prop in self._meta.lazy_props:
                self._load_lazy_prop(self, prop)
        dic = self._recursive_dict() if recursive else self._meta.data
        return fast_copy(dic) if deepcopy else dic.copy()


class PyotContainerObject:

    class Meta:
        # THIS META CLASS IS NOT INHERITED ON CORE, USED ONLY ON CONTAINER
        server: str
        server_type: str = "locale"
        server_type_names = {"platform", "region", "locale"}
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
            if name in self._meta.server_type_names and val is not None:
                setattr(self, name, val.lower())

    def _get_server(self):
        server_type = self._meta.server_type
        server = getattr(self, server_type)
        list_ = getattr(self._meta, server_type+"_list")
        if server.lower() not in list_:
            raise ValueError(
                f"Invalid '{server_type}' value, '{server}' was given"
                f"{'. Did you activate the settings and set a default value ?' if not server else ''}"
            )
        self._meta.server = server.lower()
        return self

    def _set_server_type(self, kwargs):
        for server in self._meta.server_type_names:
            if server in kwargs:
                self._meta.server_type = server
                return
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
        server_type_names = {"platform", "region", "locale"}
        allow_query: bool = False
        rules: Mapping[str, List[str]] = {}
        region_list = []
        platform_list = []
        locale_list = []
        turbo_level: int = 0
        raw_data: Any
        filtered_load: str = ""

    def _lazy_set(self, kwargs):
        # META CLASS UNIQUE MUTABLE OBJECTS
        self._meta = self.Meta()
        self._meta.query = {}
        self._meta.data = {}
        self._meta.body = {}

        kwargs.pop("self")
        for name, val in kwargs.items():
            if val is not None:
                self._meta.data[name] = val
                setattr(self, name, val)
        return self

    async def get(self, sid: str = None, pipeline: str = None, deepcopy: bool = False):
        '''Awaitable. Execute a GET request against the pipeline.'''
        self.set_pipeline(pipeline)
        token = await self.create_token()
        data = await self._meta.pipeline.get(token, sid)
        data = self._filter(data)
        self._meta.raw_data = fast_copy(data) if deepcopy else data
        self._meta.data = self._transform(data)
        self._fill()
        return self

    async def post(self, sid: str = None, pipeline: str = None, deepcopy: bool = False):
        '''Awaitable. Execute a POST request against the pipeline.'''
        self.set_pipeline(pipeline)
        token = await self.create_token()
        data = await self._meta.pipeline.post(token, self._meta.body, sid)
        data = self._filter(data)
        self._meta.raw_data = fast_copy(data) if deepcopy else data
        self._meta.data = self._transform(data)
        self._fill()
        return self

    async def put(self, sid: str = None, pipeline: str = None, deepcopy: bool = False):
        '''Awaitable. Execute a PUT request against the pipeline.'''
        self.set_pipeline(pipeline)
        token = await self.create_token()
        data = await self._meta.pipeline.put(token, self._meta.body, sid)
        data = self._filter(data)
        self._meta.raw_data = fast_copy(data) if deepcopy else data
        self._meta.data = self._transform(data)
        self._fill()
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

    async def create_token(self) -> PipelineToken:
        '''Awaitable. Create a pipeline token that identifies this object (its parameters).'''
        await self._setup()
        self._get_rule()
        self._get_server()
        self._clean()
        try:
            return PipelineToken(self._meta.pipeline.model, self._meta.server, self._meta.key, self._meta.load, self._meta.query)
        except AttributeError as e:
            raise RuntimeError("Token creation failed, please make sure pipeline is activated") from e

    def _get_rule(self):
        if len(self._meta.rules) == 0:
            raise RuntimeError("This Pyot object is not getable")
        for key, attr in self._meta.rules.items():
            load = {}
            for a in attr:
                try:
                    load[a] = getattr(self, a)
                except AttributeError:
                    break
            else:
                self._meta.key = key
                self._meta.load = load
                return self
        raise TypeError("Incomplete values to create request token")

    def _hide_load_value(self, key):
        self._meta.filtered_load += str(self._meta.load.pop(key))

    @staticmethod
    def _parse_camel(kwargs) -> Dict:
        return {camelcase(key): val for (key, val) in kwargs.items() if key != "self" and val is not None}

    def raw(self):
        """Return the raw response of the request, only available for Core objects"""
        return self._meta.raw_data

    async def _setup(self):
        pass

    def _clean(self):
        pass

    def _transform(self, data) -> Dict:
        return data

    def _filter(self, data):
        return data
