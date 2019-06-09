from common.events import RELAY_ACTIVE
from common.observable import Observable

import logging
import time

LOG = logging.getLogger('root')


class Relay(Observable):

    def __init__(self, simulate=False):
        super(Relay, self).__init__()

        self._active = False
        if simulate:
            LOG.debug("Simulating relay data")
            self.event_loop = self.__start_simulating

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool):
        if (value != self._active):
            self._active = value
            self.property_changed(RELAY_ACTIVE, value)
            # TODO: Set GPIO state

    def __start_simulating(self):
        while not self._main_event.isSet():
            time.sleep(5)
            self.active = not self.active
