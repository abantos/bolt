"""
setup
-----

The ``setup`` task provides an automation hook to execute ``setup.py``
commands and options inside of Bolt. The task, in its simplest form,
assumes a default ``setup.py`` in the current working directory and
uses a ``build`` command as a default if no configuration is provided.

The task configuration allows spcifying a setup script, which by
default will be set to ``setup.py`` if no script is specified, a valid
command, and it command arguments. The following example shows how to
configure the task. ::

    config = {
        'setup':{
            'script': 'special_setup.py',
            'command': 'install',
            'options': {
                'verbose': True,
                'dry-run': True
            }
        }
    }
"""

import logging

import bolt.api as api
import bolt.utils as utilities

DEFAULT_ARGUMENTS = ["build"]
DEFAULT_SETUP_SCRIPT = "setup.py"


class ExecuteSetupTask(api.Task):
    def _configure(self):
        self.setup_script = self._optional("script")
        if self.setup_script:
            self.config["script"] = False
        else:
            self.setup_script = DEFAULT_SETUP_SCRIPT
        generator = _SetupArgumentGenerator()
        self.args = generator.generate_from(self.config)
        logging.debug(f"Setup script: {self.setup_script}")
        logging.debug(f"Arguments: {self.args}")

    def _execute(self):
        result = self._execute_setup()
        if not result.dist_files:
            raise BuildSetupError()

    def _execute_setup(self):
        try:
            import distutils.core as dcore

            return dcore.run_setup(self.setup_script, self.args)
        except ImportError:
            logging.warning(
                "Failed to import <distutils> please install the <setuptools> package."
            )


def register_tasks(registry):
    registry.register_task("setup", ExecuteSetupTask())


class _SetupArgumentGenerator(utilities.CommonCommandAndArgumentsGenerator):
    def __init__(self):
        return super(_SetupArgumentGenerator, self).__init__(DEFAULT_ARGUMENTS)


class BuildSetupError(api.TaskFailedError):
    def __repr__(self):
        return "BuildSetupError({code})".format(code=self.code)
