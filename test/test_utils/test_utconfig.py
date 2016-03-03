import unittest

import bolt.utils._utconfig as utconfig


class TestCommonCommandAndArgumentGenerator(unittest.TestCase):

    def setUp(self):
        self.subject = CommonCommandAndArgumentsGeneratorMock()
        return super(TestCommonCommandAndArgumentGenerator, self).setUp()


    def test_returns_default_arguments_if_empty_configuration(self):
        self.given({})
        self.expect(self.subject.DEFAULT_ARGUMENTS)


    def test_returns_default_arguments_if_no_configuration(self):
        self.given(None)
        self.expect(self.subject.DEFAULT_ARGUMENTS)


    def test_options_are_passed_to_command(self):
        config = {
            'command': 'install',
            'options': {
                'requirement': 'a_requirements_file.txt'
            }
        }
        self.given(config)
        self.expect(['install', '--requirement', 'a_requirements_file.txt'])


    def test_options_can_be_specified_in_their_short_form(self):
        config = {
            'command': 'install',
            'options': {
                'r': 'a_requirements_file.txt'
            }
        }
        self.given(config)
        self.expect(['install', '-r', 'a_requirements_file.txt'])


    def test_if_value_is_boolean_options_is_specified_as_flag(self):
        config = {
            'command': 'install',
            'options': {
                'requirement': 'a_requirements_file.txt',
                'force-reinstall': True
            }
        }
        self.given(config)
        self.expect(['install', '--requirement', 'a_requirements_file.txt', '--force-reinstall'])


    def test_flag_is_not_added_if_false(self):
        config = {
            'command': 'install',
            'options': {
                'requirement': 'a_requirements_file.txt',
                'force-reinstall': False
            }
        }
        self.given(config)
        self.expect(['install', '--requirement', 'a_requirements_file.txt'])


    def given(self, config):
        self.actual = self.subject.generate_from(config)


    def expect(self, expected):
        commonitems = set(self.actual).intersection(expected)
        self.assertEqual(len(commonitems), len(expected))



class CommonCommandAndArgumentsGeneratorMock(utconfig.CommonCommandAndArgumentsGenerator):

    DEFAULT_ARGUMENTS = ['a_command', '--switch', 'value']

    def __init__(self):
        return super(CommonCommandAndArgumentsGeneratorMock, self).__init__(self.DEFAULT_ARGUMENTS)



if __name__=='__main__':
    unittest.main()