import copy


class ErrorHandler:
    default_handler = {
        204 : ("T", []),
        400 : ("T", []),
        401 : ("T", []),
        404 : ("T", []),
        403 : ("T", []),
        405 : ("T", []),
        408 : ("E", [3, 3]),
        429 : ("E", [3, 3]),
        500 : ("E", [3, 3]),
        502 : ("E", [3, 3]),
        503 : ("E", [3, 3]),
        504 : ("E", [3, 3]),
        602 : ("T", []),
        800 : ("T", []),
    }

    def create_handler(self, handler):
        if handler is None:
            return self.default_handler
        for code, c in handler.items():
            if code not in self.default_handler:
                raise RuntimeError(f"Handler code {code} is not a valid status for error handling")
            strategy = c[0]
            try:
                params = c[1]
            except IndexError:
                raise AttributeError("Handler values receives 2 paramameters, 1 was given")
            for a in params:
                if not isinstance(a, int):
                    raise RuntimeError(f"Handler strategy takes 'int' parameters, '{type(a)}' was given") 
            if strategy == "T":
                if len(params) != 0:
                    raise RuntimeError(f"Handler strategy 'T' (Throw) takes 0 parameters, but {len(params)} was given")
            elif strategy == "E":
                if len(params) != 2:
                    raise RuntimeError(f"Handler strategy 'E' (Exp. backoff) takes 2 parameters, but {len(params)} was given")
            elif strategy == "R":
                if len(params) != 1:
                    raise RuntimeError(f"Handler strategy 'R' (Retry) takes 1 parameters, but {len(params)} was given")
            else:
                raise RuntimeError(f"Handler strategy '{strategy}' is not a valid token for error handling")
        hand = copy.deepcopy(self.default_handler)
        hand.update(handler)
        return hand
