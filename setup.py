#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

requirements = ['pandas',
                'numpy']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest',
                     'scipy']

setup(
    author="Stefan Holderbach",
    author_email='ho.steve@web.de',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="This is a fine selection of random useful or useless code and helper functions collected to simplify my life with the great pandas.",
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='pandasbikeshed',
    name='pandasbikeshed',
    packages=find_packages(include=['pandasbikeshed']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    extras_require={'test': test_requirements},
    url='https://github.com/sholderbach/pandasbikeshed',
    version='0.1.0',
    zip_safe=False,
)
