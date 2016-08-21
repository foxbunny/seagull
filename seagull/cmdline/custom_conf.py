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

from .. import __appdir__
from . import Command


CONFIGURATION_TEMPLATE = """[config]

defaults =
  {path}

[seagull]

# Add your settings below this line
"""


class CustomConf(Command):
    name = 'custom-conf'
    help = 'create custom configuration file skeleton'

    def add_args(self):
        self.group.add_argument('output', metavar='PATH', help='output path')

    def run(self, args):
        output_path = args.output
        conf_path = os.path.abspath(os.path.join(__appdir__, 'seagull.ini'))
        with open(output_path, 'w') as f:
            f.write(CONFIGURATION_TEMPLATE.format(path=conf_path))
        self.quit(0)
