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
Executor types.
"""

from abr.loader import load_class
from abr.mixins.logger import LoggerMixin


class Executor(LoggerMixin):
    """
    Execution strategy class.
    """

    def __init__(self, tools, *args, **kwargs):
        """
        Initializes a new instance of an Executor.

        :param tools: List of tool configurations to run.
        :type tools: list
        :param args: All non-keyword arguments (ignored).
        :type args: list
        :param kwargs: All keyword arguments (ignored).
        :rtype kwargs: dict
        """
        super().__init__()
        self.tools = tools

    def run(self):
        """
        Executes the logic for the executor. Must be overriden.
        """
        raise NotImplementedError('Must be overridden.')


class SerialExecutor(Executor):
    """
    Execute each tool in order.
    """

    def run(self):
        """
        Implements the logic to run a series of tools one at a time in the
        order provided.
        """
        for tool_config in self.tools:
            self.logger.info('Executing tool: {}'.format(tool_config['name']))
            tool_cls = load_class(
                'abr.executors.tools', tool_config['type'])
            result = tool_cls(**tool_config).run()
            if result[0] is not True:
                self.logger.fatal(
                    'Error executing {}. Stopping execution. See logs '
                    'for more information.'.format(tool_config['name']))
                return
