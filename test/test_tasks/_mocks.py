"""
"""
import bolt._btregistry as btr

class TaskRegistryDouble(btr.TaskRegistry):
    
    def contains(self, name):
        return name in self._tasks
        
