"""
"""
import unittest

import bolt.tasks.bolt_pip as bpip

class TestPipArgumentGenerator(unittest.TestCase):

    def setUp(self):
        self.subject = bpip._PipArgumentGenerator()
        return super(TestPipArgumentGenerator, self).setUp()
    
    def test_empty_configuration_assumes_a_requirements_file_in_current_directory(self):
        self.given({})
        self.expect([bpip.DEFAULT_COMMAND, '-r', bpip.DEFAULT_REQUIREMENTS_FILE])


    def test_can_install_single_package(self):
        config = {
            'command': 'install',
            'package': 'apackage'
        }
        self.given(config)
        self.expect(['install', 'apackage'])


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
        self.generated_args = self.subject.generate_from(config)


    def expect(self, expected):
        commonitems = set(self.generated_args).intersection(expected)

        self.assertEqual(len(commonitems), len(expected))




if __name__=='__main__':
    unittest.main()
