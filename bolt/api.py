"""
This module contains classes that can be used for the implementation of 
bolt tasks.
"""
import logging


class Task(object):
    """
    """

    def __call__(self, **kwargs):
        self.config = kwargs.get('config')
        self._configure()
        self._execute()


    def _configure(self):
        """
        """
        logging.warning('Derived classes should implement _configure()')


    def _execute(self):
        """
        """
        logging.warning('Derived classes should implement _execute()')


    def _require(self, key):
        value = self.config.get(key)
        if not value:
            raise RequiredConfigurationError(key)
        return value


    def _optional(self, key, default=None):
        return self.config.get(key, default)
        


class BoltError(Exception):
    """
    Base class for all exceptions in Bolt. The class is provided for inheritance
    and it should not be used by itself.

    Errors for the Bolt application itself should be derived from this class.
    """
    def __init__(self, code=1):
        self.code = code


    def __repr__(self):
        return 'BoltError({code})'.format(code=self.code)


    def __str__(self):
        return repr(self)


class TaskError(BoltError):
    """
    Base class for exceptions raised by a bolt task implementation. This class
    is provided for inheritance and it should not be used by itself.

    Exceptions derived from this class should be implemented to indicate errors
    during the execution of a class. More specific exception base classes are
    provided for the distinct processes of executing a class.

    ..  seealso::
        :class:`RequiredConfigurationError`
        :class:`ConfigurationValueError`
        :class:`TaskFailedError`
    """
    def __init__(self, code=999):
        super(TaskError, self).__init__(code)


    def __repr__(self):
        return 'TaskError({code})'.format(code=self.code)


class RequiredConfigurationError(TaskError):
    """
    Exception raised by tasks when a required configuration parameter is missing.

    :param str parameter:
        Name of the parameter missing.
    """
    def __init__(self, parameter):
        super(RequiredConfigurationError, self).__init__(2)
        self.parameter = parameter


    def __repr__(self):
        return 'RequiredConfigurationError({param})'.format(param=self.parameter)



class ConfigurationValueError(TaskError):
    """
    Exception raised by tasks when the value of a configuration parameter is
    invalid.

    :param str parameter:
        Name of the parameter that has an invalid value.
    :param any value:
        Invalid value specified.
    """
    def __init__(self, parameter, value):
        super(ConfigurationValueError, self).__init__(3)
        self.parameter = parameter
        self.value = value


    def __repr__(self):
        return 'ConfigurationValueError({param}, {value})'.format(param=self.parameter, value=self.value)
        


class TaskFailedError(TaskError):
    """
    Exception to indicate that a task execution has failed. Tasks can choose
    to raise this exception directly or derive from a more specific exception
    to provide more information about the error.
    """
    def __init__(self, code=4):
        super(TaskFailedError, self).__init__(code)


    def __repr__(self):
        return 'TaskFailedError({code})'.format(code=self.code)

