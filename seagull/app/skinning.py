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

import logging
from os.path import normpath, join, isdir

from seagull import __appdir__


DEFAULT_SKIN = 'seagull'


def configure(conf):
    """
    Configure a seagull to use templates and assets from specified skin
    """
    skin = conf.get('seagull.skin', DEFAULT_SKIN)
    extra_skins = conf.get('seagull.extra_skins')
    skin_path = ''
    if extra_skins:
        # Let's try the extra skins directory first
        skin_path = normpath(join(extra_skins, skin))
    if not isdir(skin_path):
        skin_path = normpath(join(__appdir__, 'skins', skin))
    if skin != DEFAULT_SKIN:
        logging.debug("Using skin '{}'".format(skin))
    templates_dir = join(skin_path, 'templates')
    assets_dir = join(skin_path, 'assets')
    conf['runtime.skin_templates_dir'] = templates_dir
    conf['runtime.assets_dir'] = assets_dir
