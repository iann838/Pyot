from pyot.models.tft import base


def platform_to_region(platform: str) -> str:
    return base.PyotRouting._platform2regions[platform]
