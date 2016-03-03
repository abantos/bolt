"""
"""
import distutils.core as dcore

import bolt.utils as utilities

DEFAULT_ARGUMENTS = ['build']
DEFAULT_SETUP_SCRIPT = 'setup.py'

class _SetupArgumentGenerator(utilities.CommonCommandAndArgumentsGenerator):

    def __init__(self):
        return super(_SetupArgumentGenerator, self).__init__(DEFAULT_ARGUMENTS)



def execute_setup(**kwargs):
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
