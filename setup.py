#!/usr/bin/env python

import sys
from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
    "wheel",
    "python-dateutil>=2.8",
    "aiohttp>=3.7",
    "pytz",
    "lor-deckcodes",
]

extras_require = {
    "diskcache": ["diskcache>=5.1", "asgiref>=3.2"],
    "redis": ["aioredis<2.0"],
    "mongodb": ["motor>=2.3"],
    "test": ["typeguard>=2.13"],
}


# Require python 3.7
if sys.version_info.major != 3 and sys.version_info.minor < 7:
    sys.exit("'Pyot' requires Python >= 3.7")

setup(
    name="pyot",
    version="5.3.0",
    author="Paaksing",
    author_email="paaksingtech@gmail.com",
    url="https://github.com/paaksing/Pyot",
    description="AsyncIO based high level Python framework Riot Games API framework which encourages rapid development and clean, pragmatic design.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["Riot Games", "League of Legends", "Teamfight Tactics", "Valorant", "Legends of Runeterra", "API", "REST", "asyncio"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
    ],
    license="MIT",
    packages=find_packages(exclude=("test")),
    zip_safe=True,
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
)
