"""
This is the main module that exposes the required functions to use bolt in your applications.
"""
import logging
import sys

import bolt._btapp as btapp
import bolt._btoptions as btoptions
import bolt.utils.log as btlog


def register_module_tasks(module):
    """
    """
    app = btapp.get_application()
    app.registry.register_module_tasks(module)


def register_task(name, task):
    """
    """
    app = btapp.get_application()
    app.registry.register_task(name, task)


def run_task(task_name, continue_on_error=None):
    continue_on_error = continue_on_error or False
    app = btapp.get_application()
    app.run_task(task_name, continue_on_error)


def run():
    """
    Entry point for the `bolt` executable.
    """
    options = btoptions.Options()
    btlog.initialize_logging(options.log_level, options.log_file)
    app = btapp.get_application()
    app.run()

    

if __name__=="__main__":
    run()
