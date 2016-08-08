"""
"""
import glob
import logging
import os

class FileFinder(object):
    """
    """

    def __init__(self, sourcedir, pattern, recursive):
        self.sourcedir = sourcedir
        self.pattern = pattern
        self.recursive = recursive
        self.matches = None


    def find(self):
        """
        """
        self.matches = []
        if self.recursive:
            self.matches = self._search_recursive(self.sourcedir, self.pattern)
        else:
            fullpattern = os.path.join(self.sourcedir, self.pattern)
            self.matches = self._search_matches(fullpattern)
        return self.matches



    def _search_recursive(self, path, pattern):
        result = []
        for path, dirs, files in os.walk(self.sourcedir):
            fullpattern = os.path.join(path, self.pattern)
            result.extend(self._search_matches(fullpattern))
        return result

    def _search_matches(self, fullpattern):
        return glob.glob(fullpattern)



def delete_files_in(all_files):
    """
    """
    for f in all_files:
        os.remove(f)
        logging.info(f + ' deleted')
