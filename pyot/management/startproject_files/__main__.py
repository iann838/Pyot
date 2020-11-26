# Entry point of this module
# Defaults to executing the task manager
# To run this module: `python -m <moduleName> <funcName> <funcArgs>`.

import sys
from .manage import execute_task_from_args

if __name__ == "__main__":
    execute_task_from_args()
