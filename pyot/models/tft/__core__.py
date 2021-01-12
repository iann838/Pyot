from pyot.core.objects import PyotCoreObject, PyotStaticObject
from pyot.utils import case_insensitive_dict


REGIONS = {"americas", "europe", "asia"}
PLATFORMS = {"br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"}
LOCALES = {"cs_cz", "de_de", "en_us", "el_gb", "en_au", "en_gb", "en_ph", "en_sg", "es_ar",
    "es_es", "es_mx", "fr_fr", "hu_hu", "it_it", "ja_jp", "ko_kr", "pl_pl", "pt_br", "ro_ro",
    "ru_ru", "th_th", "tr_tr", "vn_vn", "zh_cn", "zh_my", "zh_tw", "default"}

LOCALIZATIONS = {
    "br1": "en_us",
    "eun1": "en_us",
    "euw1": "en_us",
    "jp1": "en_us",
    "kr": "en_us",
    "la1": "en_us",
    "la2": "en_us",
    "na1": "en_us",
    "oc1": "en_us",
    "tr1": "en_us",
    "ru": "en_us",
    "americas": "en_us",
    "europe": "en_us",
    "asia": "en_us",
}
REGIONALIZATIONS = {
    "na1": "americas",
    "br1": "americas",
    "la1": "americas",
    "la2": "americas",
    "oc1": "americas",
    "kr": "asia",
    "jp1": "asia",
    "eun1": "europe",
    "euw1": "europe",
    "tr1": "europe",
    "ru": "europe"
}


class ModelMixin:

    class Meta:
        region_list = REGIONS
        platform_list = PLATFORMS
        locale_list = LOCALES
        localizations = case_insensitive_dict(LOCALIZATIONS)
        regionalizations = case_insensitive_dict(REGIONALIZATIONS)

    @classmethod
    def set_region(cls, region):
        cls.region = region.lower()
    
    @classmethod
    def set_platform(cls, platform):
        cls.platform = platform.lower()

    @classmethod
    def set_locale(cls, locale):
        cls.locale = locale.lower()

    @classmethod
    def override_locale(cls, locale_map):
        LOCALIZATIONS.update(locale_map)
        cls.Meta.localizations = case_insensitive_dict(LOCALIZATIONS)
    
    def to_locale(self, platform):
        return self.Meta.localizations[platform]

    def to_region(self, platform):
        return self.Meta.regionalizations[platform]

    @classmethod
    def bind_pipeline(cls, pipeline):
        cls.Meta.pipeline = pipeline


class PyotCore(ModelMixin, PyotCoreObject):

    class Meta(ModelMixin.Meta, PyotCoreObject.Meta):
        pass


class PyotStatic(ModelMixin, PyotStaticObject):

    class Meta(ModelMixin.Meta, PyotStaticObject.Meta):
        pass
