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


class ExecuteMKDir(object):
    

    def __call__(self, **kwargs):
        config = kwargs.get('config')
        self.directory = config.get('directory')
        logging.debug('Creating directory: {directory}'.format(directory=self.directory))
        if not os.path.exists(self.directory):
            self._create_directories()


    def _create_directories(self):
        os.makedirs(self.directory)


def register_tasks(registry):
    registry.register_task('mkdir', ExecuteMKDir())
    