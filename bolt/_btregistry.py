"""

"""
from bolt._bterror import InvalidTaskError

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
            raise InvalidTaskError()
        self._tasks[name] = task


    def get(self, name):
        """

        :param name:
        :return:
        """
        return  self._tasks[name]


    def _is_valid_task(self, task):
        is_list = isinstance(task, list)
        if is_list:
            for t in task:
                if not isinstance(t, str):
                    return False
        return callable(task) or is_list


