"""
"""
import subprocess as sp

from bolt._bterror import InvalidConfigurationError


class ShellExecuteTask(object):
    
    def __call__(self, **kwargs):
        self.config = kwargs.get('config')
        self._verify_valid_configuration()
        self._build_command_line()
        self._run()


    def _verify_valid_configuration(self):
        if not self.config:
            raise InvalidConfigurationError('A shell command is required')
        self.command = self.config.get('command')
        if not self.command:
            raise InvalidConfigurationError('A command must be specified')


    def _build_command_line(self):
        self.command_line = [self.command]
        arguments = self.config.get('arguments')
        if arguments:
            self.command_line.extend(arguments)


    def _run(self):
        result = sp.call(self.command_line)
        result.check_returncode()
        


def register_tasks(registry):
    registry.register_task('shell', ShellExecuteTask())