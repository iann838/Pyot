from pyot.models.tft import base


def platform_to_region(platform: str) -> str:
    '''Return the region correspondent to a given platform'''
    return base.PyotRouting._platform2regions[platform]
