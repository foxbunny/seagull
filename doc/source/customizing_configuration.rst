Customizing the configuration
=============================

Although there are many configuration settings in the default configuration
file that comes with Seagull, we normally only need to change a few things. In
this section, we will gloss over the process of creating a custom configuration
file, and change the password. Configuration will be covered in more detail in
the deployment section later on.

Creating the custom configuration file
--------------------------------------

The ``seagull`` command we have been using has a shortcut for creating our own
configuration file. Let's try it::

    > seagull custom-conf mygull.ini

Now let's open the file in an editor. The contents look like this::

    [config]

    defaults =
      /usr/lib/python3.5/site-packages/seagull/seagull.ini

    [seagull]

    # Add your settings below this line

The part that says ``/usr/lib/python3.5/...`` is going to be different
depending on what operating system you are on, and where Seagull is installed,
but it always points to the default configuration file.

.. note::
    Any setting that appears in the default configuration file can be
    overridden by your custom configuration file. You just need to make sure
    the appropriate section header exists in both (e.g., ``[seagull]`` in the
    above example) and that the setting you want to override is under the
    correct section.

Changing the password
---------------------

We'll use this opportunity to change the reindex password. The comment in the
default configuration file says that this password must be URL-friendly.  To
keep it simple, we'll take this to mean that we can only use letters and
numbers and dashes (in reality, there are many more characters that can be
used, but discussing the full set of rules about what can and cannot be used in
an URL is outside the scope of this tutorial). ::

    [seagull]

    # Reindexing password: asked for when using the reindex page, must be 
    # URL-friendly
    password = my-new-password

We can also change the gallery folder path using the ``gallery_dir`` setting,
but I'll leave that to you to play with. :-)

.. note::
    When modifying the settings, it's good practice to copy the comments from
    the default configuration file so you can remember what the setting does
    when you come back to it later.
