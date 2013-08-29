#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

import exconsole

setup(
    name='python-exconsole',
    version=exconsole.__version__,
    install_requires=[
    ],
    description='Emergency/postmortem Python console',
    author='Eugene Pankov',
    author_email='e@ajenti.org',
    url='https://github.com/Eugeny/exconsole',
    packages=find_packages(exclude=['*test*']),
)
