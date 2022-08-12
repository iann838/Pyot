from typing import Dict, List, Mapping, Any, Set, Tuple, Type, Union, get_type_hints
import inspect
import re

from pyot.conf.pipeline import pipelines
from pyot.pipeline.core import Pipeline
from pyot.pipeline.token import PipelineToken
from pyot.utils.copy import fast_copy

from .functional import lazy_property, is_laziable, convert_keys_camel_case


class PyotLazy:

    def __init__(self, container: Union[None, Type[list], Type[dict]], clas: Union[Type["PyotStaticBase"], Type["PyotCoreBase"]], obj: Any, root: "PyotCoreBase"):
        self.container = container
        self.clas = clas
        self.root = root
        self.obj = obj

    def __call__(self):
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
        except Exception as e:
            raise RuntimeError(f"Failed to lazy load '{self.clas.__name__}' object due to: ({type(e)}) {e}") from e

    def load_static(self, obj):
        instance: "PyotStaticBase" = self.clas(obj)
        instance._meta.root = self.root
        return instance.fill()

    def load_core(self, obj):
        kwargs = {}
        if "version" in self.clas.Meta.arg_names:
            try: kwargs["version"] = self.root.version
            except AttributeError: pass
        if "locale" in self.clas.Meta.arg_names:
            try: kwargs["locale"] = self.root.locale
            except AttributeError: pass
        if "platform" in self.clas.Meta.arg_names and "platform" in self.root.Meta.arg_names:
            try: kwargs["platform"] = self.root.platform
            except AttributeError: pass
        if "region" in self.clas.Meta.arg_names and "region" in self.root.Meta.arg_names:
            try: kwargs["region"] = self.root.region
            except AttributeError: pass
        instance: "PyotCoreBase" = self.clas(**kwargs)
        instance._meta.root = self.root
        instance._meta.data = instance.transform(obj)
        return instance.fill()


class PyotRoutingBase:

    class Meta:
        root: "PyotCoreBase"
        pipeline: Pipeline

    _meta: Meta
    _region: str = None
    _platform: str = None
    _locale: str = None
    _version: str = None
    _regions: Set[str] = set()
    _platforms: Set[str] = set()
    _platform2regions: Dict[str, str] = {None: None}

    @property
    def region(self) -> str:
        val = self._region or self._meta.root._region or \
            self._platform2regions.get(self._platform or self._meta.root._platform, None)
        if val is None:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'region'")
        return val

    @region.setter
    def region(self, val: str):
        val = val.lower()
        if val not in self._regions:
            raise ValueError(f"'{val}' is not a valid region")
        self._region = val

    @property
    def platform(self) -> str:
        val = self._platform or self._meta.root._platform
        if val is None:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'platform'")
        return val

    @platform.setter
    def platform(self, val: str):
        val = val.lower()
        if val not in self._platforms:
            raise ValueError(f"'{val}' is not a valid platform")
        self._platform = val

    @property
    def locale(self) -> str:
        val = self._locale or self._meta.root._locale
        if val is None:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'locale'")
        return val

    @locale.setter
    def locale(self, val: str):
        self._locale = val

    @property
    def version(self) -> str:
        val = self._version or self._meta.root._version
        if val is None:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute 'version'")
        return val

    @version.setter
    def version(self, val: str):
        self._version = val

    @property
    def metaroot(self) -> "PyotCoreBase":
        return self._meta.root

    @property
    def metapipeline(self) -> Pipeline:
        return self._meta.pipeline


class PyotMetaClass(type):

    def __new__(cls, name, bases, attrs):
        if 'Meta' not in attrs and cls.is_static_core(bases):
            attrs['Meta'] = type('Meta', (cls.get_static_core(bases).Meta,), {'__module__': attrs['__module__'] + f".{name}"})
        clas: "PyotStaticBase" = super().__new__(cls, name, bases, attrs)
        clas.Meta.types = cls.get_types(clas)
        clas.Meta.nomcltrs = {}
        if cls.is_static_core(bases):
            if issubclass(clas, PyotCoreBase):
                try:
                    arg_names = set(inspect.getfullargspec(clas.__init__).args)
                    cls.set_server_type(clas, arg_names)
                    clas.Meta.arg_names = arg_names
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
    def get_types(clas: "PyotStaticBase"):
        types = get_type_hints(clas)
        for typ, clas in types.items():
            try:
                if clas.__origin__ is list:
                    types[typ] = (clas.__args__[0], list)
                elif clas.__origin__ is dict:
                    types[typ] = (clas.__args__[1], dict)
                else:
                    types[typ] = (clas, None)
            except Exception:
                types[typ] = (clas, None)
        return types

    @staticmethod
    def get_lazy_props(clas: "PyotStaticBase", props, prefix=""):
        props += [prefix + p for p in dir(clas) if isinstance(getattr(clas, p), lazy_property)]
        types = {attr:cl for attr, cl in clas.Meta.types.items() if inspect.isclass(cl) and issubclass(cl, PyotStaticBase)}
        for typ, cl in types.items():
            PyotMetaClass.get_lazy_props(cl, props, prefix + typ + ".")
        return props

    @staticmethod
    def set_server_type(clas: "PyotCoreBase", args):
        for server in clas.Meta.server_type_names:
            if server in args:
                clas.Meta.server_type = server
                return


class PyotStaticBase(PyotRoutingBase, metaclass=PyotMetaClass):

    class Meta(PyotRoutingBase.Meta):
        # Mutable objects should be overriden on inheritance
        server_type: str = None
        lazy_props: List[str]
        nomcltrs: Dict[str, Any]
        types: Dict[str, Tuple[Any, Union[None, Type[list], Type[dict]]]]
        data: Dict[str, Any]
        raws: Set[str] = set()
        renamed: Dict[str, str] = {}

    _meta: Meta

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

    def qualkey(self, key: str) -> str:
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
        newkey = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        if newkey in self._meta.renamed:
            newkey = self._meta.renamed[newkey]
        return newkey

    def fill(self):
        mapping = self._meta.nomcltrs

        for key, val in self._meta.data.items():
            try:
                attr = mapping[key]
            except KeyError:
                attr = self.qualkey(key)
                mapping[key] = attr

            if is_laziable(val):
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

    def load_lazy_properties(self, instance, prop, ind=0):
        if ind == len(prop):
            return
        try:
            attr = getattr(instance, prop[ind])
        except AttributeError:
            return
        if isinstance(attr, list):
            for val in attr:
                self.load_lazy_properties(val, prop, ind + 1)
        elif isinstance(attr, dict):
            for val in attr.values():
                self.load_lazy_properties(val, prop, ind + 1)
        else:
            self.load_lazy_properties(attr, prop, ind + 1)

    def rdict(self):
        dic = {}
        for key, (val, container) in self._meta.types.items():
            if key.startswith("_"):
                continue
            try:
                obj = getattr(self, key)
            except AttributeError:
                continue
            try:
                if issubclass(val, PyotStaticBase):
                    try:
                        if container is None:
                            dic[key] = obj.rdict()
                        elif issubclass(container, list):
                            dic[key] = [ob.rdict() for ob in obj]
                        elif issubclass(container, dict):
                            dic[key] = {okey: ob.rdict() for okey, ob in obj.items()}
                        else:
                            raise TypeError(f"Invalid container type '{container.__name__}'")
                    except AttributeError:
                        pass
                else:
                    dic[key] = obj
            except TypeError:
                pass
        return dic

    def dict(self, force_copy=False, lazy_props=False, recursive=False):
        if lazy_props:
            for prop in self._meta.lazy_props:
                self.load_lazy_properties(self, prop)
        dic = self.rdict() if recursive else self._meta.data
        return fast_copy(dic) if force_copy else dic.copy()


class PyotCoreBase(PyotStaticBase):

    class Meta(PyotStaticBase.Meta):
        # Mutable objects should be overriden on inheritance
        key: str
        server: str
        load: Mapping[str, Any]
        query: Mapping[str, Any]
        body: Mapping[str, Any]
        arg_names: Set[str]
        server_type: str
        server_type_names = {"platform", "region"}
        rules: Mapping[str, List[str]] = {}
        raw_data: Any

    _meta: Meta

    def initialize(self, kwargs: Dict):
        # Instantiate meta class and fill kwargs
        self._meta = self.Meta()
        self._meta.root = self
        self._meta.query = {}
        self._meta.data = {}
        self._meta.body = {}

        kwargs.pop("self", None)
        kwargs.pop("__class__", None)
        for name, val in kwargs.items():
            if val is not None:
                self._meta.data[name] = val
                setattr(self, name, val)
        return self

    def _match_rule(self):
        if len(self._meta.rules) == 0:
            raise TypeError("This Pyot object is static")
        for key, attr in self._meta.rules.items():
            load = {}
            for a in attr:
                try:
                    checkonly = a.startswith('?')
                    if checkonly:
                        getattr(self, a[1:])
                        continue
                    load[a] = getattr(self, a)
                except AttributeError:
                    break
            else:
                self._meta.key = key
                self._meta.load = load
                return self
        raise TypeError("Incomplete values for pipeline token creation")

    def _match_server(self):
        server_type = self._meta.server_type
        if server_type:
            server: str = getattr(self, server_type)
            self._meta.server = server.lower()
        else:
            self._meta.server = None
        return self

    def _place_query(self, kwargs: Dict):
        '''Parse and place request query parameters from dict.'''
        kwargs.pop("self", None)
        kwargs.pop("__class__", None)
        self._meta.query = convert_keys_camel_case(kwargs)

    def _place_body(self, kwargs: Dict):
        '''Parse and place request body parameters from dict.'''
        kwargs.pop("self", None)
        kwargs.pop("__class__", None)
        self._meta.body = convert_keys_camel_case(kwargs)

    def _after_request(self, data: Any, force_copy: bool):
        data = self.filter(data)
        self._meta.raw_data = fast_copy(data) if force_copy else data
        self._meta.data = self.transform(data)
        self.fill()

    async def setup(self):
        """Coroutine. Set up the object to make request, this comes before `validate()`."""

    async def token(self) -> PipelineToken:
        '''Coroutine. Create a pipeline token that identifies this object (its parameters).'''
        await self.setup()
        self._match_rule()
        self._match_server()
        self.validate()
        try:
            return PipelineToken(self._meta.pipeline.model, self._meta.server, self._meta.key, self._meta.load, self._meta.query)
        except AttributeError as e:
            raise ValueError("Token creation failed, please ensure a pipeline is activated or provided") from e

    async def get(self, force_copy: bool = False):
        '''Coroutine. Make a GET request to the pipeline.'''
        data = await self._meta.pipeline.get(await self.token())
        self._after_request(data, force_copy)
        return self

    async def post(self, force_copy: bool = False):
        '''Coroutine. Make a POST request to the pipeline.'''
        data = await self._meta.pipeline.post(await self.token(), self._meta.body)
        self._after_request(data, force_copy)
        return self

    async def put(self, force_copy: bool = False):
        '''Coroutine. Make a PUT request to the pipeline.'''
        data = await self._meta.pipeline.put(await self.token(), self._meta.body)
        self._after_request(data, force_copy)
        return self

    def using(self, pipeline_name: str):
        '''Set the pipeline used for request.'''
        try:
            self._meta.pipeline = pipelines[pipeline_name]
        except KeyError as e:
            raise ValueError(f"Pipeline '{pipeline_name}' does not exist, inactive or dead") from e
        return self

    def validate(self):
        """Validate the object to make request, this comes right before the request."""

    def filter(self, data):
        """Filter out the requested data from the response, this comes right after the request and before 'transform()'."""
        return data

    def transform(self, data) -> Dict:
        """Transform the data into a pyot compatible structure non-destructively, this comes after `filter()`."""
        return data

    def raw(self):
        """Return the raw response of the request, only available for Core objects"""
        return self._meta.raw_data

    @classmethod
    def load(cls, raw: Any):
        o = cls()
        o._meta.raw_data = raw
        o._meta.data = o.transform(raw)
        o.fill()
        return o


class PyotUtilBase: pass
