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

import sys
import argparse


class ArgBase:
    def run(self, args):
        pass

    @staticmethod
    def quit(code=0):
        sys.exit(code)


class Option(ArgBase):
    flags = None
    kwargs = {}

    def __init__(self, register, parser, subparsers, conf={}):
        self.parser = parser
        self.conf = conf
        self.add_args()
        register(self)

    def add_args(self):
        pass

    def test(self, args):
        return False


class Command(ArgBase):
    name = None
    help = None

    def __init__(self, register, parser, subparsers, conf={}):
        self.conf = conf
        self.group = subparsers.add_parser(self.name, help=self.help)
        self.add_args()
        self.group.set_defaults(callback=self)

    def add_args(self):
        pass
