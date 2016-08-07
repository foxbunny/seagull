#!/usr/bin/python3
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

# These imports need to be here at the top so monkey patching can be done as
# early as possible.

import gevent.monkey
gevent.monkey.patch_all(aggressive=True)

# For more details on the below see: http://bit.ly/18fP1uo
import gevent.hub
gevent.hub.Hub.NOT_ERROR = (Exception,)

# Continuing with normal imports

import os
import sys

import bottle

from seagull import __version__, __appdir__
from seagull.app import App


DEFAULT_CONF = os.path.join(__appdir__, 'seagull.ini')
DEFAULT_PID = '/var/run/seagull.pid'

bottle.DEBUG = True


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Start seagull photo gallery')
    parser.add_argument('--version', '-V', action='store_true',
                        help='print the version number and quit')
    parser.add_argument('--conf', '-c', metavar='PATH', default=DEFAULT_CONF,
                        help='set the configuration file path')
    parser.add_argument('--background', '-b', action='store_true',
                        help='run in background')
    parser.add_argument('--pid-file', '-p', metavar='PATH',
                        default=DEFAULT_PID, help='create a PID file at '
                        'specified path (default is /var/run/seagull.pid)')
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return 0

    app = App(conf=args.conf, background=args.background,
              pid_file=args.pid_file)
    return app.start()


if __name__ == '__main__':
    sys.exit(main())
