import doctest
import os
import unittest

from setuptools import find_packages, setup

requirements = []

with open("README.md", "r") as readme:
    README = readme.read()

exec(open("src/rhabm/version.py", "r").read())

setup(
    name="rhabm",
    version=__version__,
    install_requires=requirements,
    author="Nikoleta Glynatsi, Vince Knight",
    author_email=("glynatsine@cardiff.ac.uk"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="",
    license="The MIT License (MIT)",
    description="A rhino poaching agent based simulation tool.",
    long_description=README,
)
