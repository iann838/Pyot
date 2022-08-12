
import re


def snake_case(attr: str, sep_numbers=False) -> str:
    '''Convert string to python snake_case.'''
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', attr)
    snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    if sep_numbers:
        snake_case = re.sub('([a-z])([0-9])', r'\1_\2', snake_case)
    return snake_case


def camel_case(snake_str: str) -> str:
    '''Convert string to json camel_case.'''
    components = snake_str.split('_')
    if len(components) == 1:
        return components[0]
    return components[0] + ''.join(x.title() for x in components[1:])
