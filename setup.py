# -*- coding: utf-8 -*-
##############################################################################
#
#  res-address, Simple Resource Address Parser
#  Copyright (C) 2018-2019 Mariano Ruiz
#  https://github.com/mrsarm/python-res-address
#
#  Author: Mariano Ruiz <mrsarm@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this library.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from setuptools import setup
from os.path import abspath, dirname, join
from res_address import __version__, __license__, __doc__, __url__


def read(*pathcomponents):
    """Read the contents of a file located relative to setup.py"""
    with open(join(abspath(dirname(__file__)), *pathcomponents)) as thefile:
        return thefile.read()

setup(
    name = 'res-address',
    version=__version__,
    license=__license__,
    url=__url__,
    download_url=__url__ + '/tarball/' + __version__,
    author='Mariano Ruiz',
    author_email='mrsarm@gmail.com',
    description=__doc__,
    long_description=read('README.rst'),
    packages=[
        'res_address',
    ],
    test_suite='tests',
    zip_safe=False,
    platforms='any',
    #install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: System :: Networking',
    ],
)
