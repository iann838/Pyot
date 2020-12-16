from datetime import datetime
from pyot.models import lol, val, lor
from pyot.utils import loop_run


def assert_status(obj: lol.Status):
    assert isinstance(obj.id, str)
    assert isinstance(obj.name, str)
    for locale in obj.locales:
        assert isinstance(locale, str)
    for t in [obj.maintenances, obj.incidents]:
        for m in t:
            assert isinstance(m.id, int)
            assert isinstance(m.maintenance_status, str) or m.maintenance_status is None
            assert isinstance(m.incident_severity, str) or m.incident_severity is None
            assert isinstance(m.created_at, datetime) or m.created_at is None
            assert isinstance(m.archive_at, datetime) or m.archive_at is None
            assert isinstance(m.updated_at, datetime) or m.updated_at is None
            for p in m.platforms:
                assert isinstance(p, str)
            up = m.updates
            tit = m.titles
            for ti in tit:
                assert isinstance(ti.locale, str)
                assert isinstance(ti.content, str)
            for u in up:
                assert isinstance(u.id, int)	
                assert isinstance(u.author, str)
                assert isinstance(u.publish, bool)
                assert isinstance(u.created_at, datetime) or u.created_at is None
                assert isinstance(u.updated_at, datetime) or u.updated_at is None
                for p in u.publish_locations:
                    assert isinstance(p, str)
                tra = u.translations
                for tr in tra:
                    assert isinstance(tr.locale, str)
                    assert isinstance(tr.content, str)


async def async_lol_status():
    status = await lol.Status(platform="NA1").get()
    assert_status(status)

async def async_lor_status():
    status = await lor.Status(region="AMERICAS").get()
    assert_status(status)

async def async_val_status():
    status = await val.Status(platform="NA").get()
    assert_status(status)


def test_lol_status():
    loop_run(async_lol_status())

def test_lor_status():
    loop_run(async_lor_status())

def test_val_status():
    loop_run(async_val_status())
