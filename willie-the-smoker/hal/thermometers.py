# External deps
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
        self._sensor_poll_interval_s = 1
        self._previous_temp = self.get_temperature("")
        if simulate:
            LOG.debug("Simulating thermometer data")
            self.event_loop = self.__start_simulating

    def get_temperature(self, sensor_name: str, celcius=True) -> float:
        # TODO GPIO nonsense
        if celcius:
            return self._read_temp()
        else:
            return self._to_f(self._read_temp())

    def _read_temp(self) ->float:
        return 100.0

    def event_loop(self):  # override
        while not self._main_event.isSet():
            cur_temp = self.get_temperature("")
            LOG.debug("Polling temp: {}".format(cur_temp))
            if cur_temp != self._previous_temp:
                self._previous_temp = cur_temp
                self.property_changed(TEMP_CHANGED, cur_temp)
            time.sleep(self._sensor_poll_interval_s)

    def __start_simulating(self):
        while not self._main_event.isSet():
            LOG.debug("Simulating a temp reading")
            res = [{"sensor_name": "Hank Hill", "sensor_value": random.randint(100, 300)}]
            self.property_changed(TEMP_CHANGED, res)
            time.sleep(self._sensor_poll_interval_s)

    def _to_f(self, value: float) -> float:
        return (value * (9.0/5.0)) + 32.0
