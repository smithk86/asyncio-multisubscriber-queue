#!/usr/bin/env python

import os.path

from setuptools import setup

dir_ = os.path.abspath(os.path.dirname(__file__))
# get the version to include in setup()
with open(f'{dir_}/asyncio_multisubscriber_queue/__init__.py') as fh:
    for line in fh:
        if '__version__' in line:
            exec(line)
# get long description from README.md
with open(f'{dir_}/README.md') as fh:
    long_description = fh.read()


setup(
    name='asyncio-multisubscriber-queue',
    version=__version__,
    license='MIT',
    author='Kyle Smith',
    author_email='smithk86@gmail.com',
    url='https://github.com/smithk86/asyncio-multisubscriber-queue',
    packages=['asyncio_multisubscriber_queue'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-asyncio'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Framework :: AsyncIO',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
