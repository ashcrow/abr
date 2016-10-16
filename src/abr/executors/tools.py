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
Tool types.
"""

import subprocess

from abr.mixins.logger import LoggerMixin


class Tool(LoggerMixin):

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of a Tool.

        :param args: All non-keyword arguments (ignored).
        :type args: list
        :param kwargs: All keyword arguments (ignored).
        :rtype kwargs: dict
        """
        super().__init__()

    def run(self):
        """
        Executes the logic for the tool. Must be overriden.
        """
        raise NotImplementedError('Must be overridden.')


class Shell(Tool):
    """
    Shell tool abstraction.
    """

    def __init__(self, command, success_codes=[0], *args, **kwargs):
        """

        :param command: The shell command to execute.
        :type command: str
        :param success_codes: Successful return codes the command may return.
        :type success_codes: list
        :param args: All non-keyword arguments (ignored).
        :type args: list
        :param kwargs: All keyword arguments (ignored).
        :rtype kwargs: dict
        """
        super().__init__()
        self.command = command
        self.success_codes = success_codes

    def run(self):
        """
        Implements the execution of a single shell command.

        :returns: The success result and command output of the shell command.
        :rtype: tuple(bool, str)
        """
        self.logger.info('Executing command: "{}"'.format(self.command))
        results = subprocess.Popen(
            self.command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Turn the output into a string.
        command_output = b''.join(results.communicate()).decode('utf8')
        # NOTE: communicate() must be called before returncode is available.
        self.logger.debug('Command return code: {}'.format(results.returncode))
        self.logger.info(command_output)
        # If it is considered successful
        if results.returncode in self.success_codes:
            return (True, command_output)
        # If it is not
        return (False, command_output)
