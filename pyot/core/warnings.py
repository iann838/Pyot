import warnings


class PyotConfWarning(UserWarning):
    pass


class PyotPipelineWarning(RuntimeWarning):
    pass


class PyotStoreWarning(RuntimeWarning):
    pass


class PyotRuntimeWarning(RuntimeWarning):
    pass


class PyotResourceWarning(ResourceWarning):
    pass


warnings.simplefilter("default", PyotResourceWarning)
