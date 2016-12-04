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


class ExecuteConttest(object):

    def __call__(self, **kwargs):
        config = kwargs.get('config') 
        self.task_name = config.get('task')
        self.directory = config.get('directory') or os.getcwd()
        self.continue_on_error = True
        logging.info('Executing continously "{task}" at {directory}'.format(task=self.task_name, directory=self.directory))
        self.execute_task()


    def execute_task(self):
        import conttest.conttest as ct
        ct.watch_dir(self.directory, lambda: bolt.run_task(self.task_name, self.continue_on_error), method=ct.TIMES)



def register_tasks(registry):
    registry.register_task('conttest', ExecuteConttest())
