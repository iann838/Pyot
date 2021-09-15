from typing import List, TYPE_CHECKING

from pyot.conf.model import models

from .base import PyotCore

if TYPE_CHECKING:
    from .champion import Champion
    from .merakichampion import MerakiChampion


# PYOT CORE OBJECTS

class ChampionRotation(PyotCore):
    free_champion_ids: List[int]
    free_newie_champion_ids: List[int]
    newie_max_level: int

    class Meta(PyotCore.Meta):
        rules = {"champion_v3_rotation": []}
        raws = {"free_champion_ids", "free_newie_champion_ids"}
        renamed = {"free_champion_ids_for_new_players": "free_newie_champion_ids", "max_new_player_level": "newie_max_level"}

    def __init__(self, platform: str = models.lol.DEFAULT_PLATFORM):
        self.initialize(locals())

    @property
    def free_champions(self) -> List["Champion"]:
        from .champion import Champion
        mutable = []
        for i in self.free_champion_ids:
            mutable.append(Champion(id=i))
        return mutable

    @property
    def free_newie_champions(self) -> List["Champion"]:
        from .champion import Champion
        mutable = []
        for i in self.free_newie_champion_ids:
            mutable.append(Champion(id=i))
        return mutable

    @property
    def meraki_free_champions(self) -> List["MerakiChampion"]:
        from .merakichampion import MerakiChampion
        mutable = []
        for i in self.free_champion_ids:
            mutable.append(MerakiChampion(id=i))
        return mutable

    @property
    def meraki_free_newie_champions(self) -> List["MerakiChampion"]:
        from .merakichampion import MerakiChampion
        mutable = []
        for i in self.free_newie_champion_ids:
            mutable.append(MerakiChampion(id=i))
        return mutable
