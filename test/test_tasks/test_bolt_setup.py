import unittest
import bolt.tasks.bolt_setup as bsetup


class TestSetupArgumentGenerator(unittest.TestCase):

    def setUp(self):
        self. subject = bsetup._SetupArgumentGenerator()
        return super(TestSetupArgumentGenerator, self).setUp()


    def test_uses_default_if_empty_configuration(self):
        self.given({})
        self.expect(bsetup.DEFAULT_ARGUMENTS)


    def given(self, config):
        self.generated_args = self.subject.generate_from(config)


    def expect(self, expected):
        commonitems = set(self.generated_args).intersection(expected)
        self.assertEqual(len(commonitems), len(expected))




if __name__=='__main__':
    unittest.main()