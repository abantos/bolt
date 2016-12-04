"""
"""
import logging
import unittest

import bolt._btoptions as btoptions

class TestOptions(unittest.TestCase):
    
    def setUp(self):
        # If we don't initialize it from an empty options list, it parses
        # the arguments to nosetests and the test fail. The actual code using
        # it doesn't need to do it because it will parse the arguments to 
        # bolt.
        self.default_options = btoptions.Options([])
        return super(TestOptions, self).setUp()


    def test_default_command_is_properly_initialized(self):
        self.assertEqual(self.default_options.command, btoptions.Default.COMMAND)


    def test_command_is_version_if_switch_specified(self):
        self.given(btoptions.OptionSwitch.VERSION_LONG)
        self.assertEqual(self.options.command, btoptions.Commands.VERSION)


    def test_default_task_is_properly_initialized(self):
        self.assertEqual(self.default_options.task, btoptions.Default.TASK)


    def test_returns_correct_task_if_specified(self):
        task = 'a_task'
        self.given(task)
        self.assertEqual(self.options.task, task)


    def test_default_boltfile_is_properly_initialized(self):
        self.assertEqual(self.default_options.bolt_file, btoptions.Default.BOLTFILE)


    def test_sets_boltfile_with_long_switch(self):
        boltfile = 'a_bolt_file.py'
        self.given(btoptions.OptionSwitch.BOLTFILE_LONG, boltfile)
        self.assertEqual(self.options.bolt_file, boltfile)


    def test_sets_boltfile_with_short_switch(self):
        boltfile = 'a_bolt_file.py'
        self.given(btoptions.OptionSwitch.BOLTFILE_SHORT, boltfile)
        self.assertEqual(self.options.bolt_file, boltfile)


    def test_default_log_level_is_properly_initialized(self):
        self.assertEqual(self.default_options.log_level, btoptions.Default.LOG_LEVEL)


    def test_sets_log_level_with_long_switch(self):
        log_level = 'error'
        self.given(btoptions.OptionSwitch.LOG_LEVEL_LONG, log_level)
        self.assertEqual(self.options.log_level, logging.ERROR)


    def test_sets_log_level_with_short_switch(self):
        log_level = 'debug'
        self.given(btoptions.OptionSwitch.LOG_LEVEL_SHORT, log_level)
        self.assertEqual(self.options.log_level, logging.DEBUG)


    def test_converts_correctly_from_log_level_string_to_logging_level(self):
        # NOTSET
        self.verify_log_level('', logging.NOTSET)
        self.verify_log_level('n', logging.NOTSET)
        self.verify_log_level('notset', logging.NOTSET)
        # DEBUG
        self.verify_log_level('d', logging.DEBUG)
        self.verify_log_level('dbg', logging.DEBUG)
        self.verify_log_level('debug', logging.DEBUG)


    def test_default_log_file_is_properly_initialized(self):
        self.assertEqual(self.default_options.log_file, btoptions.Default.LOG_FILE)


    def test_sets_the_log_file_with_long_switch(self):
        log_file = 'log.txt'
        self.given(btoptions.OptionSwitch.LOG_FILE_LONG, log_file)
        self.assertEqual(self.options.log_file, log_file)


    def test_sets_the_log_file_with_short_switch(self):
        log_file = 'log.txt'
        self.given(btoptions.OptionSwitch.LOG_FILE_SHORT, log_file)
        self.assertEqual(self.options.log_file, log_file)


    def test_continue_on_error_is_properly_initialized(self):
        self.assertEqual(self.default_options.continue_on_error, btoptions.Default.CONTINUE_ON_ERROR)


    def test_sets_continue_on_error_with_long_switch(self):       
        self.given(btoptions.OptionSwitch.CONTINUE_ON_ERROR_LONG)
        self.assertTrue(self.options.continue_on_error)


    def given(self, *args):
        self.options = btoptions.Options(args)

    
    def verify_log_level(self, str_level, expected):
        self.given(btoptions.OptionSwitch.LOG_LEVEL_LONG, str_level)
        self.assertEqual(self.options.log_level, expected)



if __name__=="__main__":
    unittest.main()
