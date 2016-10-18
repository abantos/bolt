"""
"""
import os.path
import unittest

import bolt.tasks.bolt_mkdir as mkd
import _mocks as mck

class TestExecuteMKDir(unittest.TestCase):
    
    def setUp(self):
        self.subject = ExecuteMKDirSpy()
        return super(TestExecuteMKDir, self).setUp()
    
    def test_creates_specified_directory(self):
        directory = os.path.join(os.getcwd(), 'new_dir') 
        config = {
            'directory': directory
        }
        self.given(config)
        self.assertEqual(self.subject.directory, directory)
        self.assertTrue(self.subject.directory_created)


    def test_skips_directory_creation_if_directory_exists(self):
        directory = os.getcwd()
        config = {
            'directory': directory
        }
        self.given(config)
        self.assertFalse(self.subject.directory_created)


    def given(self, config):
        self.subject(config=config)



class ExecuteMKDirSpy(mkd.ExecuteMKDir):
    
    def __init__(self):
        self.directory_created = False
        return super(ExecuteMKDirSpy, self).__init__()
    
    def _create_directories(self):
        self.directory_created = True



class TestRegisterTasks(unittest.TestCase):
    
    def test_registers_mkdir_task(self):
        registry = mck.TaskRegistryDouble()
        mkd.register_tasks(registry)
        self.assertTrue(registry.contains('mkdir'))

if __name__=="__main__":
    unittest.main()