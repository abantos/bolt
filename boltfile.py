import logging

import bolt

config = {
    'setup': {
		'command': 'build',
		'options': {}
    }
}


bolt.register_task('default', ['pip'])