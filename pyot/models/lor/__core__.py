from pyot.core.objects import PyotCoreObject, PyotStaticObject, PyotContainerObject


class PyotBaseObject:

    class Meta:
        region_list = ["americas", "europe", "asia", "sea"]
        platform_list = []
        locale_list = ["de_de", "en_us", "es_es", "es_mx", "fr_fr", "it_it", "ja_jp", "ko_kr", "pl_pl", "pt_br", "th_th", "tr_tr", "ru_ru", "zh_tw"]

        to_locale = {
            # "br1": "en_us",
            # "eun1": "en_us",
            # "euw1": "en_us",
            # "jp1": "en_us",
            # "kr": "en_us",
            # "la1": "en_us",
            # "la2": "en_us",
            # "na1": "en_us",
            # "oc1": "en_us",
            # "tr1": "en_us",
            # "ru": "en_us",
            "americas": "en_us",
            "europe": "en_us",
            "asia": "en_us",
        }

        to_region = {
            # "na1": "americas",
            # "br1": "americas",
            # "la1": "americas",
            # "la2": "americas",
            # "oc1": "americas",
            # "kr": "asia",
            # "jp1": "asia",
            # "eun1": "europe",
            # "euw1": "europe",
            # "tr1": "europe",
            # "ru": "europe"
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

    def to_region(self, platform):
        return self.Meta.to_region[platform]


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


class PyotContainer(PyotBaseObject, PyotContainerObject):

    class Meta(PyotBaseObject.Meta, PyotContainerObject.Meta):
        pass

    def to_locale(self, platform):
        return self.Meta.to_locale[platform]
