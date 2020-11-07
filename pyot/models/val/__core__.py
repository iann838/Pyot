from pyot.core.objects import PyotCoreObject, PyotStaticObject


class PyotBaseObject:

    class Meta:
        region_list = ["americas", "europe", "asia"]
        platform_list = ["ap", "br", "eu", "kr", "latam", "na"]
        locale_list = ["ar-ae", "de-de", "en-gb", "en-us", "es-es", "es-mx", "fr-fr", "id-id",
            "it-it", "ja-jp", "ko-kr", "pl-pl", "pt-br", "ru-ru", "th-th", "tr-tr",
            "vi-vn", "zh-cn", "zh-tw"]

        to_locale = {
            "ap": "en-us",
            "br": "en-us",
            "eu": "en-us",
            "kr": "en-us",
            "latam": "en-us",
            "na": "en-us",
        }

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
        cls.Meta.to_locale.update(locale_map)
    
    def to_locale(self, platform):
        return self.Meta.to_locale[platform]


class PyotCore(PyotBaseObject, PyotCoreObject):

    class Meta(PyotBaseObject.Meta, PyotCoreObject.Meta):
        pass

    @classmethod
    def bind_pipeline(cls, pipeline):
        cls.Meta.pipeline = pipeline


class PyotStatic(PyotStaticObject):

    class Meta(PyotBaseObject.Meta, PyotStaticObject.Meta):
        pass

    def to_locale(self, platform):
        return self.Meta.to_locale[platform]
