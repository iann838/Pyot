from dataclasses import dataclass, field
from importlib import import_module
from typing import Mapping, Any, List
from .pipeline import PyotPipeline
from .__core__ import run, REGISTRY
import aiohttp


@dataclass
class Settings:
    MODEL: str
    PIPELINE: Mapping[str, Any]
    DEFAULT_REGION: str = "AMERICAS"
    DEFAULT_PLATFORM: str = "NA1"
    DEFAULT_LOCALE: str = "EN_US"
    GATHERER: Mapping[str, Any] = field(default_factory=dict)
    LOCALE_MAP: Mapping[str, str] = field(default_factory=dict)

    def activate(self):
        module = import_module(f"pyot.models.{self.MODEL.lower()}.__core__")
        pyot_base = getattr(module, "PyotBaseObject")
        self._check_platform(self.DEFAULT_PLATFORM, pyot_base)
        self._check_region(self.DEFAULT_REGION, pyot_base)
        self._check_locale(self.DEFAULT_LOCALE, pyot_base)
        self._check_locale_map(self.LOCALE_MAP, pyot_base)
        pyot_obj = getattr(module, "PyotCore")
        self.pipeline = PyotPipeline(self._make_pipeline(self.PIPELINE))
        pyot_obj.set_pipeline(self.pipeline)
        pyot_base.set_platform(self.DEFAULT_PLATFORM)
        pyot_base.set_region(self.DEFAULT_REGION)
        pyot_base.set_locale(self.DEFAULT_LOCALE)
        self.LOCALE_MAP = {key.lower(): val.lower() for (key, val) in self.LOCALE_MAP.items()}
        pyot_base.override_locale(self.LOCALE_MAP)
        self.GATHERER = {key.lower(): val for (key, val) in self.GATHERER.items()}
        self._check_gatherer()
        REGISTRY.GATHERER_SETTINGS.update(self.GATHERER)
        run(self.pipeline.initialize())
        REGISTRY.PIPELINES[self.MODEL.lower()] = self.pipeline

    def _make_pipeline(self, pipeline_configs):
        stores = []
        _track = []
        for config in pipeline_configs:
            config = { key.lower():value for (key,value) in config.items()}
            store_cls_name = config["backend"].split('.')[-1]
            store_path = '.'.join(config.pop("backend").split('.')[:-1])
            module = import_module(store_path)
            store_cls = getattr(module, store_cls_name)
            if store_cls_name in _track and store_cls.unique == True:
                raise RuntimeError(f"Store '{store_cls_name}' should only have one instance in the pipeline")
            _track.append(store_cls_name)
            config.update({"game": self.MODEL.lower()})
            store = store_cls(**config)
            stores.append(store)
        return stores

    def _check_gatherer(self):
        for key in self.GATHERER.keys():
            if key not in REGISTRY.GATHERER_SETTINGS.keys():
                raise AttributeError(f"Invalid attribute for 'PyotGatherer' object, '{key}' was given")

    def _check_platform(self, value, base):
        if value.lower() not in base.Meta.platform_list:
            raise AttributeError(f"Invalid 'platform' attribute, '{value}' was given")

    def _check_region(self, value, base):
        if value.lower() not in base.Meta.region_list:
            raise AttributeError(f"Invalid 'region' attribute, '{value}' was given")

    def _check_locale(self, value, base):
        if value.lower() not in [l.lower() for l in base.Meta.locale_list]:
            raise AttributeError(f"Invalid 'locale' attribute, '{value}' was given")

    def _check_locale_map(self, locale, base):
        for key, val in locale.items():
            try:
                self._check_platform(key, base)
            except AttributeError:
                self._check_region(key, base)
            self._check_locale(val, base)
