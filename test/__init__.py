import os
import platform

from pyot.conf.pipeline import activate_pipeline, PipelineConf
from pyot.conf.model import activate_model, ModelConf

from .core import inject_guards


inject_guards()

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
        },
        {
            "backend": "pyot.stores.cdragon.CDragon",
            "log_level": 30,
        },
        {
            "backend": "pyot.stores.riotapi.RiotAPI",
            "log_level": 30,
            "api_key": os.environ["RIOT_API_KEY"],
        }
    ]


@activate_model("tft")
class TftModel(ModelConf):
    default_platform = "na1"
    default_region = "americas"
    default_version = "latest"
    default_locale = "en_us"


@activate_pipeline("tft")
class TftPipeline(PipelineConf):
    name = "tft_main"
    default = True
    stores = [
        {
            "backend": "pyot.stores.omnistone.Omnistone",
            "log_level": 30,
            "expirations": {
                "summoner_v1_by_name": 100,
                "match_v1_match": 600,
            }
        },
        {
            "backend": "pyot.stores.cdragon.CDragon",
            "log_level": 30,
        },
        {
            "backend": "pyot.stores.riotapi.RiotAPI",
            "log_level": 30,
            "api_key": os.environ["TFT_API_KEY"],
        }
    ]


@activate_model("val")
class ValModel(ModelConf):
    default_platform = "na"
    default_region = "americas"


@activate_pipeline("val")
class ValPipeline(PipelineConf):
    name = "val_main"
    default = True
    stores = [
        {
            "backend": "pyot.stores.omnistone.Omnistone",
            "log_level": 30,
            "expirations": {
                "account_v1_by_riot_id": 100,
                "match_v1_match": 600,
            }
        },
        {
            "backend": "pyot.stores.riotapi.RiotAPI",
            "log_level": 30,
            "api_key": os.environ["PYOT_DEV_KEY"],
        }
    ]


@activate_model("lor")
class LorModel(ModelConf):
    default_region = "americas"
    default_version = "latest"
    default_locale = "en_us"


@activate_pipeline("lor")
class LorPipeline(PipelineConf):
    name = "lor_main"
    default = True
    stores = [
        {
            "backend": "pyot.stores.omnistone.Omnistone",
            "log_level": 30,
            "expirations": {
                "account_v1_by_riot_id": 100,
                "match_v1_match": 600,
            }
        },
        {
            "backend": "pyot.stores.ddragon.DDragon",
            "log_level": 30,
        },
        {
            "backend": "pyot.stores.riotapi.RiotAPI",
            "log_level": 30,
            "api_key": os.environ["LOR_API_KEY"],
        }
    ]
