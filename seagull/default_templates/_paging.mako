<%doc>
    Pager elements
    ==============

    This template contains fragments that are used to construct the gallery 
    list pager.

    This template uses the ``pager`` object, which is passed by the Seagull 
    backend. This object has the following properties:

    - ``current_page``: current page number
    - ``pages``: total number of pages
    - ``page_entries``: entries belonging to the current page
    - ``has_next``: whether next page exists
    - ``has_prev``: whether previous page exists
    - ``next_page``: next page number
    - ``prev_page``: previous page number
    - ``to_last``: number of pages to the last one
    - ``to_first``: number of pages to the first

    Seagull photo gallery app
    Copyright (C) 2016  Hajime Yamasaki Vukelic

    This program is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
    more details.
</%doc>

<%def name="simple_pager()">
    <p class="pager">
        %if pager.has_prev:
            <a href="${url('gallery:main', page=pager.prev_page)}" class="pager-prev pager-page">
                previous
            </a>
        %endif
        %if pager.has_next:
            <a href="${url('gallery:main', page=pager.next_page)}" class="pager-next pager-page">
                next
            </a>
        %endif
    </p>
</%def>
