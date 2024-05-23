import os.path
import sys

import bolt
import bolt.about as about


# Development tasks
bolt.register_task('clear-pyc', ['delete-pyc', 'delete-pyc.test-pyc'])
bolt.register_task('ut', ['clear-pyc', 'shell.pytest'])
bolt.register_task('ct', ['conttest'])
bolt.register_task('lcov', ['clear-pyc', 'mkdir', 'mkdir.test', 'shell.pytest.coverage'])
bolt.register_task('pack', ['setup', 'setup.egg-info'])

# CI/CD tasks
bolt.register_task('run-unit-tests', ['clear-pyc', 'mkdir', 'mkdir.test', 'shell.pytest.ci'])

# Default task (not final).
bolt.register_task('default', ['pip', 'ut'])


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, 'bolt')
TEST_DIR = os.path.join(PROJECT_ROOT, 'test')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
COVERAGE_DIR = os.path.join(OUTPUT_DIR, 'coverage')
COVERAGE_REPORT = os.path.join(COVERAGE_DIR, 'coverage.xml')
TEST_OUTPUT_DIR =  os.path.join(OUTPUT_DIR, 'unit')
TEST_REPORT = os.path.join(TEST_OUTPUT_DIR, 'results.md')

config = {
    'pip': {
        'command': 'install',
        'options': {
            'r': './requirements.txt'
        }
    },
    'delete-pyc': {
        'sourcedir': SRC_DIR,
        'recursive': True,
        'test-pyc': {
            'sourcedir': TEST_DIR,
        }
    },
    "shell": {
        "pytest": {
            "command": sys.executable,
            "arguments": ["-m", "pytest", TEST_DIR],
            "ci": {
                "arguments": [
                    "-m",
                    "pytest",
                    "--github-report",
                    f"--cov=bolt",
                    "--cov-report",
                    f"xml:{COVERAGE_REPORT}",
                    TEST_DIR,
                ]
            },
            'coverage': {
                'arguments': [
                    '-m',
                    'pytest',
                    '--github-report',
                    f'--cov={about.package}',
                    '--cov-report',
                    f'html:{COVERAGE_DIR}',
                    TEST_DIR,
                ]
            },
        },
    },
    'conttest': {
        'task': 'ut'
    },
    'mkdir': {
        'directory': OUTPUT_DIR,
        'test': {
            'directory': TEST_OUTPUT_DIR
        }
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
        'output': os.path.join(OUTPUT_DIR, 'ut_coverage')
    }
}
