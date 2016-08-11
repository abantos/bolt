"""
"""
import logging
import os.path

import bolt.utils as utilities


DEFAULT_DIR = './'
DEFAULT_ARGUMENTS = [DEFAULT_DIR]


class _NoseArgumentGenerator(utilities.ArgumentsGenerator):

    def __init__(self):
        return super(_NoseArgumentGenerator, self).__init__(DEFAULT_ARGUMENTS, utilities.append_with_equal)


    def _convert_config_to_arguments(self):
        self.args.append('dummy')
        super(_NoseArgumentGenerator, self)._convert_config_to_arguments()
        directory = self.config.get('directory') or DEFAULT_DIR
        directory = os.path.abspath(directory)
        self.args.append(directory)





def execute_nose(**kwargs):
    logging.info('Executing nose')
    import nose.core
    config = kwargs.get('config')
    generator = _NoseArgumentGenerator()
    args = generator.generate_from(config)
    logging.debug('Arguments: ' + repr(args))
    try:
        nose.core.main(argv=args)
    except SystemExit as ex:
        # Nose tries to sys.exit(), so we have to intercept it.
        pass



def register_tasks(registry):
    registry.register_task('nose', execute_nose)
    logging.debug('nose task registered.')


