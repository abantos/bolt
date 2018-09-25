import unittest

import bolt.api as api


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