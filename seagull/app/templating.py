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

from mako.lookup import TemplateLookup
from streamline import (
    TemplateRoute as StreamlineTemplateRoute,
    XHRPartialRoute as StreamlineXHRPartialRoute)

from seagull import __appdir__


DEFAULT_CACHE = '/tmp/seagull-template-cache'
DEFAULT_TEMPLATES_DIR = os.path.join(__appdir__, 'default_templates')
TEMPLATE_CONFIG = {
    'lookup': None,
    'defaults': {},
}


def configure(conf, **options):
    debug = conf.get('seagull.debug')
    cache_dir = conf.get('seagull.template_cache', DEFAULT_CACHE)
    templates_dirs = [conf['runtime.skin_templates_dir'],
                      DEFAULT_TEMPLATES_DIR]
    default_filters = ['unicode', 'h']
    TEMPLATE_CONFIG['lookup'] = TemplateLookup(directories=templates_dirs,
                                               filesystem_checks=debug,
                                               default_filters=default_filters,
                                               module_directory=cache_dir,
                                               **options)
    TEMPLATE_CONFIG['defaults'] = conf['runtime.template_defaults']
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)


def render(template, ctx):
    final_ctx = TEMPLATE_CONFIG['defaults'].copy()
    final_ctx.update(ctx)
    template = TEMPLATE_CONFIG['lookup'].get_template(template)
    return template.render(**final_ctx)


class TemplateRoute(StreamlineTemplateRoute):
    template_func = staticmethod(render)


class XHRPartialRoute(StreamlineXHRPartialRoute):
    template_func = staticmethod(render)
