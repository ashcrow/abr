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
CLI related code.
"""

import yaml

from abr.loader import load_class


def main():
    """
    Main entry point.
    """
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config', help='Release configuration to utilize.', nargs=1)
    args = parser.parse_args()

    try:
        with open(args.config[0], 'r') as f:
            config = yaml.safe_load(f)
    except Exception as error:
        parser.error(error)

    for project_name in config.get('projects', []):
        project_config = config['projects'][project_name]

        releaser_config = config['releasers'][project_config['releaser']]
        releaser_cls = load_class('abr.releasers', releaser_config['type'])
        releaser = releaser_cls(releaser_config, project_config)
        releaser.run()


if __name__ == '__main__':
    main()
