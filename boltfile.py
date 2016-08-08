import logging

import bolt

config = {
    'delete-pyc': {
        'sourcedir': './',
        'recursive': True
    },
    'shell': {
		'command': 'nosetests',
		'arguments': ['./test/']
    },
    'conttest' : {
        'task': 'ut'
    }
}

bolt.register_task('ut', ['delete-pyc', 'shell'])
bolt.register_task('ct', ['conttest'])
bolt.register_task('default', ['shell'])
