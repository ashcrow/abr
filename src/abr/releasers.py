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
Release types.
"""

import os

from abr.loader import load_class
from abr.mixins.logger import LoggerMixin


class Releaser(LoggerMixin):
    """
    Base class for all Releasers.
    """

    def __init__(self, releaser_config, project_config, *args, **kwargs):
        """
        Initializes a new Release instance.

        :param releaser_config: Releaser specific configuration.
        :type releaser_config: dict
        :param project_config: Project specific configuration.
        :type project_config: dict
        :param args: All non-keyword arguments (ignored).
        :type args: list
        :param kwargs: All keyword arguments (ignored).
        :rtype kwargs: dict
        """
        super().__init__()
        self.releaser_config = releaser_config
        self.project_config = project_config

    def run(self):
        """
        Executes the logic for the releaser. Must be overriden.
        """
        raise NotImplementedError('Must be overridden.')


class RunOnce(Releaser):
    """
    Runs the release once and then returns control.
    """
    # TODO: Break repo out since not everyone uses git
    from git import Repo

    def run(self):
        """
        Implements the run-once-then-return-control logic for a release run.
        """
        dir_name = os.path.basename(self.project_config['repo'])

        # If we have a checkout, use it.
        if os.path.isdir(dir_name):
            self.logger.info('Using local clone {}'.format(dir_name))
            repo = self.Repo(dir_name)
        # Otherwise clone
        else:
            self.logger.info('Cloning {} to {}'.format(
                self.project_config['repo'], dir_name))
            repo = self.Repo.clone_from(self.project_config['repo'], dir_name)

        # Update the copy to make sure it's fresh
        # and to get the fetch_info instance
        fetch_info = repo.remote().pull()[0]
        # Log the last commit
        self.logger.info('Fetch Info: {}: {} "{}"'.format(
            fetch_info.commit.hexsha, fetch_info.commit.author.name,
            fetch_info.commit.message))

        # Find the unreleased tag
        # TODO: Think about if this should be moved to a 'release strategy'
        # type ... or if we should always assume tags are how people release.
        unreleased = None
        tags = [x.name for x in repo.tags]
        for tag in tags:
            if 'released-{}'.format(tag) not in tags:
                unreleased = tag
                break

        if not unreleased:
            self.logger.info('No unreleaed tags.')
            return
        self.logger.info('Unreleased tag found: {}'.format(unreleased))

        executor_cls = load_class(
            'abr.executors', self.releaser_config['executor'])
        self.logger.debug('Beginning executor run: {}({})'.format(
            self.releaser_config['executor'], self.releaser_config['tools']))
        executor_cls(self.releaser_config['tools']).run()
        self.logger.debug('Executor finished')
