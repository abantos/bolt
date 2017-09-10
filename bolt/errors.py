"""
This module defines exception classes used in the implementation of Bolt to
report errors or as base classes to define other error conditions.
"""

class BoltError(Exception):
    """
    Base class for all exceptons explicitely raised by Bolt.
    """
    def __init__(self, code=1):
        self.code = code


    def __str__(self):
        return 'BoltError()'


    def __repr__(self):
        return self.__str__()



class InvalidTaskError(BoltError):
    """
    TBD
    """
    pass



class InvalidConfigurationError(BoltError):
    """
    Base class for all task configuration errors.
    """
    
    def __str__(self):
        return 'InvalidConfigurationError()'



class ConfigurationParameterError(InvalidConfigurationError):
    """
    Base class for configuration parameters errors.
    """
    def __init__(self, param_name):
        self.parameter = param_name


    def __str__(self):
        return 'ConfigurationParameterError({pn})'.format(pn=repr(self.parameter))




class RequiredParameterMissingError(ConfigurationParameterError):
    """
    Indicates a requiered configuration parameter is missing from the task 
    configuration
    """
    
    def __str__(self):
        return 'RequiredParameterMissingError({pn})'.format(pn=repr(self.parameter))




class ConfigurationValueError(ConfigurationParameterError):
    """
    Indicates the value for a configuration parameter is invalid.
    """
    def __init__(self, param_name, value):
        super(ConfigurationValueError, self).__init__(param_name)
        self.value = value


    def __str__(self):
        fmt = 'ConfigurationValueError({pn}, {v})'
        return fmt.format(pn=repr(self.parameter), v=repr(self.value))



class TaskError(BoltError):
    """
    Base class for exceptions raised during task execution. Developers should
    raise this exception or a derived type to indicate an error during the 
    execution of the task they are implementing.
    """

    def __str__(self):
        return 'TaskError()'