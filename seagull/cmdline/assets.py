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
import shutil
import signal
import tempfile
import subprocess
from os.path import normpath, join, dirname, exists, isdir, abspath

from . import Command


TMPDIR = tempfile.gettempdir()
COMPASS_PID = join(TMPDIR, 'compass.pid')
COFFEE_PID = join(TMPDIR, 'coffee.pid')
COMPASS = shutil.which('compass')
COFFEE = shutil.which('coffee')


class AssetsCommand:
    """
    Base class for assets-related commands
    """
    DEFAULT_SKIN = 'seagull'
    THISDIR = dirname(__file__)
    ROOTDIR = dirname(THISDIR)
    SKINDIR = join(ROOTDIR, normpath('seagull/skins'))

    def __init__(self, conf):
        if conf['runtime.skin_path_override']:
            self.skindir = abspath(conf['runtime.skin_path_override'])
        else:
            self.skindir = abspath(conf['runtime.skin_path'])
        print("using skin in '{}'".format(self.skindir))
        self.static_url = conf['assets.static_url']
        self.srcdir = join(self.skindir, 'src')
        self.assetsdir = join(self.skindir, 'assets')
        self.scssdir = join(self.srcdir, 'scss')
        self.csdir = join(self.srcdir, 'coffee')
        self.cssdir = join(self.assetsdir, 'css')
        self.jsdir = join(self.assetsdir, 'js')
        self.imgdir = join(self.assetsdir, 'img')
        self.fontdir = join(self.assetsdir, 'font')

    def compass_cmd(self, *cmds):
        return [
            COMPASS,
            *cmds,
            '--http-path', self.static_url,
            '--app-dir', self.skindir,
            '--sass-dir', self.scssdir,
            '--css-dir', self.cssdir,
            '--images-dir', self.imgdir,
            '--fonts-dir', self.fontdir,
            '--javascript-dir', self.jsdir,
            '--output-style', 'expanded',
            '--relative-assets',
        ]

    def coffee_cmd(self, *cmds):
        return [
            COFFEE,
            *cmds,
            '--bare',
            '--output', self.jsdir,
            self.csdir,
        ]


def write_pid(pid, pidfile):
    with open(pidfile, 'w') as f:
        f.write(str(pid))


def read_pid(pidfile):
    with open(pidfile, 'r') as f:
        return int(f.read())


def kill_pid(pid):
    if sys.platform == 'win32':
        # On win32, a cmd.exe is spawned, which then spawns the process, so
        # the pid is for the cmd.exe process and not the main process
        # itself. Therefore we need to send an interrupt to the cmd.exe
        # process which will then hopefully terminate the children.
        os.kill(pid, signal.CTRL_BREAK_EVENT)
    os.kill(pid, signal.SIGTERM)


def kill_pidfile(pidfile):
    pid = read_pid(pidfile)
    kill_pid(pid)
    os.unlink(pidfile)


def start_watchers(conf):
    print('starting watchers')
    cmd = AssetsCommand(conf)
    if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP'):
        # On Windows, commands are run in a subshell regardless of the
        # ``shell`` argument unless CREATE_NEW_PROCESS_GROUP flag is used.
        # This flag is not supported on *nix platforms, so we test that the
        # flag is supposed instead of testing for platform.
        popen_kw = dict(creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        popen_kw = {}
    compass = subprocess.Popen(cmd.compass_cmd('watch'), **popen_kw)
    coffee = subprocess.Popen(cmd.coffee_cmd('--watch'), **popen_kw)
    write_pid(compass.pid, COMPASS_PID)
    write_pid(coffee.pid, COFFEE_PID)
    sys.exit(0)


def recompile_assets(conf):
    print('recompiling assets')
    cmd = AssetsCommand(conf)
    try:
        subprocess.check_call(cmd.compass_cmd('compile', '--force'))
        subprocess.check_call(cmd.coffee_cmd('--compile'))
    except subprocess.CalledProcessError:
        print('Error compiling assets')
        sys.exit(1)
    else:
        sys.exit(0)


class Watch(Command):
    name = 'watch'
    help = 'watch a skin directory for changes and recompile assets'

    def add_args(self):
        self.group.add_argument('--skin-path', '-P', metavar='PATH',
                                help='use PATH instead of skin specified by '
                                'the configuration file')

    def run(self, args):
        self.conf['runtime.skin_path_override'] = args.skin_path
        self.conf['runtime.start_hooks'].append(start_watchers)


class StopWatchers(Command):
    name = 'stop-watchers'
    help = 'stop the assets watchers'

    @staticmethod
    def kill_process(name, pidfile):
        try:
            kill_pidfile(pidfile)
        except FileNotFoundError:
            print('{} PID file not found, nothing to do'.format(name))
        except OSError:
            print('{} could not be stopped, is it still running?'.format(name))
            os.unlink(pidfile)

    def run(self, args):
        print('stopping watchers')
        self.kill_process('compass', COMPASS_PID)
        self.kill_process('coffee', COFFEE_PID)
        self.quit(0)


class Recompile(Command):
    name = 'recompile'
    help = 'recompile assets'

    def add_args(self):
        self.group.add_argument('--skin-path', '-P', metavar='PATH',
                                help='use PATH instead of skin specified by '
                                'the configuration file')

    def run(self, args):
        self.conf['runtime.skin_path_override'] = args.skin_path
        self.conf['runtime.start_hooks'].append(recompile_assets)
