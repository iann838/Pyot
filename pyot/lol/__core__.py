from ..core.object import PyotCoreObject, PyotStaticObject

class PyotCore(PyotCoreObject):

    @classmethod
    def set_pipeline(cls, pipeline):
        cls.Meta.pipeline = pipeline

    @classmethod
    def set_region(cls, region):
        cls.region = region
    
    @classmethod
    def set_platform(cls, platform):
        cls.platform = platform

    @classmethod
    def set_locale(cls, locale):
        cls.locale = locale


class PyotStatic(PyotStaticObject): pass