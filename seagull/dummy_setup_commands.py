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

from distutils.cmd import Command


class DummyCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print('This command is only supported on Python 3.5 or newer')


class Watch(DummyCommand):
    pass


class Stop(DummyCommand):
    pass


class Recompile(DummyCommand):
    pass
