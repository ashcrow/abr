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
Logging specific mixins.
"""

import logging


class LoggerMixin:
    """
    Mixin that provides a basic instance level logger.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes an instance level logger upon instance creation.

        :param args: All non-keyword arguments (ignored).
        :type args: list
        :param kwargs: All keyword arguments (ignored).
        :rtype kwargs: dict
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        # If we have no handlers then we need to configure
        if len(self.logger.handlers) == 0:
            self.logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            handler.formatter = logging.Formatter('%(levelname)s: %(message)s')
            self.logger.addHandler(handler)
