import unittest
import bolt.utils as btutils
import bolt.tasks.bolt_sleep as btsleep
import _mocks as mck


class TestSleepTask(unittest.TestCase):
    def test_sleeps_forever_if_no_time_specified(self):
        config = {}
        self.call_with(config)
        self.assertTrue(self.subject.sleep_forever)

    def test_sleeps_forever_if_specified(self):
        config = {"duration": btutils.FOREVER}
        self.call_with(config)
        self.assertTrue(self.subject.sleep_forever)

    def test_sleeps_specified_duration(self):
        expected = 10 * btutils.MINUTES
        config = {"duration": expected}
        self.call_with(config)
        self.assertEqual(self.subject.sleep_time, expected)

    def call_with(self, config):
        self.subject = SleepTaskSpy()
        self.subject(config=config)


class SleepTaskSpy(btsleep.SleepTask):
    def _sleep(self, seconds):
        self.sleep_time = seconds

    def _sleep_forever(self):
        self.sleep_forever = True


class TestRegisterTasks(unittest.TestCase):
    def test_registers_sleep_task(self):
        registry = mck.TaskRegistryDouble()
        btsleep.register_tasks(registry)
        self.assertTrue(registry.contains("sleep"))


if __name__ == "__main__":
    unittest.main()
