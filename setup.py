import doctest
import os
import unittest

from setuptools import find_packages, setup

requirements = []

with open("README.md", "r") as readme:
    README = readme.read()

exec(open("src/poaching_simulator/version.py", "r").read())

setup(
    name="poaching_simulator",
    version=__version__,
    install_requires=requirements,
    author="Nikoleta Glynatsi, Vince Knight",
    author_email=("glynatsine@cardiff.ac.uk"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="",
    license="The MIT License (MIT)",
    description="An agent based poaching simulation tool.",
    long_description=README,
)
