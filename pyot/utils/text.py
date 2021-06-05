
import re


def snakecase(attr: str) -> str:
    '''Convert string to python snakecase.'''
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', attr)
    snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    return snake_case


def camelcase(snake_str: str) -> str:
    '''Convert string to json camelcase.'''
    components = snake_str.split('_')
    if len(components) == 1:
        return components[0]
    return components[0] + ''.join(x.title() for x in components[1:])
