import logging

import bolt

config = {
    'pip': {
        'command': 'install',
        'options': {
            'r': './requirements.txt'    
        }
    },
    'delete-pyc': {
        'sourcedir': './bolt/',
        'recursive': True,
        'test-pyc': {
            'sourcedir': './test/'
        }
    },
    'shell': {
        'command': 'nosetests',
        'arguments': ['./test/']
    },
    'conttest' : {
        'task': 'ut'
    },
    'nose': {
        'directory': './test/',
        'options': {
            'with-xunit': True,
            'xunit-file': 'unit_tests_log.xml'
        }
    },
    "setup": {
        'command': 'bdist_wheel',
        'egg-info': {
            'command': 'egg_info'
        }
    }
}

bolt.register_task('clear-pyc', ['delete-pyc', 'delete-pyc.test-pyc'])
bolt.register_task('ut', ['clear-pyc', 'nose'])
bolt.register_task('ct', ['conttest'])
bolt.register_task('pack', ['setup', 'setup.egg-info'])
bolt.register_task('default', ['pip', 'ut'])
