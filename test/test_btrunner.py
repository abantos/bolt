import unittest

import bolt._btconfig as config
import bolt.errors as bterror
import bolt._btregistry as registry

import bolt._btrunner as runner


class TestTaskRunner(unittest.TestCase):

    def setUp(self):
        self.setUpRegistry()
        self.setUpConfig()
        self.subject = runner.TaskRunner(self.config_mgr, self.registry, False)
        self.executed_tasks = []
        return super(TestTaskRunner, self).setUp()


    def setUpRegistry(self):
        self.registry = registry.TaskRegistry()
        self.registry.register_task('task_1', self.task_1_callback)
        self.registry.register_task('task_2', self.task_2_callback)
        self.registry.register_task('invalid', self.invalid_task)
        self.registry.register_task('multi_task', ['task_1', 'task_2'])
        self.registry.register_task('configurable', self.configurable_task)
        self.registry.register_task('failing_task', self.failing_task)
        self.registry.register_task('multi_task_with_failures', ['task_1', 'failing_task', 'task_2'])
        self.tear_down_task = TearDownTask()
        self.registry.register_task('has_tear_down', self.tear_down_task)
        self.registry.register_task('partially_executed', ['failing_task', 'has_tear_down'])


    def setUpConfig(self):
        self.config = {
                'configurable': {
                    'param': 'value'
                }
            }
        self.config_mgr = config.ConfigurationManager(self.config)
    

    def test_runs_the_specified_task(self):
        self.given('task_1')
        self.expect_executed('task_1')


    def test_configuration_is_passed_to_task_by_named_parameter(self):
        self.given('task_2')
        self.expect_executed('task_2')


    def test_raises_if_task_definition_does_not_meet_spec(self):
        with self.assertRaises(Exception):
            self.given('invalid')


    def test_executes_all_tasks_in_multi_task(self):
        self.given('multi_task')
        self.expect_executed('task_1')
        self.expect_executed('task_2')


    def test_task_is_executed_with_correct_configuration(self):
        self.given('configurable')
        self.expect_executed('configurable')


    def test_build_is_enforced_before_run(self):
        with self.assertRaises(Exception):
            subject = runner.TaskRunner(self.config_mgr, self.registry, False)
            subject.run()


    def test_build_fails_if_a_task_is_not_registered(self):
        with self.assertRaises(Exception):
            self.subject.build('inexistent')


    def test_exits_if_task_does_not_return_zero(self):
        with self.assertRaises(bterror.TaskError):
            self.given('failing_task')


    def test_continues_on_error_if_specified(self):
        continue_on_error = True
        self.subject = runner.TaskRunner(self.config_mgr, self.registry, continue_on_error)
        self.given('multi_task_with_failures')
        self.expect_executed('task_2')


    def test_calls_tear_down_on_tasks_that_implement_it(self):
        self.given('has_tear_down')
        self.assertTrue(self.tear_down_task.tear_down_called)


    def test_does_not_call_teardown_if_script_fails_before_executing_task(self):
        with self.assertRaises(bterror.TaskError):
            self.given('partially_executed')
            self.assertFalse(self.tear_down_task.tear_down_called)


    def test_uses_same_execution_context_with_all_tasks(self):
        self.given('multi_task')
        self.assertTrue(self.context_shared)



    def given(self, task_name):
        try:
            self.subject.run(task_name)
        finally:
            self.subject.tear_down()


    def expect_executed(self, task_name):
        self.assertIn(task_name, self.executed_tasks)


    def task_1_callback(self, **kwargs):
        context = kwargs.get('context')
        context['shared-property'] = 1
        self.executed_tasks.append('task_1')


    def task_2_callback(self, **kwargs):
        config = kwargs.get('config')
        context = kwargs.get('context')
        if context.get('shared-property') == 1:
            self.context_shared = True
        self.executed_tasks.append('task_2')


    def invalid_task(self, noconfig):
        pass


    def configurable_task(self, **kwargs):
        config = kwargs.get('config')
        param = config.get('param')
        self.assertEqual(param, 'value')
        self.executed_tasks.append('configurable')


    def failing_task(self, **kwargs):
        raise bterror.TaskError()



class TearDownTask(object):

    def __init__(self):
        self.called = False
        self.tear_down_called = False
        return super(TearDownTask, self).__init__()

    def __call__(self, **kwargs):
        self.called = True

    def tear_down(self):
        self.tear_down_called = True



if __name__=='__main__':
    unittest.main()