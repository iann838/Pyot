from .__core__ import PyotCore, PyotStatic
from typing import List

# PYOT STATIC OBJECTS

class StatusTranslation(PyotStatic):
    updated_at: str
    locale: str
    content: str


class StatusMessage(PyotStatic):
    id: str
    severity: str
    updated_at: str
    author: str
    created_at: str
    content: str
    translations: List[StatusTranslation]


class StatusIncident(PyotStatic):
    id: int
    active: bool
    created_at: str
    updates: List[StatusMessage]


class StatusService(PyotStatic):
    incidents: List[StatusIncident]
    name: str
    slug: str
    status: str


# PYOT CORE OBJECTS

class Status(PyotCore):
    locales: List[str]
    hostname: str
    name: str
    services: List[StatusService]
    slug: str
    region_tag: str

    class Meta(PyotCore.Meta):
        rules = {"status_v3_shard_data": []}
        raws = ["locales"]

    def __init__(self, platform: str = None):
        self._lazy_set(locals())