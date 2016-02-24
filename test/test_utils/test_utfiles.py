import unittest

import bolt.utils._utfiles as utfiles


class TestFileDeleter(unittest.TestCase):

    def setUp(self):
        self.sourcedir = 'C:\\sourcedir'
        self.pattern = '*.py'
        self.recursive = True
        self.subject = FileFinderSpy(self.sourcedir, self.pattern, self.recursive)
        return super(TestFileDeleter, self).setUp()


    def test_searches_specified_directory(self):
        self.subject.find()
        self.assert_sourcedir(self.sourcedir)


    def test_searches_specified_pattern(self):
        self.subject.find()
        self.assert_pattern(self.pattern)


    def test_respects_recursive_flag(self):
        self.subject.find()
        self.assert_recursive(self.recursive)


    def test_invokes_recursive_search_if_specified(self):
        self.subject.find()
        self.assertTrue(self.subject.recursive_search)


    def test_invokes_non_recursive_search_if_specified(self):
        subject = FileFinderSpy(self.sourcedir, self.pattern, False)
        subject.find()
        self.assertTrue(subject.non_recursive_search)


    def execute(self):
        self.subject.execute()


    def assert_sourcedir(self, expected):
        self.assertEqual(self.subject.sourcedir, expected)


    def assert_pattern(self, expected):
        self.assertEqual(self.subject.pattern, expected)


    def assert_recursive(self, expected):
        self.assertEqual(self.subject.recursive, expected)



class FileFinderSpy(utfiles.FileFinder):

    def __init__(self, sourcedir, pattern, recursive):
        self.recursive_search = False
        self.non_recursive_search = False
        return super(FileFinderSpy, self).__init__(sourcedir, pattern, recursive)

    def _search_recursive(self, path, pattern):
        self.recursive_search = True


    def _search_matches(self, fullpattern):
        self.non_recursive_search = True



if __name__=='__main__':
    unittest.main()