Software requirements
=====================

In order to run Seagull on your machine, you will need to have a bunch of
programs installed that Seagull depends on. Some of these programs are for
running Seagull itself, some are for developing the skins. This section is
divided into subsections so you can skip the parts you do not need at this
time. You must, however, cover the Basics_ section.

Basics
------

At absolute minimum you will need to have Python 3.5 or newer installed.
Seagull specifically uses features that were newly introduced in Python 3.5, so
older versions will not work (not even older versions in the 3.x series). 

If you are on Linux, you should use your distro's package manager to install
Python. In some distributions (e.g., Arch Linux), the default ``python``
package is Python 3.x. On other distros, default is usually Python 2.x so the
Python 3.x will use a package named ``python3`` or something along those lines.

Windows and Mac users can peruse the `download page on python.org
<https://www.python.org/downloads/>`_.

Once Python is installed, check that you have the correct version. Run the
following command in the command line (command prompt)::

    > python --version
    Python 3.5.2

In some instances, you may need to refer to Python 3.5 as ``python3`` or even
``python3.5`` in the command line::

    > python3 --version
    Python 3.5.2

Throughout the rest of the guide, when you see ``python`` in the command
examples, you will use the command name that worked for you, be it ``python``
or ``python3`` (and the same applies to ``pip`` as you will see later on).

.. note::
    If your Linux distro does not ship the latest and greatest version, you
    will need to figure out a way to get the latest version. For older releases
    of Ubuntu, for example, follow `this advice
    <http://askubuntu.com/a/682875/189682>`_. Debian has Python 3.5 `in the
    unstable branch <https://packages.debian.org/sid/python3.5>`_. If you are
    going to eventually deploy Seagull yourself, it would probably be
    worthwhile to explore these upgrades now.

If your Python install does not come with `pip
<https://pip.pypa.io/en/stable/>`_, the Python package manager, you will also
need to `install pip <https://pip.pypa.io/en/stable/installing/>`_.  The
version of the pip package is not critical for using Seagull but asking for its
version is a good way to test if it's installed::

    > pip --version
    pip 8.1.2 from ..... (python 3.5)

Make sure that it says 'python 3.5' in the result. If it says something like
'python 2.7' or any version other than 3.5, then you probably installed pip for
the wrong version of Python. For example, on Linux, pip for Python 3.5 would be
in a package named ``python3-pip`` or something similar. In some cases, the
command itself may be different (e.g., ``pip3`` instead of ``pip``).

Software needed for skin development
------------------------------------

If you intend to customize the built-in skins (but not strictly required if you
just want to create a completely new skin), you will also need:

- NodeJS and NPM for `CoffeeScript <http://coffeescript.org/>`_ support (see
  `this guide <https://docs.npmjs.com/getting-started/installing-node>`_)
- Ruby and Ruby Gems for `Compass <http://compass-style.org/>`_ support (see
  `this guide <http://www.ruby-lang.org/en/documentation/installation/>`_)

To verify the installs::

    > npm --version
    3.10.3

    > gem --version
    2.5.1

Exact versions are not really important here. Once you have NodeJS, NPM, Ruby,
and Ruby Gems installed, you will need to install CoffeeScript and Compass. To
install CoffeeScript with NPM, run this command::

    > npm install --global coffee-script

Next install Compass using Ruby Gem::

    > gem install compass

You probably want to verify that these tools were installed correctly::

    > coffee --version
    CoffeeScript version 1.10.0

    > compass --version
    Compass 1.0.3 (Polaris)
    Copyright (c) 2008-2016 Chris Eppstein
    Released under the MIT License.
    Compass is charityware.
    Please make a tax deductable donation for a worthy cause: http://umdf.org/compass

Tools for working on the documentation
--------------------------------------

If you wish to hack at this guide, you will need to install Sphinx and the
ReadTheDocs theme for Sphinx::

    > pip install sphinx sphinx-rtd-theme

To verify that Sphinx was installed::

    > sphinx-build --version
    Sphinx (sphinx-build) 1.4.5

Tools for working with the source code
--------------------------------------

The Seagull source code can always be browsed through `on GitHub
<https://github.com/foxbunny/seagull>`_, so making a local copy of the source
code and tracking it is not strictly necessary. If you still wish to give it a
try, here are the tools you will need:

- `Git <https://git-scm.com/downloads>`_
- `virtualenvwrapper
  <http://virtualenvwrapper.readthedocs.io/en/latest/install.html>`_
