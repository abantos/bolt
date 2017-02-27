import unittest
import bolt.utils._uttime as uttime


class TestDateTimeUnitConstants(unittest.TestCase):

    def test_milliseconds_are_used_as_base(self):
        self.assertEqual(uttime.MILLISECOND, 0.001)


    def test_second_is_defined_correctly(self):
        self.assertEqual(uttime.SECOND, 1000 * uttime.MILLISECONDS)


    def test_minute_is_defined_correctly(self):
        self.assertEqual(uttime.MINUTE, 60 * uttime.SECONDS)


    def test_hour_is_defined_correctly(self):
        self.assertEqual(uttime.HOUR, 60 * uttime.MINUTES)


    def test_day_is_defined_correctly(self):
        self.assertEqual(uttime.DAY, 24 * uttime.HOURS)
        self.assertEqual(uttime.DAY, uttime.DAYS)


    def test_forever_is_exposed(self):
        self.assertEqual(uttime.FOREVER, -1)




if __name__=="__main__":
    unittest.main()

