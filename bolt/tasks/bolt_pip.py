"""
"""
import pip

DEFAULT_COMMAND = 'install'
DEFAULT_REQUIREMENTS_FILE = 'requirements.txt'

class _PipArgumentGenerator(object):

    DEFAULT_ARGUMENTS = [DEFAULT_COMMAND, '-r', DEFAULT_REQUIREMENTS_FILE]
    TO_ENABLE_FLAG = True
    TO_DISABLE_FLAG = False
    
    def generate_from(self, config):
        if not config:
            return self.DEFAULT_ARGUMENTS
        self.config = config
        return self._convert_config_to_arguments()


    def _convert_config_to_arguments(self):
        self.command = self.config.get('command')
        self.package = self.config.get('package')
        return [DEFAULT_COMMAND, self.package] if self._installing_single_package else self._converted_options
            

    @property
    def _installing_single_package(self):
        return self.command == DEFAULT_COMMAND and self.package

    @property
    def _converted_options(self):
        self.args = [self.command]
        self.options = self.config.get('options')
        {self._push_as_arguments(option, value) for option, value in self.options.items()}       
        return self.args

    def _push_as_arguments(self, option, value):
        if value is not self.TO_DISABLE_FLAG:
            self._do_push(option, value)        


    def _do_push(self, option, value):
        formatted_option = self._format_option(option)
        self.args.append(formatted_option)
        if value is not self.TO_ENABLE_FLAG:
            self.args.append(value)

    def _format_option(self, option):
        if len(option) == 1:
            fmt_str = '-{option}'
        else:
            fmt_str = '--{option}'
        formatted_option = fmt_str.format(option=option)
        return formatted_option

    



def execute_pip(**kwargs):
    config = kwargs.get('config')
    generator = _PipArgumentGenerator()
    args = generator.generate_from(config)
    pip.main(args)




def register_tasks(registry):
    registry.register_task('pip', execute_pip)
    