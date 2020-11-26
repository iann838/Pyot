import os
import sys
from distutils.dir_util import copy_tree

def startproject(dirname):
    src = os.path.dirname(os.path.realpath(__file__))
    if '\\' in src:
        src += '\\startproject_files'
    else:
        src += '/startproject_files'
    copy_tree(src, dirname)


scripts = {
    'startproject': startproject,
}

def main():
    vals = sys.argv[1:]
    if len(vals) < 2:
        raise ValueError('At least 2 argument needs to be provided')
    command = vals[0]
    args = vals[1:]
    scripts[command](*args)
