from pyot.utils import loop_run
from pyot.models import val


async def async_content_locale():
    content = await val.Content(platform="NA").query(locale="en-US").get()
    assert isinstance(content.version, str)
    for item in [content.characters, content.maps, content.chromas, content.skins, 
        content.skin_levels, content.equips, content.game_modes, content.sprays, 
        content.spray_levels, content.charms, content.charm_levels, content.player_cards, 
        content.player_titles]:
        for i in item:
            assert isinstance(i.name, str)
            assert isinstance(i.asset_name, str)

async def async_content_full():
    content = await val.Content(platform="NA").get()
    assert isinstance(content.version, str)
    for item in [content.characters, content.maps, content.chromas, content.skins, 
        content.skin_levels, content.equips, content.game_modes, content.sprays, 
        content.spray_levels, content.charms, content.charm_levels, content.player_cards, 
        content.player_titles]:
        for i in item:
            assert isinstance(i.name, str)
            assert isinstance(i.asset_name, str)
            if i.name != "":
                local = i.localized_names
                assert isinstance(local.ar_ae, str)
                assert isinstance(local.de_de, str)
                assert isinstance(local.en_gb, str)
                assert isinstance(local.en_us, str)
                assert isinstance(local.es_es, str)
                assert isinstance(local.es_mx, str)
                assert isinstance(local.fr_fr, str)
                assert isinstance(local.id_id, str)
                assert isinstance(local.it_it, str)
                assert isinstance(local.ja_jp, str)
                assert isinstance(local.ko_kr, str)
                assert isinstance(local.pl_pl, str)
                assert isinstance(local.pt_br, str)
                assert isinstance(local.ru_ru, str)
                assert isinstance(local.th_th, str)
                assert isinstance(local.tr_tr, str)
                assert isinstance(local.vi_vn, str)
                assert isinstance(local.zh_cn, str)
                assert isinstance(local.zh_tw, str)


def test_content_locale():
    loop_run(async_content_locale())

def test_content_full():
    loop_run(async_content_full())