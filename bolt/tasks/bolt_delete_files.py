"""
.. _task-delete-files:

delete-files
------------

This task deletes files matching a specified ``pattern`` found in a specified
``sourcedir``. A ``recursive`` flag can be specified to search also in 
sub-directories of ``sourcedir``.

The ``pattern`` specified follows the matching rules of the |python|_ standard
library ``glob.glob()`` function.

The following example configures the ``delete-file`` task to delete all the
files in a ``tmp`` directory located at the project root, and all its
sub-directories::

    config = {
        'delete-files': {
            'sourcedir': './tmp',
            'pattern': '*.*',
            'recursive': True
        }
    }

The ``sourcedir`` configuration option indicates the directory to search for
file matches. This option is required.

The ``pattern`` option specifies the matching pattern to find files. This
option is required.

The ``recursive`` option indicates if sub-directories should be searched for
matches. This option is optional and has a value of ``False`` by default.


.. _task-delete-pyc:

delete-pyc
----------

Searches for ``.pyc`` in the specified directory and deletes them. The task
allows to recursively search sub-directories for ``.pyc`` files.

The following example shows how to configure the task to recursively delete
files from a source directory and its sub-directories::

    config = {
        'delete-pyc': {
            'sourcedir': './source',
            'recursive': True
        }
    }

The ``sourcedir`` option specifies the directory to search for ``.pyc`` files.
This option is required.

The ``recursive`` option indicates if sub-directories should be searched for
matches. This option is optional and has a value of ``False`` by default. 
"""
import glob
import logging
import os

import bolt.errors as bterrors
import bolt.utils as utilities

class DeleteFilesTask(object):

    def __call__(self, **kwargs):
        self._set_valid_configuration(kwargs.get('config'))
        self._execute_delete()


    def _set_valid_configuration(self, config):
        if not config:
            raise bterrors.InvalidConfigurationError('Configuration cannot be empty')
        self.sourcedir = config.get('sourcedir')
        if not self.sourcedir:
            raise bterrors.InvalidConfigurationError('Source directory not specified')
        self.pattern = config.get('pattern')
        if not self.pattern:
            raise bterrors.InvalidConfigurationError('File pattern not specified')
        self.recursive = config.get('recursive')


    def _execute_delete(self):
        logging.info('Deleting {pat} from {srcdir}.'.format(pat=self.pattern, srcdir=self.sourcedir))
        finder = utilities.FileFinder(self.sourcedir, self.pattern, self.recursive)
        matches = finder.find()
        utilities.delete_files_in(matches)



class DeletePycTask(DeleteFilesTask):

    def __call__(self, **kwargs):
        config = kwargs.get('config')
        config['pattern'] = '*.pyc'
        logging.debug('Delete pattern set to ' + config['pattern'])
        return super(DeletePycTask, self).__call__(**kwargs)



def register_tasks(registry):
    registry.register_task('delete-files', DeleteFilesTask())
    registry.register_task('delete-pyc', DeletePycTask())   

