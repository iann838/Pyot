
from .engines import ModelsDocEngine, UtilsDocEngine


def build_docs():
    ModelsDocEngine().run()
    UtilsDocEngine().run()


if __name__ == '__main__':
    build_docs()
