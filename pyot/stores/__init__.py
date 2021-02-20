try:
    from .djangocache import DjangoCache
except ImportError as e:
    DjangoCache = e

from .riotapi import RiotAPI
from .omnistone import Omnistone
from .rediscache import RedisCache

try:
    from .diskcache import DiskCache
except ImportError as e:
    DiskCache = e

from .merakicdn import MerakiCDN
from .cdragon import CDragon

try:
    from .mongodb import MongoDB
except ImportError as e:
    MongoDB = e

from .ddragon import DDragon
