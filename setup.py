#!/usr/bin/env python

import os.path

from setuptools import setup  # type: ignore

from asyncio_multisubscriber_queue import __VERSION__


dir_ = os.path.abspath(os.path.dirname(__file__))

# get long description from README.md
with open(f'{dir_}/README.md') as fh:
    long_description = fh.read()


setup(
    name='asyncio-multisubscriber-queue',
    version=__VERSION__,
    license='MIT',
    author='Kyle Smith',
    author_email='smithk86@gmail.com',
    url='https://github.com/smithk86/asyncio-multisubscriber-queue',
    package_data={"asyncio_multisubscriber_queue": ["py.typed"]},
    packages=['asyncio_multisubscriber_queue'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'mypy',
        'pytest',
        'pytest-asyncio',
        'pytest-mypy'
    ],
    python_requires='>=3.7',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Framework :: AsyncIO',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
