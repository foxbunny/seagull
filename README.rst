=======
Seagull
=======

Photography folio site w/ FTP support.

Skins: organization of static assets and templates
==================================================

Static assets and templates are organized into skins. Skin is a directory
structure that contains the assets and templates and has a name that can be
referred to by the application and its tooling.

Skins are normally found in ``seagull/skins`` directory. Each skin directory
contains the following structure::

    skin_dir/
        assets/
            css/
            js/
            img/
            font/
        templates/
        src/
            coffee/
            scss/

The ``assets`` directory contains the compiled CSS, JavaScript, images, and
fonts. The assets are compiled from the sources found in the ``src`` directory.
Compiling the assets from sources is optional, and not a requirement for a
valid skin. The templates are found in the ``templates`` directory.

Compiling static assets
=======================

The makefile provided in the source tree can be used to compile assets for the
skins that are found in the ``seagull/skins`` directory. The following make
targets can be used to work with the assets:

==================  ===========================================================
make [start]        Start Compass and CoffeeScript watchers
------------------  -----------------------------------------------------------
make stop           Stop the watchers
------------------  -----------------------------------------------------------
make recompile      One-time recompile of all assets
==================  ===========================================================
