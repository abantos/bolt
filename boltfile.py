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
    }
}

bolt.register_task('clear-pyc', ['delete-pyc', 'delete-pyc.test-pyc'])
bolt.register_task('ut', ['clear-pyc', 'shell'])
bolt.register_task('ct', ['conttest'])
bolt.register_task('default', ['shell'])
