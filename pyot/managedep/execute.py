
from .commands import commands


def execute_from_sys_args(argv):
    args = argv[1:]
    command = args[0]
    command_args = args[1:]
    commands[command](*command_args)
