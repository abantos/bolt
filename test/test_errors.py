import unittest

import bolt.errors as bt_errors


class TestInvalidTaskError(unittest.TestCase):
    # I need to check what InvalidTaskError is doing now, and evaluate if it
    # needs to provide more information.
    pass


class TestInvalidConfigurationError(unittest.TestCase):
    def setUp(self):
        super(TestInvalidConfigurationError, self).setUp()
        self.exc = bt_errors.InvalidConfigurationError()

    def test_returns_expected_string_representation(self):
        expected = "InvalidConfigurationError()"
        self.assertEqual(str(self.exc), expected)

    def test_representation_matches_string(self):
        self.assertEqual(repr(self.exc), str(self.exc))


class TestConfigurationParameterError(unittest.TestCase):
    def setUp(self):
        super(TestConfigurationParameterError, self).setUp()
        self.param_name = "parameter"
        self.exc = bt_errors.ConfigurationParameterError(self.param_name)

    def test_provides_parameter_name(self):
        self.assertEqual(self.exc.parameter, self.param_name)

    def test_returns_expected_string_representation(self):
        expected = "ConfigurationParameterError('parameter')"
        self.assertEqual(str(self.exc), expected)


class TestRequiredParameterMissingError(unittest.TestCase):
    def setUp(self):
        super(TestRequiredParameterMissingError, self).setUp()
        self.param_name = "required"
        self.exc = bt_errors.RequiredParameterMissingError(self.param_name)

    def test_provides_parameter_name(self):
        self.assertEqual(self.exc.parameter, self.param_name)

    def test_returns_expected_string_representation(self):
        expected = "RequiredParameterMissingError('required')"
        self.assertEqual(str(self.exc), expected)


class TestConfigurationValueError(unittest.TestCase):
    def setUp(self):
        super(TestConfigurationValueError, self).setUp()
        self.param_name = "parameter"
        self.value = "value"
        self.exc = bt_errors.ConfigurationValueError(self.param_name, self.value)

    def test_provides_parameter_name(self):
        self.assertEqual(self.exc.parameter, self.param_name)

    def test_provides_invalid_value(self):
        self.assertEqual(self.exc.value, self.value)

    def test_returns_expected_string_representation(self):
        expected = "ConfigurationValueError('parameter', 'value')"
        self.assertEqual(str(self.exc), expected)


class TestTaskError(unittest.TestCase):
    def setUp(self):
        super(TestTaskError, self).setUp()
        self.exc = bt_errors.TaskError()

    def test_returns_expected_string_representation(self):
        expected = "TaskError()"
        self.assertEqual(str(self.exc), expected)


if __name__ == "__main__":
    unittest.main()
