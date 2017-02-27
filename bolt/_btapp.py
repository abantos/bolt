"""
"""
import logging
import os.path

import bolt._btconfig as btconfig
import bolt._btoptions as btoptions
import bolt._btregistry as btregistry
import bolt._btrunner as btrunner
from bolt._btutils import load_script

# Standard task modules.
import bolt.tasks.bolt_pip as bolt_pip
import bolt.tasks.bolt_delete_files as bolt_delete_files
import bolt.tasks.bolt_setup as bolt_setup
import bolt.tasks.bolt_shell as bolt_shell
import bolt.tasks.bolt_conttest as bolt_conttest
import bolt.tasks.bolt_nose as bolt_nose
import bolt.tasks.bolt_mkdir as bolt_mkdir 
import bolt.tasks.bolt_coverage as bolt_coverage
import bolt.tasks.bolt_sleep as bolt_sleep


class BoltApplication(object):
    """
    """

    def __init__(self, options=None, registry=None, config_manager=None):
        self._options = options or self._get_default_options()
        self._registry = registry or self._get_default_registry()
        self._config_manager = config_manager
        self._register_standard_tasks()


    @property
    def config_manager(self):
        """
        """
        return self._config_manager

    
    @property
    def options(self):
        """
        """
        return self._options


    @property
    def registry(self):
        """
        """
        return self._registry


    def run(self):
        """
        """
        self.run_task(self.options.task)


    def run_task(self, task_name, continue_on_error=None):
        """
        """
        continue_on_error = continue_on_error or self.options.continue_on_error
        if not self._config_manager:
            self._config_manager = self._get_default_config_manager()
        runner = btrunner.TaskRunner(self.config_manager, self.registry, continue_on_error)
        try:
            runner.run(task_name)
        finally:
            runner.tear_down()


    def _get_default_options(self):
        return btoptions.Options()


    def _get_default_registry(self):
        return btregistry.TaskRegistry()


    def _get_default_config_manager(self):
        bf = BoltFile(self.options.bolt_file)
        return btconfig.ConfigurationManager(bf.config)


    def _register_standard_tasks(self):
        self.registry.register_module_tasks(bolt_conttest)
        self.registry.register_module_tasks(bolt_coverage)
        self.registry.register_module_tasks(bolt_delete_files)
        self.registry.register_module_tasks(bolt_mkdir)
        self.registry.register_module_tasks(bolt_nose)
        self.registry.register_module_tasks(bolt_pip)
        self.registry.register_module_tasks(bolt_setup)
        self.registry.register_module_tasks(bolt_shell)
        self.registry.register_module_tasks(bolt_sleep)


    def _register_module(self, module):
        module.register_tasks(self.registry)



class BoltFile(object):
    """
    """
    
    def __init__(self, bolt_file_name):
        self.filename = os.path.abspath(bolt_file_name)
        self._bolt_file_module = self._load()


    def _load(self):
        return load_script(self.filename)


    @property
    def config(self):
        """
        """
        return self._bolt_file_module.config


_application_instance = None

def get_application(options=None):
    global _application_instance
    if not _application_instance:
        _application_instance = BoltApplication(options=options)
    return _application_instance

