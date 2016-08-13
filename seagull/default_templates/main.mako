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

<%block name="title">Seagull photo gallery | page ${pager.current_page}</%block>

${images.list()}
${paging.simple_pager()}
