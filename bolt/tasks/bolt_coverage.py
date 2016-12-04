"""
coverage
--------

This task allows to measure code coverage of source code executed by the specified
task. The following is a sample configuration:

..  code-block:: python

    config = {
        'coverage': {
            'task': 'registered-task',
            'include': './directory/for/source',
            'output': 'directory/to/write/results'
        }
    }

The specified task must exercise the code that will be measured.
"""
import logging
import bolt


class ExecuteCoverage(object):
    
    def __call__(self, **kwargs):
        self.config = kwargs.get('config')
        self.task_name = self.config.get('task')
        self.include_dir = self.config.get('include')
        self.out_dir = self.config.get('output')
        logging.info('Code coverage for {task}. Output at {directory}'.format(task=self.task_name, directory=self.out_dir))
        self.execute_with_coverage()


    def execute_with_coverage(self):
        import coverage.control as cov
        controller = cov.Coverage(auto_data=False, branch=True, source=self.include_dir)
        controller.start()
        bolt.run_task(self.task_name)
        controller.stop()
        controller.html_report(directory=self.out_dir)



def register_tasks(registry):
    registry.register_task('coverage', ExecuteCoverage())
    