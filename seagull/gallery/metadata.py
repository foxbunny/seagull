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

import bleach
import markdown


def url_method(urlpattern, keyname):
    @property
    def meth(self):
        return self._get_url(urlpattern, keyname)
    return meth


class Contact:
    def __init__(self, contact_info):
        self.info = contact_info

    def _get_url(self, urlpattern, key):
        if key not in self.info:
            return None
        return urlpattern.format(self.info[key])

    email = url_method('mailto:{}', 'email')
    facebook = url_method('https://www.facebook.com/{}/', 'facebook')
    twitter = url_method('https://twitter.com/{}', 'twitter')
    flickr = url_method('https://www.flickr.com/photos/{}', 'flickr')
    linkedin = url_method('https://www.linkedin.com/in/{}', 'linkedin')
    googleplus = url_method('https://plus.google.com/+{}', 'googleplus')


class Metadata:
    def __init__(self, title, desc, author, copyright, about, contact):
        self.title = title
        self.description = desc
        self.author = author
        self.copyright_year = copyright
        self.about_file = about
        self.contact_file = contact
        self.about = ''
        self.contact = ''
        self.reload()

    def reload(self):
        self.about = self.get_html(self.about_file)
        self.contact = self.get_kval(self.contact_file)

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
        contact = {}
        try:
            with open(path, 'r') as f:
                for line in f:
                    key, val = line.split(':', 1)
                    contact[key] = val.strip()
        except (OSError, IOError, IndexError):
            return None
        else:
            return Contact(contact)
