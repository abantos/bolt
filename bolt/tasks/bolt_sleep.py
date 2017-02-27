"""
sleep
-----

This task allows to set the bolt process to sleep for the specified duration. 
If no duration is specified, the process will sleep forever. This task can be 
used to wait for a subprocess to start in cases where the subprocess might take 
some time to initialize. You can also use it to wait forever in case that an 
independent subprocess needs to be kept running in the background./

..  code-block:: python

    config = {
        'sleep': {
            'duration': 10      # Waits 10 seconds.
        }
    }
"""
import logging
import time

import bolt.utils as btutils


class SleepTask(object):

    def __call__(self, **kwargs):
        self.config = kwargs.get('config')
        self.duration = self.config.get('duration') or btutils.FOREVER
        if self.duration == btutils.FOREVER:
            self._sleep_forever()
        else:
            self._sleep(self.duration)


    def _sleep(self, seconds):
        time.sleep(seconds)


    def _sleep_forever(self):
        while True: pass



def register_tasks(registry):
    registry.register_task('sleep', SleepTask())

