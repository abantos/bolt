import os.path
import sys

import bolt
import bolt.about as about


# Development tasks
bolt.register_task('clear-pyc', ['delete-pyc', 'delete-pyc.test-pyc'])
bolt.register_task('ut', ['clear-pyc', 'shell.pytest'])
bolt.register_task('ct', ['conttest'])
bolt.register_task('pack', ['setup', 'setup.egg-info'])

# CI/CD tasks
bolt.register_task('run-unit-tests', ['clear-pyc', 'mkdir', 'shell.pytest.coverage'])

# Default task (not final).
bolt.register_task('default', ['pip', 'ut'])


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
_src_dir = os.path.join(PROJECT_ROOT, 'bolt')
_test_dir = os.path.join(PROJECT_ROOT, 'test')
_output_dir = os.path.join(PROJECT_ROOT, 'output')
_coverage_dir = os.path.join(_output_dir, 'coverage')
_coverage_report = os.path.join(_coverage_dir, 'coverage.xml')

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
    "shell": {
        "pytest": {
            "command": sys.executable,
            "arguments": ["-m", "pytest", _test_dir],
            "coverage": {
                "arguments": [
                    "-m",
                    "pytest",
                    f"--cov=bolt",
                    "--cov-report",
                    f"xml:{_coverage_report}",
                    _test_dir,
                ]
            },
        },
    },
    'conttest': {
        'task': 'ut'
    },
    'mkdir': {
        'directory': _output_dir,
    },
    'setup': {
        'command': 'bdist_wheel',
        'egg-info': {
            'command': 'egg_info'
        }
    },
    'coverage': {
        'task': 'shell.pytest',
        'include': ['bolt'],
        'output': os.path.join(_output_dir, 'ut_coverage')
    }
}
