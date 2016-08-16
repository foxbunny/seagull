Installing Seagull
==================

Once all the prerequisites are satisfied (see :doc:requirements), you can
install Seagull itself.

Install from GitHub
-------------------

To install Seagull on your computer as a package (as opposed to creating a
local copy of the source, that is), you can install directly from the GitHub
repository of the project::

    > pip install https://github.com/foxbunny/seagull/archive/master.zip

If you need to know where it got installed, run the following command::

    > python -c 'import seagull; print(seagull.__appdir__)'
    /usr/lib/python3.5/site-packages/seagull
    # or on Windows: c:\python35\lib\site-packages\seagull

Clone the source code
---------------------

If you installed the tools for working with the source code in the
:doc:requirements section, you now get a chance to put them to use. First you
will need to clone the Git repository::

    > git clone https://github.com/foxbunny/seagull.git
    Cloning into 'seagull'...
    remote: Counting objects: 418, done.
    remote: Compressing objects: 100% (194/194), done.
    emote: Total 418 (delta 226), reused 377 (delta 185), pack-reused 0
    Receiving objects:  73% (306/418), 556.00 KiB | 260.00 KiB/s
    Receiving objects: 100% (418/418), 613.73 KiB | 260.00 KiB/s, done.
    Resolving deltas: 100% (226/226), done.
    Checking connectivity... done.
    > cd seagull
    > mkvirtualenv seagull
    Using base prefix '<path to python>'
    New python executable in <path to copy of python>
    Installing setuptools, pip, wheel...done.
    > pip install -e .
    Obtaining file://<path to cloned repository>
    Collecting bottle==0.12.9 (from seagull==1.0.dev1)
    Collecting bottle-streamline==1.0 (from seagull==1.0.dev1)
    Collecting confloader==1.1 (from seagull==1.0.dev1)
    ....
    ....
    
Later if you wish to update the source code do::

    > git reset --hard HEAD
    > git pull origin master

.. note::
    If you wish to learn more about Git, there is plenty of material on the Git
    homepage, in `the documentation section <https://git-scm.com/doc>`_,
    including introductory videos.

Verifying the install
---------------------

To verify that seagull was installed correctly, you can run this command::

    > seagull --version
    1.0.dev1
