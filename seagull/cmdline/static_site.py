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

from . import Command

from ..gallery.pager import Pager
from ..app.templating import render


def page_file(page_number):
    if page_number > 1:
        return 'page{}.html'.format(page_number)
    return 'index.html'


def render_page(ctx, page_number):
    ctx['pager'] = Pager(ctx['index'], page_number)
    return render('main.mako', ctx)


def write_page(output_dir, page_number, html):
    filename = page_file(page_number)
    path = os.path.join(output_dir, filename)
    with open(path, 'w') as f:
        f.write(html)


def build(conf):
    index = conf['runtime.gallery']
    output_dir = conf['runtime.gallery_dir']
    ctx = conf['runtime.template_defaults'].copy()
    ctx.pop('request')
    ctx['index'] = index
    ctx['static'] = True
    ctx['page_file'] = page_file
    total_pages = Pager(index).pages
    print('Gallery has {} pages'.format(total_pages))
    for page_number in range(1, total_pages + 1):
        print('Rendering page {}: '.format(page_number), end='')
        html = render_page(ctx, page_number)
        write_page(output_dir, page_number, html)
        print('DONE')
    sys.exit(0)


class StaticSite(Command):
    name = 'static-site'
    help = 'dump a static version of the gallery in the gallery dir'

    def add_args(self):
        self.conf['runtime.static_site'] = False

    def run(self, args):
        self.conf['runtime.static_site'] = True
        self.conf['runtime.start_hooks'].append(build)
