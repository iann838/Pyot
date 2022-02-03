from pyot.core.objects import PyotCoreBase, PyotStaticBase
from pyot.conf.pipeline import pipelines


MODULE_REPR = 'Legends of Runeterra'


class PyotRouting:

    _regions = {"americas", "europe", "asia", "esports", "sea", "apac"}


class PyotCore(PyotRouting, PyotCoreBase):

    class Meta(PyotCoreBase.Meta):
        pipeline = pipelines.lor


class PyotStatic(PyotRouting, PyotStaticBase):

    class Meta(PyotStaticBase.Meta):
        pipeline = pipelines.lor


bases = (PyotCore, PyotStatic)
