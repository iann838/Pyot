# Installation

Pyot requires Python **3.7** or newer.

Get the latest version of Python at <https://www.python.org/downloads/> or with your operating system’s package manager.

## Pip

Installing an official release with pip:

```shell
pip install pyot -U
```

## Github

Installing from source code master, it may include hotfixes and unstable code:

```shell
pip install git+https://github.com/paaksing/Pyot.git
```

## Extras

Depending on the need, installation of extras may be needed:

```shell
pip install pyot[diskcache]     # installs: ["diskcache>=5.1", "asgiref>=3.2"]
pip install pyot[redis]         # installs: ["aioredis<2.0"]
pip install pyot[mongodb]       # installs: ["motor>=2.3"]
pip install pyot[test]          # installs: ["typeguard>=2.13"]
```
