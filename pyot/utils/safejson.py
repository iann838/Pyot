
from typing import Any, Union
from io import FileIO, BytesIO
import json


def loads(content: Union[str, bytes], **kwargs) -> Any:
    '''Same as json.loads with graceful fallback by returning the passed content as is'''
    try:
        return json.loads(content, **kwargs)
    except json.decoder.JSONDecodeError:
        return content

def load(fp: Union[FileIO, BytesIO], **kwargs) -> Any:
    '''Same as json.load with graceful fallback by returning the read content as is'''
    try:
        return json.load(fp, **kwargs)
    except json.decoder.JSONDecodeError:
        return fp.read()
