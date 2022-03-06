from typing import List, TYPE_CHECKING

from pyot.conf.model import models
from pyot.core.functional import parse_camelcase
from .base import PyotCore, PyotStatic

if TYPE_CHECKING:
    from .ranked import Leaderboard


# PYOT STATIC OBJECTS


class ContentLocalizedNamesData(PyotStatic):
    ar_ae: str
    de_de: str
    en_gb: str
    en_us: str
    es_es: str
    es_mx: str
    fr_fr: str
    id_id: str
    it_it: str
    ja_jp: str
    ko_kr: str
    pl_pl: str
    pt_br: str
    ru_ru: str
    th_th: str
    tr_tr: str
    vi_vn: str
    zh_cn: str
    zh_tw: str

    class Meta(PyotStatic.Meta):
        renamed = {
            "ar-ae": "ar_ae",
            "de-de": "de_de",
            "en-gb": "en_gb",
            "en-us": "en_us",
            "es-es": "es_es",
            "es-mx": "es_mx",
            "fr-fr": "fr_fr",
            "id-id": "id_id",
            "it-it": "it_it",
            "ja-jp": "ja_jp",
            "ko-kr": "ko_kr",
            "pl-pl": "pl_pl",
            "pt-br": "pt_br",
            "ru-ru": "ru_ru",
            "th-th": "th_th",
            "tr-tr": "tr_tr",
            "vi-vn": "vi_vn",
            "zh-cn": "zh_cn",
            "zh-tw": "zh_tw",
        }


class ContentItemData(PyotStatic):
    id: str
    name: str
    asset_name: str
    asset_path: str
    localized_names: ContentLocalizedNamesData


class ContentActData(PyotStatic):
    id: str
    name: str
    type: str
    parent_id: str
    localized_names: ContentLocalizedNamesData
    is_active: bool

    @property
    def leaderboard(self) -> "Leaderboard":
        from .ranked import Leaderboard
        return Leaderboard(act_id=self.id, platform=self.platform)


# PYOT CORE OBJECTS

class Content(PyotCore):
    version: str
    characters: List[ContentItemData]
    maps: List[ContentItemData]
    chromas: List[ContentItemData]
    skins: List[ContentItemData]
    skin_levels: List[ContentItemData]
    equips: List[ContentItemData]
    game_modes: List[ContentItemData]
    sprays: List[ContentItemData]
    spray_levels: List[ContentItemData]
    charms: List[ContentItemData]
    charm_levels: List[ContentItemData]
    player_cards: List[ContentItemData]
    player_titles: List[ContentItemData]
    ceremonies: List[ContentItemData]
    acts: List[ContentActData]

    class Meta(PyotCore.Meta):
        rules = {"content_v1_contents": []}

    def __init__(self, platform: str = models.val.DEFAULT_PLATFORM):
        self.initialize(locals())

    def query(self, locale: str = None):
        '''Query parameters setter.'''
        self._meta.query = parse_camelcase(locals())
        return self
