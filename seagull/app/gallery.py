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
import logging

from ..gallery.index import Index


DEFAULT_DIR = '/tmp/seagull-gallery'


def configure(conf):
    """
    Configure the gallery
    """
    gallery_dir = conf.get('seagull.gallery_dir', DEFAULT_DIR)
    gallery_dir = os.path.abspath(os.path.normpath(gallery_dir))
    try:
        index = Index(gallery_dir)
    except ValueError:
        # the gallery directory did not exist
        logging.critical("Quitting, no gallery directory '%s'", gallery_dir)
        sys.exit(1)
    index.rescan()
    conf['runtime.gallery_dir'] = gallery_dir
    conf['runtime.gallery'] = index
    conf['runtime.template_defaults']['gallery'] = index
