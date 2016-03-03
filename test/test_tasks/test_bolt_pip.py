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
        self.expect(bpip.DEFAULT_ARGUMENTS)


    def test_can_install_single_package(self):
        config = {
            'command': 'install',
            'package': 'apackage'
        }
        self.given(config)
        self.expect(['install', 'apackage'])


    def given(self, config):
        self.generated_args = self.subject.generate_from(config)


    def expect(self, expected):
        commonitems = set(self.generated_args).intersection(expected)
        self.assertEqual(len(commonitems), len(expected))




if __name__=='__main__':
    unittest.main()
