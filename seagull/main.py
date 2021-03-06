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

import sys
import locale

from seagull.app import App


def main():
    # Initialize the locale
    locale.setlocale(locale.LC_ALL, '')

    return App().start()


if __name__ == '__main__':
    sys.exit(main())
