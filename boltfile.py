import logging
import os.path 

import bolt
import bolt.about

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
_src_dir = os.path.join(PROJECT_ROOT, 'bolt')
_test_dir = os.path.join(PROJECT_ROOT, 'test')
_output_dir = os.path.join(PROJECT_ROOT, 'output')
_coverage_dir = os.path.join(_output_dir, 'coverage')

config = {
    'pip': {
        'command': 'install',
        'options': {
            'r': './requirements.txt'    
        }
    },
    'delete-pyc': {
        'sourcedir': _src_dir,
        'recursive': True,
        'test-pyc': {
            'sourcedir': _test_dir,
        }
    },
    'conttest' : {
        'task': 'ut'
    },
    'mkdir': {
        'directory': _output_dir,
    },
    'nose': {
        'directory': _test_dir,
        'ci': {
            'options': {
                'with-xunit': True,
                'xunit-file': os.path.join(_output_dir, 'unit_tests_log.xml'),
                'with-coverage': True,
                'cover-erase': True,
                'cover-package': 'bolt',
                'cover-html': True,
                'cover-html-dir': _coverage_dir,
                'cover-branches': True,
            }
        }
    },
    'setup': {
        'command': 'bdist_wheel',
        'egg-info': {
            'command': 'egg_info'
        }
    },
    'coverage': {
        'task': 'nose',
        'include': ['bolt'],
        'output': os.path.join(_output_dir, 'ut_coverage')
    }
}

# Development tasks
bolt.register_task('clear-pyc', ['delete-pyc', 'delete-pyc.test-pyc'])
bolt.register_task('ut', ['clear-pyc', 'nose'])
bolt.register_task('ct', ['conttest'])
bolt.register_task('pack', ['setup', 'setup.egg-info'])

# CI/CD tasks
bolt.register_task('run-unit-tests', ['clear-pyc', 'mkdir', 'nose.ci'])

# Default task (not final).
bolt.register_task('default', ['pip', 'ut'])
