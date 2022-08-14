
from .engines import ModelsDocEngine, UtilsDocEngine, ExamplesDocEngine


def build_docs():
    ModelsDocEngine().run()
    UtilsDocEngine().run()
    ExamplesDocEngine().run()


if __name__ == '__main__':
    build_docs()
