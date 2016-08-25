"""
mkdir
-----

Creates the directory specified, including intermediate directories, if they
do not exist::

    config = {
        'mkdir': {
            'directory': 'several/intermediate/directories'
        }
    }
"""
import logging
import os


def execute_mkdir(**kwargs):
    config = kwargs.get('config')
    directory = config.get('directory')
    if not os.path.exists(directory):
        os.makedirs(directory)


def register_tasks(registry):
    registry.register_task('mkdir', execute_mkdir)
    logging.debug('mkdir task registered.')
    