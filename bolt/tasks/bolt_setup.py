"""
setup
-----

The ``setup`` task provides an automation hook to execute ``setup.py``
commands and options inside of Bolt. The task, in its simplest form,
assumes a default ``setup.py`` in the current working directory and
uses a ``build`` command as a default if no configuration is provided.

The task configuration allows spcifying a setup script, which by 
default will be set to ``setup.py`` if no script is specified, a valid
command, and it command arguments. The following example shows how to
configure the task. ::

    config = {
        'script': 'special_setup.py',
        'command': 'install',
        'options': {
            'verbose': True,
            'dry-run': True
        }
    }
"""
import distutils.core as dcore
import logging

import bolt.utils as utilities

DEFAULT_ARGUMENTS = ['build']
DEFAULT_SETUP_SCRIPT = 'setup.py'

class _SetupArgumentGenerator(utilities.CommonCommandAndArgumentsGenerator):

    def __init__(self):
        return super(_SetupArgumentGenerator, self).__init__(DEFAULT_ARGUMENTS)



def execute_setup(**kwargs):
    logging.info('Executing Setup')
    config = kwargs.get('config')
    setup_script = config.get('script')
    if setup_script:
        config['script'] = False
    else:
        setup_script = DEFAULT_SETUP_SCRIPT
    generator = _SetupArgumentGenerator()
    args = generator.generate_from(config)
    dcore.run_setup(setup_script, args)


def register_tasks(registry):
    registry.register_task('setup', execute_setup)
    logging.debug('setup task registered.')
