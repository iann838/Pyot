from dataclasses import dataclass, field
from importlib import import_module
from typing import Mapping, Any, List

from pyot.pipeline.core import Pipeline
from pyot.pipeline import pipelines
from pyot.utils import import_class


@dataclass
class Settings:
    '''
    A settings object that modifies Pyot models behavior and its pipeline stacks.
    This object is essential for Pyot to work properly, unless pipelines are managed manually.
    `activate()` needs to be called to take effect the settings.
    '''
    MODEL: str
    PIPELINE: Mapping[str, Any] = None
    DEFAULT_REGION: str = None
    DEFAULT_PLATFORM: str = None
    DEFAULT_LOCALE: str = None
    LOCALE_MAP: Mapping[str, str] = field(default_factory=dict)

    def activate(self):
        '''Make the settings take effect.'''
        # IMPORT THE MODULE
        module = import_module(f"pyot.models.{self.MODEL.lower()}.__core__")
        # GET PYOT BASE FROM MODULE
        pyot_base = getattr(module, "PyotBaseObject")
        # CHECK THAT DEFAULTS MATCHES THE BASE AND SET IT
        if self.DEFAULT_PLATFORM:
            self._check_platform(self.DEFAULT_PLATFORM, pyot_base)
            pyot_base.set_platform(self.DEFAULT_PLATFORM)
        if self.DEFAULT_REGION:
            self._check_region(self.DEFAULT_REGION, pyot_base)
            pyot_base.set_region(self.DEFAULT_REGION)
        if self.DEFAULT_LOCALE:
            self._check_locale(self.DEFAULT_LOCALE, pyot_base)
            pyot_base.set_locale(self.DEFAULT_LOCALE)
        self._check_locale_map(self.LOCALE_MAP, pyot_base)
        self.LOCALE_MAP = {key.lower(): val.lower() for (key, val) in self.LOCALE_MAP.items()}
        pyot_base.override_locale(self.LOCALE_MAP)
        if self.PIPELINE is None:
            return
        # GET PYOT CORE FROM MODULE
        pyot_obj = getattr(module, "PyotCore")
        # MAKE PIPELINE AND APPEND IT
        self.pipeline = Pipeline(self.MODEL.lower(), self._make_pipeline(self.PIPELINE))
        pyot_obj.bind_pipeline(self.pipeline)
        # REGISTER THE PIPELINE
        pipelines[self.MODEL.lower()] = self.pipeline

    def _make_pipeline(self, pipeline_configs):
        stores = []
        _track = []
        for config in pipeline_configs:
            config = {key.lower() if key.upper() == key else key: value for (key,value) in config.items()}
            store_cls = import_class(config.pop("backend"))
            if store_cls in _track and store_cls.unique == True:
                raise RuntimeError(f"Store '{store_cls.__name__}' should only have one instance in the pipeline")
            _track.append(store_cls)
            config.update({"game": self.MODEL.lower()})
            store = store_cls(**config)
            stores.append(store)
        return stores

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
        if "*" in locale:
            locale_val = locale.pop("*")
            for key in base.Meta.to_locale:
                if key not in locale:
                    locale[key] = locale_val
        for key, val in locale.items():
            try:
                self._check_platform(key, base)
            except AttributeError:
                self._check_region(key, base)
            self._check_locale(val, base)
