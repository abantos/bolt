"""
"""

class TaskRunner(object):
    """
    """

    def __init__(self, config, registry):
        self._config = config
        self._registry = registry
        self._script = None


    def build(self, task_name):
        self._script = []
        self._build_task(task_name)


    def run(self):
        for task in self._script:
            operation, config = task
            operation(config=config)


    def _build_task(self, task_name):
        task_operation = self._registry.get(task_name)
        if callable(task_operation):
            task_config = self._config.get(task_name)
            requested_task = (task_operation, task_config)
            self._script.append(requested_task)
        else:
            for subtask in task_operation:
                self._build_task(subtask)