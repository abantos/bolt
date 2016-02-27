"""

"""

class ConfigurationManager(object):

    def __init__(self, full_config):
        self._full_config = full_config


    def get(self, task_key):
        self.result_config = {}
        self.current_config = self._full_config.copy()
        [self._add_task_options(task_option) for task_option in  task_key.split('.')]
        return self.result_config
        
        
    def _add_task_options(self, task_option):
        task_config = self.current_config.get(task_option)
        if task_config:
            self._merge_into_result(task_config)
            self._remove_from_result(task_option)
        self.current_config = task_config
        
        
    def _merge_into_result(self, task_config):
        self.result_config.update(task_config)
        
        
    def _remove_from_result(self, task_option):
        if task_option in self.result_config:
            del self.result_config[task_option]
        
