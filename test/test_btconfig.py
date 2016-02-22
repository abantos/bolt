import unittest

import bolt._btconfig as config


class TestConfigurationManager(unittest.TestCase):

    def setUp(self):
        self.configuration = {
            'task': {
                'option': 1,
                'overridable': 'initial',
                'child': {
                    'overridable': 'inchild',
                    'grandchild': {
                        'overridable': 'ingrandchild'
                    }
                }
            }
        }
        self.subject = config.ConfigurationManager(self.configuration)


    def test_returns_empty_configuration_if_task_id_does_not_exists(self):
        config = self.subject.get('inexistent')
        self.assertFalse(config)


    def test_returns_the_specified_configuration(self):
        self.given('task')
        self.expect('option', 1)


    def test_options_can_be_overriden_in_child_configurations(self):
        self.given('task.child')
        self.expect('overridable', 'inchild')


    def test_child_configuration_maintains_parent_values_if_not_overriden(self):
        self.given('task.child')
        self.expect('option', 1)


    def test_supports_many_levels_of_child_indentation(self):
        self.given('task.child.grandchild')
        self.expect('overridable', 'ingrandchild')


    def given(self, key):
        self.result = self.subject.get(key)


    def expect(self, option, expected):
        actual_value = self.result.get(option)
        self.assertEqual(actual_value, expected)




if __name__=="__main__":
    unittest.main()
