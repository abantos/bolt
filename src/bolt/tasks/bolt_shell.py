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

spawn
-----

The ``spawn`` task works exactly the same as the shell task, but creates a
separate process for the program execution, which allows executing a process
that needs to keep running while other programs execute. On tear down, the
process is terminated.

..  code-block:: python

    config = {
        'spawn': {
            'command': 'python',
            'arguments': ['existing_script.py', '--with-argument', '-f', '--arg-with', 'a_value']
        }
    }
"""

import logging
import subprocess as sp

import bolt.api as api

SUCCESS = 0


class ShellExecuteTask(api.Task):
    def _configure(self):
        self.command = self._require("command")
        self.command_line = [self.command]
        arguments = self._optional("arguments", [])
        self.command_line.extend(arguments)

    def _execute(self):
        logging.debug("Shell command line: %s", repr(self.command_line))
        result = self._invoke(self.command_line)
        if result != SUCCESS:
            raise ShellError(result)

    def _invoke(self, command_line):
        return sp.call(command_line)


class SpawnExecuteTask(ShellExecuteTask):
    def tear_down(self):
        self._process.terminate()

    def _invoke(self, command_line):
        try:
            self._process = self._spawn_process(command_line)
        except OSError as error:
            logging.warning(error)
            return error.errno
        return SUCCESS

    def _spawn_process(self, command_line):
        return sp.Popen(command_line)


def register_tasks(registry):
    registry.register_task("shell", ShellExecuteTask())
    registry.register_task("spawn", SpawnExecuteTask())


class ShellError(api.TaskFailedError):
    def __init__(self, shell_code):
        super(ShellError, self).__init__(shell_code)

    def __repr__(self):
        return "ShellError({code})".format(code=self.code)
