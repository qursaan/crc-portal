#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Daemon: superclass used to implement a daemon easily
#
# Copyright (C)2009-2012, UPMC Paris Universitas
# Authors:
#   Marc-Olivier Buob <marc-olivier.buob@lip6.fr>

# see also: http://www.jejik.com/files/examples/daemon3x.py

# This is used to import the daemon package instead of the local module which is
# named identically...
from __future__ import absolute_import

from manifold.util.singleton    import Singleton
from manifold.util.log          import Log
from manifold.util.options      import Options

import atexit, os, signal, lockfile, logging, sys

class Daemon(object):
    __metaclass__ = Singleton

    DEFAULTS = {
        # Running
        "uid"                 : os.getuid(),
        "gid"                 : os.getgid(),
        "working_directory"   : "/",
        "debugmode"           : False,
        "no_daemon"           : False,
        "pid_filename"        : "/var/run/%s.pid" % Options().get_name()
    }
    
    #-------------------------------------------------------------------------
    # Checks 
    #-------------------------------------------------------------------------

    def check_python_daemon(self):
        """
        \brief Check whether python-daemon is properly installed
        \return True if everything is file, False otherwise
        """
        # http://www.python.org/dev/peps/pep-3143/    
        ret = False 
        try:
            import daemon
            getattr(daemon, "DaemonContext")
            ret = True 
        except AttributeError, e:
            print e
            # daemon and python-daemon conflict with each other
            Log.critical("Please install python-daemon instead of daemon. Remove daemon first.")
        except ImportError:
            Log.critical("Please install python-daemon - easy_install python-daemon.")
        return ret

    #------------------------------------------------------------------------
    # Initialization 
    #------------------------------------------------------------------------

    def make_handler_rsyslog(self, rsyslog_host, rsyslog_port, log_level):
        """
        \brief (Internal usage) Prepare logging via rsyslog
        \param rsyslog_host The hostname of the rsyslog server
        \param rsyslog_port The port of the rsyslog server
        \param log_level Log level
        """
        # Prepare the handler
        shandler = handlers.SysLogHandler(
            (rsyslog_host, rsyslog_port),
            facility = handlers.SysLogHandler.LOG_DAEMON
        )

        # The log file must remain open while daemonizing 
        self.files_to_keep.append(shandler.socket)
        self.prepare_handler(shandler, log_level)
        return shandler

    def make_handler_locallog(self, log_filename, log_level):
        """
        \brief (Internal usage) Prepare local logging
        \param log_filename The file in which we write the logs
        \param log_level Log level
        """
        # Create directory in which we store the log file
        log_dir = os.path.dirname(log_filename)
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except OSError, why: 
                log_error("OS error: %s" % why)

        # Prepare the handler
        shandler = logging.handlers.RotatingFileHandler(
            log_filename,
            backupCount = 0
        )

        # The log file must remain open while daemonizing 
        self.files_to_keep.append(shandler.stream)
        self.prepare_handler(shandler, log_level)
        return shandler

    def prepare_handler(self, shandler, log_level):
        """
        \brief (Internal usage)
        \param shandler Handler used to log information
        \param log_level Log level
        """
        shandler.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s %(message)s")
        shandler.setFormatter(formatter)
        self.log.addHandler(shandler)
        self.log.setLevel(getattr(logging, log_level, logging.INFO))

    def __init__(
        self,
        #daemon_name,
        terminate_callback = None
        #uid               = os.getuid(),
        #gid               = os.getgid(),
        #working_directory = "/",
        #pid_filename      = None,
        #no_daemon         = False,
        #debug             = False,
        #log               = None,        # logging.getLogger("plop")
        #rsyslog_host      = "localhost", # Pass None if no rsyslog server
        #rsyslog_port      = 514,
        #log_file          = None,
        #log_level         = logging.INFO
   ):
        """
        \brief Constructor
        \param daemon_name The name of the daemon
        \param uid UID used to run the daemon
        \param gid GID used to run the daemon
        \param working_directory Working directory used to run the daemon.
            Example: /var/lib/foo/
        \param pid_filename Absolute path of the PID file
            Example: /var/run/foo.pid
            (ignored if no_daemon == True)
        \param no_daemon Do not detach the daemon from the terminal
        \param debug Run daemon in debug mode
        \param log The logger, pass None if unused
            Example: logging.getLogger('foo'))
        \param rsyslog_host Rsyslog hostname, pass None if unused.
            If rsyslog_host is set to None, log are stored locally
        \param rsyslog_port Rsyslog port
        \param log_file Absolute path of the local log file.
            Example: /var/log/foo.log)
        \param log_level Log level
            Example: logging.INFO
        """

        # Daemon parameters
        #self.daemon_name        = daemon_name
        self.terminate_callback = terminate_callback
        #Options().uid               = uid
        #Options().gid               = gid
        #Options().working_directory = working_directory
        #self.pid_filename      = None if no_daemon else pid_filename
        #Options().no_daemon         = no_daemon
        #Options().lock_file         = None
        #Options().debug             = debug
        #self.log               = log 
        #self.rsyslog_host      = rsyslog_host
        #self.rsyslog_port      = rsyslog_port 
        #self.log_file          = log_file 
        #self.log_level         = log_level

        # Reference which file descriptors must remain opened while
        # daemonizing (for instance the file descriptor related to
        # the logger)
        self.files_to_keep = []

        # Initialize self.log (require self.files_to_keep)
        #if self.log: # for debugging by using stdout, log may be equal to None
        #    if rsyslog_host:
        #        shandler = self.make_handler_rsyslog(
        #            rsyslog_host,
        #            rsyslog_port,
        #            log_level
        #        )
        #    elif log_file:
        #        shandler = self.make_handler_locallog(
        #            log_file,
        #            log_level
        #        )

    @classmethod
    def init_options(self):
        opt = Options()

        opt.add_option(
            "--uid", dest = "uid",
            help = "UID used to run the dispatcher.",
            default = self.DEFAULTS['uid']
        )
        opt.add_option(
            "--gid", dest = "gid",
            help = "GID used to run the dispatcher.",
            default = self.DEFAULTS['gid']
        )
        opt.add_option(
            "-w", "--working-directory", dest = "working_directory",
            help = "Working directory.",
            default = self.DEFAULTS['working_directory']
        )
        opt.add_option(
            "-D", "--debugmode", action = "store_false", dest = "debugmode",
            help = "Daemon debug mode (useful for developers).",
            default = self.DEFAULTS['debugmode']
        )
        opt.add_option(
            "-n", "--no-daemon", action = "store_true", dest = "no_daemon",
            help = "Run as daemon (detach from terminal).",
            default = self.DEFAULTS["no_daemon"]
        )
        opt.add_option(
            "-i", "--pid-file", dest = "pid_filename",
            help = "Absolute path to the pid-file to use when running as daemon.",
            default = self.DEFAULTS['pid_filename']
        )

        

    #------------------------------------------------------------------------
    # Daemon stuff 
    #------------------------------------------------------------------------

    def remove_pid_file(self):
        """
        \brief Remove the pid file (internal usage)
        """
        # The lock file is implicitely released while removing the pid file
        Log.debug("Removing %s" % Options().pid_filename)
        if os.path.exists(Options().pid_filename) == True:
            os.remove(Options().pid_filename)

    def make_pid_file(self):
        """
        \brief Create a pid file in which we store the PID of the daemon if needed 
        """
        if Options().pid_filename and Options().no_daemon == False:
            atexit.register(self.remove_pid_file)
            file(Options().pid_filename, "w+").write("%s\n" % str(os.getpid()))

    def get_pid_from_pid_file(self):
        """
        \brief Retrieve the PID of the daemon thanks to the pid file.
        \return None if the pid file is not readable or does not exists
        """
        pid = None
        if Options().pid_filename:
            try:
                f_pid = file(Options().pid_filename, "r")
                pid = int(f_pid.read().strip())
                f_pid.close()
            except IOError:
                pid = None
        return pid

    def make_lock_file(self):
        """
        \brief Prepare the lock file required to manage the pid file
            Initialize Options().lock_file
        """
        if Options().pid_filename and Options().no_daemon == False:
            Log.debug("Daemonizing using pid file '%s'" % Options().pid_filename)
            Options().lock_file = lockfile.FileLock(Options().pid_filename)
            if Options().lock_file.is_locked() == True:
                log_error("'%s' is already running ('%s' is locked)." % (Options().get_name(), Options().pid_filename))
                self.terminate()
            Options().lock_file.acquire()
        else:
            Options().lock_file = None

    def start(self):
        """
        \brief Start the daemon
        """
        # Check whether daemon module is properly installed
        if self.check_python_daemon() == False:
            self.terminate()
        import daemon

        # Prepare Options().lock_file
        self.make_lock_file()

        # Prepare the daemon context
        dcontext = daemon.DaemonContext(
            detach_process     = (not Options().no_daemon),
            working_directory  = Options().working_directory,
            pidfile            = Options().lock_file if not Options().no_daemon else None,
            stdin              = sys.stdin,
            stdout             = sys.stdout,
            stderr             = sys.stderr,
            uid                = Options().uid,
            gid                = Options().gid,
            files_preserve     = Log().files_to_keep
        )

        # Prepare signal handling to stop properly if the daemon is killed 
        # Note that signal.SIGKILL can't be handled:
        # http://crunchtools.com/unixlinux-signals-101/
        dcontext.signal_map = {
            signal.SIGTERM : self.signal_handler,
            signal.SIGQUIT : self.signal_handler,
            signal.SIGINT  : self.signal_handler
        }

        if Options().debugmode == True:
            self.main()
        else:
            with dcontext:
                self.make_pid_file()
                try:
                    self.main()
                except Exception, why:
                    Log.error("Unhandled exception in start: %s" % why)

    def signal_handler(self, signal_id, frame):
        """
        \brief Stop the daemon (signal handler)
            The lockfile is implicitly released by the daemon package
        \param signal_id The integer identifying the signal
            (see also "man 7 signal")
            Example: 15 if the received signal is signal.SIGTERM
        \param frame
        """
        self.terminate()

    def stop(self):
        Log.debug("Stopping '%s'" % self.daemon_name)

    def terminate(self):
        if self.terminate_callback:
            self.terminate_callback()
        else:
            sys.exit(0)

Daemon.init_options()
