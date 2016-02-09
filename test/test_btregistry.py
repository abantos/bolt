import unittest

import bolt
import bolt._btregistry as registry

class TestTaskRegistry(unittest.TestCase):

    def setUp(self):
        self.subject = registry.instance

    def test_can_register_callable_as_task(self):
        task_name = 'test'
        self.subject.register_task(task_name, self.test_callable)
        actual = self.subject.get(task_name)

        self.assertEqual(actual, self.test_callable)


    def test_can_register_list_of_task_names(self):
        task_name = 'list'
        task_list = ['task1', 'task2', 'task3']
        self.subject.register_task(task_name, task_list)
        actual_list = self.subject.get(task_name)

        self.assertSequenceEqual(task_list, actual_list)


    def test_fails_if_task_is_not_callable_or_list(self):
        with self.assertRaises(bolt.InvalidTask):
            self.subject.register_task("invalid", 1)


    def test_raises_if_list_contains_anything_other_than_strings(self):
        with self.assertRaises(bolt.InvalidTask):
            self.subject.register_task("invalid", ['foo', 'bar', 3])



    def test_callable(self):
        pass


if __name__ == '__main__':
    unittest.main()
