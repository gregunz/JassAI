#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='jass',
    version='0.1.0',
    license='BSD 3-Clause',
    description='Let\'s show humans how robots can play jass!',
    packages=[pkg for pkg in find_packages() if pkg.startswith('jass')],
    install_requires=[

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite="tests",
)
