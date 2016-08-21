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
import signal

from . import Option, Command


DEFAULT_PID = '/var/run/seagull.pid'


class Startup(Option):
    def add_args(self):
        group = self.parser.add_argument_group('startup options')
        if hasattr(os, 'fork'):
            group.add_argument('--background', '-b', action='store_true',
                                help='run in background')
            group.add_argument('--pid-file', '-p', metavar='PATH',
                               default=DEFAULT_PID, help='create a PID file '
                               'at specified path (default is '
                               '{})'.format(DEFAULT_PID))
            group.add_argument('--user', '-U', metavar='USER',
                                help='user to use for the process')
            group.add_argument('--group', '-G', metavar='GROUP',
                                help='group to use for the process')
        else:
            group.set_defaults(background=False, pid_file=None, user=None,
                               group=None)
        group.add_argument('--debug', action='store_true',
                           help='whether to enable debugging')
        group.add_argument('--quiet', '-q', action='store_true',
                            help='suppress terminal output')

    def test(self, args):
        return True

    def run(self, args):
        user_default = self.conf.get('seagull.user')
        group_default = self.conf.get('seagull.group')
        debug_default = self.conf.get('seagull.debug')
        self.conf['runtime.background'] = args.background
        self.conf['runtime.pid_file'] = args.pid_file
        self.conf['runtime.user'] = args.user or user_default
        self.conf['runtime.group'] = args.group or user.default
        self.conf['runtime.debug'] = args.debug or debug_default
        self.conf['runtime.quiet'] = args.quiet or args.command is not None


class Stop(Command):
    name = 'stop'
    help = 'stop the process that would be started with given options'

    def run(self, args):
        with open(args.pid_file, 'r') as f:
            pid = f.read()
        try:
            os.kill(int(pid), signal.SIGTERM)
        except (ValueError, TypeError):
            print('Invalid pid in pid file: {}'.format(pid), file=sys.stderr)
            self.quit(1)
        except Exception as e:
            print('Could not stop Seagull: {}'.format(e))
            self.quit(1)
        self.quit(0)
