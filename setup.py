# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import zipstream


setup(
    name='zipstream-longaccess',
    version=zipstream.__version__,
    description='Zipfile generator',
    author='Allan Lei',
    author_email='allanlei@helveticode.com',
    url='https://github.com/allanlei/python-zipstream',
    packages=find_packages(),
    keywords='zip streaming',

    test_suite='nose.collector',
    tests_require = ['nose'],
)
