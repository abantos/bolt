import unittest

import bolt
import bolt.tasks.bolt_delete_files as df
import _mocks as mck


class TestDeleteFilesTask(unittest.TestCase):

    def setUp(self):
        self.subject = DeleteFilesTaskSpy()
        return super(TestDeleteFilesTask, self).setUp()


    def test_raises_if_configuration_specified_is_empty(self):
        with self.assertRaises(bolt.InvalidConfigurationError):
            self.subject(config={})


    def test_it_requires_a_root_folder(self):
        with self.assertRaises(bolt.InvalidConfigurationError):
            config={
                    'pattern': '*.*',
                }
            self.given(config)


    def test_requires_a_file_pattern(self):
        with self.assertRaises(bolt.InvalidConfigurationError):
            config={
                    'sourcedir': 'C:\\sourcedir',
                }
            self.given(config)


    def test_it_default_to_no_recursive(self):
        config = {
                'sourcedir': 'C:\\sourcedir',
                'pattern': '*.*',
            }
        self.given(config)
        self.expect_not_recursive()


    def test_recursive_can_be_changed(self):
        config = {
                'sourcedir': 'C:\\sourcedir',
                'pattern': '*.*',
                'recursive': True
            }
        self.given(config)
        self.expect_recursive()


    def test_executes_file_deletion(self):
        config = {
                'sourcedir': 'C:\\sourcedir',
                'pattern': '*.*',
                'recursive': True
            }
        self.given(config)
        self.assert_executes_deletion()


    def given(self, config):
        self.subject(config=config)


    def expect_recursive(self):
        self.assertTrue(self.subject.recursive)


    def expect_not_recursive(self):
        self.assertFalse(self.subject.recursive)


    def assert_executes_deletion(self):
        self.assertTrue(self.subject.executed)



class DeleteFilesTaskSpy(df.DeleteFilesTask):
    
    def __init__(self):
        self.executed = False
        return super(DeleteFilesTaskSpy, self).__init__()


    def _execute_delete(self):
        self.executed = True



class TestDeletePycTask(unittest.TestCase):
    
    def test_uses_pyc_file_patter(self):
        subject = DeletePycTaskSpy()
        config = {
            'sourcedir': 'C:\\sourcedir'
        }
        subject(config=config)
        self.assertEqual(subject.pattern, '*.pyc')


class DeletePycTaskSpy(df.DeletePycTask):
    
    def _execute_delete(self):
        pass
    


class TestRegisterTasks(unittest.TestCase):
    
    def setUp(self):
        self.registry = mck.TaskRegistryDouble()
        df.register_tasks(self.registry)
        return super(TestRegisterTasks, self).setUp()
    
    def test_registers_delete_files_task(self):
        self.assertTrue(self.registry.contains('delete-files'))


    def test_registers_delete_pyc_task(self):
        self.assertTrue(self.registry.contains('delete-pyc'))
        





if __name__=='__main__':
    unittest.main()