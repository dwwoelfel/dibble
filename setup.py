#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='dibble',
    version='0.1',
    description='Mongodb Object Mapper',
    url='https://github.com/voxelbrain/dibble',
    packages=['dibble'],
    install_requires=['pymongo'],
    setup_requires=['nose', 'coverage']
)
