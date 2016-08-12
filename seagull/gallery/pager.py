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

import math


class Pager:
    """
    This class provides methods for paging through a gallery index. It is
    initialized with a gallery index object and optional current page number.
    """

    PER_PAGE = 10

    def __init__(self, index, current_page=1):
        self.index = index
        self.total_entries = len(index)
        self.current_page = current_page

    @property
    def pages(self):
        """
        Total number of pages
        """
        return math.ceil(self.total_entries / self.PER_PAGE)

    @property
    def page_entries(self):
        """
        Return entries belonging to current page
        """
        first_item = (self.current_page - 1) * self.PER_PAGE
        last_item = first_item + self.PER_PAGE
        return self.index[first_item:last_item]

    @property
    def has_next(self):
        """
        Whether there is a next page
        """
        return self.current_page < self.pages

    @property
    def has_prev(self):
        """
        Whether there is a previous page
        """
        return self.current_page > 1

    @property
    def next_page(self):
        """
        Page number of the next page if any, otherwise returns ``None``
        """
        if self.has_next:
            return self.current_page + 1
        return None

    @property
    def prev_page(self):
        """
        Page number of the previous page if any, otherwise returns ``None``
        """
        if self.has_prev:
            return self.current_page - 1
        return None

    @property
    def to_last(self):
        """
        Number of pages between current and last page including the last page
        """
        return self.pages - self.current_page

    @property
    def to_first(self):
        """
        Number of pages between current and first page including the first page
        """
        return self.current_page - 1

    def __len__(self):
        return len(self.page_entries)

    def __iter__(self):
        return iter(self.page_entries)
