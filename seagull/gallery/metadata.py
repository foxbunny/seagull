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

import datetime
import functools
from os.path import join

import markdown


def url_method(urlpattern, keyname):
    @property
    def meth(self):
        return self._get_url(urlpattern, keyname)
    return meth


class AboutInfo:
    DEFAULT_INFO = {
        'title': 'Seagull',
        'description': 'Open-source skinnable photo gallery app',
        'copyright': 2016,
        'author': 'Seagull',
    }

    def __init__(self, contact_info):
        self.info = self.DEFAULT_INFO.copy()
        self.info.update(contact_info)

    def __getattr__(self, name):
        if name in self.info:
            return self.info[name]
        return super().__getattribute__(name)

    def _get_url(self, urlpattern, key):
        if key not in self.info:
            return None
        return urlpattern.format(self.info[key])

    @property
    def copyright(self):
        try:
            return int(self.info['copyright'])
        except (KeyError, TypeError, ValueError):
            return datetime.date.today().year

    email = url_method('mailto:{}', 'email')
    facebook = url_method('https://www.facebook.com/{}/', 'facebook')
    twitter = url_method('https://twitter.com/{}', 'twitter')
    flickr = url_method('https://www.flickr.com/photos/{}', 'flickr')
    linkedin = url_method('https://www.linkedin.com/in/{}', 'linkedin')
    googleplus = url_method('https://plus.google.com/+{}', 'googleplus')
    youtube = url_method('https://www.youtube.com/channel/{}', 'youtube')


class Metadata:
    def __init__(self, gallery_dir):
        self.gallery_dir = gallery_dir
        self.cover = None
        self.logo = None
        self.about = ''
        self.info = None
        self.reload()
        self.title = self.info.title
        self.description = self.info.description
        self.copyright_year = self.info.copyright
        self.author = self.info.author
        self.contact = self.info

    def reload(self):
        self.about = self.get_html(join(self.gallery_dir, '_about.mkd'))
        self.info = self.get_kval(join(self.gallery_dir, '_about.info'))

    @property
    def copyright_range(self):
        year = datetime.date.today().year
        if year == self.copyright_year:
            return str(year)
        return '{}&mdash;{}'.format(self.copyright_year, year)

    @staticmethod
    def get_html(path):
        try:
            with open(path, 'r') as f:
                return markdown.markdown(f.read())
        except (OSError, IOError):
            return ''

    @staticmethod
    def get_kval(path):
        info = {}
        try:
            with open(path, 'r') as f:
                for line in f:
                    key, val = line.split(':', 1)
                    info[key] = val.strip()
        except (OSError, IOError, IndexError):
            return None
        else:
            return AboutInfo(info)
