import logging

import bolt

config = {}

def hello_tasks(config):
    print 'Hello Bolt!!!'


bolt.register_task('default', hello_tasks)