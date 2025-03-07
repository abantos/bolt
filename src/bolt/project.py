"""
"""
import sys

if sys.version_info < (3, 11):
    import tomli as toml
else:
    import tomllib as toml


PYPROJECT_FILE = "pyproject.toml"

def load_project(pyproject_file=PYPROJECT_FILE):
    with open(pyproject_file, 'rb') as file:
        return _wrap(toml.load(file))

def _wrap(raw_value):
    if isinstance(raw_value, dict): return _Object(raw_value)
    if isinstance(raw_value, list): return _List(raw_value)
    return raw_value


class _Object:
    def __init__(self, raw):
        self._obj = raw

    def __getattr__(self, name):
        if name not in self._obj: super().__getattribute__(name)
        return _wrap(self._obj[name])


class _List:
    def __init__(self, raw):
        self._list = raw

    def __getitem__(self, index):
        return _wrap(self._list[index])