"""
"""
import glob
import os

import bolt
import bolt.utils as ut

class DeleteFilesTask(object):

    def __call__(self, **kwargs):
        self._set_valid_configuration(kwargs.get('config'))
        self._execute_delete()


    def _set_valid_configuration(self, config):
        if not config:
            raise bolt.InvalidConfigurationError('Configuration cannot be empty')
        self.sourcedir = config.get('sourcedir')
        if not self.sourcedir:
            raise bolt.InvalidConfigurationError('Source directory not specified')
        self.pattern = config.get('pattern')
        if not self.pattern:
            raise bolt.InvalidConfigurationError('File pattern not specified')
        self.recursive = config.get('recursive')


    def _execute_delete(self):
        finder = ut.FileFinder(self.sourcedir, self.pattern, self.recursive)
        matches = finder.find()
        ut.delete_files_in(matches)




def register_tasks(registry):
    registry.register_task('delete-files', DeleteFilesTask())

