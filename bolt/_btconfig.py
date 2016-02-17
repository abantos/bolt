"""

"""

class ConfigurationManager(object):

    def __init__(self, full_config):
        self._full_config = full_config


    def get(self, task_key):
        self._task_tokens = task_key.split('.')
        self._last_token_index = len(self._task_tokens) - 1
        config = self._get_at(self._full_config, 0)
        return config

    def _get_at(self, config, index):
        id = self._task_tokens[index]
        result_config = {}
        current_config = config.get(id)
        if current_config:
            result_config.update(current_config)
            if index < self._last_token_index:
                child_index = index + 1
                child_config = self._get_at(current_config, child_index)
                result_config.update(child_config)
                child_id = self._task_tokens[child_index]
                del result_config[child_id]
        return result_config
