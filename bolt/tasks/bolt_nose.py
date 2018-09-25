"""
.. _task-nose:

nose
----

Executes unit tests using nose and nosetests as the unit test runner. The task
allows to specify the directory where the tests are located through the ``directory``
parameter and supports all the arguments available in the installed version 
of nosetests::

    config = {
        'nose': {
            'directory': 'test/unit',
            'options': {
                'xunit-file': 'output/unit_tests.xml'
                'with-coverage': True,
                'cover-erase': True,
                'cover-package': 'mypackage',
                'cover-html': True,
                'cover-html-dir': 'output/coverage',
            }
    }
"""
import logging
import os.path
import subprocess as sp

import bolt.api as api
import bolt.utils as utilities


DEFAULT_DIR = './'
DEFAULT_ARGUMENTS = [DEFAULT_DIR]


class ExecuteNoseTask(api.Task):
    
    def _configure(self):
        generator = _NoseArgumentGenerator()
        self.args = generator.generate_from(self.config)
        logging.debug('Arguments: ' + repr(self.args))


    def _execute(self):
        result = sp.call(self.args)
        if result != 0:
            raise NoseError(result)



def register_tasks(registry):
    registry.register_task('nose', ExecuteNoseTask())



class NoseError(api.TaskFailedError):

    def __init__(self, nose_code):
        super(NoseError, self).__init__(nose_code)


    def __repr__(self):
        return 'NoseError({code})'.format(code=self.code)



class _NoseArgumentGenerator(utilities.ArgumentsGenerator):

    def __init__(self):
        return super(_NoseArgumentGenerator, self).__init__(DEFAULT_ARGUMENTS, utilities.append_with_equal)


    def _convert_config_to_arguments(self):
        self.args.append('nosetests')
        super(_NoseArgumentGenerator, self)._convert_config_to_arguments()
        directory = self.config.get('directory') or DEFAULT_DIR
        directory = os.path.abspath(directory)
        self.args.append(directory)

