"""
"""
import pip
import bolt.utils as utilities

DEFAULT_COMMAND = 'install'
DEFAULT_REQUIREMENTS_FILE = 'requirements.txt'
DEFAULT_ARGUMENTS = [DEFAULT_COMMAND, '-r', DEFAULT_REQUIREMENTS_FILE]

class _PipArgumentGenerator(utilities.CommonCommandAndArgumentsGenerator):


    def __init__(self):
        return super(_PipArgumentGenerator, self).__init__(DEFAULT_ARGUMENTS)


    def _convert_config_to_arguments(self):
        self.command = self.config.get('command')
        self.package = self.config.get('package')
        return [DEFAULT_COMMAND, self.package] if self._installing_single_package else self._converted_options
            

    @property
    def _installing_single_package(self):
        return self.command == DEFAULT_COMMAND and self.package
    



def execute_pip(**kwargs):
    config = kwargs.get('config')
    generator = _PipArgumentGenerator()
    args = generator.generate_from(config)
    pip.main(args)




def register_tasks(registry):
    registry.register_task('pip', execute_pip)
    