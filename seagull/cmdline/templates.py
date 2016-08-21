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
import sys

from . import Command


def templates_hook(conf):
    for t in conf['runtime.template_dirs']:
        print(os.path.abspath(t))
    sys.exit(0)



class Templates(Command):
    name = 'templates'
    help = 'list the template directories'

    def run(self, args):
        self.conf['runtime.start_hooks'].append(templates_hook)
