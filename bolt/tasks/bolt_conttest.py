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
import bolt 




def execute_conttest(**kwargs):
    import conttest.conttest as ct
    config = kwargs.get('config')
    task_name = config.get('task')
    directory = config.get('directory') or './'
    logging.info('Executing continously "{task}" at {directory}'.format(task=task_name, directory=directory))
    continue_on_error = True
    ct.watch_dir(directory, lambda: bolt.run_task(task_name, continue_on_error), method=ct.TIMES)



def register_tasks(registry):
    registry.register_task('conttest', execute_conttest)
    logging.debug('conttest task registered.')
