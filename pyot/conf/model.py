from abc import ABC

from .utils import ConfDict, reraise_model_inactive


AVAILABLE_MODELS = {"riot", "lol", "tft", "lor", "val"}


class ModelConf(ABC):

    default_platform: str = None
    default_region: str = None
    default_locale: str = None
    default_version: str = None


class Model:

    def __init__(self, default_platform: str, default_region: str, default_locale: str, default_version: str) -> None:
        self.default_platform = default_platform
        self.default_region = default_region
        self.default_locale = default_locale
        self.default_version = default_version

    @property
    @reraise_model_inactive
    def DEFAULT_PLATFORM(self):
        return self.default_platform

    @property
    @reraise_model_inactive
    def DEFAULT_REGION(self):
        return self.default_region

    @property
    @reraise_model_inactive
    def DEFAULT_LOCALE(self):
        return self.default_locale

    @property
    @reraise_model_inactive
    def DEFAULT_VERSION(self):
        return self.default_version


models: ConfDict[str, Model] = ConfDict(Model, "Model '{0}' is inactive or does not exist")


def activate_model(name: str):
    '''Make the settings take effect.'''

    keys = {"default_platform", "default_region", "default_locale", "default_version"}

    if name not in AVAILABLE_MODELS:
        raise ValueError(f"Invalid model, '{name}' was given")

    def wrapper(cls: "ModelConf"):
        # module = import_module(f"pyot.models.{name.lower()}.__core__")
        # CHECK THAT DEFAULTS MATCHES THE BASE AND SET IT
        # if cls.default_platform:
        #     module.ModelMixin.set_platform(cls.default_platform)
        # if cls.default_region:
        #     module.ModelMixin.set_region(cls.default_region)
        # if cls.default_locale:
        #     module.ModelMixin.set_locale(cls.default_locale)
        for key in keys:
            if hasattr(cls, key):
                continue
            raise ValueError(f"Missing value for '{key}' in {cls} conf")
        if name in models:
            raise ValueError(f"Model '{name}' is already active")
        if hasattr(models, name):
            raise ValueError("This model is already activated")
        models[name] = Model(cls.default_platform, cls.default_region, cls.default_locale, cls.default_version)
        return cls

    return wrapper
