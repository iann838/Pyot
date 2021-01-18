from pyot.core.objects import PyotCoreObject, PyotStaticObject
from pyot.utils import case_insensitive_dict


REGIONS = {"americas", "europe", "asia"}
PLATFORMS = {"ap", "br", "eu", "kr", "latam", "na"}
LOCALES = {"ar-ae", "de-de", "en-gb", "en-us", "es-es", "es-mx", "fr-fr", "id-id",
    "it-it", "ja-jp", "ko-kr", "pl-pl", "pt-br", "ru-ru", "th-th", "tr-tr",
    "vi-vn", "zh-cn", "zh-tw"}

LOCALIZATIONS = {
    "ap": "en-us",
    "br": "en-us",
    "eu": "en-us",
    "kr": "en-us",
    "latam": "en-us",
    "na": "en-us",
}


class ModelMixin:

    class Meta:
        region_list = REGIONS
        platform_list = PLATFORMS
        locale_list = LOCALES
        localizations = case_insensitive_dict(LOCALIZATIONS)

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

    @classmethod
    def bind_pipeline(cls, pipeline):
        cls.Meta.pipeline = pipeline


class PyotCore(ModelMixin, PyotCoreObject):

    class Meta(ModelMixin.Meta, PyotCoreObject.Meta):
        pass


class PyotStatic(ModelMixin, PyotStaticObject):

    class Meta(ModelMixin.Meta, PyotStaticObject.Meta):
        pass
