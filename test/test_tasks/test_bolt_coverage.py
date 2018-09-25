"""
"""
import unittest

import bolt.tasks.bolt_coverage as cov
import _mocks as mck

class TestRegisterTasks(unittest.TestCase):
    
    def test_coverage_task_is_registered(self):
        registry = mck.TaskRegistryDouble()
        cov.register_tasks(registry)
        self.assertTrue(registry.contains('coverage'))



class TestExecuteCoverage(unittest.TestCase):
    
    def setUp(self):
        self.task_name = 'test-task'
        self.include_dir = './include'
        self.out_dir = './output'
        self.config = {
            'task': self.task_name,
            'include': self.include_dir,
            'output': self.out_dir
        }
        self.subject = ExecuteCoverageSpy()
        self.subject(config=self.config)
        return super(TestExecuteCoverage, self).setUp()


    def test_uses_specified_task(self):
        self.assertEqual(self.subject.task_name, self.task_name)


    def test_uses_specified_include_dir(self):
        self.assertEqual(self.subject.include_dir, self.include_dir)


    def test_uses_specified_output_dir(self):
        self.assertEqual(self.subject.out_dir, self.out_dir)


class ExecuteCoverageSpy(cov.ExecuteCoverage):
    
    def _execute(self):
        pass


if __name__=="__main__":
    unittest.main()
