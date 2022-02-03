from pyot.core.objects import PyotCoreBase, PyotStaticBase
from pyot.conf.pipeline import pipelines


MODULE_REPR = 'Riot Services'


class PyotRouting:

    _regions = {"americas", "europe", "asia", "esports"}


class PyotCore(PyotRouting, PyotCoreBase):

    class Meta(PyotCoreBase.Meta):
        pipeline = pipelines.riot


class PyotStatic(PyotRouting, PyotStaticBase):

    class Meta(PyotStaticBase.Meta):
        pipeline = pipelines.riot


bases = (PyotCore, PyotStatic)
