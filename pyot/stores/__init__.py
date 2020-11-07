try:
    from .djangocache import DjangoCache
except ImportError:
    pass
from .riotapi import RiotAPI
from .omnistone import Omnistone
from .rediscache import RedisCache
from .diskcache import DiskCache
from .merakicdn import MerakiCDN
from .cdragon import CDragon
from .mongodb import MongoDB
from .ddragon import DDragon
