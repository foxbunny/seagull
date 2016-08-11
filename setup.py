#!/usr/bin/python
#
# Seagull photo gallery app
# Copyright (C) 2016  Hajime Yamasaki Vukelic
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#

import os

from setuptools import setup, find_packages
import seagull


def read(fname):
    """ Return content of specified file """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='seagull',
    version=seagull.__version__,
    author=seagull.__author__,
    author_email='hayavuk@gmail.com',
    description='Photography folio app',
    license='GPLv3+',
    keywords='photography app website ajax json ftp',
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.rst'),
    install_requires=[
        'bottle==0.12.9',
        'bottle-streamline==1.0',
        'confloader==1.1',
        'pyftpdlib==1.5.1',
        'Mako==1.0.4',
        'gevent==1.1.2',
        'cssmin==0.2.0',
        'webassets==0.11.1',
    ],
    entry_points={
        'console_scripts': [
            'seagull = seagull.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Framework :: Bottle',
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
