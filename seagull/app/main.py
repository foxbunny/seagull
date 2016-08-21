#
# Seagull photo gallery app
# Copyright (C) 2016  Hajime Yamasaki Vukelic
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#

import os
import sys
import signal
import logging
import importlib

import bottle
import gevent
import confloader
import gevent.pywsgi

from .. import __appdir__, __version__
from ..routes import ROUTES
from . import (
    logger,
    skinning,
    templating,
    assets,
    gallery,
    metadata,
    commands,
)

try:
    import pwd, grp
except ImportError:
    has_user = False
else:
    has_user = True


class App:
    READ = 'r'
    WRITE = 'a+'
    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = 8080
    LOOP_INTERVAL = 10

    def __init__(self):
        self.app = bottle.Bottle()
        self.conf = confloader.ConfDict({
            'runtime.appdir': __appdir__,
            'runtime.version': __version__,
            'runtime.work_dir': os.getcwd(),
            'runtime.initialize_hooks': [],
            'runtime.start_hooks': [],
        })

        # Commands fire as soon as possible
        commands.parse_args(self.conf)

        # Runtime config
        self.child = False
        self.running = False
        self.quiet = self.conf.pop('runtime.quiet')
        self.background = self.conf.pop('runtime.background')
        self.pid_file = self.conf.pop('runtime.pid_file')
        self.user = self.conf.pop('runtime.user')
        self.group = self.conf.pop('runtime.group')
        self.debug = self.conf['runtime.debug']
        bottle.debug(self.debug)

        # Hooks
        self.initialize_hooks = self.conf.pop('runtime.initialize_hooks')
        self.start_hooks = self.conf.pop('runtime.start_hooks')

        # Runtime params
        self.server = None
        self.host = None
        self.port = None

        self.template_defaults = {
            'request': bottle.request,
            'url': self.app.get_url,
        }
        self.conf['runtime.template_defaults'] = self.template_defaults

        # Set up logger
        logger.configure(self.conf, self.quiet)

        for hook in self.initialize_hooks:
            hook(self.conf)

    def fork(self):
        """
        Attempt to fork the current process

        Raises ``RuntimeError`` if the fork is not successful.
        """
        try:
            pid = os.fork()
        except OSError:
            raise RuntimeError('process failed to fork')
        if pid == 0:
            if not self.child:
                os.setsid()
        else:
            os._exit(0)
        return pid

    def setuid(self):
        """
        Set user and group ID of the process

        If ``self.group`` is not defined, then this method uses the group ID of
        the ``self.user``.

        Returns a tuple containing the active user and group IDs.
        """
        if not has_user:
            logging.warn('User switching is disabled on this OS')
            return
        logging.debug('Setting process UID and GID')
        pwinfo = pwd.getpwnam(self.user)
        uid = pwinfo.pw_uid
        os.setuid(uid)
        os.seteuid(uid)
        if self.group:
            logging.debug('Using specified group for GID')
            gid = grp.getgrpnam(self.group).grp_gid
        else:
            logging.debug('Using specified user for GID')
            gid = pwinfo.pw_gid
        os.setgid(gid)
        os.setegid(gid)
        logging.debug('Process UID=%s and GID=%s', uid, gid)
        return uid, gid

    def redirect(self, fd, path, mode=WRITE):
        """
        Redirect a file descriptor ``fd`` to specified path

        This method is normally used with ``sys.stderr`` and similar file
        descriptors.

        This function has no return value.
        """
        fd2 = open(path, mode)
        os.dup2(fd2.fileno(), fd.fileno())

    def daemonize(self):
        """
        Background the process in which the app instance is initialized

        This method converts the process to which this instance belongs, to a
        double-forking daemon.

        This method returns the current PID of the forked child process.
        """
        logging.info('Forking into background')
        # Fork once
        try:
            self.fork()
        except RuntimeError:
            logging.critical('Could not fork the process')
            sys.exit(1)
        logging.debug('Started child process')
        self.child = True
        # Set up the process environment
        os.chdir(os.path.normpath(self.work_dir))
        os.umask(0)
        # Fork second time
        try:
            self.fork()
        except RuntimeError:
            logging.critical('Could not double-fork the process')
            sys.exit(1)
        logging.debug('Running as daemon (PID={})'.format(os.getpid()))
        # Write the PID as needed
        if self.pid_file:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
            logging.debug('PID file written to %s', self.pid_file)
        # Switch to unprivileged user
        if self.user:
            self.setuid()

    def load_conf(self):
        """
        Load the configuration file
        """
        self.conf = confloader.ConfDict.from_file(self.conf_file)

    def prepare_app(self, skip_server_init=False):
        """
        Prepare the application for start
        """
        logging.info('Preparing application to run')
        if not skip_server_init:
            self.host = self.conf.get('http.host', self.DEFAULT_HOST)
            self.port = self.conf.get('http.port', self.DEFAULT_PORT)
            self.server = gevent.pywsgi.WSGIServer(
                (self.host, self.port), self.app, log=None)
        self.app.config = self.conf
        self.app.config.update({
            'catchall': self.debug,
            'autojson': False,
        })
        skinning.configure(self.conf)
        templating.configure(self.conf)
        gallery.configure(self.conf)
        assets.configure(self.conf)
        metadata.configure(self.conf)

    def prepare_routes(self):
        for route in ROUTES:
            route.route(app=self.app)
            logging.debug('Route %s mapped to %s', route.get_name(),
                          route.path)

    def stop_app(self):
        self.server.stop(self.LOOP_INTERVAL)
        self.running = False
        logging.info('Server stopped')

    def start_app(self):
        self.prepare_app()
        self.prepare_routes()

        for hook in self.start_hooks:
            hook(self.conf)

        self.server.start()
        if not self.server.started:
            logging.critical('Failed to start server')
            sys.exit(0)
        self.running = True
        logging.info('Server started on http://%s:%s/', self.host, self.port)
        print('Server started on http://{}:{}/'.format(
            self.host, self.port))

    def onhup(self, signum, exc):
        """
        Reload the configuration and restart the server
        """
        self.load_conf()
        logging.info('Configuration reloaded')
        self.prepare_app(skip_server_init=True)

    def onhalt(self, signum, exc):
        """
        Generic signal handler
        """
        self.stop_app()
        if os.path.exists(self.pid_file):
            os.unlink(self.pid_file)

    onint = onhalt
    onterm = onhalt

    def handle_signals(self):
        """
        Set up signal handling
        """
        if hasattr(signal, 'SIGHUP'):
            logging.debug('Registering SIGHUP handler')
            signal.signal(signal.SIGHUP, self.onhup)
        if hasattr(signal, 'SIGINT'):
            logging.debug('Registering SIGINT handler')
            signal.signal(signal.SIGINT, self.onint)
        if hasattr(signal, 'SIGTERM'):
            logging.debug('Registering SIGTERM handler')
            signal.signal(signal.SIGTERM, self.onterm)

    def start(self):
        """
        Start the manager
        """
        logging.info('Starting Seagull')
        if self.background:
            self.daemonize()
        self.handle_signals()
        self.start_app()
        self.loop()

    def loop(self):
        while self.running:
            gevent.sleep(self.LOOP_INTERVAL)

    @staticmethod
    def import_object(name):
        """
        Import an object given fully qualified name.

        For a name 'foo.bar.baz', this is equivalent to::

            from foo.bar import baz

        """
        try:
            mod, obj = name.rsplit('.', 1)
        except ValueError:
            raise ImportError('Cannot import name {}'.format(name))
        mod = importlib.import_module(mod)
        try:
            return getattr(mod, obj)
        except AttributeError:
            raise ImportError('Cannot import name {}'.format(name))
