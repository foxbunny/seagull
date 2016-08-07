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

import sys

from seagull import __version__


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Start seagull photo gallery')
    parser.add_argument('--version', '-V', help='print the version number and '
                        'quit', action='store_true')
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
