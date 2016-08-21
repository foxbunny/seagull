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
import argparse


from ..cmdline.version import Version
from ..cmdline.conf import Conf
from ..cmdline.process import Startup, Stop
from ..cmdline.templates import Templates
from ..cmdline.custom_conf import CustomConf
from ..cmdline.custom_skin import CustomSkin
from ..cmdline.static_site import StaticSite


COMMANDS = (
    Version,
    Conf,
    Startup,
    Stop,
    Templates,
    CustomConf,
    CustomSkin,
    StaticSite,
)

DESCRIPTION = 'Seagull application manager and utility commands'


def parse_args(conf):
    registered = []
    parser = argparse.ArgumentParser(prog='seagull', description=DESCRIPTION)
    subparsers = parser.add_subparsers(title='commands', dest='command')

    for cmd in COMMANDS:
        cmd(registered.append, parser, subparsers, conf)
    args = parser.parse_args()
    for cmd in registered:
        if cmd.test(args):
            cmd.run(args)
    if args.command:
        args.callback.run(args)
