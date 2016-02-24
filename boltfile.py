import logging

import bolt

config = {
    'delete-pyc': {
        'sourcedir': './',
        'recursive': True
    }
}


def hello_tasks(config):
    print 'Hello Bolt!!!'


bolt.register_task('default', hello_tasks)