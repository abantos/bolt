"""
conttest
--------

This task uses ``conttest`` to monitor a directory for changes and executes the specified
task everytime a change is made. The following configuration is supported::

    config = {
        'conttest': {
            'task': 'registered_task',
            'directory': './directory/to/monitor/'
        }
    }

The ``task`` parameter is the task to be executed and must be registered in ``boltfile.py``.
The ``directory`` parameter is the directory (including sub-directories) to monitor for 
changes.

To use this task, you need to have ``conttest`` installed, which you can do by calling::

    pip install conttest
"""
import logging
import os

import bolt 
import bolt.api as api


class ExecuteConttest(api.Task):
    
    def _configure(self):
        self.task_name = self._require('task')
        self.directory = self._optional('directory', os.getcwd())
        self.continue_on_error = True
        logging.info('Executing continously "{task}" at {directory}'.format(task=self.task_name, directory=self.directory))



    def _execute(self):
        import conttest.conttest as ct
        try:
            ct.watch_dir(self.directory, self._execute_assigned_task, method=ct.TIMES)
        except KeyboardInterrupt:
            logging.info('Exiting continuous execution')


    def _execute_assigned_task(self):
        bolt.run_task(self.task_name, self.continue_on_error)
        logging.info('Press <ctrl+c> to exit')



def register_tasks(registry):
    registry.register_task('conttest', ExecuteConttest())
