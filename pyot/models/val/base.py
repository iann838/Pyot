from pyot.core.objects import PyotCoreBase, PyotStaticBase
from pyot.conf.pipeline import pipelines


MODULE_REPR = 'Valorant'


class PyotRouting:

    _regions = {"americas", "europe", "asia", "esports"}
    _platforms = {"ap", "br", "esports", "eu", "kr", "latam", "na"}


class PyotCore(PyotRouting, PyotCoreBase):

    class Meta(PyotCoreBase.Meta):
        pipeline = pipelines.val


class PyotStatic(PyotRouting, PyotStaticBase):

    class Meta(PyotStaticBase.Meta):
        pipeline = pipelines.val


bases = (PyotCore, PyotStatic)
