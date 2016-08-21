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
import shutil

from .. import __appdir__
from . import Command


class CustomSkin(Command):
    name = 'custom-skin'
    help = 'create custom skin directory'

    def add_args(self):
        self.group.add_argument('output', metavar='PATH', help='output path')

    def run(self, args):
        output_path = args.output
        if os.path.exists(output_path):
            print("ERROR: '{}' already exists".format(
                args.custom_skin))
            self.quit(1)
        skin_dir = os.path.abspath(os.path.join(__appdir__, 'skins',
                                                'seagull'))
        shutil.copytree(skin_dir, output_path)
        print("Created skin in '{}'".format(output_path))
        self.quit(0)
