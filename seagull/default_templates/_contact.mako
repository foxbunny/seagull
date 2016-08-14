<%doc>
    Contacts template
    =================

    This partial template renders components for the contacts pare/area. It 
    currently supports the following contact methods:

    - email
    - facebook
    - twitter
    - linkedin
    - flickr
    - googleplus

    See the ``main.mako`` template for examples of how blocks are used, and
    refer to Mako documentation for in-depth coverage.

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

<%def name="contact_detail(label, url)">
    %if url:
        <li class="contact-detail">
        <a href="${url}" rel="nofollow" class="contact-${label.lower()}">${label}</a>
        </li>
    % endif
</%def>

<section id="contact" class="contact">
<ul class="contact-info">
    ${self.contact_detail('Email', metadata.contact.email)}
    ${self.contact_detail('Facebook', metadata.contact.facebook)}
    ${self.contact_detail('Twitter', metadata.contact.twitter)}
    ${self.contact_detail('YouTube', metadata.contact.youtube)}
    ${self.contact_detail('Flickr', metadata.contact.flickr)}
    ${self.contact_detail('Google', metadata.contact.googleplus)}
    ${self.contact_detail('LinkedIn', metadata.contact.linkedin)}
</ul>
</section>
