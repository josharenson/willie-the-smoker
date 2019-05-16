# External deps
from typing import Callable

# Internal deps
from common.event_names import TEMP_CHANGED
from common.observable import Observable

class Thermometers(Observable):

    def __init__(self):
        super(Thermometers, self).__init__()

    def get_temperature(self, sensor_name: str, celcius=True) -> float:
        # TODO GPIO nonsense
        fake_reading = 100.0
        if (celcius):
            return fake_reading
        else:
            return self._to_f(fake_reading)

    def _to_f(self, value: float) -> float:
        return (value * (9.0/5.0)) + 32.0
