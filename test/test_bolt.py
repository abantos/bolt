import unittest

import bolt

class TestGetArgumentParser(unittest.TestCase):

    def test_returns_specified_task(self):
        self.given('a_task')
        self.expect_task('a_task')


    def test_returns_default_if_no_task_specified(self):
        self.given()
        self.expect_task('default')


    def test_returns_specified_bolt_file(self):
        self.given('--bolt-file specified.py')
        self.expect_bolt_file('specified.py')


    def test_returns_default_bolt_file_if_not_specified(self):
        self.given()
        self.expect_bolt_file('boltfile.py')


    def given(self, args=''):
        parser = bolt._get_argument_parser()
        self.args = parser.parse_args(args.split())


    def expect_task(self, task_name):
        self.assertEqual(task_name, self.args.task)


    def expect_bolt_file(self, filename):
        self.assertEqual(filename, self.args.bolt_file)

if __name__=="__main__":
    unittest.main()

