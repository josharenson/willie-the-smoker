# External deps
import logging
import json
import random
import time

# Internal deps
from common.events import TEMP_CHANGED
from common.observable import Observable

LOG = logging.getLogger("root")


class Thermometers(Observable):

    def __init__(self, fahrenheit=False, polling_interval_s=5, simulate=False):
        super(Thermometers, self).__init__()
        # TODO: This will come from settings in the future
        self._fahrenheit = fahrenheit
        self._polling_interval_s = polling_interval_s
        self._simulate = simulate
        self._thermometers = {"Upper Ambient": 100,
                              "Internal Food": 80}

    def _fake_read(self, name):
        return random.randint(50, 100)

    def __real_read(self, name):
        raise NotImplementedError

    def _poll_thermometers(self):
        read_fn = self._fake_read if self._simulate else self.__real_read
        thermometers_changed = []
        for thermometer_name in self._thermometers:
            new_temp = read_fn(thermometer_name)
            if new_temp != self._thermometers[thermometer_name]:
                self._thermometers[thermometer_name] = new_temp
                thermometers_changed.append(thermometer_name)

        if thermometers_changed:
            params = {}
            for thermometer_name in thermometers_changed:
                temp = self._thermometers[thermometer_name]
                if self._fahrenheit:
                    temp = self._to_f(temp)
                params[thermometer_name] = temp
            self.property_changed(TEMP_CHANGED, json.dumps(params))

    def event_loop(self):  # override
        while not self._main_event.isSet():
            self._poll_thermometers()
            time.sleep(self._polling_interval_s)

    def _to_f(self, value: float) -> float:
        return (value * (9.0/5.0)) + 32.0
