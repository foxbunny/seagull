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

from bottle import static_file

from streamline import NonIterableRouteBase


class Static(NonIterableRouteBase):
    name = 'app:static'
    path = '/static/<path:path>'

    def get(self, path):
        staticdir = self.app.config['runtime.static_dir']
        return static_file(path, staticdir)
