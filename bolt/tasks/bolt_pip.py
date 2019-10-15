"""
.. _task-pip:

pip
---

The ``pip`` task provides an automation hook to execute ``pip`` inside of
Bolt. In its simplest form, the task does not require any configuration,
and it just assumes a ``requirements.txt`` file is provided at the 
current working directory, which will be used to execute a ``pip install``.

The task also provides a simple form where a ``command`` and ``package``
are specified to allow install a single package. ::

    config = {
        'pip': {
            'command': 'install',
            'package': 'package_name'
        }
    }

The supported ``pip`` functionality can be configured by setting the
``command`` option to a valid ``pip`` command, and providing a set of
arguments to ``pip`` as an ``options`` dictionary where the keys are
valid ``pip`` arguments in short or long form without leading dashes
and the values are the respective argument values, or ``True`` in the
case of flags. The following shows a more advance use of this task. ::

    config = {
        'pip': {
            'command': 'install',
            'options': {
                'r': './data/project_requirements.txt',
                'target': './requirements',
                'upgrade': True,
                'force-reinstall': True
            }
        }
    }

"""
import logging
import subprocess

import bolt.api as api
import bolt.utils as utilities

DEFAULT_COMMAND = 'install'
DEFAULT_REQUIREMENTS_FILE = 'requirements.txt'
DEFAULT_ARGUMENTS = [DEFAULT_COMMAND, '-r', DEFAULT_REQUIREMENTS_FILE]


class ExecutePipTask(api.Task):
    
    def _configure(self):
        generator = _PipArgumentGenerator()
        self.args = generator.generate_from(self.config)
        logging.debug('Arguments: ' + repr(self.args))


    def _execute(self):
    
        result_code = self._execute_pip()
        if result_code != 0:
            raise PipError(result_code)
        return 0


    def _execute_pip(self):
        command = ['pip']
        command.extend(self.args)
        return subprocess.call(command)



def register_tasks(registry):
    registry.register_task('pip', ExecutePipTask())



class _PipArgumentGenerator(utilities.CommonCommandAndArgumentsGenerator):


    def __init__(self):
        return super(_PipArgumentGenerator, self).__init__(DEFAULT_ARGUMENTS)


    def _convert_config_to_arguments(self):
        self.command = self.config.get('command')
        self.package = self.config.get('package')
        if self._installing_single_package:
            self.args = [DEFAULT_COMMAND, self.package]
        else:
            super(_PipArgumentGenerator, self)._convert_config_to_arguments()
            

    @property
    def _installing_single_package(self):
        return self.command == DEFAULT_COMMAND and self.package



class PipError(api.TaskFailedError):

    def __init__(self, pip_code):
        super(PipError, self).__init__(pip_code)


    def __repr__(self):
        return 'PipError({code})'.format(code=self.code)
    