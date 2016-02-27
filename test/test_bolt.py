import unittest

import bolt

class TestRegisterModuleTasks(unittest.TestCase):

    def test_module_is_invoked_to_register_tasks(self):
        module = self
        self.given(module)
        self.expect('test')
        

    def given(self, module):
        bolt.register_module_tasks(module)


    def expect(self, task_name):
        task = bolt._bolt_application.registry.get(task_name)
        self.assertTrue(callable(task))


    def register_tasks(self, registry):
        registry.register_task('test', self.the_task)


    def the_task(self, config): pass



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
        parser = bolt._bolt_application._get_argument_parser()
        self.args = parser.parse_args(args.split())


    def expect_task(self, task_name):
        self.assertEqual(task_name, self.args.task)


    def expect_bolt_file(self, filename):
        self.assertEqual(filename, self.args.bolt_file)



if __name__=="__main__":
    unittest.main()

