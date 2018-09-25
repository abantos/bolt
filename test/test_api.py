import unittest

import bolt.api as api


class TestTask(unittest.TestCase):

    def setUp(self):
        self.config = {
            'param': 'value'
        }
        self.task = TaskSpy()

    def test_retrieves_config_attribute_on_call(self): 
        self.invoke()
        self.assertIs(self.task.config, self.config)


    def test_delegates_configuration_to_derived_classes(self):
        self.invoke()
        self.assertTrue(self.task.configure_invoked)


    def test_delegate_execution_to_derived_classes(self):
        self.invoke()
        self.assertTrue(self.task.execute_invoked)


    def test_raises_if_required_parameter_is_missing_in_configuration(self):
        with self.assertRaises(api.RequiredConfigurationError):
            self.invoke({})


    def test_sets_optional_to_default_value_if_not_specified_in_config(self):
        self.invoke()
        self.assertEqual(self.task.other, 3)


    def test_sets_optional_to_none_if_not_specified_and_no_default_provided(self):
        self.invoke()
        self.assertIsNone(self.task.must_be_none)


    def invoke(self, config=None):
        config = config if config is not None else self.config
        self.task(config=config)



class TaskSpy(api.Task):
    def __init__(self):
        self.configure_invoked = False
        self.execute_invoked = False


    def _configure(self):
        self.configure_invoked = True
        self.param = self._require('param')
        self.other = self._optional('other', 3)
        self.must_be_none = self._optional('no-default')


    def _execute(self):
        self.execute_invoked = True



class TestBoltError(unittest.TestCase):

    def setUp(self):
        self.exception = api.BoltError()

    def test_code_is_1_by_default(self):
        self.assertEqual(self.exception.code, 1)


    def test_code_can_be_specified(self):
        self.assertEqual(api.BoltError(2).code, 2)


    def test_provides_repr(self):
        self.assertEqual(repr(self.exception), 'BoltError(1)')


    def test_string_representation_uses_repr_by_default(self):
        self.assertEqual(str(self.exception), repr(self.exception))



class TestTaskError(unittest.TestCase):

    def setUp(self):
        self.exception = api.TaskError()

    def test_code_is_999_by_default(self):
        self.assertEqual(self.exception.code, 999)


    def test_overrides_repr_to_show_generic_name(self):
        self.assertEqual(repr(self.exception), 'TaskError(999)')




class TestRequiredConfigurationError(unittest.TestCase):

    def setUp(self):
        self.param = 'param-name'
        self.exception = api.RequiredConfigurationError(self.param)

    def test_uses_code_2(self):
        self.assertEqual(self.exception.code, 2)


    def test_requires_parameter_name(self):
        self.assertEqual(self.exception.parameter, self.param)


    def test_shows_parameter_value_in_representation(self):
        self.assertEqual(repr(self.exception), 'RequiredConfigurationError(param-name)')



class TestConfigurationValueError(unittest.TestCase):

    def setUp(self):
        self.param = 'param'
        self.value = 'value'
        self.exception = api.ConfigurationValueError(self.param, self.value)


    def test_uses_code_3(self):
        self.assertEqual(self.exception.code, 3)


    def test_requires_parameter_name(self):
        self.assertEqual(self.exception.parameter, 'param')


    def test_requires_error_value(self):
        self.assertEqual(self.exception.value, self.value)


    def test_shows_parameter_and_value_in_representation(self):
        self.assertEqual(repr(self.exception), 'ConfigurationValueError(param, value)')



class TestTaskFailedError(unittest.TestCase):

    def setUp(self):
        self.exception = api.TaskFailedError()

    def test_uses_code_4(self):
        self.assertEqual(self.exception.code, 4)


    def test_overrides_repr_to_show_generic_name(self):
        self.assertEqual(repr(self.exception), 'TaskFailedError(4)')



if __name__=="__main__":
    unittest.main()