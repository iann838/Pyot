from abc import ABC
from typing import Dict, List, Mapping

from pyot.pipeline.core import Pipeline
from pyot.utils.logging import Logger
from pyot.utils.importlib import import_class

from .utils import ConfDict, valid_attribute_key

LOGGER = Logger(__name__)
AVAILABLE_MODELS = {"lol", "tft", "lor", "val"}

pipelines: ConfDict[str, Pipeline] = ConfDict(Pipeline, False)


def activate_pipeline(model: str):

    keys = {"name", "stores", "default"}

    if model not in AVAILABLE_MODELS:
        raise ValueError(f"Invalid model, '{model}' was given")

    def build_pipeline(pipeline_configs: List[Dict]):
        stores = []
        for config in pipeline_configs:
            store_cls = import_class(config.pop("backend"))
            config.update({"game": model.lower()})
            store = store_cls(**config)
            stores.append(store)
        return stores

    def wrapper(cls: "PipelineConf"):
        for key in keys:
            if hasattr(cls, key):
                continue
            raise ValueError(f"Missing value for '{key}' in {cls} conf")
        if not valid_attribute_key(key):
            raise ValueError("Name of pipeline must be alphanumeric")
        pipeline = Pipeline(model, cls.name, build_pipeline(cls.stores))
        if cls.name in AVAILABLE_MODELS and (not cls.default or not cls.name == model):
            raise ValueError("Pipeline name must be different than model's name or the same as the subscripted model if set to default")
        if model in pipelines:
            LOGGER.warning(f"[Trace: Pyot Setup] WARN: An attempt to activate pipeline '{cls.name}' was ignored (default pipeline of model already active)")
            return cls
        if cls.name in pipelines:
            LOGGER.warning(f"[Trace: Pyot Setup] WARN: An attempt to activate pipeline '{cls.name}' was ignored (pipeline already active)")
            return cls
        if cls.default:
            pipelines[model] = pipeline
        pipelines[cls.name] = pipeline
        return cls

    return wrapper


class PipelineConf(ABC):

    name: str
    stores: List[Mapping[str, Dict]]
    default: bool = False
