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
Dynamic loading of code.
"""

import importlib


def load_class(module_name, class_name):
    """
    Loads a class from a module.

    :param module_name: The full name of the module. EX: abr.executors
    :type module_name: str
    :param class_name: The name of the class to load from the module.
    :type class_name: str
    :returns: The class requested.
    :rtype: class
    """
    return getattr(importlib.import_module(module_name), class_name)
