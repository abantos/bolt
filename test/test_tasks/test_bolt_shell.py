import unittest

import bolt.api as api
import bolt.tasks.bolt_shell as bsh
import _mocks as mck

FAIL_COMMAND = 'failed'


class TestShellExecuteTask(unittest.TestCase):
    def setUp(self):
        self.subject = ShellExecuteTaskSpy()

    def test_configuration_cannot_be_empty(self):
        with self.assertRaises(api.RequiredConfigurationError):
            self.given({})

    def test_configuration_must_contain_command(self):
        with self.assertRaises(api.RequiredConfigurationError):
            config = {'arguments': ['foo']}
            self.given(config)

    def test_command_line_contains_no_arguments_if_none_specified(self):
        config = {'command': 'ls'}
        self.given(config)
        self.expect_command_line(['ls'])

    def test_command_line_contains_specified_arguments(self):
        config = {'command': 'command', 'arguments': ['arg1', 'arg2']}
        self.given(config)
        self.expect_command_line(['command', 'arg1', 'arg2'])

    def test_raises_if_command_fails(self):
        with self.assertRaises(Exception):
            config = {
                'command': FAIL_COMMAND,
            }
            self.given(config)

    def given(self, config):
        self.result = self.subject(config=config)

    def expect_command_line(self, expected):
        self.assertListEqual(self.subject.args, expected)


class ShellExecuteTaskSpy(bsh.ShellExecuteTask):
    def __init__(self):
        self.returncode = 0
        return super(ShellExecuteTaskSpy, self).__init__()

    def _invoke(self, command_line):
        self.args = command_line
        return 1 if self.args[0] == FAIL_COMMAND else 0

    def check_returncode(self):
        if self.returncode != 0:
            raise Exception('Failed command')
        

class TestSpawnExecuteTask(unittest.TestCase):
    def setUp(self):
        self.subject = SpawnExecuteTaskSpy()
        self.config = {
            'command': 'spawned'
        }

    def test_raises_exception_if_creating_the_process_fails(self):
        with self.assertRaises(bsh.ShellError):
            self.subject(config={'command': 'failed'})

    def test_terminates_process_on_tear_down(self):
        self.subject(config=self.config)
        self.subject.tear_down()
        self.assertTrue(self.subject.process_terminated)
        


class SpawnExecuteTaskSpy(bsh.SpawnExecuteTask):
    def __init__(self):
        super().__init__()
        self.process_terminated = False
    
    def _spawn_process(self, command_line):
        if command_line[0] == FAIL_COMMAND: raise OSError(999, 'test error')
        return self
    
    def terminate(self):
        self.process_terminated = True


class TestRegisterTasks(unittest.TestCase):
    def test_registers_shell(self):
        registry = mck.TaskRegistryDouble()
        bsh.register_tasks(registry)
        self.assertTrue(registry.contains('shell'))
        self.assertTrue(registry.contains('spawn'))


if __name__ == '__main__':
    unittest.main()
