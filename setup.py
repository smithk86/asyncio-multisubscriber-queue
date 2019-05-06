#!/usr/bin/env python

from setuptools import setup

setup(
    name='asyncio-multisubscriber-queue',
    version='0.1.3',
    license='MIT',
    author='Kyle Smith',
    author_email='smithk86@gmail.com',
    packages=['asyncio_multisubscriber_queue'],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-asyncio'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
