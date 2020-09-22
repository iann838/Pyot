from pyot.models import riot
from pyot.utils import loop_run


async def async_account():
    account = await riot.Account(name="stelar7", tag="stl7", region="AMERICAS", pipeline="val").get()
    assert isinstance(account.puuid, str)
    assert isinstance(account.name, str)
    assert isinstance(account.tag, str)


async def async_active_platform():
    account = await riot.Account(name="stelar7", tag="stl7", region="AMERICAS", pipeline="val").get()
    active = await riot.ActivePlatform(puuid=account.puuid, game="val", pipeline="val", region="AMERICAS").get()
    assert isinstance(active.puuid, str)
    assert isinstance(active.pipeline, str)
    assert isinstance(active.platform_id, str)


def test_account():
    loop_run(async_account())

def test_active_platform():
    loop_run(async_active_platform())