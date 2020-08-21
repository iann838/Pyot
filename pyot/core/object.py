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
        if platform is not None:
            if isinstance(obj, list):
                for l in obj:
                    l.update({"platform": platform})
            else:
                obj.update({"platform": platform})
        if region is not None:
            if isinstance(obj, list):
                for l in obj:
                    l.update({"region": region})
            else:
                obj.update({"region": region})
        if locale is not None:
            if isinstance(obj, list):
                for l in obj:
                    l.update({"locale": locale})
            else:
                obj.update({"locale": locale})
        self.obj = obj

    def __call__(self):
        if issubclass(self.clas, PyotCoreObject):
            if isinstance(self.obj, list):
                l = []
                for obj in self.obj:
                    l.append(self.clas(**obj))
                return l
            else:
                return self.clas(**self.obj)
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
        types: Dict[str, Any] = {}
        data: Dict[str, Any] = {}
        renamed: Dict[str, str] = {}
        special: Dict[str, Any] = {}

    region: str
    platform: str
    locale: str

    def __init__(self, data):
        self.Meta.types = get_type_hints(self.__class__)
        self.Meta.data = data

    def __getattribute__(self, name):
        try:
            if type(super().__getattribute__(name)) is PyotLazyObject:
                return super().__getattribute__(name)()
            else:
                return super().__getattribute__(name)
        except (KeyError, AttributeError):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _lazy_set(self, kwargs):
        self.Meta.types = get_type_hints(self.__class__)
        self.Meta.data = {}
        for name, val in kwargs.items():
            if val is not None and name != "self":
                self.Meta.data[name] = val
                setattr(self, name, val)
        return self
    
    def _normalize(self, data):
        new_data = {}
        for attr, val in data.items():
            name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', attr)
            snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
            new_data[snake_case] = val
        return new_data
    
    def _fill(self):
        data_ = self._normalize(self.Meta.data)
        if "platform" in data_.keys():
            self.platform = data_["platform"]
        if "region" in data_.keys():
            self.region = data_["region"]
        if "locale" in data_.keys():
            self.locale = data_["locale"]
        for attr, val in data_.items():
            attr = attr if attr not in self.Meta.renamed.keys() else self.Meta.renamed[attr]
            if attr in self.Meta.raws:
                setattr(self, attr, val)
            elif PyotLazyObject.need_lazy(val):
                try:
                    platform = self.platform
                except AttributeError:
                    platform = None
                try:
                    region = self.region
                except AttributeError:
                    region = None
                try:
                    locale = self.locale
                except AttributeError:
                    locale = None
                setattr(self, attr, PyotLazyObject(self.Meta.types[attr], val, platform, region, locale))
            elif attr not in ["platform", "region", "locale"]:
                setattr(self, attr, val)
        return self

    def dict(self, pyotify: bool = False):
        if not pyotify:
            return copy.deepcopy(self.Meta.data)
        def recursive(obj):
            dic = copy.deepcopy(obj.__dict__)
            for key, val in dic.items():
                if type(val) is PyotLazyObject:
                    obj = val()
                    if isinstance(obj, list):
                        dic[key] = []
                        for i in range(len(obj)):
                            recursive(obj[i])
                            dic[key].append(obj[i].__dict__)
                    else:
                        recursive(obj)
                        dic[key] = obj.__dict__
            return dic
        return recursive(self)


    def json(self, pyotify: bool = False):
        if not pyotify:
            return json.dumps(self.Meta.data)
        return json.dumps(self.pyot_dict())



class PyotCoreObject(PyotStaticObject):

    class Meta(PyotStaticObject.Meta):
        pipeline: PyotPipeline
        key: str
        server: str
        load: Mapping[str, Any]
        query: Mapping[str, Any] = {}
        types: Dict[str, Any] = None
        rules: Mapping[str, List[str]] = {}
        server_type: str = "platform"
        allow_query: bool = False
        region_list = ["americas", "europe", "asia"]
        platform_list = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"]
        locale_list = ["cs_cz", "de_de", "en_us", "el_gr", "en_au", "en_gb", "en_ph", "en_sg", "es_ar", 
            "es_es", "es_mx", "fr_fr", "hu_hu", "it_it", "ja_jp", "ko_kr", "pl_pl", "pt_br", "ro_ro", 
            "ru_ru", "th_th", "tr_tr", "vn_vn", "zh_cn", "zh_my", "zh_tw"]

    def __getattribute__(self, name):
        if name in ["region", "platform"] and name != self.Meta.server_type:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return super().__getattribute__(name)

    def query(self, **kwargs):
        if not self.Meta.allow_query:
            raise RuntimeError("This Pyot object does not accept queries")
        self.Meta.query = self._parse_query(locals())
        return self

    async def get(self):
        token = await self._create_token()
        data = await self.Meta.pipeline.get(token)
        self.Meta.data = await self._transform(data)
        self._fill()
        return self

    def _lazy_set(self, kwargs):
        if "platform" in kwargs.keys():
            self.Meta.server_type = "platform"
        elif "region" in kwargs.keys():
            self.Meta.server_type = "region"
        elif "locale" in kwargs.keys():
            self.Meta.server_type = "locale"
        else:
            raise RuntimeError("Invalid or missing server type was passed as subclass")
        return super()._lazy_set(kwargs)

    def _parse_query(self, kwargs):
        return {key: val for (key,val) in kwargs.items() if key != "self" and val is not None}

    async def _create_token(self):
        if not hasattr(self.Meta, "pipeline"): raise RuntimeError("Pyot for this variant wasn't activated")
        await self._clean()
        await self._get_rule()
        await self._check_server()
        token = PyotPipelineToken(self.Meta.server, self.Meta.key, self.Meta.load, self.Meta.query)
        await self._token_transform(token)
        return token

    async def _get_rule(self):
        if len(self.Meta.rules.keys()) == 0:
            raise RuntimeError("This Pyot object is not get-able")
        for key, attr in self.Meta.rules.items():
            load = {}
            for a in attr:
                try:
                    load[a] = getattr(self, a)
                except AttributeError:
                    break
            if len(load.keys()) != len(attr):
                continue
            self.Meta.key = key
            self.Meta.load = load
            return self
        raise AttributeError(f"'{self.__class__.__name__}' has missing or incomplete attributes")

    async def _check_server(self):
        if self.Meta.server_type == "platform":
            if self.platform.lower() not in self.Meta.platform_list:
                raise AttributeError(f"Invalid 'platform' attribute, '{self.platform}' was given")
            self.Meta.server = self.platform
        elif self.Meta.server_type == "region":
            if self.region.lower() not in self.Meta.region_list:
                raise AttributeError(f"Invalid 'region' attribute, '{self.region}' was given")
            self.Meta.server = self.region
        elif self.Meta.server_type == "locale":
            if self.locale.lower() not in self.Meta.locale_list:
                raise AttributeError(f"Invalid 'locale' attribute, '{self.locale}' was given")
            self.Meta.server = self.locale
        else:
            raise RuntimeError("Invalid or missing server type was passed as subclass")
        return self

    async def _transform(self, data):
        return data

    async def _clean(self):
        pass

    async def _token_transform(self, token):
        pass