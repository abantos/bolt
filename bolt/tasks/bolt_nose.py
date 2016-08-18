"""
"""
import logging
import os.path
import subprocess as sp

import bolt.utils as utilities


DEFAULT_DIR = './'
DEFAULT_ARGUMENTS = [DEFAULT_DIR]


class _NoseArgumentGenerator(utilities.ArgumentsGenerator):

    def __init__(self):
        return super(_NoseArgumentGenerator, self).__init__(DEFAULT_ARGUMENTS, utilities.append_with_equal)


    def _convert_config_to_arguments(self):
        self.args.append('nosetests')
        super(_NoseArgumentGenerator, self)._convert_config_to_arguments()
        directory = self.config.get('directory') or DEFAULT_DIR
        directory = os.path.abspath(directory)
        self.args.append(directory)





def execute_nose(**kwargs):
    logging.info('Executing nose')
    config = kwargs.get('config')
    generator = _NoseArgumentGenerator()
    args = generator.generate_from(config)
    logging.debug('Arguments: ' + repr(args))
    result = sp.call(args)
    # try:
    #     test_program = nose.core.TestProgram(argv=args, exit=False) 
    #     result = test_program.success
    #     del(test_program)

    #     # nose.core.run(argv=args)
    # except SystemExit as ex:
    #     # Nose tries to sys.exit(), so we have to intercept it.
    #     pass



def register_tasks(registry):
    registry.register_task('nose', execute_nose)
    logging.debug('nose task registered.')


