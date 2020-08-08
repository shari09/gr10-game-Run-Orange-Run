#!/usr/bin/env python

import setuptools
from setuptools import find_namespace_packages
from distutils.core import setup
import os

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(name = 'runorangerun',
      version = '1.0.0',
      description = 'shari shari shari',
      long_description = readme(),
      long_description_content_type="text/markdown",
      author = 'Shari',
      author_email = 'shari09cxxcr@gmail.com',
      url = 'https://github.com/shari09/gr10-game-Run-Orange-Run',
      keywords = 'shari chari cherry',
      packages = ['runorangerun'],
      scripts = ['scripts/runorangerun'],
      install_requires=open('requirements.txt', 'r').read().strip().split('\n'),
      data_files=[('', ['data/' + x for x in os.listdir('data')])],
      #package_data={'runorangerun': ['data/*']},
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.6'),
