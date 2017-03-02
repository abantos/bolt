"""
"""
import logging

class TaskRunner(object):
    """
    """

    def __init__(self, config, registry, continue_on_error):
        self._config = config
        self._registry = registry
        self._continue_on_error = continue_on_error
        self._context = {}
        self._script = None
        self._executed_operations = None


    def run(self, task):
        self._build(task)
        for task in self._script:
            self._try_run_task(task)


    def tear_down(self):
        for operation in self._executed_operations:
            if hasattr(operation, 'tear_down'):
                operation.tear_down()

    def _build(self, task_name):
        self._script = []
        self._executed_operations = []
        self._build_task(task_name)


    def _build_task(self, task_name):
        task_operation = self._registry.get(task_name)
        if callable(task_operation):
            task_config = self._config.get(task_name)
            requested_task = (task_operation, task_config)
            self._script.append(requested_task)
        else:
            for subtask in task_operation:
                self._build_task(subtask)


    def _try_run_task(self, task):
        if self._continue_on_error:
            self._run_task_protected(task)
        else:
            self._run_task(task)


    def _run_task_protected(self, task):
        try:
            self._run_task(task)
        except Exception as ex:
            logging.exception(ex)


    def _run_task(self, task):
        operation, config = task
        result = operation(config=config, context=self._context)
        self._executed_operations.append(operation)
