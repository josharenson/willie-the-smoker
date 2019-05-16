# External deps
from typing import Callable

# Internal deps
from common.observable import Observable

class Relay(Observable):
    def __init__(self):
        super(Relay, self).__init__()

        self._active = False

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value: bool):
        if (value != self._active):
            self._active = value
            self.property_changed("relay_active", value)
            # TODO: Set GPIO state
