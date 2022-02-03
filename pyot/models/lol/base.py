from pyot.core.objects import PyotCoreBase, PyotStaticBase
from pyot.conf.pipeline import pipelines


MODULE_REPR = 'League of Legends'


class PyotRouting:

    _regions = {"americas", "europe", "asia", "esports"}
    _platforms = {"br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"}
    _platform2regions = {
        "br1": "americas",
        "eun1": "europe",
        "euw1": "europe",
        "jp1": "asia",
        "kr": "asia",
        "la1": "americas",
        "la2": "americas",
        "na1": "americas",
        "oc1": "americas",
        "tr1": "europe",
        "ru": "europe",
    }


class PyotCore(PyotRouting, PyotCoreBase):

    class Meta(PyotCoreBase.Meta):
        pipeline = pipelines.lol


class PyotStatic(PyotRouting, PyotStaticBase):

    class Meta(PyotStaticBase.Meta):
        pipeline = pipelines.lol


bases = (PyotCore, PyotStatic)
