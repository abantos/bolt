"""
"""
import imp
import os.path
import sys


def add_search_path(*path_tokens):
    """
    Adds a new search path from where modules can be loaded. 
    
    This function is provided for test applications to add locations to the search path, so any required functionality
    can be loaded. It helps keeping the step implementation modules simple by placing the bulk of the implementation in
    separate utility libraries. This function can also be used to add the application being tested to the path, so its
    functionality can be made available for testing.

    :param arglist path_tokens: 
        Variable list of path tokens that is joined to create the full, absolute path to be added.
    """
    full_path = os.path.join(*path_tokens)
    if full_path not in sys.path:
        sys.path.insert(0, os.path.abspath(full_path))



def load_script(filename):
    """
    Loads a python script as a module.

    This function is provided to allow applications to load a Python module by its file name.

    :param string filename:
        Name of the python file to be loaded as a module.

    :return:
        A |Python|_ module loaded from the specified file.
    """
    path, module_name, ext = _extract_script_components(filename)
    add_search_path(path)
    return _load_module(module_name)


def _extract_script_components(filename):
    path = os.path.dirname(filename)
    base_name = os.path.basename(filename)
    module_name, ext = os.path.splitext(base_name)
    return path, module_name, ext


def _load_module(module_name):
    file = None
    try:
        file, pathname, description = imp.find_module(module_name)
        module = imp.load_module(module_name, file, pathname, description)
        return module
    finally:
        if file:
            file.close()


