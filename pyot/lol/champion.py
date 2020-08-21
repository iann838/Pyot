from .__core__ import PyotCore, PyotStatic


class Champion(PyotCore):

    class Meta(PyotCore.Meta):
        rules = {
            "cdragon-champion-by-id": ["id"],
            "cdragon-champion-by-id": ["key"],
            "cdragon-champion-by-id": ["name"],
        }

    def __init__(self, id: int = None, key: str = None, name: str = None, locale: str = None):
        self._lazy_set(locals())


