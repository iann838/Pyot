from pyot.core.objects import PyotCoreObject, PyotStaticObject


class PyotBaseObject:

    class Meta:
        region_list = ["americas", "europe", "asia"]
        platform_list = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru", "pbe"]
        locale_list = ["cs_cz", "de_de", "en_us", "el_gb", "en_au", "en_gb", "en_ph", "en_sg", "es_ar", 
            "es_es", "es_mx", "fr_fr", "hu_hu", "it_it", "ja_jp", "ko_kr", "pl_pl", "pt_br", "ro_ro", 
            "ru_ru", "th_th", "tr_tr", "vn_vn", "zh_cn", "zh_my", "zh_tw", "default"]

        to_locale = {
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
