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
from distutils.cmd import Command
from os.path import normpath, join, dirname, exists, isdir


TMPDIR = tempfile.gettempdir()
COMPASS_PID = join(TMPDIR, 'compass.pid')
COFFEE_PID = join(TMPDIR, 'coffee.pid')
COMPASS = shutil.which('compass')
COFFEE = shutil.which('coffee')


class AssetsCommand(Command):
    """
    Base class for assets-related commands
    """
    DEFAULT_SKIN = 'seagull'
    THISDIR = dirname(__file__)
    ROOTDIR = dirname(THISDIR)
    SKINDIR = join(ROOTDIR, normpath('seagull/skins'))

    user_options = [
        ('skin=', 's', 'skin name'),
        ('static-url=', 'u', 'base URL used for static files'),
    ]

    def initialize_options(self):
        self.skin = self.DEFAULT_SKIN
        self.skindir = None
        self.static_url = '/static/'

    def finalize_options(self):
        if isdir(self.skin):
            skindir = self.skin
        else:
            skindir = join(self.SKINDIR, self.skin)
        if not exists(skindir):
            raise RuntimeError("'{}': no such skin".format(self.skin))
        self.skindir = skindir
        self.srcdir = join(skindir, 'src')
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


class Watch(AssetsCommand):
    description = 'run the CoffeeScript and Compass watchers'

    @staticmethod
    def write_pid(pid, pidfile):
        with open(pidfile, 'w') as f:
            f.write(str(pid))

    def run(self):
        if hasattr(subprocess, 'CREATE_NEW_PROCESS_GROUP'):
            # On Windows, commands are run in a subshell regardless of the
            # ``shell`` argument unless CREATE_NEW_PROCESS_GROUP flag is used.
            # This flag is not supported on *nix platforms, so we test that the
            # flag is supposed instead of testing for platform.
            popen_kw = dict(creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            popen_kw = {}
        compass = subprocess.Popen(self.compass_cmd('watch'), **popen_kw)
        coffee = subprocess.Popen(self.coffee_cmd('--watch'), **popen_kw)
        print('pid for Compass is {}'.format(compass.pid))
        self.write_pid(compass.pid, COMPASS_PID)
        print('pid for CoffeeScript is {}'.format(coffee.pid))
        self.write_pid(coffee.pid, COFFEE_PID)


class Stop(Command):
    description = 'stop the CoffeeScript and Compass watchers'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def read_pid(pidfile):
        with open(pidfile, 'r') as f:
            return int(f.read())

    @staticmethod
    def kill_pid(pid):
        if sys.platform == 'win32':
            # On win32, a cmd.exe is spawned, which then spawns the process, so
            # the pid is for the cmd.exe process and not the main process
            # itself. Therefore we need to send an interrupt to the cmd.exe
            # process which will then hopefully terminate the children.
            os.kill(pid, signal.CTRL_BREAK_EVENT)
        os.kill(pid, signal.SIGTERM)

    def kill_pidfile(self, pidfile):
        pid = self.read_pid(pidfile)
        self.kill_pid(pid)
        os.unlink(pidfile)

    def run(self):
        self.kill_pidfile(COMPASS_PID)
        self.kill_pidfile(COFFEE_PID)


class Recompile(AssetsCommand):
    description = 'recompile the CoffeeScript and Compass watchers'

    def run(self):
        subprocess.check_call(self.compass_cmd('compile', '--force'),
                              shell=True)
        subprocess.check_call(self.coffee_cmd('--compile'), shell=True)
