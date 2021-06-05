from abc import ABC, abstractproperty
from typing import Dict

from pyot.core import exceptions as exc
from pyot.pipeline.token import PipelineToken


class BaseEndpoint(ABC):

    @abstractproperty
    def base_url(self) -> str:
        raise NotImplementedError

    shared: Dict[str, str] = {}
    all: Dict[str, Dict[str, str]] = {}

    def __init__(self, game: str):
        try:
            self.endpoints = self.all[game]
        except KeyError as e:
            name = self.__class__.__name__.replace("Endpoint", "")
            raise NotImplementedError(f"{name} does not support '{e}' model") from e
        self.endpoints.update(self.shared)

    def resolve(self, token: PipelineToken) -> str:
        try:
            url = (self.base_url + self.endpoints[token.method]).format(**self.clean(token))
            query = self.query(token.queries)
            return url + query
        except KeyError as e:
            raise exc.NotFindable from e

    def query(self, queries: Dict) -> str:
        query = ""
        for a, b in queries.items():
            if isinstance(b, list):
                for val in b:
                    query = query + "&" + str(a) + "=" + str(val)
            else:
                query = query + "&" + str(a) + "=" + str(b)
        if len(query) > 1:
            query = "?" + query[1:]
        return query

    def clean(self, token: PipelineToken) -> Dict[str, str]:
        return token.params
