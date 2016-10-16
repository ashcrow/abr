#!/usr/bin/env python3
# abr: Always Be Releasing
# Copyright (C) 2016 Steve Milner
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
"""
Installation script.
"""

from setuptools import setup, find_packages


setup(
    name='abr',
    version='0.1.0',
    description='Always Be Releasing',
    url='https://github.com/ashcrow/abr',
    license="LGPLv2+",

    install_requires=['gitpython', 'PyYAML'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'abr = abr.cli:main',
        ],
    }
)
