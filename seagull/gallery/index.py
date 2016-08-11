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
import locale
import hashlib
import logging
import functools
from pathlib import PosixPath, WindowsPath


class Entry:
    """
    This class encapsulates a single gallery entry. It contains information
    about the file path, extension, modification timestamp, and file size.
    Entries are created from ``os.Direntry`` objects returned by calls such as
    ``os.scandir()``.

    Instantianting this class doubles as path validation. Passing objects that
    have any of the following characteristics results in a ``ValidationError``:

    - path is a directory
    - path has no extension
    - path has an extenion that is not supported
    - path starts with a dot
    - file at the path has 0 size

    """

    #: Supported extensions
    EXTENSIONS = ('.jpg', '.png', '.gif')

    def __init__(self, dentry):
        self.validate(dentry)
        self.path = dentry.path
        self.name = dentry.name
        self.ext = os.path.splitext(self.name)[1]
        self.size = dentry.stat().st_size
        self.mtime = dentry.stat().st_mtime
        self._hash = None

    @property
    def hash(self):
        """
        MD5 hash of the path
        """
        if not self._hash:
            md5 = hashlib.md5()
            md5.update(self.path.encode('utf8'))
            self._hash = md5.hexdigest()
        return self._hash

    @classmethod
    def from_path(cls, path):
        """
        Instantiate an entry from a path (string)
        """
        try:
            pentry = WindowsPath(path)
        except NotImplementedError:
            pentry = PosixPath(path)
        return cls(pentry)

    def validate(self, dentry):
        """
        Validate the ``os.DirEntry`` object for use with ``Entry`` class
        """
        path = dentry.path
        # Is a directory
        if dentry.is_dir():
            raise ValueError('{} is a directory'.format(path))
        if dentry.name.startswith('.'):
            raise ValueError('{} starts with a dot'.format(path))
        if dentry.stat().st_size <= 0:
            raise ValueError('{} is an empty file'.format(path))
        if '.' not in dentry.name:
            raise ValueError('{} has no extension'.format(path))
        if os.path.splitext(dentry.name)[1].lower() not in self.EXTENSIONS:
            raise ValueError('{} has unsupported extension'.format(path))

    @staticmethod
    def cmp(entry):
        """
        Comparison function to be used in ``key`` arguments when sorting
        """
        collated_cmp = functools.cmp_to_key(locale.strcoll)
        return collated_cmp(entry.path)

    def __hash__(self):
        return int(self.hash, 16)

    def __str__(self):
        return self.path

class Index:
    """
    This class encapsulates the gallery index information (file list) and the
    related methods. This object should be instantiated once and then used as
    the authoritative source on the state of the gallery folder.

    The Index also behaves as a container for the ``Entry`` objects and can be
    iterated over, tested for inclusion, reversed, etc.

    The entries in the gallery index are sorted alphabetically with full
    support for Unicode collation according to currently active system locale.
    """

    def __init__(self, path):
        if not os.path.isdir(path):
            raise ValueError('{} is missing or not a directory'.format(path))
        self.path = path
        self.entries = []
        self.last_update = None
        logging.debug('Setting up index for %s', self.path)

    def check_last_update(self, entry):
        """
        Update ``last_update`` property if ``entry`` is newer.
        """
        if not self.last_update:
            self.last_update = entry.mtime
        if entry.mtime > self.last_update:
            self.last_update = entry.mtime

    def rescan(self):
        """
        Perform full rescan of the gallery directory.
        """
        self.entries = []
        for dentry in os.scandir(self.path):
            try:
                entry = Entry(dentry)
            except ValueError:
                logging.debug('Omitted %s from gallery', dentry.path)
                continue
            self.check_last_update(entry)
            self.entries.append(entry)
        logging.debug('Added %s items to the index', len(self.entries))
        self.sort()

    def sort(self):
        """
        Sort the entries alphabetically
        """
        logging.debug('Sorting items')
        self.entries.sort(key=Entry.cmp)

    def __getitem__(self, key):
        return self.entries[key]

    def __reversed__(self):
        return reversed(self.entries)

    def __contains__(self, item):
        return item in self.entries

    def __iter__(self):
        return iter(self.entries)
