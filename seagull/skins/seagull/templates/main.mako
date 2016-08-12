<!doctype html>

<html lang="en">
    <head>
        <title>Seagull photo gallery</title>
        <link rel="stylesheet" href="${assets['css/app']}">
    </head>
    <body>
        %for entry in gallery:
            <img src="${url('gallery:index', path=gallery.get_urlpath(entry))}">
        %endfor
        <p>Nothing to see here.</p>
        <script src="${assets['js/app']}"></script>
    </body>
</html>
