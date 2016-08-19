<%doc>
    Base template
    =============

    This template lays the main sections for all the pages in a HTML 5 format.

    The following blocks are provided for override:

    - ``title``: contents of the TITLE tag
    - ``extra_head``: arbitrary content inside the HEAD
    - ``body_class``: HTML class attribute of the BODY element
    - ``pre_script``: arbitrary content between ``body`` and the script tag at
      the bottom of the BODY tag
    - ``post_script``: arbitrary content after the script tag at the bottom of
    the BODY tag.

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

<!doctype html>

<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="initial-scale=1">
        <meta name="description" content="${metadata.description}">
        <title><%block name="title"/></title>
        <link rel="stylesheet" href="${assets['css/app']}">
        <%block name="extra_head"/>
    </head>
    <body class="<%block name="body_class"/>">
        ${self.body()}
        <footer id="footer" class="footer">
            <p class="copyright">
                &copy;${metadata.copyright_range | n} ${metadata.author}.
                All rights reserved.
            </p>
        </footer>
        <%block name="pre_script"/>
        <script src="${assets['js/app']}"></script>
        <%block name="post_script"/>
    </body>
</html>
