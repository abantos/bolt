import logging
import os.path
import unittest

import bolt._btapp as btapp
import bolt.errors as bterror
import bolt._btregistry as btregistry


class TestBoltApplication(unittest.TestCase):
    
    def setUp(self):
        self.options = OptionsDummy()
        self.registry = btregistry.TaskRegistry()
        self.config_manager = ConfigManagerDummy()
        self.application = btapp.BoltApplication(self.options, self.registry, self.config_manager)
        self.default_application = BoltApplicationSpy()
        return super(TestBoltApplication, self).setUp()

    
    def test_uses_specified_options(self):
        self.assertIs(self.application.options, self.options)


    def test_uses_default_options_if_none_specified(self):
        self.assertIs(self.default_application.options, self.default_application.default_options)


    def test_uses_specified_registry(self):
        self.assertIs(self.application.registry, self.registry)


    def test_uses_default_registry_if_none_specified(self):
        self.assertIs(self.default_application.registry, self.default_application.default_registry)


    def test_uses_specified_configuration_manager(self):
        self.assertIs(self.application.config_manager, self.config_manager)


    def test_delays_initialization_of_configuration_manager_if_not_specified(self):
        self.assertIsNone(self.default_application.config_manager)


    def test_runs_task_specified(self):
        self.setup_tasks()
        self.application.run_task('successful_task')
        self.assertTrue(self.successful_task_executed)


    def test_continues_on_error_if_specified(self):
        self.setup_tasks()
        self.application.options.continue_on_error = True
        self.application.run_task('continue')
        self.assertTrue(self.successful_task_executed)


    def test_can_override_continue_on_error(self):
        self.setup_tasks()
        self.application.run_task('continue', True)
        self.assertTrue(self.successful_task_executed)


    def test_raises_system_exit_if_no_continue_on_error_set(self):
        with self.assertRaises(bterror.TaskError):
            self.setup_tasks()
            self.application.run_task('continue')
            self.assertFalse(self.successful_task_executed)


    def test_tears_down_tasks_at_the_end(self):
        self.setup_tasks()
        self.application.run_task('tearable')
        self.assertTrue(self.tearable_task.tear_down_invoked)


    def test_tears_down_even_if_exception(self):
        try:
            self.setup_tasks()
            self.application.run_task('insure_teardown')
        except bterror.TaskError:
            self.assertTrue(self.tearable_task.tear_down_invoked)


    def test_executes_specified_task(self):
        self.setup_tasks()
        self.application.options.task = 'successful_task'
        self.application.run()
        self.assertTrue(self.successful_task_executed)


    def test_standard_tasks_are_registered(self):
        self.assert_registered('conttest')
        self.assert_registered('coverage')
        self.assert_registered('delete-files')
        self.assert_registered('delete-pyc')
        self.assert_registered('mkdir')
        self.assert_registered('nose')
        self.assert_registered('pip')
        self.assert_registered('setup')
        self.assert_registered('shell')
        self.assert_registered('sleep')


    def setup_tasks(self):
        self.tearable_task = TearableTask()
        self.application.registry.register_task('tearable', self.tearable_task)
        self.application.registry.register_task('successful_task', self.successful_task)
        self.application.registry.register_task('failed_task', self.failed_task)
        self.application.registry.register_task('continue', ['failed_task', 'successful_task'])
        self.application.registry.register_task('insure_teardown', ['tearable', 'failed_task'])


    def assert_registered(self, task_name):
        task = self.application.registry.get(task_name)
        self.assertIsNotNone(task)
        


    def successful_task(self, **kwargs):
        self.successful_task_executed = True
        return 0


    def failed_task(self, **kwargs):
        raise bterror.TaskError()





class OptionsDummy(object):
    
    def __init__(self):
        self.log_level = logging.CRITICAL
        self.log_file = None
        self.continue_on_error = False


class ConfigManagerDummy(object):
    
    def get(self, task):
        return {}


class BoltApplicationSpy(btapp.BoltApplication):
    
    def __init__(self):
        self.default_options = OptionsDummy()
        self.default_registry = None
        self.default_config_manager = ConfigManagerDummy()
        return super(BoltApplicationSpy, self).__init__()


    def _get_default_options(self):
        return self.default_options


    def _get_default_registry(self):
        registry = super(BoltApplicationSpy, self)._get_default_registry()
        self.default_registry = registry
        return self.default_registry


    def _get_default_config_manager(self):
        return self.default_config_manager


    def _get_file_logger_handler(self, filename):
        return logging.StreamHandler()



class TearableTask(object):
    
    def __call__(self, **kwargs):
        pass 


    def tear_down(self):
        self.tear_down_invoked = True



class LoggerDummy(object):
    
    def __init__(self):
        self.handler_count = 0


    def setLevel(self, level):
        self.level = level


    def addHandler(self, handler):
        self.handler_count += 1




class TestBoltFile(unittest.TestCase):
    

    def test_loads_specified_file(self):
        bfile = os.path.abspath('a_bolt_file.py')
        boltfile = BoltFileSpy(bfile)
        self.assertEqual(boltfile.filename, bfile)


    def test_returns_config_from_module(self):
        boltfile = BoltFileSpy('a_bolt_file.py')
        self.assertEqual(boltfile.config, boltfile.expected_module.config)



class BoltFileSpy(btapp.BoltFile):
    
    def _load(self):
        self.expected_module = BoltModuleDouble()
        return self.expected_module



class BoltModuleDouble(object):
    
    @property
    def config(self):
        return {}



if __name__=="__main__":
    unittest.main()