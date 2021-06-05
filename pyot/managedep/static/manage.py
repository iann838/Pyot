# Default task manager for pyot projects.
# Feel free to change this file to your wanted behavior.

import os
import sys

from pyot.management.execute import execute_from_sys_args


def main():
    os.environ.setdefault("PYOT_PROJECT_MODULE", "__projectname__")
    execute_from_sys_args(sys.argv)


if __name__ == "__main__":
    main()
