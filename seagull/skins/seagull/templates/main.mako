<!doctype html>

<html lang="en">
    <head>
        <title>Seagull photo gallery</title>
        <link rel="stylesheet" href="${assets['css/app']}">
    </head>
    <body>
        %for entry in pager:
            <img src="${url('gallery:image', path=gallery.get_urlpath(entry))}">
        %endfor
        %if pager.has_prev:
            <a href="${url('gallery:main', page=pager.prev_page)}">previous</a>
        %endif
        %if pager.has_next:
            <a href="${url('gallery:main', page=pager.next_page)}">next</a>
        %endif
        <p>Nothing to see here.</p>
        <script src="${assets['js/app']}"></script>
    </body>
</html>
