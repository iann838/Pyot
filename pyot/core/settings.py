from dataclasses import dataclass, field
from importlib import import_module
from typing import Mapping, Any, List
from .pipeline import PyotPipeline
from .__core__ import run, registry

region_list = {
    "lol": ["americas", "europe", "asia"],
}
platform_list = {
    "lol": ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"]
}
locale_list = {
    "lol": ["cs_cz", "de_de", "en_us", "el_gr", "en_au", "en_gb", "en_ph", "en_sg", "es_ar", 
        "es_es", "es_mx", "fr_fr", "hu_hu", "it_it", "ja_jp", "ko_kr", "pl_pl", "pt_br", "ro_ro", 
        "ru_ru", "th_th", "tr_tr", "vn_vn", "zh_cn", "zh_my", "zh_tw"]
}


@dataclass
class PyotSettings:
    GAME_VARIANT: str
    PIPELINE: Mapping[str, Any]
    DEFAULT_REGION: str = "AMERICAS"
    DEFAULT_PLATFORM: str = "NA1"
    DEFAULT_LOCALE: str = "EN_US"
    LOCALE_MAP: Mapping[str, str] = field(default_factory=dict)

    def activate(self):
        module = import_module(f"pyot.models.{self.GAME_VARIANT.lower()}.__core__")
        self._check_platform(self.DEFAULT_PLATFORM, self.GAME_VARIANT.lower())
        self._check_region(self.DEFAULT_REGION, self.GAME_VARIANT.lower())
        self._check_locale(self.DEFAULT_LOCALE, self.GAME_VARIANT.lower())
        self._check_locale_map(self.LOCALE_MAP, self.GAME_VARIANT.lower())
        pyot_obj = getattr(module, "PyotCore")
        pyot_base = getattr(module, "PyotBaseObject")
        self.pipeline = PyotPipeline(self._make_pipeline(self.PIPELINE))
        pyot_obj.set_pipeline(self.pipeline)
        pyot_base.set_platform(self.DEFAULT_PLATFORM)
        pyot_base.set_region(self.DEFAULT_REGION)
        pyot_base.set_locale(self.DEFAULT_LOCALE)
        pyot_base.override_locale(self.LOCALE_MAP)
        run(self.pipeline.initialize())
        registry.PYOT_PIPELINES.append(self.pipeline)

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

    def _check_platform(self, value, game):
        if value.lower() not in platform_list[game]:
            raise AttributeError(f"Invalid 'platform' attribute, '{value}' was given")

    def _check_region(self, value, game):
        if value.lower() not in region_list[game]:
            raise AttributeError(f"Invalid 'region' attribute, '{value}' was given")

    def _check_locale(self, value, game):
        if value.lower() not in locale_list[game]:
            raise AttributeError(f"Invalid 'locale' attribute, '{value}' was given")

    def _check_locale_map(self, locale, game):
        for key, val in locale.items():
            try:
                self._check_platform(key, game)
            except AttributeError:
                self._check_region(key, game)
            self._check_locale(val, game)
