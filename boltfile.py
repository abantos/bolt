import logging

import bolt

config = {
    'shell': {
		'command': 'conttest',
		'arguments': ['nosetests', './test/']
    }
}

bolt.register_task('ct', ['shell'])
bolt.register_task('default', ['shell'])
