"""
.. _task-set-vars:

set-vars
--------

Sets environment variables for all specified variable:value pairs. The following
shows how the task is configured:

..  code-block:: python

    config = {
        'set-vars': {
            'vars': {
                'STRING_VAR': 'string_value',
                'INT_VAR': 10
            }
        }
    }


Numeric vars will be converted to their integer representation.
"""
import os

import bolt.api as api

class SetVarsTask(api.Task):
    
    def _configure(self):
        self.vars = self._require('vars')


    def _execute(self):
        for var in self.vars:
            os.environ[var] = str(self.vars[var])




def register_tasks(registry):
    registry.register_task('set-vars', SetVarsTask())