import os
import platform

from pyot.conf.pipeline import activate_pipeline, PipelineConf
from pyot.conf.model import activate_model, ModelConf


if platform.system() == 'Windows':
    from pyot.utils.runtime import silence_proactor_pipe_deallocation
    silence_proactor_pipe_deallocation()


@activate_model("riot")
class RiotModel(ModelConf):
    default_platform = "na1"
    default_region = "americas"
    default_version = "latest"
    default_locale = "en_us"


@activate_model("lol")
class LolModel(ModelConf):
    default_platform = "na1"
    default_region = "americas"
    default_version = "latest"
    default_locale = "en_us"


@activate_pipeline("lol")
class LolPipeline(PipelineConf):
    name = "lol_main"
    default = True
    stores = [
        {
            "backend": "pyot.stores.omnistone.Omnistone",
            "log_level": 30,
            "expirations": {
                "summoner_v4_by_name": 100,
                "match_v5_match": 600,
                "match_v5_timeline": 600,
            }
        },
        {
            "backend": "pyot.stores.merakicdn.MerakiCDN",
            "log_level": 30,
            "error_handler": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "backend": "pyot.stores.cdragon.CDragon",
            "log_level": 30,
            "error_handler": {
                404: ("T", []),
                500: ("R", [3])
            }
        },
        {
            "backend": "pyot.stores.riotapi.RiotAPI",
            "log_level": 30,
            "api_key": os.environ["RIOT_API_KEY"],
            "rate_limiter": {
                "backend": "pyot.limiters.redis.RedisLimiter",
                # "limiting_share": 1,
                "host": "127.0.0.1",
                "port": 6379,
                "db": 0,
            },
            "error_handler": {
                400: ("T", []),
                503: ("E", [3, 3])
            }
        }
    ]
