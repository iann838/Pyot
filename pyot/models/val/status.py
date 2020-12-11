from .__core__ import PyotCore, PyotStatic
from dateutil.parser import parse
from datetime import datetime
from typing import List


# PYOT STATIC OBJECTS

class StatusContentData(PyotStatic):
    locale: str
    content: str


class StatusUpdateData(PyotStatic):
    id: int
    author: str
    publish: bool
    publish_locations: List[str] # (Legal values: riotclient, riotstatus, game)
    translations: List[StatusContentData]
    created_at: datetime
    updated_at: datetime

    class Meta(PyotCore.Meta):
        raws = ["publish_locations"]

    def __getattribute__(self, name):
        if name in ["created_at", "updated_at"]:
            timestr = super().__getattribute__(name)
            return parse(timestr) if timestr is not None else timestr
        return super().__getattribute__(name)


class StatusDetailData(PyotStatic):
    id: int
    maintenance_status: str # (Legal values: scheduled, in_progress, complete)
    incident_severity: str # (Legal values: info, warning, critical)
    titles: List[StatusContentData]
    updates: List[StatusUpdateData]
    created_at: datetime
    archive_at: datetime
    updated_at: datetime
    platforms: List[str]

    class Meta(PyotCore.Meta):
        raws = ["platforms"]

    def __getattribute__(self, name):
        if name in ["created_at", "archive_at", "updated_at"]:
            timestr = super().__getattribute__(name)
            return parse(timestr) if timestr is not None else timestr
        return super().__getattribute__(name)


# PYOT CORE OBJECTS

class Status(PyotCore):
    id: str
    name: str
    locales: List[str]
    maintenances: List[StatusDetailData]
    incidents: List[StatusDetailData]

    class Meta(PyotCore.Meta):
        rules = {"status_v1_platform_data": []}
        raws = ["locales"]

    def __init__(self, platform: str = None):
        self._lazy_set(locals())
