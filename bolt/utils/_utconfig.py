"""
Classes to help processing configurations.
"""

TO_ENABLE_FLAG = True
TO_DISABLE_FLAG = False


def append_with_equal(arg_list, formatted_option, value):
    if value is TO_ENABLE_FLAG:
        arg_list.append(formatted_option)
    elif value is not TO_ENABLE_FLAG:
        formatted_argument = '{option}={value}'.format(option=formatted_option, value=value)
        arg_list.append(formatted_argument)



def append_as_tokens(arg_list, formatted_option, value):

    arg_list.append(formatted_option)
    if value is not TO_ENABLE_FLAG:
        arg_list.append(value)


class ArgumentsGenerator(object):
    
    def __init__(self, default_args, append_callback=None):
        self.default_arguments = default_args
        self.append_callback = append_callback or append_as_tokens


    def generate_from(self, config):
        self.args = []
        if not config:
            return self.default_arguments
        self.config = config
        self._convert_config_to_arguments()
        return self.args


    def _convert_config_to_arguments(self):
        self.options = self.config.get('options')
        if self.options:
            {self._push_as_arguments(option, value) for option, value in self.options.items()}       
        
        

    def _push_as_arguments(self, option, value):
        if value is not TO_DISABLE_FLAG:
            self._do_push(option, value)        


    def _do_push(self, option, value):
        formatted_option = self._format_option(option)
        self.append_callback(self.args, formatted_option, value)
        
        

    def _format_option(self, option):
        if len(option) == 1:
            fmt_str = '-{option}'
        else:
            fmt_str = '--{option}'
        formatted_option = fmt_str.format(option=option)
        return formatted_option


    





class CommonCommandAndArgumentsGenerator(ArgumentsGenerator):

    
    def _convert_config_to_arguments(self):
        self.command = self.config.get('command')
        self.args.append(self.command)
        return super(CommonCommandAndArgumentsGenerator, self)._convert_config_to_arguments()