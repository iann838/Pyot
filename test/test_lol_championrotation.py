from pyot.utils import loop_run
from pyot.models import lol


async def async_free_champ():
    rotation = await lol.ChampionRotation(platform="NA1").get()
    assert isinstance(rotation.newie_max_level, int)
    assert rotation.free_champion_ids is not None
    assert rotation.free_newie_champion_ids is not None
    for champ in rotation.free_champions:
        assert isinstance(champ, lol.Champion)
    for champ in rotation.free_newie_champions:
        assert isinstance(champ, lol.Champion)
    for champ in rotation.meraki_free_champions:
        assert isinstance(champ, lol.MerakiChampion)
    for champ in rotation.meraki_free_newie_champions:
        assert isinstance(champ, lol.MerakiChampion)


def test_champ_rotation():
    loop_run(async_free_champ())