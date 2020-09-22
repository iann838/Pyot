from pyot.utils import loop_run
from pyot.models import lol


async def async_profile_icons():
    val = await lol.ProfileIcons(locale="en_us").get()
    for v in val:
        v.dict(pyotify=True)


async def async_profile_icon():
    val = await lol.ProfileIcon(id=28, locale="en_us").get()
    val.dict(pyotify=True)


async def async_merakichampion():
    val = await lol.MerakiChampion(id=235).get()
    val.dict(pyotify=True)


async def async_merakiitem():
    val = await lol.MerakiItem(id=3153).get()
    val.dict(pyotify=True)


async def async_champion():
    val = await lol.Champion(key="Senna").get()
    val.dict(pyotify=True)


async def async_spells():
    val = await lol.Spells(locale="zh_cn").get()
    for v in val:
        v.dict(pyotify=True)


async def async_spell():
    val = await lol.Spell(id=12, locale="es_es").get()
    val.dict(pyotify=True)


async def async_items():
    val = await lol.Items(locale="zh_cn").get()
    for v in val:
        v.dict(pyotify=True)


async def async_item():
    val = await lol.Item(id=3153, locale="fr_fr").get()
    val.dict(pyotify=True)


async def async_runes():
    val = await lol.Runes(locale="zh_cn").get()
    for v in val:
        v.dict(pyotify=True)


async def async_rune():
    val = await lol.Rune(id=8112, locale="es_es").get()
    val.dict(pyotify=True)


def test_profile_icons():
    loop_run(async_profile_icons())

def test_profile_icon():
    loop_run(async_profile_icon())

def test_merakichampion():
    loop_run(async_merakichampion())

def test_merakiitem():
    loop_run(async_merakiitem())

def test_champion():
    loop_run(async_champion())

def test_spells():
    loop_run(async_spells())

def test_spell():
    loop_run(async_spell())

def test_items():
    loop_run(async_items())

def test_item():
    loop_run(async_item())

def test_runes():
    loop_run(async_runes())

def test_rune():
    loop_run(async_rune())
