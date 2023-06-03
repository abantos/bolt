import unittest

import bolt.tasks.bolt_setup as bsetup
import _mocks as mck


class TestExecuteSetupTask(unittest.TestCase):
    def setUp(self):
        self.subject = ExecuteSetupTaskSpy()
        return super(TestExecuteSetupTask, self).setUp()

    def test_uses_default_if_empty_configuration(self):
        self.given({})
        self.expect(bsetup.DEFAULT_ARGUMENTS)

    def test_uses_specified_script(self):
        script = "my_setup.py"
        config = {"script": script}
        self.given(config)
        self.assertEqual(self.subject.setup_script, script)

    def test_raises_exception_if_building_setup_fails(self):
        self.subject.dist_files = []
        with self.assertRaises(bsetup.BuildSetupError):
            self.given({})

    def given(self, config):
        self.subject(config=config)

    def expect(self, expected):
        commonitems = set(self.subject.args).intersection(expected)
        self.assertEqual(len(commonitems), len(expected))


class ExecuteSetupTaskSpy(bsetup.ExecuteSetupTask):
    def __init__(self):
        super(ExecuteSetupTaskSpy, self).__init__()
        self.dist_files = [("bdist_wheel", "3.5", "/some/colation/the.whl")]

    def _execute_setup(self):
        return self


class TestRegisterTasks(unittest.TestCase):
    def test_registers_setup(self):
        registry = mck.TaskRegistryDouble()
        bsetup.register_tasks(registry)
        self.assertTrue(registry.contains("setup"))


if __name__ == "__main__":
    unittest.main()
