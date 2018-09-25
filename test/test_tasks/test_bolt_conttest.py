"""
"""
import os.path
import unittest

import bolt.tasks.bolt_conttest as ct
import _mocks as mck


class TestRegisterTasks(unittest.TestCase):
    
    def test_registers_conttest_task(self):
        registry = mck.TaskRegistryDouble()
        ct.register_tasks(registry)
        self.assertTrue(registry.contains('conttest'))
        

class TestExecuteConttest(unittest.TestCase):

    def setUp(self):
        self.subject = ExecuteConttestSpy()
        return super(TestExecuteConttest, self).setUp()

    def test_executes_configured_task(self):
        task_name = 'configured'
        config = {
            'task': task_name
        }
        self.given_configuration(config)
        self.expect_task(task_name)


    def test_monitors_specified_directory(self):
        directory = os.path.join(os.getcwd(), 'foo')
        config = {
            'task': 'foo',
            'directory': directory
        }
        self.given_configuration(config)
        self.expect_path(directory)


    def test_default_to_current_directory_if_none_specified(self):
        self.given_configuration({
            'task': 'foo'
        })
        self.expect_path(os.getcwd())


    def test_continue_on_error_is_set_to_true(self):
        self.given_configuration({
            'task': 'foo'
        })
        self.assertTrue(self.subject.continue_on_error)


    def given_configuration(self, config):
        self.subject(config=config)


    def expect_task(self, task):
        self.assertEqual(self.subject.task_name, task)
        


    def expect_path(self, path):
        self.assertEqual(self.subject.directory, path)



class ExecuteConttestSpy(ct.ExecuteConttest):
    
    def _execute(self): pass
    

    



if __name__=="__main__":
    unittest.main()