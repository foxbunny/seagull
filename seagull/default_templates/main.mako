<%doc>
    Gallery main page
    =================

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

<%inherit file="/base.mako"/>
<%namespace name="images" file="/_images.mako"/>
<%namespace name="paging" file="/_paging.mako"/>
<%namespace name="contact" file="/_contact.mako"/>

<%block name="title">${metadata.title} | page ${pager.current_page}</%block>

<heading class="hero${' hero-short' if pager.has_prev else ''}" id="top">
<h1>
    %if pager.has_prev:
    <a href="${url('gallery:main')}" class="logo">
    %endif
    <span class="logo">
        <img src="${url('app:static', path='img/logo.png')}">
    </span>
    ${metadata.title}
    %if pager.has_prev:
    </a>
    %endif
</h1>
<p>
    ${metadata.description}
</p>
<nav id="navigation" class="navigation">
    <% prefix = url('gallery:main') if pager.has_prev else '' %>
    <a href="#top">Top</a>
    %if metadata.about:
        <a href="${prefix}#about">About</a>
    %endif
    <a href="${prefix}#gallery">Gallery</a>
    %if metadata.contact:
        <a href="${prefix}#contact">Contact</a>
    %endif
</nav>
</heading>

%if not pager.has_prev and metadata.about:
    <section id="about" class="about">
    ${metadata.about | n,unicode}
    </section>
%endif

<section id="gallery" class="gallery">
<ul class="gallery-list">
    ${images.body()}
</ul>
</section>

${paging.simple_pager()}

%if metadata.contact:
    ${contact.body()}
%endif
