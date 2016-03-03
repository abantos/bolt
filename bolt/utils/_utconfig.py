"""
Classes to help processing configurations.
"""

TO_ENABLE_FLAG = True
TO_DISABLE_FLAG = False

class CommonCommandAndArgumentsGenerator(object):

    def __init__(self, default_args):
        self.default_arguments = default_args


    def generate_from(self, config):
        if not config:
            return self.default_arguments
        self.config = config
        return self._convert_config_to_arguments()


    def _convert_config_to_arguments(self):
        self.command = self.config.get('command')
        return self._converted_options
            

    @property
    def _converted_options(self):
        self.args = [self.command]
        self.options = self.config.get('options')
        {self._push_as_arguments(option, value) for option, value in self.options.items()}       
        return self.args

    def _push_as_arguments(self, option, value):
        if value is not TO_DISABLE_FLAG:
            self._do_push(option, value)        


    def _do_push(self, option, value):
        formatted_option = self._format_option(option)
        self.args.append(formatted_option)
        if value is not TO_ENABLE_FLAG:
            self.args.append(value)

    def _format_option(self, option):
        if len(option) == 1:
            fmt_str = '-{option}'
        else:
            fmt_str = '--{option}'
        formatted_option = fmt_str.format(option=option)
        return formatted_option
