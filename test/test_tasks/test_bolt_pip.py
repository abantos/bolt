"""
"""
import unittest

import bolt.tasks.bolt_pip as bpip
import _mocks as mck


class TestExecutePipTask(unittest.TestCase):
    def setUp(self):
        self.subject = ExecutePipTaskSpy()
        return super(TestExecutePipTask, self).setUp()

    def test_empty_configuration_assumes_a_requirements_file_in_current_directory(self):
        self.given({})
        self.expect(bpip.DEFAULT_ARGUMENTS)

    def test_can_install_single_package(self):
        config = {"command": "install", "package": "apackage"}
        self.given(config)
        self.expect(["install", "apackage"])

    def test_raises_exception_if_pip_raises_system_exit(self):
        self.subject.raise_system_exit = True
        with self.assertRaises(bpip.PipError):
            self.given({})

    def given(self, config):
        self.result = self.subject(config=config)

    def expect(self, expected):
        commonitems = set(self.subject.args).intersection(expected)
        self.assertEqual(len(commonitems), len(expected))


class ExecutePipTaskSpy(bpip.ExecutePipTask):
    def __init__(self):
        self.raise_system_exit = False

    def _execute_pip(self):
        if self.raise_system_exit:
            return 1
        return 0


class TestRegisterTasks(unittest.TestCase):
    def test_registers_pip(self):
        registry = mck.TaskRegistryDouble()
        bpip.register_tasks(registry)
        self.assertTrue(registry.contains("pip"))


if __name__ == "__main__":
    unittest.main()
