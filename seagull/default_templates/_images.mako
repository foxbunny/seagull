<%doc>
    Gallery elements
    ================

    This template contains fragments that are used to construct the gallery 
    list. The defs in this template are used in the ``main.mako`` template, so 
    look there for example usage.

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

<%def name="image(entry)">
    <li class="gallery-list-item" data-path="${gallery.get_urlpath(entry)}">
    <img src="${url('gallery:image', path=gallery.get_urlpath(entry))}">
    </li>
</%def>

<%def name="list()">
    <section id="gallery" class="gallery">
    <ul class="gallery-list">
        %for entry in pager:
            ${self.image(entry)}
        %endfor
    </ul>
    </section>
</%def>
