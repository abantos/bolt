"""
shell
-----

The ``shell`` task allows executing a shell command with specified arguments
inside the bolt execution context. This task comes handy when no bolt
specific implementation has been provided for a particular task or to invoke
an existing script that should be included as part of the process. 

The trade-off of using this task is that commands are system specific and
it makes it harder to implement a cross-platform ``boltfile.py``.

The task takes a ``command`` parameter specifying the command to be executed,
and an ``arguments`` option that must be set to a list of string for each of
the command line argument tokens to be passed to the tool.

The following example shows how to invoke an existing |python|_ script that
takes a few parameters::

    config = {
        'shell': {
            'command': 'python',
            'arguments': ['existing_script.py', '--with-argument', '-f', '--arg-with', 'a_value']
        }
    }

..  todo::  Find a better example.
"""
import logging
import subprocess as sp

import bolt.api as api


class ShellExecuteTask(api.Task):
    
    def _configure(self):
        self.command = self._require('command')
        self.command_line = [self.command]
        arguments = self._optional('arguments', [])
        self.command_line.extend(arguments)


    def _execute(self):
        logging.debug('Shell command line: ', repr(self.command_line))
        result = sp.call(self.command_line)
        if result != 0:
            raise ShellError(result)


        


def register_tasks(registry):
    registry.register_task('shell', ShellExecuteTask())



class ShellError(api.TaskFailedError):

    def __init__(self, shell_code):
        super(ShellError, self).__init__(shell_code)


    def __repr__(self):
        return 'ShellError({code})'.format(code=self.code)