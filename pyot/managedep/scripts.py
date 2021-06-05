import os
import sys
from distutils.dir_util import copy_tree
from shutil import copyfile


def _change_project_name(path, name):
    with open(path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "__projectname__" in line:
                lines[i] = line.replace('__projectname__', name)
    with open(path, "w") as f:
        f.writelines(lines)


def startproject(dirname):
    admin_dir = os.path.dirname(os.path.realpath(__file__))

    if '\\' in admin_dir:
        sep = "\\"
    else:
        sep = "/"

    src_folder = admin_dir + sep + 'static' + sep + 'startproject'
    src_manage = admin_dir + sep + 'static' + sep + 'manage.py'
    dst_manage = os.getcwd() + sep + 'manage.py'

    copy_tree(src_folder, dirname)
    copyfile(src_manage, dst_manage)
    _change_project_name(dst_manage, dirname)
    _change_project_name(dirname + sep + 'wsgi.py', dirname)


scripts = {
    'startproject': startproject,
}


def main():
    vals = sys.argv[1:]
    command = vals[0]
    args = vals[1:]
    scripts[command](*args)


if __name__ == '__main__':
    main()
