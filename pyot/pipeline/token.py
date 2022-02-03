from typing import Any, Dict


class PipelineToken:
    value: str
    hashval: str
    model: str
    server: str
    method: str
    params: Dict[str, str]
    queries: Dict[str, Any]

    def __init__(self, model: str, server: str, method: str, params: Dict[str, str], queries: Dict[str, Any]):
        self.model = model
        self.server = server
        self.method = method
        self.params = params
        self.queries = queries
        if self.server:
            self.parent = f"{self.model}/{self.server}/{self.method}"
        else:
            self.parent = f"{self.model}/{self.method}"
        self.value = f"{self.parent}{self.parse_params(self.params)}{self.parse_queries(self.queries)}"
        self.hashval = hash((self.model, self.server, self.method, str(self.params), str(self.queries)))

    def __hash__(self):
        return self.hashval

    @staticmethod
    def parse_params(dic: Dict) -> str:
        res = "/".join(str(v) for v in dic.values())
        return "/" + res if res else ""

    @staticmethod
    def parse_queries(dic: Dict) -> str:
        res = "&".join(f"{k}={v}" for k, v in dic.items())
        return "?" + res if res else ""

    def dict(self) -> dict:
        return {
            "model": self.model,
            "server": self.server,
            "method": self.method,
            "params": self.params,
            "queries": self.queries,
        }

    @classmethod
    def load(cls, dic) -> 'PipelineToken':
        return cls(dic["model"], dic["server"], dic["method"], dic["params"], dic["queries"])
