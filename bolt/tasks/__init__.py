"""
"""
# Import tasks modules here.
#
import bolt_pip
import delete_files

def register_standard_modules(registry):
    bolt_pip.register_tasks(registry)
    delete_files.register_tasks(registry)