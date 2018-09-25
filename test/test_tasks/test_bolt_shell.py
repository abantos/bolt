import unittest

import bolt.api as api
import bolt.tasks.bolt_shell as bsh
import _mocks as mck

class TestShellExecuteTask(unittest.TestCase):

    def setUp(self):
        self.subject = ShellExecuteTaskSpy()
        return super(TestShellExecuteTask, self).setUp()


    def test_configuration_cannot_be_empty(self):
        with self.assertRaises(api.RequiredConfigurationError):
            self.given({})


    def test_configuration_must_contain_command(self):
        with self.assertRaises(api.RequiredConfigurationError):
            config = {
                'arguments': ['foo']
            }
            self.given(config)


    def test_command_line_contains_no_arguments_if_none_specified(self):
        config = {
            'command': 'ls'
        }
        self.given(config)
        self.expect_command_line(['ls'])


    def test_command_line_contains_specified_arguments(self):
        config = {
            'command': 'command',
            'arguments': ['arg1', 'arg2']
        }
        self.given(config)
        self.expect_command_line(['command', 'arg1', 'arg2'])


    def test_raises_if_command_fails(self):
        with self.assertRaises(Exception):
            config = {
                'command': 'failed',
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

    def _run(self):
        self.args = self.command_line 
        if self.args[0] == 'failed':
            self.returncode = 1
        self.check_returncode()


    def check_returncode(self):
        if self.returncode != 0:
            raise Exception('Failed command')



class TestRegisterTasks(unittest.TestCase): 

    def test_registers_shell(self):
        registry = mck.TaskRegistryDouble()
        bsh.register_tasks(registry)
        self.assertTrue(registry.contains('shell'))



if __name__=='__main__':
    unittest.main()