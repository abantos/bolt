import os
import unittest

import bolt.tasks.bolt_set_vars as bt_svars
import _mocks as mck


class TestSetVarsTask(unittest.TestCase):
    def setUp(self):
        super(TestSetVarsTask, self).setUp()
        self.svar = "STRING_VAR"
        self.svalue = "the_value"
        self.nvar = "INTEGER_VAR"
        self.nvalue = 10
        self.config = {"vars": {self.svar: self.svalue, self.nvar: self.nvalue}}
        self.subject = bt_svars.SetVarsTask()
        self.subject(config=self.config)

    def tearDown(self):
        os.environ.pop(self.svar)
        os.environ.pop(self.nvar)

    def test_sets_specified_vars_in_environment(self):
        self.expect(self.svar, self.svalue)

    def test_sets_numeric_var_as_string(self):
        self.expect(self.nvar, str(self.nvalue))

    def given(self, config):
        self.subject(config=config)

    def expect(self, var, expected):
        actual = os.environ.get(var)
        self.assertEqual(actual, expected)


class TestRegisterTasks(unittest.TestCase):
    def test_registers_set_vars_task(self):
        registry = mck.TaskRegistryDouble()
        bt_svars.register_tasks(registry)
        self.assertTrue(registry.contains("set-vars"))


if __name__ == "__main__":
    unittest.main()
