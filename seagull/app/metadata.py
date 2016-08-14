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

from os.path import normpath, join

from ..gallery.metadata import Metadata


def configure(conf):
    gallery_dir = conf['runtime.gallery_dir']
    title = conf['seagull.title']
    description = conf['seagull.description']
    author = conf['seagull.author']
    copyright = conf['seagull.copyright']
    metadata = Metadata(title, description, author, copyright, gallery_dir)
    conf['runtime.metadata'] = metadata
    conf['runtime.template_defaults']['metadata'] = metadata
