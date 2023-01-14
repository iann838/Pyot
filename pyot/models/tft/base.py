from pyot.core.objects import PyotCoreBase, PyotStaticBase
from pyot.conf.pipeline import pipelines


MODULE_REPR = 'Teamfight Tactics'


class PyotRouting:

    _regions = {"americas", "europe", "asia", "sea", "esports"}
    _platforms = {"br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru", "ph2", "sg2", "th2", "tw2", "vn2"}
    _platform2regions = {
        "br1": "americas",
        "eun1": "europe",
        "euw1": "europe",
        "jp1": "asia",
        "kr": "asia",
        "la1": "americas",
        "la2": "americas",
        "na1": "americas",
        "oc1": "sea",
        "tr": "europe",
        "ru": "europe",
        "ph2": "sea",
        "sg2": "sea",
        "th2": "sea",
        "tw2": "sea",
        "vn2": "sea",
    }


class PyotCore(PyotRouting, PyotCoreBase):

    class Meta(PyotCoreBase.Meta):
        pipeline = pipelines.tft


class PyotStatic(PyotRouting, PyotStaticBase):

    class Meta(PyotStaticBase.Meta):
        pipeline = pipelines.tft


bases = (PyotCore, PyotStatic)
