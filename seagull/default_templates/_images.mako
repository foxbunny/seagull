<%doc>
    Gallery elements
    ================

    This template contains fragments that are used to construct the gallery 
    image list.

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

%for entry in pager:
    <%
        path = gallery.get_urlpath(entry)
        image_url = path if static else url('gallery:image', path=path)
    %>
    <li class="gallery-entry" data-path="${path}" data-url="${image_url}">\
    <img class="gallery-image" src="${image_url}">\
    </li>\
%endfor
