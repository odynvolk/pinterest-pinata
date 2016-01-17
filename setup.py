#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="pinterest-pinata",
      version="1.1.5",
      description="Pinterest client",
      install_requires=["requests>=2.5.0", "vcrpy>=1.7.4"],
      author="Alexi Rahman",
      author_email="alexi.rahman@r76.se",
      url="http://github.com/odynvolk/pinterest-pinata",
      packages=find_packages(),
      keywords="pinterest api",
      zip_safe=True)
