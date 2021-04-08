# Quick Start Guide

Build your first pyot project.

::: warning Before starting this guide
* This guide only applies to pyot v2.0.0 or higher.
* For integrating with Django, there is a totally different [setup](django.html)
:::

## Create a new project

If this is your first time using Pyot, you’ll have to take care of some initial setup. Namely, you’ll need to change the environment that establishes a Pyot project – a collection of settings for an instance of Pyot, including API key setup, store specific options and pipeline-specific settings.

From the command line, change your working directory into a directory where you’d like to store your code, then run the following command:

```shell
pyot startproject myproject
```
This will create a **myproject** directory in your current directory.

:::warning
You’ll need to avoid naming projects after built-in Python or Pyot components. In particular, this means you should avoid using names like pyot (which will conflict with Pyot itself) or test (which conflicts with a built-in Python package).
:::

```shell
myproject/
    __init__.py
    __main__.py
    manage.py
    settings.py
    tasks.py
```

These files are:
* **__init__.py**: Marks the directory as module, imports the Pyot settings from **settings.py** and others.
* **__main__.py**: Marks the module as executable, the entry point of the module, defaults to executing the task manager in **manage.py**.
* **manage.py**: Managers for this Pyot project, you can change this file to your wanted behavior.
* **settings.py**: Settings/Configuration for this Pyot project, [Pyot settings](settings.html) will tell you how settings work.
* **tasks.py**: Tasks of this Pyot project, all callables in this file will be accessible by managers. 

## Running your project for the first time

There is a default task added by `startproject` command

First, please verify that your API key is set, Pyot will default to get your environment variable called `RIOT_API_KEY`, you can change the name of the variable to match yours if needed, ***hardcoding your API key is not recommended*** because it will risk API key leakage.

```python
# settings.py
    # ...
        'API_KEY': os.environ['RIOT_API_KEY'] 
```

Now that everything is set up, run the following command:

```shell
python -m myproject summoner_level Morimorph NA1
```

You should get printed in your console:
```shell
Morimorph in NA1 is level <int>
```

Congrats! Your first project is all set up.

## How it works

We executed above:
```shell
python -m myproject summoner_level Morimorph NA1
```

1. `python -m myproject` tells python to execute `myproject` as a module, which then translates into calling the manager in `__main__.py`.
2. `summoner_level` tells the manager the name of task in `tasks.py` to load and execute.
3. `Morimorph NA1` are the arguments that the callable `summoner_level` takes, it will be unpacked in the same order as given.

Below is source code for `summoner_level` in `tasks.py`:

```python
async def summoner_level(name, platform):
    '''Get summoner level by name and platform'''
    try:
        summoner = await lol.Summoner(name=name, platform=platform).get()
        print(summoner.name, 'in', summoner.platform.upper(), 'is level', summoner.level)
    except NotFound:
        print('Summoner not found')
```

## Clarification

This is only a **base template** that developers can work out as a startup is not limited to that template, if you're integrating pyot to other frameworks (e.g. Flask, FastAPI), you can choose to import the tasks written in this module and execute it in your other framework, or integrate pyot to that framework by adding imports and applying settings. For more information please check **[Integrating pyot to other framework / environment](/topics/integrating.html)**.
