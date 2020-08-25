import pyot


async def async_profile_icons():
    val = await pyot.lol.ProfileIcons(locale="en_us").get()
    for v in val:
        v.dict(pyotify=True)


async def async_profile_icon():
    val = await pyot.lol.ProfileIcon(id=28, locale="en_us").get()
    val.dict(pyotify=True)


async def async_merakichampion():
    val = await pyot.lol.MerakiChampion(id=235).get()
    val.dict(pyotify=True)


async def async_merakiitem():
    val = await pyot.lol.MerakiItem(id=3153).get()
    val.dict(pyotify=True)


async def async_champion():
    val = await pyot.lol.Champion(key="Senna").get()
    val.dict(pyotify=True)


async def async_spells():
    val = await pyot.lol.Spells(locale="zh_cn").get()
    for v in val:
        v.dict(pyotify=True)


async def async_spell():
    val = await pyot.lol.Spell(id=12, locale="es_es").get()
    val.dict(pyotify=True)


async def async_items():
    val = await pyot.lol.Items(locale="zh_cn").get()
    for v in val:
        v.dict(pyotify=True)


async def async_item():
    val = await pyot.lol.Item(id=3153, locale="fr_fr").get()
    val.dict(pyotify=True)


async def async_runes():
    val = await pyot.lol.Runes(locale="zh_cn").get()
    for v in val:
        v.dict(pyotify=True)


async def async_rune():
    val = await pyot.lol.Rune(id=8112, locale="es_es").get()
    val.dict(pyotify=True)


def test_profile_icons():
    pyot.run(async_profile_icons())

def test_profile_icon():
    pyot.run(async_profile_icon())

def test_merakichampion():
    pyot.run(async_merakichampion())

def test_merakiitem():
    pyot.run(async_merakiitem())

def test_champion():
    pyot.run(async_champion())

def test_spells():
    pyot.run(async_spells())

def test_spell():
    pyot.run(async_spell())

def test_items():
    pyot.run(async_items())

def test_item():
    pyot.run(async_item())

def test_runes():
    pyot.run(async_runes())

def test_rune():
    pyot.run(async_rune())
