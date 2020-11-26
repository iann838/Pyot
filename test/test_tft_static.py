from pyot.utils import loop_run
from pyot.models import tft


async def async_profile_icons():
    val = await tft.ProfileIcons(locale="en_us").get()
    for v in val:
        v.dict(pyotify=True)


async def async_profile_icon():
    val = await tft.ProfileIcon(id=28, locale="en_us").get()
    val.dict(pyotify=True)


async def async_champions():
    val = await tft.Champions(set=3).get()
    for v in val:
        v.dict(pyotify=True)

async def async_champion():
    val = await tft.Champion(key="TFT4_Aatrox").get()
    val.dict(pyotify=True)


async def async_items():
    val = await tft.Items(locale="en_us").get()
    for v in val:
        v.dict(pyotify=True)

async def async_item():
    val = await tft.Item(id=28).get()
    val.dict(pyotify=True)


async def async_traits():
    val = await tft.Traits(set=4, locale="zh_cn").get()
    for v in val:
        v.dict(pyotify=True)

async def async_trait():
    val = await tft.Trait(key="Divine", set=4).get()
    val.dict(pyotify=True)


def test_profile_icons():
    loop_run(async_profile_icons())

def test_profile_icon():
    loop_run(async_profile_icon())

def test_champions():
    loop_run(async_champions())

def test_champion():
    loop_run(async_champion())

def test_items():
    loop_run(async_items())

def test_item():
    loop_run(async_item())

def test_traits():
    loop_run(async_traits())

def test_trait():
    loop_run(async_trait())