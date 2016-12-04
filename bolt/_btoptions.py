"""
Exposes classes related to the supported options for Bolt.
"""
import argparse
import logging

class Commands(object):
    """
    Defines the supported commands.
    """
    EXECUTE = 'execute'
    HELP = 'help'
    VERSION = 'version'


class Default(object):
    """
    Defines default values for options.
    """
    COMMAND = Commands.EXECUTE
    TASK = 'default'
    BOLTFILE = 'boltfile.py'
    LOG_LEVEL = logging.INFO
    LOG_FILE = None
    CONTINUE_ON_ERROR = False


class OptionSwitch(object):
    """
    Defines values for the command line switches.
    """
    TASK = 'task'
    BOLTFILE_SHORT = '-b'
    BOLTFILE_LONG = '--bolt-file'
    LOG_LEVEL_SHORT = '-v'
    LOG_LEVEL_LONG = '--log-level'
    LOG_FILE_SHORT = '-o'
    LOG_FILE_LONG = '--log-file'
    CONTINUE_ON_ERROR_LONG = '--continue-on-error'
    VERSION_LONG = '--version'



class Options(object):
    """
    Exposes application options that are initialized from the command line or
    by specifying a parameters list. 
    """

    def __init__(self, opt_list=None):
        self._command = Commands.EXECUTE
        self._initialize_options(opt_list)
    
    @property
    def command(self):
        """
        Returns the command to be executed.
        """
        return self._command


    @property
    def task(self):
        """
        Returns the task to be executed or the default task if none specified.
        """
        return self._options.task


    @property
    def bolt_file(self):
        """
        Returns the bolt file to use or the default bolt file if none specified.
        """
        return self._options.bolt_file


    @property
    def log_level(self):
        """
        Returns the log level to use or the default log level if none specified.
        """
        return self._options.log_level


    @property
    def log_file(self):
        """
        Returns the log file to use or None if no file is specified.
        """
        return self._options.log_file


    @property
    def continue_on_error(self):
        """
        Returns whether to continue executing tasks when errors are found. The
        default is false.
        """
        return self._options.continue_on_error


    def _initialize_options(self, opt_list=None):
        parser = self._build_parser()
        self._options = parser.parse_args(opt_list)
        self._marshall_options()


    def _build_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(OptionSwitch.TASK, nargs='?', default=Default.TASK, 
            help='Task to be executed. It uses "default" if not specified')
        parser.add_argument(OptionSwitch.BOLTFILE_SHORT, OptionSwitch.BOLTFILE_LONG, default=Default.BOLTFILE,
            help='Bolt file containing the configuration and task. The default is "boltfile.py"')
        parser.add_argument(OptionSwitch.LOG_LEVEL_SHORT, OptionSwitch.LOG_LEVEL_LONG, default=Default.LOG_LEVEL,
            help='Specifies logging level.')
        parser.add_argument(OptionSwitch.LOG_FILE_SHORT, OptionSwitch.LOG_FILE_LONG, default=None, 
            help='Log file to write the output.')
        parser.add_argument(OptionSwitch.CONTINUE_ON_ERROR_LONG, action='store_true', 
            help='Continue executing even if errors are found')
        parser.add_argument(OptionSwitch.VERSION_LONG, action='store_true',
            help='Shows the the application version')
        return parser


    def _marshall_options(self):
        self._marshall_command()
        self._marshall_log_level()


    def _marshall_command(self):
        if self._options.version:
            self._command = Commands.VERSION


    def _marshall_log_level(self):
        if self._options.log_level == Default.LOG_LEVEL:
            return
        lc_level = self._options.log_level.lower()
        if lc_level in ['', 'n', 'notset']:
            self._options.log_level = logging.NOTSET
        elif lc_level in ['debug', 'd', 'dbg']:
            self._options.log_level = logging.DEBUG
        elif lc_level in ['info', 'i', 'information']:
            self._options.log_level = logging.INFO
        elif lc_level in ['warning', 'warn', 'w']:
            self._options.log_level = logging.WARNING
        elif lc_level in ['error', 'err', 'e']:
            self._options.log_level = logging.ERROR
        elif lc_level in ['critical', 'crit', 'c']:
            self._options.log_level = logging.CRITICAL

        