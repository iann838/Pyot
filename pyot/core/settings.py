from dataclasses import dataclass
from importlib import import_module
from typing import Mapping, Any
from .pipeline import PyotPipeline
from .core import run

_region_list = ["americas", "europe", "asia"]
_platform_list = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"]
_locale_list = ["cs_cz", "de_de", "en_us", "el_gr", "en_au", "en_gb", "en_ph", "en_sg", "es_ar", 
    "es_es", "es_mx", "fr_fr", "hu_hu", "it_it", "ja_jp", "ko_kr", "pl_pl", "pt_br", "ro_ro", 
    "ru_ru", "th_th", "tr_tr", "vn_vn", "zh_cn", "zh_my", "zh_tw"]


@dataclass
class PyotSettings:
    GAME_VARIANT: str
    PIPELINE: Mapping[str, Any]
    DEFAULT_REGION: str = "AMERICAS"
    DEFAULT_PLATFORM: str = "NA1"
    DEFAULT_LOCALE: str = "EN_US"

    def activate(self):
        self._check_platform(self.DEFAULT_PLATFORM)
        self._check_region(self.DEFAULT_REGION)
        self._check_locale(self.DEFAULT_LOCALE)
        module = import_module(f"pyot.{self.GAME_VARIANT.lower()}.__core__")
        pyot_obj = getattr(module, "PyotCore")
        self.pipeline = PyotPipeline(self._make_pipeline(self.PIPELINE))
        pyot_obj.set_pipeline(self.pipeline)
        pyot_obj.set_platform(self.DEFAULT_PLATFORM)
        pyot_obj.set_region(self.DEFAULT_REGION)
        pyot_obj.set_locale(self.DEFAULT_LOCALE)
        run(self.pipeline.initialize())

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
            config.update({"game": self.GAME_VARIANT.lower()})
            store = store_cls(**config)
            stores.append(store)
        return stores

    def _check_platform(self, value):
        if value.lower() not in _platform_list:
            raise AttributeError(f"Invalid 'platform' attribute, '{value}' was given")

    def _check_region(self, value):
        if value.lower() not in _region_list:
            raise AttributeError(f"Invalid 'region' attribute, '{value}' was given")

    def _check_locale(self, value):
        if value.lower() not in _locale_list:
            raise AttributeError(f"Invalid 'locale' attribute, '{value}' was given")
