from common.events import TEMP_CHANGED
from hal.thermometers import Thermometers

from unittest.mock import MagicMock, patch

import json
import time
import unittest


class TestThermometers(unittest.TestCase):

    @patch("hal.thermometers.Thermometers._fake_read")
    def test_observer(self, mock_read_fn):
        expected_temp = 42
        mock_read_fn.return_value = expected_temp
        polling_interval_s = 0.1
        observer = MagicMock()

        t = Thermometers(polling_interval_s=polling_interval_s, simulate=True)
        t.add_observer(TEMP_CHANGED, observer)
        time.sleep(2 * polling_interval_s)
        t.remove_observer(TEMP_CHANGED, observer)

        self.assertTrue(observer.called)
        params = json.loads(observer.call_args[0][0])
        for thermometer_name, actual_temp in params.items():
            self.assertTrue(thermometer_name in t._thermometers)
            self.assertEqual(actual_temp, expected_temp)

    def test_to_f(self):

        thermometers = Thermometers(simulate=True)

        actual_temp = thermometers._to_f(0)
        expected_temp = 32.0
        self.assertEqual(actual_temp, expected_temp)

        actual_temp = thermometers._to_f(100)
        expected_temp = 212.0
        self.assertEqual(actual_temp, expected_temp)

        actual_temp = thermometers._to_f(121.111)
        expected_temp = 250.0
        self.assertAlmostEqual(actual_temp, expected_temp, places=1)
