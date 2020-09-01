try:
    from .djangocache import DjangoCache
except ImportError:
    pass
from .riotapi import RiotAPI
from .omnistone import Omnistone
from .merakicdn import MerakiCDN
from .cdragon import CDragon