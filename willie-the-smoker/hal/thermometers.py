# External deps
from threading import Thread
from typing import Callable

import atexit
import logging
import random
import time

# Internal deps
from common.events import TEMP_CHANGED
from common.observable import Observable

LOG = logging.getLogger("root")


class Thermometers(Observable):

    def __init__(self, polling_interva_s=5, simulate=False):
        super(Thermometers, self).__init__()

        self._polling = False
        self._sensor_poll_interval_s = 1

        target = self._start_polling if not simulate else self.__start_simulating
        self._polling_thread = Thread(target=target)
        self._previous_temp = self.get_temperature("")

    def add_observer(self, event_name: str, observer: Callable):
        LOG.debug("Adding an observer for {}".format(TEMP_CHANGED))
        super(Thermometers, self).add_observer(event_name, observer)
        # Start polling the temp only when an observer is added
        if not self._polling:
            self._polling = True
            self._polling_thread.start()
            atexit.register(self._stop_polling)

    def get_temperature(self, sensor_name: str, celcius=True) -> float:
        # TODO GPIO nonsense
        if celcius:
            return self._read_temp()
        else:
            return self._to_f(self._read_temp())

    def remove_observer(self, event_name: str, observer: Callable):
        super(Thermometers, self).remove_observer(event_name, observer)
        if not self._observers:
            self._stop_polling()

    def _read_temp(self) ->float:
        return 100.0

    def _start_polling(self):
        while self._polling:
            cur_temp = self.get_temperature("")
            LOG.debug("Polling temp: {}".format(cur_temp))
            if cur_temp != self._previous_temp:
                self._previous_temp = cur_temp
                self.property_changed(TEMP_CHANGED, cur_temp)
            time.sleep(self._sensor_poll_interval_s)

    def __start_simulating(self):
        while self._polling:
            LOG.debug("Simulating a temp reading")
            res = {"sensor_name": "Hank Hill", "sensor_value": random.randint(100, 300)}
            self.property_changed(TEMP_CHANGED, res)
            time.sleep(self._sensor_poll_interval_s)

    def _stop_polling(self):
        LOG.debug("Exit handler is stopping temp polling")
        self._polling = False
        self._polling_thread.join()

    def _to_f(self, value: float) -> float:
        return (value * (9.0/5.0)) + 32.0
