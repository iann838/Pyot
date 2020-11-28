#!/usr/bin/env python

import sys

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
    "wheel",
    "python-dateutil",
    "aiohttp",
    "pytz",
    "redis",
    "diskcache",
    "asgiref",
    "motor",
    "lor-deckcodes",
]

# Require python 3.7
if sys.version_info.major != 3 and sys.version_info.minor < 7:
    sys.exit("'Pyot' requires Python >= 3.7!")

setup(
    name="pyot",
    version="2.0.4", 
    author="Paaksing",
    author_email="paaksingtech@gmail.com",
    url="https://github.com/paaksing/Pyot",
    description="AsyncIO based high level Python framework for the Riot Games API that encourages rapid development and clean, pragmatic design.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["Riot Games", "League of Legends", "Teamfight Tactics", "Valorant", "Legends of Runeterra", "API", "REST", "Django", "asyncio"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.7",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
        "Framework :: Django :: 3.0",
    ],
    license="MIT",
    packages=find_packages(exclude=("test","test_djot")),
    zip_safe=True,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pyot=pyot.management.scripts:main'
        ]
    }
)
