import pyot

async def async_account():
    account = await pyot.val.Account(name="stelar7", tag="stl7", region="AMERICAS").get()
    assert isinstance(account.puuid, str)
    assert isinstance(account.name, str)
    assert isinstance(account.tag, str)


async def async_active_platform():
    account = await pyot.val.Account(name="stelar7", tag="stl7", region="AMERICAS").get()
    active = await pyot.val.ActivePlatform(puuid=account.puuid, game="val").get()
    assert isinstance(active.puuid, str)
    assert isinstance(active.game, str)
    assert isinstance(active.platform_id, str)


def test_account():
    pyot.run(async_account())

def test_active_platform():
    pyot.run(async_active_platform())