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
import logging.config

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}
DEFAULT_SIZE = 10 * 1024 * 1024
DEFAULT_BACKUPS = 0
DEFAULT_LEVEL = logging.DEBUG


def configure(conf, quiet=False):
    """
    Set up the global logger configuration
    """
    path = conf.get('logger.path')
    maxsize = conf.get('logger.size', DEFAULT_SIZE)
    backups = conf.get('logger.backups', DEFAULT_BACKUPS)
    format = conf.get('logger.format')
    date_fmt = conf.get('logger.date_format')
    if conf.get('seagull.debug'):
        # When application is in debug mode, logger always uses DEBUG level
        level = logging.DEBUG
    else:
        level = LEVELS.get(conf.get('logger.level', 'debug'), DEFAULT_LEVEL)

    handlers = {
        'file': {
            'class': 'logging.NullHandler',
            'formatter': 'default',
        }
    }

    if not quiet:
        handlers['console'] = {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        }

    if path:
        handlers['file'].update({
            'class': 'logging.FileHandler',
            'filename': path,
        })
    if backups:
        handlers['file'].update({
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': maxsize,
            'backupCount': backups,
        })

    logging.config.dictConfig({
        'version': 1,
        'root': {
            'handlers': handlers.keys(),
            'level': level
        },
        'handlers': handlers,
        'formatters': {
            'default': {
                'format': format,
                'datefmt': date_fmt,
            },
        },
    })
