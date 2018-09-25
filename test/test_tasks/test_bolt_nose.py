"""
"""
import unittest
import os.path

import bolt.tasks.bolt_nose as bnose
import _mocks as mck


class TestExecuteNoseTask(unittest.TestCase):

    def setUp(self):
        self.subject = ExecuteNoseTaskSpy()
        return super(TestExecuteNoseTask, self).setUp()


    def test_specifying_no_config_runs_with_defaults(self):
        self.given({})
        self.expect(bnose.DEFAULT_ARGUMENTS)


    def test_uses_specified_directory(self):
        directory = os.path.abspath('./my/tests')
        config = {
            'directory': directory
        }
        self.given(config)
        self.expect([directory])


    def test_options_are_added_to_arguments(self):
        config = {
            'options': {
                'option': 'foo'    
            }    
        }
        self.given(config)
        self.expect(['--option=foo'])


    def test_single_char_option_is_appended_correctly(self):
        config = {
            'options': {
                's': 'single'    
            }    
        }
        self.given(config)
        self.expect(['-s=single'])


    def test_directory_is_appended_to_options(self):
        directory = os.path.abspath('./my/tests')
        config = {
            'directory': directory,
            'options': {
                'option': 'foo'
            }    
        }
        self.given(config)
        self.expect(['--option=foo', directory])


    def test_switches_are_appended_correctly(self):
        config = {
            'options': {
                'switch': True    
            }
        }
        self.given(config)
        self.expect(['--switch'])


    def given(self, config):
        self.subject(config=config)


    def expect(self, expected):        
        commonitems = set(self.subject.args).intersection(expected)
        self.assertEqual(len(commonitems), len(expected))



class ExecuteNoseTaskSpy(bnose.ExecuteNoseTask):
    
    def _execute(self):
        self.result = 0
    

class TestRegisterTasks(unittest.TestCase):
    
    def test_registers_nose_task(self):
        registry = mck.TaskRegistryDouble()
        bnose.register_tasks(registry)
        self.assertTrue(registry.contains('nose'))



if __name__=='__main__':
    unittest.main()