"""
This is the main module that exposes the required functions to use bolt in your applications.
"""
import argparse
import os
import sys


from _bterror import InvalidTask
from _btregistry import TaskRegistry

_registry = TaskRegistry()

def register_module_tasks(module):
    """
    """
    module.register_tasks(_registry)


def register_task(name, task):
    """
    """
    _registry.register_task(name, task)


def run():
    """
    Entry point for the `bolt` executable.

    :return: 0 if the application succeeds or a non-zero value otherwise.
    """
    try:
        _run_bolt()
    except Exception as e:
        print e
        return 1
    return 0


def _run_bolt():
    args = _get_arguments()
    print args


def _get_arguments():
    parser = _get_argument_parser()
    return parser.parse_args()


def _get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('task', nargs='?', default='default')
    parser.add_argument('--bolt-file', default='boltfile.py')
    return parser
