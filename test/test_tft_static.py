import pyot


async def async_profile_icons():
    val = await pyot.tft.ProfileIcons(locale="en_us").get()
    for v in val:
        v.dict(pyotify=True)


async def async_profile_icon():
    val = await pyot.tft.ProfileIcon(id=28, locale="en_us").get()
    val.dict(pyotify=True)


async def async_champions():
    val = await pyot.tft.Champions(set=3).get()
    for v in val:
        v.dict(pyotify=True)

async def async_champion():
    val = await pyot.tft.Champion(key="TFT3_Darius").get()
    val.dict(pyotify=True)


async def async_items():
    val = await pyot.tft.Items(locale="en_us").get()
    for v in val:
        v.dict(pyotify=True)

async def async_item():
    val = await pyot.tft.Item(id=28).get()
    val.dict(pyotify=True)


async def async_traits():
    val = await pyot.tft.Traits(set=3, locale="zh_cn").get()
    for v in val:
        v.dict(pyotify=True)

async def async_trait():
    val = await pyot.tft.Trait(key="Battlecast", set=3).get()
    val.dict(pyotify=True)


def test_profile_icons():
    pyot.run(async_profile_icons())

def test_profile_icon():
    pyot.run(async_profile_icon())

def test_champions():
    pyot.run(async_champions())

def test_champion():
    pyot.run(async_champion())

def test_items():
    pyot.run(async_items())

def test_item():
    pyot.run(async_item())

def test_traits():
    pyot.run(async_traits())

def test_trait():
    pyot.run(async_trait())