from typing import Any


class UntypedAttribute(Exception):
    '''Exception for flagging an untyped attribute in pyot objects'''

    def __init__(self, clas, key: str, value: Any) -> None:
        super().__init__(f"Untyped attribute '{clas.__name__}.{key}': {value}")
