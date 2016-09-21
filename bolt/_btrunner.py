"""
"""

class TaskRunner(object):
    """
    """

    def __init__(self, config, registry, continue_on_error):
        self._config = config
        self._registry = registry
        self._continue_on_error = continue_on_error
        self._script = None
        self._executed_operations = None


    def build(self, task_name):
        self._script = []
        self._executed_operations = []
        self._build_task(task_name)


    def run(self):
        for task in self._script:
            operation, config = task
            result = operation(config=config)
            self._check_result(result)
            self._executed_operations.append(operation)


    def tear_down(self):
        for operation in self._executed_operations:
            if hasattr(operation, 'tear_down'):
                operation.tear_down()


    def _build_task(self, task_name):
        task_operation = self._registry.get(task_name)
        if callable(task_operation):
            task_config = self._config.get(task_name)
            requested_task = (task_operation, task_config)
            self._script.append(requested_task)
        else:
            for subtask in task_operation:
                self._build_task(subtask)


    def _check_result(self, result):
        if result not in {0, None} and not self._continue_on_error:
            raise SystemExit(result or 1)