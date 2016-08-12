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

from .app import Static
from ..app.templating import TemplateRoute


class Main(TemplateRoute):
    """
    Main page
    """
    path = '/'
    template_name = 'main.mako'

    def get(self):
        return {}


class Image(Static):
    path = '/gallery/<path:path>'

    def get_base_path(self):
        return self.config['runtime.gallery_dir']


