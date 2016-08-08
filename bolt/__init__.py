"""
This is the main module that exposes the required functions to use bolt in your applications.
"""
import argparse
import logging
import os
import sys

import bolt.tasks
from bolt._btconfig import ConfigurationManager
from bolt._bterror import *
from bolt._btregistry import TaskRegistry
from bolt._btrunner import TaskRunner
from bolt._btutils import load_script

# Standard task modules.
import bolt.tasks.bolt_pip as bolt_pip
import bolt.tasks.bolt_delete_files as bolt_delete_files
import bolt.tasks.bolt_setup as bolt_setup
import bolt.tasks.bolt_shell as bolt_shell
import bolt.tasks.bolt_conttest as bolt_conttest

def _register_standard_modules(registry):
    bolt_delete_files.register_tasks(registry)
    bolt_pip.register_tasks(registry)
    bolt_setup.register_tasks(registry)
    bolt_shell.register_tasks(registry)
    bolt_conttest.register_tasks(registry)


class _BoltApplication(object):

    def __init__(self):
        self._registry = TaskRegistry()
        self._config_mgr = None


    @property
    def registry(self):
        return self._registry


    @property
    def config_manager(self):
        return self._config_mgr

    def run(self):
        self._initialize_execution_options()
        self._initialize_logging()
        logging.info("Current working directory: " + os.getcwd())
        self._register_standard_modules()
        self._load_bolt_file()
        self._initialize_configuration_manager()
        self._run_main_task()


    def run_task(self, task_name):
        runner = TaskRunner(self.config_manager, self.registry)
        runner.build(task_name)
        runner.run()


    def _register_standard_modules(self):
        logging.debug('Registering standard task modules')
        _register_standard_modules(self.registry)


    def _initialize_execution_options(self):
        parser = self._get_argument_parser()
        self._options = parser.parse_args()


    def _initialize_logging(self):
        logger = logging.getLogger()
        level = self._get_log_level()
        logger.setLevel(level)

        # Console logging
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # File logging if specified.
        log_file = self._options.log_file 
        if log_file:
            handler = logging.FileHandler(log_file, 'w')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)


    def _get_log_level(self):
        log_level_arg = self._options.log_level.lower()
        if log_level_arg == 'debug': return logging.DEBUG
        elif log_level_arg == 'info': return logging.INFO
        elif log_level_arg == 'warning': return logging.WARNING
        elif log_level_arg == 'error': return logging.ERROR
        elif log_level_arg == 'critical': return logging.CRITICAL
        else: return logging.INFO



    def _get_argument_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('task', nargs='?', default='default')
        parser.add_argument('--bolt-file', default='boltfile.py')
        parser.add_argument('--log-level', default='info')
        parser.add_argument('--log-file', default=None)
        return parser


    def _load_bolt_file(self):
        bolt_file_name = self._options.bolt_file
        bolt_script = os.path.abspath(bolt_file_name)
        logging.debug('Loading {bolt_file}'.format(bolt_file=bolt_script))
        self._boltmodule = load_script(bolt_script)

    def _initialize_configuration_manager(self):
        self._config_mgr = ConfigurationManager(self._boltmodule.config)


    def _run_main_task(self):
        self.run_task(self._options.task)


_bolt_application = _BoltApplication()


def register_module_tasks(module):
    """
    """
    module.register_tasks(_bolt_application.registry)


def register_task(name, task):
    """
    """
    _bolt_application.registry.register_task(name, task)


def run_task(task_name):
    _bolt_application.run_task(task_name)


def run():
    """
    Entry point for the `bolt` executable.
    """
    try:
        _bolt_application.run()
    except Exception as e:
        logging.exception(e)
        sys.exit(1)
    sys.exit(0)


