"""
"""
import logging

import bolt.api as api

class TaskRegistry(object):
    """

    """
    def __init__(self):
        self._tasks = {}

    def register_task(self, name, task):
        """

        :param name:
        :param task:
        :return:
        """
        if not self._is_valid_task(task):
            raise InvalidTaskTypeError(type(task))
        self._tasks[name] = task
        msg = '{task_name} task is registered.'.format(task_name=name)
        logging.debug(msg)


    def register_module_tasks(self, module):
        """
        """
        module.register_tasks(self)


    def get(self, name):
        """

        :param name:
        :return:
        """
        task_name = self._extract_task_name(name)
        return  self._tasks[task_name]


    def _is_valid_task(self, task):
        is_list = isinstance(task, list)
        if is_list:
            for t in task:
                if not isinstance(t, str):
                    return False
        return callable(task) or is_list


    def _extract_task_name(self, full_task):
        return full_task.split('.')[0]



class InvalidTaskTypeError(api.BoltError):
    """
    """
    def __init__(self, task_type):
        super(InvalidTaskTypeError, self).__init__(100)
        self.task_type = task_type


    def __repr__(self):
        return 'InvalidTaskTypeError({t})'.format(t=self.task_type)



