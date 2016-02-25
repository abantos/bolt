"""
"""
import pip

DEFAULT_COMMAND = 'install'
DEFAULT_REQUIREMENTS_FILE = 'requirements.txt'

class _PipArgumentGenerator(object):

    DEFAULT_ARGUMENTS = [DEFAULT_COMMAND, '-r', DEFAULT_REQUIREMENTS_FILE]
    
    def generate_from(self, config):
        if not config:
            return self.DEFAULT_ARGUMENTS
        self.config = config
        return self._process_config()


    def _process_config(self):
        self.command = self.config.get('command')
        self.package = self.config.get('package')
        if self._installing_single_package():
            return [DEFAULT_COMMAND, self.package]
        else:
            self.generated_args = []
            self.generated_args.append(self.command)
            self._process_options()
            return self.generated_args

    def _installing_single_package(self):
        return self.command == DEFAULT_COMMAND and self.package


    def _process_options(self):
        self.options = self.config.get('options')
        for option, value in self.options.iteritems():
            formatted_option = self._format_option(option)
            if value:
                self.generated_args.append(formatted_option)
                if value is not True:
                    self.generated_args.append(value)


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
    