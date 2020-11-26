# Installation Guide

Before you can use Pyot, you’ll need to get it installed. This guide will guide you to a minimal installation that’ll work while you walk through the introduction.

## Install Python

Being a Python framework, Pyot requires Python v3.7 or higher.

Get the latest version of Python at https://www.python.org/downloads/ or with your operating system’s package manager.

You can verify that Python is installed by typing `python` from your shell; you should see something like:

```shell
Python 3.x.y
[GCC 4.x] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## Install Pyot Code

Installing an official release with pip
This is the recommended way to install Pyot.

Install [pip](https://pip.pypa.io/). The easiest is to use the [standalone pip installer](https://pip.pypa.io/en/latest/installing/#installing-with-get-pip-py). If your distribution already has pip installed, you might need to update it if it’s outdated. If it’s outdated, you’ll know because installation won’t work.

Take a look at [venv](https://docs.python.org/3/tutorial/venv.html). This tool provides isolated Python environments, which are more practical than installing packages systemwide. It also allows installing packages without administrator privileges.

* Windows
```shell
python -m venv venv
venv\scripts\activate
```

* Unix
```shell
python -m venv venv
source venv/bin/activate
```

After you’ve created and activated a virtual environment, enter the command:

```shell
pip install pyot
```
