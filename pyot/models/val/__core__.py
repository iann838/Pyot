from ...core.object import PyotCoreObject

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

