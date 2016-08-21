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
import pprint

from . import Option
from confloader import ConfDict


DEFAULT_PID = '/var/run/seagull.pid'


class Conf(Option):
    def add_args(self):
        appdir = self.conf['runtime.appdir']
        default_conf = os.path.join(appdir, 'seagull.ini')
        self.parser.add_argument('--conf', '-c', metavar='PATH',
                                 default=default_conf,
                                 help='set the configuration file path')
        self.parser.add_argument('--debug-conf', action='store_true',
                                 help='print out the configuration options '
                                 'and quit')

    def test(self, args):
        return True

    def run(self, args):
        self.conf.update(ConfDict.from_file(args.conf))
        if args.debug_conf:
            pprint.pprint(self.conf, indent=4)
            self.quit(0)
