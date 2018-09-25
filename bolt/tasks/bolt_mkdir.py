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

import bolt.api as api


class ExecuteMKDir(api.Task):
    
    def _configure(self):
        self.directory = self._require('directory')
        logging.debug('Creating directory: {directory}'.format(directory=self.directory))


    def _execute(self):
        if not os.path.exists(self.directory):
            self._create_directories()


    def _create_directories(self):
        os.makedirs(self.directory)


def register_tasks(registry):
    registry.register_task('mkdir', ExecuteMKDir())
    